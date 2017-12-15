# -*- coding: utf-8 -*-
"""
Created on Fri Oct 28 17:59:00 2016

@author: nphelps1

This file generates runscripts for a given set of Sobol analysis parameters.
It can be modified to output python scripts for Abaqus model generation or to act
on .inp files directly. The current script is setup to work with the current version
of the unit cell code in which the extract process is carried out in a separate script.
"""
from shutil import copyfile
import fileinput
from SALib.sample import saltelli
from SALib.analyze import sobol
import numpy as np
import os
import csv

def main():
    """
    Create files for Sobol Analysis
    """
    #Setup Analysis Baseline Files
    mainpath = (os.path.dirname(os.path.abspath(__name__))) + '/'
    basefile = mainpath + 'UnitCellProbabilistic.py'
    extractbase = mainpath + 'UnitCellProbabilistic_Extract.py'
    basename = 'UnitCell_{0}.py'
    extractbasename = 'UnitCell_{0}_Extract.py'

    # Setup Fixed Inputs
    Fapplied = .02
    FiberDiameter = .0071

    # Setup Sampling
    # Set Base Sample Count. Total sample count = nsamples*(nvariables+2)
    nsamples = 1

    # Dict input to Saltelli sampling.
    problem = {
        'num_vars': 8,
        'names': ['Volume Fraction', 'E1f', 'E2f', 'Nu12f', 'Nu23f', 'G12f', 'EMa', 'NuMa'],
        'bounds': [[.0*.7, .6*1.3],
                   [235000*.7, 235000*1.3],
                   [14000*.7, 14000*1.3],
                   [.2*.7, .2*1.3],
                   [.25*.7, .25*1.3],
                   [28000*.7, 28000*1.3],
                   [379000*.7, 379000*1.3],
                   [.1*.7, .1*1.3]]
    }

    #Run Sampling
    fileparams = saltelli.sample(problem, nsamples, calc_second_order=False)

    #Write Outputs to CSV for reference
    header = ['Applied Force', 'Fiber Diameter', 'Volume Fraction',
              'Fiber E1', 'Fiber E2', 'Fiber nu12', 'Fiber nu23', 'Fiber G12',
              'Matrix E', 'Matrix nu']

    with open(mainpath+ 'ModelParameters.csv', 'w', newline='') as outfile:
        writer = csv.writer(outfile)
        writer.writerow(header)
        writer.writerows(np.insert(i, 0, [Fapplied, FiberDiameter]) for i in fileparams)

    # Generate file names
    outnames = filenamegen(basename, start=1, end=len(fileparams))
    outnames = list(outnames)
    extnames = filenamegen(extractbasename, start=1, end=len(fileparams))

    # Read Baseline model generation script into memory
    with open(basefile, 'r') as infile:
        baseline = infile.read()

    # Read baseline extract script into memory
    with open(extractbase, 'r') as infile:
        extractbaseline = infile.read()

    # Iterate through output file names
    for i, j, k in zip(fileparams, outnames, extnames):
        newfile = baseline
        newextract = extractbaseline
        newfile = newfile.replace('<Fapplied>', str(Fapplied))
        newfile = newfile.replace('<FiberD>', str(FiberDiameter))
        newfile = newfile.replace('<Vf>', str(i[0]))
        newfile = newfile.replace('<E1f>', str(i[1]))
        newfile = newfile.replace('<E2f>', str(i[2]))
        newfile = newfile.replace('<Nu12f>', str(i[3]))
        newfile = newfile.replace('<Nu23f>', str(i[4]))
        newfile = newfile.replace('<G12f>', str(i[5]))
        newfile = newfile.replace('<Ema>', str(i[6]))
        newfile = newfile.replace('<Numa>', str(i[7]))
        newextract = newextract.replace('<Fapplied>', str(Fapplied))
        newextract = newextract.replace('<FiberD>', str(FiberDiameter))
        newextract = newextract.replace('<Vf>', str(i[0]))
        with open(j, 'w', newline='') as outfile:
            outfile.write(newfile)
        with open(k, 'w', newline='') as outfile:
            outfile.write(newextract)

def filenamegen(basename, start=1, end=100):
    """Generates the names of the runs."""
    return (basename.format(str(i).zfill(5)) for i in range(start, end+1))

if __name__ == "__main__":
    main()
