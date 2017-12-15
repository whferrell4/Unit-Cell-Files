# -*- coding: mbcs -*-
#
# Abaqus/CAE Release 6.14-2 replay file
# Internal Version: 2014_08_22-10.00.46 134497
# Run by hhajdik on Thu Dec 07 16:02:03 2017
#

# from driverUtils import executeOnCaeGraphicsStartup
# executeOnCaeGraphicsStartup()
#: Executing "onCaeGraphicsStartup()" in the site directory ...
from abaqus import *
from abaqusConstants import *
session.Viewport(name='Viewport: 1', origin=(1.76302, 1.76389), width=259.517, 
    height=174.978)
session.viewports['Viewport: 1'].makeCurrent()
from driverUtils import executeOnCaeStartup
executeOnCaeStartup()
execfile(
    'C:/Users/hhajdik/Documents/GitHub/Unit-Cell-Files/New folder/UnitCell_00001/UnitCell_00001_Extract.py', 
    __main__.__dict__)
#: Model: C:/Users/hhajdik/Documents/GitHub/Unit-Cell-Files/New folder/UnitCell_00001/./UnitCell_00001.odb
#: Number of Assemblies:         1
#: Number of Assembly instances: 0
#: Number of Part instances:     7
#: Number of Meshes:             7
#: Number of Element Sets:       4
#: Number of Node Sets:          12
#: Number of Steps:              1
print 'RT script done'
#: RT script done
