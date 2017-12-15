# -*- coding: utf-8 -*-
"""
Created on Fri Oct 21 13:15:48 2016

@author: nphelps1
"""

import csv
import os
import pandas as pd

def main():
    """Simply Execute csvread when called as a script"""
    targdir = (os.path.dirname(os.path.abspath(__name__)))
    basename = os.path.join(targdir, "UnitCell_{0}.csv")
    nfiles=120
    csvread(basename, nfiles)

def csvread(basename, nfiles):
    """Reads multiple csv files containing similiar data and identical headers
    and merges them into a single csv file"""

    # Create List of Filenames
    filenames = filenamegen(basename, start=1, end=nfiles)

    # Load each csv into list of DataFrames
    data=[]
    for filename in filenames:
        data.append(pd.read_csv(filename))

    # Concatenate DataFrames
    compileddata = pd.concat(data, ignore_index=True)
    # Fix Indexing To Match Run Count Indexing
    compileddata.index += 1

    # Output to single CSV
    compileddata.to_csv(basename.format('compiled'))


def filenamegen(basename, start=1, end=100):
    """Generates the names of the runs."""
    return (basename.format(str(i).zfill(5)) for i in range(start, end+1))

if __name__ == "__main__":
    main()
