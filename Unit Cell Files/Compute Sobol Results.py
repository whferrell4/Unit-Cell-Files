# -*- coding: utf-8 -*-
"""
Spyder Editor

Nathan Phelps
SciTech RVE Processing for Sobol
"""

from SALib.sample import saltelli
from SALib.analyze import sobol
import numpy as np
import pandas as pd
import os

def main():
    """Run Sobol Analysis"""
    # Setup Problem Def For Sobol Analysis. This Should match the filemaker.py problem statement.
    problem = {
        'num_vars': 8,
        'names': ['Volume Fraction', 'E1f', 'E2f', 'Nu12f', 'Nu23f', 'G12f', 'EMa', 'NuMa'],
        'bounds': [[.3, .8],
                   [229000*.7, 229000*1.3],
                   [14000*.7, 14000*1.3],
                   [.3*.7, .3*1.3],
                   [.3*.7, .3*1.3],
                   [20000*.7, 20000*1.3],
                   [4340*.7, 4340*1.3],
                   [.34*.7, .34*1.3]]
    }

    # Import Data
    targdir = (os.path.dirname(os.path.abspath(__name__)))
    basename = os.path.join(targdir, "UnitCell_compiled.csv")
    data = pd.read_csv(basename)

    # Parse data into separate valriables
    E2vals=data['Composite E2'].values
    nu23vals=data['Composite nu23'].values

    ## Perform analysis
    print('Composite E2:')
    SiE2 = sobol.analyze(problem, E2vals, print_to_console=True, calc_second_order=False)
    print('\n')
    print('Composite nu23:')
    Sinu23 = sobol.analyze(problem, nu23vals, print_to_console=True, calc_second_order=False)
    print('\n')

    # Write Results to CSV
    SiE2Out=pd.DataFrame(SiE2, index=problem['names'])
    SiE2Out.to_csv('SiE2.csv')
    
    Sinu23Out=pd.DataFrame(Sinu23, index=problem['names'])
    Sinu23Out.to_csv('Sinu23.csv')

if __name__ == "__main__":
    main()

