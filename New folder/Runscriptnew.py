# -*- coding: utf-8 -*-
"""
Created on Sun May 15 17:27:25 2016

@author: Nathan

This script provides a handy way to execute a large number of Abaqus analysis in parallel. 
"""

from multiprocessing import Pool
import subprocess
import os
from glob import glob
from glob import iglob
import shutil
from os import cpu_count
from shutil import copy
import sys
from collections import deque
from functools import partial
#%%

def main():
    """Function to run when used as a script.
    Just runs run_all with given inputs and then collects results files.
    """
    mainpath = (os.path.dirname(os.path.abspath(__name__)))
    run_all(start=1, end=10, targdir=mainpath, cpucount=30, cores_per_job=2,
            cae_cpu_limit=6, filename="UnitCell_{0}", runtype='separate')
    collector("csv", mainpath)


def run_all(start=1, end=10, targdir=os.path.dirname(os.path.abspath(__name__)),
            cpucount=cpu_count()-2, cores_per_job=4, cae_cpu_limit=8,
            filename="RoughnessModel_{0}", runtype='separate'):
    """Overall Runner. Call this if the functionality of this script is desired within another
    program or script. Simply executes the runs for the given conditions and reports when they
    are completed.
    start, end     = limits of runcount
    targdir        = path of parent directory where analysis should take place
    cpucount       = total number of cpus wanted for Abaqus analysis.
                     Should be multiple of cores_per_job.
    cores_per_job  = number of cores to dedicate to each job.
    cae_cpu_limit  = total number of Abaqus CAE instances to be executed simultaneously
    filename       = base file name for runs. Must take format "basename_{0}" to work correctly
    runtype        = determines what type of run behavior is executed:

                     'separate': Will run CAE Input Creation, analysis,
                                 and extract processes in that order

                     'caeonly' : Will run CAE only as "Abaqus cae nogui=*job*"

                     'analysisonly': Will only run analysis of given inputs

                     'extractonly' : Will run extract procedure only
    """

    # Determine number of jobs to run in parallel
    if cpucount < cores_per_job:
        cpucount = cores_per_job
        print('Total number of cores requested < number requested per job.\
                Running with cpucount={0}'.format(cpucount))
    if cpucount > cpu_count():
        cpucount = cpu_count()-2
        print('Number of CPUs requested higher than CPUs available.\
                Running with cpucount={}'.format(cpucount))
    nparallel = cpucount // cores_per_job
    print('Running {0} jobs in parallel'.format(nparallel))

    # Make sure no stray lock files mess up our runs
    cleaner(targdir)

    # Sets up filename with full path to avoid errors
    basename = os.path.join(targdir, filename)

    # Generate Iterator of Runfiles
    filenames = filenamegen(basename, start, end)

    # Create Individual Folders for Each Run
    for files in filenames:
        folderizer(files)

    # Update path to reflect new folders
    foldername = os.path.join(targdir, filename + "\\"  + filename)
    runnames = filenamegen(foldername, start, end)

    # Locate analysis runs that have already reached completion
    alreadyran = glob(targdir+"/*/*.csv", recursive=True)
    alreadyran = [os.path.splitext(each)[0] for each in alreadyran]

    # Activate this section if an analysis gets interrupted
    #badruns = glob(targdir+"/*/*.odb_f", recursive=True)
    #badruns = [os.path.splitext(each)[0] for each in badruns]
    #alreadyran=[each for each in alreadyran if each not in badruns]

    # Take runs that have already been completed out of list to be runs
    runnames = [each for each in runnames if each not in alreadyran]

    extractnames = [runname+'_Extract' for runname in runnames]

    # Run AnalysesS
    if runtype == 'caeonly':
        parallelize(analysiscae, runnames, cae_cpu_limit)
        return 'Runs Completed!'
    if runtype == 'separate':
        parallelize(analysiscae, runnames, cae_cpu_limit)
        parallelize(partial(analysis, cpucount=cores_per_job), runnames, nparallel)
        parallelize(analysiscae, extractnames, cae_cpu_limit)
        return 'Runs Completed!'
    if runtype == 'analysisonly':
        parallelize(partial(analysis, cpucount=cores_per_job), runnames, nparallel)
        return 'Runs Completed!'
    if runtype == 'extractonly':
        parallelize(analysiscae, extractnames, cae_cpu_limit)
        return 'Runs Completed!'

def cleaner(basepath=os.path.dirname(os.path.abspath(__name__)), filetype="lck"):
    """Removes pesky lck files."""
    for filename in iglob(basepath+"/*/*.{}".format(filetype), recursive=True):
        os.unlink(filename)


def parallelize(analysisin, filenames, njobs=4):
    """Parallelizes the subprocess executation."""
    with Pool(njobs) as pool:
        deque(pool.imap_unordered(analysisin, filenames), maxlen=0)


def analysiscae(filename):
    """Abaqus CAE Subprocess Caller.
    Input is Abaqus readable python script."""
    runarg = "nogui=" + filename  # Call CAE without GUI
    returncode = 1
    count = 0
    while returncode == 1 and count < 1:
        result = subprocess.run([shutil.which('abaqus'), 'cae', runarg],
                                cwd=os.path.dirname(filename))
        returncode = result.returncode
        count += 1
    return result

def analysis(filename, cpucount):
    """Abaqus Analysis Subprocess Caller
    Input is Abaqus .inp file."""
    runarg = 'job='+os.path.basename(filename)  # Call CAE without GUI
    returncode = 1
    count = 0
    while returncode == 1 and count < 2:
        result = subprocess.run([shutil.which('abaqus'), runarg, 'cpus='+str(cpucount),
                                 'interactive', 'ask_delete=OFF'], cwd=os.path.dirname(filename))
        returncode = result.returncode
        if returncode == 0:
            print('Job ' + filename + ' Completed Successfully')
        count += 1
    return result

def folderizer(filename):
    """Creates individual folders for all relavent files
    for a given set of filenames."""
    if not os.path.isdir(filename):
        os.makedirs(filename)
    if os.path.isfile(filename+".py"):
        os.rename(filename + ".py", filename + "/"+os.path.basename(filename) + ".py")
    if os.path.isfile(filename+"_Extract.py"):
        os.rename(filename + "_Extract.py", filename + "/" + os.path.basename(filename)
                  + "_Extract.py")
    if os.path.isfile(filename+".inp"):
        os.rename(filename + ".inp", filename + "/" + os.path.basename(filename) + ".inp")

def filenamegen(basename, start=1, end=100):
    """Generates the names of the runs."""
    return (basename.format(str(i).zfill(5)) for i in range(start, end+1))

def collector(filetype, colpath):
    """Collects all files of a given type within a given directory
    and it's subdirectories."""
    collected = os.path.join(colpath, "Results")
    if not os.path.isdir(collected):
        os.makedirs(collected)
    for filename in iglob(colpath+"/*/*.{}".format(filetype), recursive=True):
        copy(filename, collected)

if __name__ == "__main__":
    main()

