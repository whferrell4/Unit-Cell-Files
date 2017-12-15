# Nathan Phelps
# University of Tennessee Knoxville Mechanical Engineering
# -*- coding: mbcs -*-
## Import Necessary Libraries
from part import *
from material import *
from section import *
from optimization import *
from assembly import *
from step import *
from interaction import *
from load import *
from mesh import *
from job import *
from sketch import *
from visualization import *
from connectorBehavior import *
import sys
import os
import inspect
import math
import csv
import itertools
import numpy as np

## Set Journal Options to Coordinate mode incase we want to look at output .rpy and double check values
session.journalOptions.setValues(replayGeometry=COORDINATE, recoverGeometry=COORDINATE)

# Job Name

filename = os.path.basename (inspect.stack()[0][1])
jobname = os.path.splitext(filename)[0]
jobname = jobname.replace('_Extract', '')

## Extract Results and Process Data
# Open OBD File

path = './'
myodbpath = path + jobname + '.odb'

odb = openOdb(path=myodbpath)
step1=odb.steps['Step-1']

#Used for setup only
#print step1.historyRegions.keys()

## Calculate Geometry of Cell for Given Fiber Volume and Fiber Diameter
Fapplied=0.02
FiberDiameter=0.0071
VolumeFraction=0.6

pi=math.pi
FiberRadius=FiberDiameter/2
b=math.sqrt((pi*FiberRadius**(2))/(2*math.sqrt(3)*VolumeFraction))
c=math.sqrt(3)*b

# Pull U2

region=step1.historyRegions['Node LEFTREF-1.1']
u2Data=region.historyOutputs['U2'].data

# Pull U3

region=step1.historyRegions['Node TOPREF-1.1']
u3Data=region.historyOutputs['U3'].data

# Extract U2 and U3 from tuples

U2=u2Data[1]
U2=U2[1]

U3=u3Data[1]
U3=U3[1]

# Calculate desired values

E2out=Fapplied/(math.sqrt(3)*b*U3)
nu23=abs(U2/(U3*math.sqrt(3)))

# Print for Fun

#print E2out
#print nu23

## Output File Creation

outputfilename=jobname+'.csv'

header=['U2 Disp', 'U3 Disp', 'Composite E2', 'Composite nu23']

outputlist=[U2, U3, E2out, nu23]

with open (outputfilename, 'wb') as out:
    writer=csv.writer(out)
    writer.writerows([header, outputlist])

odb.close()
