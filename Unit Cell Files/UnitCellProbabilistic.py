# Nathan Phelps
# University of Tennessee Knoxville Mechanical Engineering
# -*- coding: mbcs -*-
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
import csv
import fileinput
session.journalOptions.setValues(replayGeometry=COORDINATE, recoverGeometry=COORDINATE)

## Import Python Math Library

import math

## Define Parameters

# Job Name

filename = os.path.basename (inspect.stack()[0][1])
jobname = os.path.splitext(filename)[0]

# Geometry

FiberDiameter=<FiberD>
VolumeFraction=<Vf>

# Fiber Properties

E1f = <E1f>
E2f = <E2f>
E3f = E2f
Nu12f = <Nu12f>
Nu13f = Nu12f
Nu23f = <Nu23f>
G12f = <G12f>*1000
G13f = G12f
G23f = E2f/(2*(1+Nu23f))

# Matrix Properties

Ema = <Ema>
Numa = <Numa>

## Calculate Geometry of Cell for Given Fiber Volume and Fiber Diameter

pi=math.pi
FiberRadius=FiberDiameter/2
l=math.sqrt((2*pi*FiberRadius**(2))/((math.sqrt(3))*VolumeFraction))
b=.5*l
c=math.sqrt(3)*l/2

## Parameterize Mesh

# Reference values: quartel = 15, elsize = .0001, squarel = 8, throughthick = 44

quartel = 12 # Number of elements on each quarter circle

shortedgesize=.0003 # Size of elements in octagonal region

cross = 15 # Number of elements on diagonal split

elbetween=6 # Number of Elements between Square in Center of Fiber and Edge of Fiber

throughthick=24 # Number of elements through thickness of unit cell

longedge=9

## Parameterize Force

Fapplied=<Fapplied>

## Create Parameterized Base Geometry

mdb.models['Model-1'].ConstrainedSketch(name='__profile__', sheetSize=0.02)
mdb.models['Model-1'].sketches['__profile__'].sketchOptions.setValues(
    decimalPlaces=4)
mdb.models['Model-1'].sketches['__profile__'].rectangle(point1=(0.0, 0.0), 
    point2=(-c, b))
mdb.models['Model-1'].sketches['__profile__'].vertices.findAt((0.0, 0.0))
mdb.models['Model-1'].sketches['__profile__'].FixedConstraint(entity=
    mdb.models['Model-1'].sketches['__profile__'].vertices.findAt((0.0, 0.0), 
    ))
mdb.models['Model-1'].sketches['__profile__'].vertices.findAt((-c, 
    b))
mdb.models['Model-1'].sketches['__profile__'].vertices.findAt((-c, 0.0))
mdb.models['Model-1'].sketches['__profile__'].ObliqueDimension(textPoint=(
    -0.00794666633009911, 0.00168132735416293), value=b, vertex1=
    mdb.models['Model-1'].sketches['__profile__'].vertices.findAt((-c, 
    b), ), vertex2=
    mdb.models['Model-1'].sketches['__profile__'].vertices.findAt((-c, 
    0.0), ))
mdb.models['Model-1'].sketches['__profile__'].vertices.findAt((0.0, b))
mdb.models['Model-1'].sketches['__profile__'].vertices.findAt((-c, 
    b))
mdb.models['Model-1'].sketches['__profile__'].ObliqueDimension(textPoint=(
    -0.0054130363278091, 0.00443314155563712), value=c, vertex1=
    mdb.models['Model-1'].sketches['__profile__'].vertices.findAt((0.0, 
    b), ), vertex2=
    mdb.models['Model-1'].sketches['__profile__'].vertices.findAt((-c, 
    b), ))
mdb.models['Model-1'].Part(dimensionality=THREE_D, name='QuarterCell', type=
    DEFORMABLE_BODY)
mdb.models['Model-1'].parts['QuarterCell'].BaseSolidExtrude(depth=b, 
    sketch=mdb.models['Model-1'].sketches['__profile__'])
del mdb.models['Model-1'].sketches['__profile__']

## Create Reference CSys

mdb.models['Model-1'].parts['QuarterCell'].DatumCsysByThreePoints(coordSysType=
    CARTESIAN, line1=(1.0, 0.0, 0.0), line2=(0.0, 1.0, 0.0), name='CSYS1', 
    origin=(0.0, 0.0, 0.0))
    
 ## Create Partitions
 
mdb.models['Model-1'].ConstrainedSketch(gridSpacing=0.0004, name='__profile__', 
    sheetSize=0.0195, transform=
    mdb.models['Model-1'].parts['QuarterCell'].MakeSketchTransform(
    sketchPlane=mdb.models['Model-1'].parts['QuarterCell'].faces.findAt((
    -c/2, b/2, b), ), sketchPlaneSide=SIDE1, 
    sketchUpEdge=mdb.models['Model-1'].parts['QuarterCell'].datums[2].axis2, 
    sketchOrientation=RIGHT, origin=(0.0, 0.0, b)))
mdb.models['Model-1'].sketches['__profile__'].sketchOptions.setValues(
    decimalPlaces=4)
mdb.models['Model-1'].sketches['__profile__'].rectangle(point1=(0.0, 0.0), 
    point2=(-c, b))
mdb.models['Model-1'].sketches['__profile__'].vertices.findAt((0.0, b))
mdb.models['Model-1'].sketches['__profile__'].vertices.findAt((-c, 
    b))
mdb.models['Model-1'].sketches['__profile__'].ObliqueDimension(textPoint=(
    -0.00599511526525021, 0.00650192238390446), value=c, vertex1=
    mdb.models['Model-1'].sketches['__profile__'].vertices.findAt((0.0, 
    b), ), vertex2=
    mdb.models['Model-1'].sketches['__profile__'].vertices.findAt((-c, 
    b), ))
mdb.models['Model-1'].sketches['__profile__'].vertices.findAt((-c, 
    b))
mdb.models['Model-1'].sketches['__profile__'].vertices.findAt((-c, 0.0))
mdb.models['Model-1'].sketches['__profile__'].ObliqueDimension(textPoint=(
    -0.0114708850160241, 0.00396986957639456), value=b, vertex1=
    mdb.models['Model-1'].sketches['__profile__'].vertices.findAt((-c, 
    b), ), vertex2=
    mdb.models['Model-1'].sketches['__profile__'].vertices.findAt((-c, 
    0.0), ))
mdb.models['Model-1'].sketches['__profile__'].vertices.findAt((0.0, 0.0))
mdb.models['Model-1'].sketches['__profile__'].FixedConstraint(entity=
    mdb.models['Model-1'].sketches['__profile__'].vertices.findAt((0.0, 0.0), 
    ))
mdb.models['Model-1'].sketches['__profile__'].CircleByCenterPerimeter(center=(
    -c, b), point1=(-c, b+FiberRadius))
mdb.models['Model-1'].sketches['__profile__'].CircleByCenterPerimeter(center=(
    0.0, 0.0), point1=(0, -FiberRadius))
mdb.models['Model-1'].sketches['__profile__'].rectangle(point1=(0.0, 0), 
    point2=(-FiberRadius/1.85, FiberRadius/1.85))
mdb.models['Model-1'].sketches['__profile__'].rectangle(point1=(-c, 
    b), point2=(-c+FiberRadius/1.85, b-FiberRadius/1.85))

d=math.sqrt(FiberRadius**(2)/2)

mdb.models['Model-1'].sketches['__profile__'].Line(point1=(-c+FiberRadius/1.85, b-FiberRadius/1.85), 
    point2=(-c+d, b-d))
mdb.models['Model-1'].sketches['__profile__'].Line(point1=(-FiberRadius/1.85, FiberRadius/1.85), 
    point2=(-d, d))   
mdb.models['Model-1'].parts['QuarterCell'].PartitionFaceBySketch(faces=
    mdb.models['Model-1'].parts['QuarterCell'].faces.findAt(((-c/2, 
    b/2, b), )), sketch=
    mdb.models['Model-1'].sketches['__profile__'], sketchUpEdge=
    mdb.models['Model-1'].parts['QuarterCell'].datums[2].axis2)
del mdb.models['Model-1'].sketches['__profile__']
 
## Create Second PartitionFaceBySketch

mdb.models['Model-1'].ConstrainedSketch(gridSpacing=0.0004, name='__profile__', 
    sheetSize=0.0174, transform=
    mdb.models['Model-1'].parts['QuarterCell'].MakeSketchTransform(
    sketchPlane=mdb.models['Model-1'].parts['QuarterCell'].faces.findAt((
    -c/2, b/2, b), ), sketchPlaneSide=SIDE1, 
    sketchUpEdge=mdb.models['Model-1'].parts['QuarterCell'].datums[2].axis2, 
    sketchOrientation=RIGHT, origin=(0.0, 0.0, b)))
mdb.models['Model-1'].sketches['__profile__'].sketchOptions.setValues(
    decimalPlaces=4)
mdb.models['Model-1'].sketches['__profile__'].rectangle(point1=(0.0, 0.0), 
    point2=(-0.01, 0.0062))
mdb.models['Model-1'].sketches['__profile__'].geometry.findAt((0.0, 0.0031))
mdb.models['Model-1'].sketches['__profile__'].geometry.findAt((-0.005, 0.0062))
mdb.models['Model-1'].sketches['__profile__'].geometry.findAt((-0.01, 0.0031))
mdb.models['Model-1'].sketches['__profile__'].geometry.findAt((-0.005, 0.0))
mdb.models['Model-1'].sketches['__profile__'].setAsConstruction(objectList=(
    mdb.models['Model-1'].sketches['__profile__'].geometry.findAt((0.0, 
    0.0031), ), mdb.models['Model-1'].sketches['__profile__'].geometry.findAt((
    -0.005, 0.0062), ), 
    mdb.models['Model-1'].sketches['__profile__'].geometry.findAt((-0.01, 
    0.0031), ), mdb.models['Model-1'].sketches['__profile__'].geometry.findAt((
    -0.005, 0.0), )))
mdb.models['Model-1'].sketches['__profile__'].ConstructionLine(point1=(-0.01, 
    0.0062), point2=(0.0, 0.0))
mdb.models['Model-1'].sketches['__profile__'].vertices.findAt((-0.01, 0.0062))
mdb.models['Model-1'].sketches['__profile__'].geometry.findAt((-0.005, 0.0031))
mdb.models['Model-1'].sketches['__profile__'].CoincidentConstraint(
    addUndoState=False, entity1=
    mdb.models['Model-1'].sketches['__profile__'].vertices.findAt((-0.01, 
    0.0062), ), entity2=
    mdb.models['Model-1'].sketches['__profile__'].geometry.findAt((-0.005, 
    0.0031), ))
mdb.models['Model-1'].sketches['__profile__'].vertices.findAt((0.0, 0.0))
mdb.models['Model-1'].sketches['__profile__'].geometry.findAt((-0.005, 0.0031))
mdb.models['Model-1'].sketches['__profile__'].CoincidentConstraint(
    addUndoState=False, entity1=
    mdb.models['Model-1'].sketches['__profile__'].vertices.findAt((0.0, 0.0), )
    , entity2=mdb.models['Model-1'].sketches['__profile__'].geometry.findAt((
    -0.005, 0.0031), ))
mdb.models['Model-1'].sketches['__profile__'].Line(point1=(-0.0006, 0.0102), 
    point2=(-0.0091, -0.0067))
mdb.models['Model-1'].sketches['__profile__'].geometry.findAt((-0.00485, 
    0.00175))
mdb.models['Model-1'].sketches['__profile__'].geometry.findAt((-0.005, 0.0031))
mdb.models['Model-1'].sketches['__profile__'].PerpendicularConstraint(entity1=
    mdb.models['Model-1'].sketches['__profile__'].geometry.findAt((-0.00485, 
    0.00175), ), entity2=
    mdb.models['Model-1'].sketches['__profile__'].geometry.findAt((-0.005, 
    0.0031), ))
mdb.models['Model-1'].sketches['__profile__'].vertices.findAt((0.0, 0.0))
mdb.models['Model-1'].sketches['__profile__'].FixedConstraint(entity=
    mdb.models['Model-1'].sketches['__profile__'].vertices.findAt((0.0, 0.0), 
    ))
mdb.models['Model-1'].sketches['__profile__'].vertices.findAt((0.0, 0.0))
mdb.models['Model-1'].sketches['__profile__'].vertices.findAt((0.0, 0.0062))
mdb.models['Model-1'].sketches['__profile__'].ObliqueDimension(textPoint=(
    0.00517026148736477, 0.00418311450630426), value=0.0062, vertex1=
    mdb.models['Model-1'].sketches['__profile__'].vertices.findAt((0.0, 0.0), )
    , vertex2=mdb.models['Model-1'].sketches['__profile__'].vertices.findAt((
    0.0, 0.0062), ))
mdb.models['Model-1'].sketches['__profile__'].vertices.findAt((0.0, 0.0062))
mdb.models['Model-1'].sketches['__profile__'].vertices.findAt((-0.01, 0.0062))
mdb.models['Model-1'].sketches['__profile__'].ObliqueDimension(textPoint=(
    -0.00727017316967249, 0.0100913653150201), value=0.01, vertex1=
    mdb.models['Model-1'].sketches['__profile__'].vertices.findAt((0.0, 
    0.0062), ), vertex2=
    mdb.models['Model-1'].sketches['__profile__'].vertices.findAt((-0.01, 
    0.0062), ))
mdb.models['Model-1'].sketches['__profile__'].geometry.findAt((-0.004915, 
    0.001787))
mdb.models['Model-1'].sketches['__profile__'].vertices.findAt((0.0, 0.0))
mdb.models['Model-1'].sketches['__profile__'].DistanceDimension(entity1=
    mdb.models['Model-1'].sketches['__profile__'].geometry.findAt((-0.004915, 
    0.001787), ), entity2=
    mdb.models['Model-1'].sketches['__profile__'].vertices.findAt((0.0, 0.0), )
    , textPoint=(-0.00328630208969116, -0.00360503420233727), value=
    b)
mdb.models['Model-1'].sketches['__profile__'].dimensions[1].setValues(value=c)
mdb.models['Model-1'].sketches['__profile__'].dimensions[0].setValues(value=b)   
mdb.models['Model-1'].parts['QuarterCell'].PartitionFaceBySketch(faces=
    mdb.models['Model-1'].parts['QuarterCell'].faces.findAt(((-c/2, 
    b/2, b), )), sketch=
    mdb.models['Model-1'].sketches['__profile__'], sketchUpEdge=
    mdb.models['Model-1'].parts['QuarterCell'].datums[2].axis2)
del mdb.models['Model-1'].sketches['__profile__']

## Create Cells

mdb.models['Model-1'].parts['QuarterCell'].PartitionCellByExtrudeEdge(cells=
    mdb.models['Model-1'].parts['QuarterCell'].cells.findAt(
        ((-c+.0001, b-.0001, b/2), )), 
        edges=(mdb.models['Model-1'].parts['QuarterCell'].edges.findAt(
        (-c+FiberRadius/1.85, b-FiberRadius/(1.85*2), b), ), 
        mdb.models['Model-1'].parts['QuarterCell'].edges.findAt(
        (-c+FiberRadius/(1.85*2), b-FiberRadius/1.85, b), )), 
        line=mdb.models['Model-1'].parts['QuarterCell'].datums[2].axis3, sense=REVERSE)
    
mdb.models['Model-1'].parts['QuarterCell'].PartitionCellByExtrudeEdge(cells=
    mdb.models['Model-1'].parts['QuarterCell'].cells.findAt(
        ((-.0001, 0.0001, b/2), )), 
        edges=(mdb.models['Model-1'].parts['QuarterCell'].edges.findAt(
        (-FiberRadius/(1.85*2), FiberRadius/1.85, b), ), 
        mdb.models['Model-1'].parts['QuarterCell'].edges.findAt(
        (-FiberRadius/1.85, FiberRadius/(1.85*2), b), )), 
        line=mdb.models['Model-1'].parts['QuarterCell'].datums[2].axis3, sense=REVERSE)
    
# Make Variables to find curves

e=(math.sin(pi/8))*FiberRadius
f=(math.cos(pi/8))*FiberRadius
g=(math.cos(pi/4))*FiberRadius
    
mdb.models['Model-1'].parts['QuarterCell'].PartitionCellByExtrudeEdge(cells=
    mdb.models['Model-1'].parts['QuarterCell'].cells.findAt(
        ((-c/2, b/2, b/2), )), 
        edges=(mdb.models['Model-1'].parts['QuarterCell'].edges.findAt(
        (-e, f, b), ), 
        mdb.models['Model-1'].parts['QuarterCell'].edges.findAt(
        (-g+.00001, g-.00001, b), )), 
        line=mdb.models['Model-1'].parts['QuarterCell'].datums[2].axis3, sense=REVERSE)
    
mdb.models['Model-1'].parts['QuarterCell'].PartitionCellByExtrudeEdge(cells=
    mdb.models['Model-1'].parts['QuarterCell'].cells.findAt(
        ((-c/2, b/2, b/2), )), 
        edges=(mdb.models['Model-1'].parts['QuarterCell'].edges.findAt(
        (-f, e, b), )), 
        line=mdb.models['Model-1'].parts['QuarterCell'].datums[2].axis3, sense=REVERSE)

mdb.models['Model-1'].parts['QuarterCell'].PartitionCellByExtrudeEdge(cells=
    mdb.models['Model-1'].parts['QuarterCell'].cells.findAt(
        ((-c/2, b/2, b/2), )), 
        edges=(mdb.models['Model-1'].parts['QuarterCell'].edges.findAt(
        (-c+e, b-f, b), ), 
        mdb.models['Model-1'].parts['QuarterCell'].edges.findAt(
        (-c+g-.00001, b-g+.00001, b), )), 
        line=mdb.models['Model-1'].parts['QuarterCell'].datums[2].axis3, sense=REVERSE)
    
mdb.models['Model-1'].parts['QuarterCell'].PartitionCellByExtrudeEdge(cells=
    mdb.models['Model-1'].parts['QuarterCell'].cells.findAt(
        ((-c/2, b/2, b/2), )), 
        edges=(mdb.models['Model-1'].parts['QuarterCell'].edges.findAt(
        (-c+f, b-e, b), )), 
        line=mdb.models['Model-1'].parts['QuarterCell'].datums[2].axis3, sense=REVERSE)
    
mdb.models['Model-1'].parts['QuarterCell'].PartitionCellByExtrudeEdge(cells=
    mdb.models['Model-1'].parts['QuarterCell'].cells.findAt(
        ((-c/2, b/2, b/2), )), 
        edges=(mdb.models['Model-1'].parts['QuarterCell'].edges.findAt(
        (-c/2, b/2, b), )), 
        line=mdb.models['Model-1'].parts['QuarterCell'].datums[2].axis3, sense=REVERSE)
    
## Create Sets

mdb.models['Model-1'].parts['QuarterCell'].Set(cells=
    mdb.models['Model-1'].parts['QuarterCell'].cells.findAt(
        ((-FiberRadius/3, FiberRadius/3, 0), ), 
        ((-FiberRadius*.9, FiberRadius*.1, 0), ), 
        ((-FiberRadius*.1, FiberRadius*.9, 0), ), 
        ((-c+FiberRadius/3, b-FiberRadius/2, 0), ), 
        ((-c+FiberRadius*.9, b-FiberRadius*.1, 0), ), 
        ((-c+FiberRadius*.1, b-FiberRadius*.9, 0), ),
        ), name='Fiber')
    
mdb.models['Model-1'].parts['QuarterCell'].Set(cells=
    mdb.models['Model-1'].parts['QuarterCell'].cells.findAt(
        ((0, b, 0), ), 
        ((-c, 0, 0), ), 
        ), name='Matrix')
    
## Define Materials
    
mdb.models['Model-1'].Material(name='FIBERMATERIAL')
mdb.models['Model-1'].materials['FIBERMATERIAL'].Elastic(table=((E1f, 
    E2f, E3f, Nu12f, Nu13f, Nu23f, G12f, G13f, G23f
), ), 
    type=ENGINEERING_CONSTANTS)
mdb.models['Model-1'].Material(name='MATRIXMATERIAL')
mdb.models['Model-1'].materials['MATRIXMATERIAL'].Elastic(table=((Ema, 
    Numa), ))
mdb.models['Model-1'].HomogeneousSolidSection(material='MATRIXMATERIAL', name=
    'MATRIXSECTION', thickness=None)
mdb.models['Model-1'].HomogeneousSolidSection(material='FIBERMATERIAL', name=
    'FIBERSECTION', thickness=None)
    
## Assign Sections

mdb.models['Model-1'].parts['QuarterCell'].SectionAssignment(offset=0.0, 
    offsetField='', offsetType=MIDDLE_SURFACE, region=
    mdb.models['Model-1'].parts['QuarterCell'].sets['Fiber'], sectionName=
    'FIBERSECTION', thicknessAssignment=FROM_SECTION)
mdb.models['Model-1'].parts['QuarterCell'].SectionAssignment(offset=0.0, 
    offsetField='', offsetType=MIDDLE_SURFACE, region=
    mdb.models['Model-1'].parts['QuarterCell'].sets['Matrix'], sectionName=
    'MATRIXSECTION', thicknessAssignment=FROM_SECTION)
    
## Assign Fiber Material Orientation

mdb.models['Model-1'].parts['QuarterCell'].MaterialOrientation(
    additionalRotationField='', additionalRotationType=ROTATION_ANGLE, angle=
    -90.0, axis=AXIS_2, fieldName='', localCsys=None, orientationType=SYSTEM, 
    region=mdb.models['Model-1'].parts['QuarterCell'].sets['Fiber'], 
    stackDirection=STACK_3)

    
## Create Mesh

# Through Thickness
mdb.models['Model-1'].parts['QuarterCell'].seedEdgeByNumber(constraint=FINER, 
    edges=mdb.models['Model-1'].parts['QuarterCell'].edges.findAt(
        ((0.0, 0.0, b/2), ), 
        ((-FiberRadius/1.85, 0.0, b/2), ), 
        ((-FiberRadius/1.85, FiberRadius/1.85, b/2), ), 
        ((0.0, 0.0, b/2), ), ((0, FiberRadius/1.85, b/2), ), 
        ((-FiberRadius*math.sqrt(2)*.5, FiberRadius*math.sqrt(2)*.5, b/2), ), 
        ((-FiberRadius, 0, b/2), ), ((0.0, FiberRadius, b/2), ), 
        ((-c, 0.0, b/2), ), ((-c, b, b/2), ), 
        ((-c, b-FiberRadius/1.85, b/2), ), 
        ((-c+FiberRadius/1.85, b-FiberRadius/1.85, b/2), ), 
        ((-c+FiberRadius/1.85, b, b/2), ), 
        ((-c+FiberRadius, b, b/2), ), ((-c, b-FiberRadius, b/2), ), 
        ((-c+FiberRadius*math.sqrt(2)*.5, b-FiberRadius*math.sqrt(2)*.5, b/2), ), 
        ((-b*2/math.sqrt(3), 0.0, b/2), ), 
        ((-c+b*2/math.sqrt(3), b, b/2), ), 
        ), number=throughthick)
    
# Quarter Circles and Related
mdb.models['Model-1'].parts['QuarterCell'].seedEdgeByNumber(constraint=FINER, 
    edges=mdb.models['Model-1'].parts['QuarterCell'].edges.findAt(
        # Front
        ((-FiberRadius/(1.85*2), 0.0, b), ),
        ((-FiberRadius/1.85, FiberRadius/(1.85*2), b), ), 
        ((-FiberRadius/(1.85*2), FiberRadius/1.85, b), ), 
        ((0.0, FiberRadius/(1.85*2), b), ), 
        ((-FiberRadius*.5, FiberRadius*math.sqrt(3)*.5, b), ), 
        ((-FiberRadius*math.sqrt(3)*.5, FiberRadius*.5, b), ), 
        ((-c, b-FiberRadius/(1.85*2), b), ), 
        ((-c+FiberRadius/(1.85*2), b, b), ), 
        ((-c+FiberRadius/1.85, b-FiberRadius/(2*1.85), b), ), 
        ((-c+FiberRadius/(1.85*2), b-FiberRadius/1.85, b), ), 
        ((-c+FiberRadius*.5, b-FiberRadius*math.sqrt(3)*.5, b), ), 
        ((-c+FiberRadius*math.sqrt(3)*.5, b-FiberRadius*.5, b), ), 
        
        # Back
        ((-FiberRadius/(1.85*2), 0.0, 0.0), ), 
        ((-FiberRadius/1.85, FiberRadius/(1.85*2), 0.0), ), 
        ((-FiberRadius/(1.85*2), FiberRadius/1.85, 0.0), ), 
        ((0.0, FiberRadius/(1.85*2), 0.0), ), 
        ((-FiberRadius*.5, FiberRadius*math.sqrt(3)*.5, 0.0), ), 
        ((-FiberRadius*math.sqrt(3)*.5, FiberRadius*.5, 0.0), ),
        ((-c, b-FiberRadius/(1.85*2), 0.0), ), 
        ((-c+FiberRadius/(1.85*2), b, 0.0), ), 
        ((-c+FiberRadius/1.85, b-FiberRadius/(2*1.85), 0.0), ), 
        ((-c+FiberRadius/(1.85*2), b-FiberRadius/1.85, 0.0), ), 
        ((-c+FiberRadius*.5, b-FiberRadius*math.sqrt(3)*.5, 0.0), ),
        ((-c+FiberRadius*math.sqrt(3)*.5, b-FiberRadius*.5, 0.0), ),
        ), number=quartel)
        
# Quarter Interstitial
mdb.models['Model-1'].parts['QuarterCell'].seedEdgeByNumber(constraint=FINER, 
    edges=mdb.models['Model-1'].parts['QuarterCell'].edges.findAt(
        # Front
        ((0.0, FiberRadius*.95, b), ),
        ((-FiberRadius*math.sqrt(2)*.5*.99, FiberRadius*math.sqrt(2)*.5*.99, b), ), 
        ((-FiberRadius*.99, 0.0, b), ), 
        ((-c+FiberRadius*.99, b, b), ), 
        ((-c+FiberRadius*math.sqrt(2)*.5*.99, b-FiberRadius*math.sqrt(2)*.5*.99, b), ), 
        ((-c, b-FiberRadius*.99, b), ), 
        
        # Back
        ((0.0, FiberRadius*.95, 0.0), ),
        ((-FiberRadius*math.sqrt(2)*.5*.99, FiberRadius*math.sqrt(2)*.5*.99, 0.0), ), 
        ((-FiberRadius*.99, 0.0, 0.0), ), 
        ((-c+FiberRadius*.99, b, 0.0), ), 
        ((-c+FiberRadius*math.sqrt(2)*.5*.99, b-FiberRadius*math.sqrt(2)*.5*.99, 0.0), ), 
        ((-c, b-FiberRadius*.99, 0.0), ), 
        ), number=elbetween)
        
# Cross Split
mdb.models['Model-1'].parts['QuarterCell'].seedEdgeByNumber(constraint=FINER, 
    edges=mdb.models['Model-1'].parts['QuarterCell'].edges.findAt(
        # Front
        ((-c/2, b/2 , b), ),
        
        # Back
        ((-c/2, b/2, 0.0), ), 
        ), number=cross)
        
# Long Matrix Edge
mdb.models['Model-1'].parts['QuarterCell'].seedEdgeByNumber(constraint=FINER, 
    edges=mdb.models['Model-1'].parts['QuarterCell'].edges.findAt(
        # Front
        ((-.0001, b , b), ),
        ((-c+.0001, 0.0 , b), ),
        
        # Back
        ((-.0001, b , 0.0), ),
        ((-c+.0001, 0.0 , 0.0), ), 
        ), number=longedge)
        
# Middle Matrix edge
mdb.models['Model-1'].parts['QuarterCell'].seedEdgeBySize(constraint=FINER, 
    edges=mdb.models['Model-1'].parts['QuarterCell'].edges.findAt(
        # Front
        ((-c+FiberRadius+.0001, b , b), ),
        ((-FiberRadius-.0001, 0.0 , b), ),
        
        # Back
        ((-c+FiberRadius+.0001, b , 0.0), ),
        ((-FiberRadius-.0001, 0.0 , 0.0), ),
        ), size=shortedgesize)
        
# Short Matrix edge
mdb.models['Model-1'].parts['QuarterCell'].seedEdgeBySize(constraint=FINER, 
    edges=mdb.models['Model-1'].parts['QuarterCell'].edges.findAt(
        # Front
        ((0.0, b-.0001 , b), ),
        ((-c, .0001 , b), ),
        
        # Back
        ((0.0, b-.0001 , 0.0), ),
        ((-c, .0001 , 0.0), ),
        ), size=shortedgesize)
        
# Set Stack Direction

mdb.models['Model-1'].parts['QuarterCell'].assignStackDirection(cells=
    mdb.models['Model-1'].parts['QuarterCell'].cells.findAt(
        ((-FiberRadius/3, FiberRadius/3, 0), ), 
        ((-FiberRadius*.9, FiberRadius*.1, 0), ), 
        ((-FiberRadius*.1, FiberRadius*.9, 0), ), 
        ((-c+FiberRadius/3, b-FiberRadius/2, 0), ), 
        ((-c+FiberRadius*.9, b-FiberRadius*.1, 0), ), 
        ((-c+FiberRadius*.1, b-FiberRadius*.9, 0), ), 
        ((0, b, 0), ),
        ((-c, 0, 0), ), 
        ), referenceRegion=
        mdb.models['Model-1'].parts['QuarterCell'].faces.findAt(
            (-FiberRadius/4, FiberRadius/4, b), ))

# Set Mesh Controls

mdb.models['Model-1'].parts['QuarterCell'].setMeshControls(algorithm=
    MEDIAL_AXIS, regions=
    mdb.models['Model-1'].parts['QuarterCell'].cells.findAt(
        ((0, b, 0), ),
        ((-c, 0, 0), ), ))

# Set Element Type

# Full Integration

#mdb.models['Model-1'].parts['QuarterCell'].setElementType(elemTypes=(ElemType(
#   elemCode=C3D8, elemLibrary=STANDARD, secondOrderAccuracy=OFF, 
#    distortionControl=DEFAULT), ElemType(elemCode=C3D6, elemLibrary=STANDARD), 
#    ElemType(elemCode=C3D4, elemLibrary=STANDARD)), regions=(
#    mdb.models['Model-1'].parts['QuarterCell'].cells.findAt(
#        ((-FiberRadius/3, FiberRadius/3, 0), ), 
#        ((-FiberRadius*.9, FiberRadius*.1, 0), ), 
#        ((-FiberRadius*.1, FiberRadius*.9, 0), ), 
#        ((-c+FiberRadius/3, b-FiberRadius/2, 0), ), 
#        ((-c+FiberRadius*.9, b-FiberRadius*.1, 0), ), 
#        ((-c+FiberRadius*.1, b-FiberRadius*.9, 0), ), 
#        ((0, b, 0), ),
#        ((-c, 0, 0), ), ), ))

# Reduced Integration

mdb.models['Model-1'].parts['QuarterCell'].setElementType(elemTypes=(ElemType(
    elemCode=C3D8R, elemLibrary=STANDARD, secondOrderAccuracy=OFF, 
    distortionControl=DEFAULT), ElemType(elemCode=C3D6, elemLibrary=STANDARD), 
    ElemType(elemCode=C3D4, elemLibrary=STANDARD)), regions=(
    mdb.models['Model-1'].parts['QuarterCell'].cells.findAt(
        ((-FiberRadius/3, FiberRadius/3, 0), ), 
        ((-FiberRadius*.9, FiberRadius*.1, 0), ), 
        ((-FiberRadius*.1, FiberRadius*.9, 0), ), 
        ((-c+FiberRadius/3, b-FiberRadius/2, 0), ), 
        ((-c+FiberRadius*.9, b-FiberRadius*.1, 0), ), 
        ((-c+FiberRadius*.1, b-FiberRadius*.9, 0), ), 
        ((0, b, 0), ),
        ((-c, 0, 0), ), ), ))

# Generate Mesh

mdb.models['Model-1'].parts['QuarterCell'].generateMesh()

## Create Reference Points

mdb.models['Model-1'].Part(dimensionality=THREE_D, name='FrontRef', type=
    DISCRETE_RIGID_SURFACE)
mdb.models['Model-1'].parts['FrontRef'].ReferencePoint(point=(b, c/2, b/2))

mdb.models['Model-1'].Part(dimensionality=THREE_D, name='BackRef', type=
    DISCRETE_RIGID_SURFACE)
mdb.models['Model-1'].parts['BackRef'].ReferencePoint(point=(0, c/2, b/2))

mdb.models['Model-1'].Part(dimensionality=THREE_D, name='LeftRef', type=
    DISCRETE_RIGID_SURFACE)
mdb.models['Model-1'].parts['LeftRef'].ReferencePoint(point=(b/2, c, b/2))

mdb.models['Model-1'].Part(dimensionality=THREE_D, name='RightRef', type=
    DISCRETE_RIGID_SURFACE)
mdb.models['Model-1'].parts['RightRef'].ReferencePoint(point=(b/2, 0.0, b/2))

mdb.models['Model-1'].Part(dimensionality=THREE_D, name='TopRef', type=
    DISCRETE_RIGID_SURFACE)
mdb.models['Model-1'].parts['TopRef'].ReferencePoint(point=(b/2, c/2, b))

mdb.models['Model-1'].Part(dimensionality=THREE_D, name='BottomRef', type=
    DISCRETE_RIGID_SURFACE)
mdb.models['Model-1'].parts['BottomRef'].ReferencePoint(point=(b/2, c/2, 0.0))



## Assembly

## Instantiate Parts

mdb.models['Model-1'].rootAssembly.DatumCsysByDefault(CARTESIAN)

mdb.models['Model-1'].rootAssembly.Instance(dependent=ON, name='QuarterCell-1', 
    part=mdb.models['Model-1'].parts['QuarterCell'])

mdb.models['Model-1'].rootAssembly.Instance(dependent=ON, name='FrontRef-1', 
    part=mdb.models['Model-1'].parts['FrontRef'])

mdb.models['Model-1'].rootAssembly.Instance(dependent=ON, name='BackRef-1', 
    part=mdb.models['Model-1'].parts['BackRef'])

mdb.models['Model-1'].rootAssembly.Instance(dependent=ON, name='RightRef-1', 
    part=mdb.models['Model-1'].parts['RightRef'])
    
mdb.models['Model-1'].rootAssembly.Instance(dependent=ON, name='LeftRef-1', 
    part=mdb.models['Model-1'].parts['LeftRef'])

mdb.models['Model-1'].rootAssembly.Instance(dependent=ON, name='TopRef-1', 
    part=mdb.models['Model-1'].parts['TopRef'])
    
mdb.models['Model-1'].rootAssembly.Instance(dependent=ON, name='BottomRef-1', 
    part=mdb.models['Model-1'].parts['BottomRef'])

# Rotate so U1, U2, U3 are in correct directions

mdb.models['Model-1'].rootAssembly.rotate(angle=-90.0, axisDirection=(0.0, 
    -1, 0.0), axisPoint=(0.0, b, 0.0), instanceList=('QuarterCell-1', ))
    
mdb.models['Model-1'].rootAssembly.rotate(angle=-90.0, axisDirection=(1, 
    0.0, 0.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('QuarterCell-1', ))
    
mdb.models['Model-1'].rootAssembly.translate(instanceList=('QuarterCell-1', ), 
    vector=(0.0, 0.0, b))

# Create Face and Plane Sets
mesh_nodes=mdb.models['Model-1'].rootAssembly.instances['QuarterCell-1'].nodes 
delta=1.0e-8
xmin, ymin, zmin = 0-delta, -1, -1
xmax, ymax, zmax = 0+delta, 1, 1 

myNodes = mesh_nodes.getByBoundingBox(xmin, ymin, zmin, xmax, ymax, zmax)
mdb.models['Model-1'].rootAssembly.Set(name='YZ Plane', nodes=myNodes) 

xmin, ymin, zmin = -1, 0-delta, -1
xmax, ymax, zmax = 1, 0+delta, 1 

myNodes = mesh_nodes.getByBoundingBox(xmin, ymin, zmin, xmax, ymax, zmax)
mdb.models['Model-1'].rootAssembly.Set(name='XZ Plane', nodes=myNodes) 

xmin, ymin, zmin = -1, -1, 0-delta
xmax, ymax, zmax = 1, 1, 0+delta

myNodes = mesh_nodes.getByBoundingBox(xmin, ymin, zmin, xmax, ymax, zmax)
mdb.models['Model-1'].rootAssembly.Set(name='XY Plane', nodes=myNodes) 

xmin, ymin, zmin = -1, -1, b-delta
xmax, ymax, zmax = 1, 1, b+delta 

myNodes = mesh_nodes.getByBoundingBox(xmin, ymin, zmin, xmax, ymax, zmax)
mdb.models['Model-1'].rootAssembly.Set(name='Top', nodes=myNodes) 

xmin, ymin, zmin = b-delta, -1, -1
xmax, ymax, zmax = b+delta, 1, 1

myNodes = mesh_nodes.getByBoundingBox(xmin, ymin, zmin, xmax, ymax, zmax)
mdb.models['Model-1'].rootAssembly.Set(name='Front', nodes=myNodes) 

xmin, ymin, zmin = -1, c-delta, -1
xmax, ymax, zmax = 1, c+delta, 1 

myNodes = mesh_nodes.getByBoundingBox(xmin, ymin, zmin, xmax, ymax, zmax)
mdb.models['Model-1'].rootAssembly.Set(name='Left', nodes=myNodes) 

# Create Reference Node Sets

mdb.models['Model-1'].rootAssembly.Set(name='FrontPoint', referencePoints=(
    mdb.models['Model-1'].rootAssembly.instances['FrontRef-1'].referencePoints[1], 
    )) 
    
mdb.models['Model-1'].rootAssembly.Set(name='BackPoint', referencePoints=(
    mdb.models['Model-1'].rootAssembly.instances['BackRef-1'].referencePoints[1], 
    )) 
    
mdb.models['Model-1'].rootAssembly.Set(name='LeftPoint', referencePoints=(
    mdb.models['Model-1'].rootAssembly.instances['LeftRef-1'].referencePoints[1], 
    )) 
    
mdb.models['Model-1'].rootAssembly.Set(name='RightPoint', referencePoints=(
    mdb.models['Model-1'].rootAssembly.instances['RightRef-1'].referencePoints[1], 
    )) 
    
mdb.models['Model-1'].rootAssembly.Set(name='TopPoint', referencePoints=(
    mdb.models['Model-1'].rootAssembly.instances['TopRef-1'].referencePoints[1], 
    )) 
    
mdb.models['Model-1'].rootAssembly.Set(name='BottomPoint', referencePoints=(
    mdb.models['Model-1'].rootAssembly.instances['BottomRef-1'].referencePoints[1], 
    ))

## Create Boundary Conditions

# Symmetry Planes

mdb.models['Model-1'].XsymmBC(createStepName='Initial', localCsys=None, name=
    'X-Symm', region=mdb.models['Model-1'].rootAssembly.sets['YZ Plane'])
    
mdb.models['Model-1'].YsymmBC(createStepName='Initial', localCsys=None, name=
    'Y-Symm', region=mdb.models['Model-1'].rootAssembly.sets['XZ Plane'])
    
mdb.models['Model-1'].ZsymmBC(createStepName='Initial', localCsys=None, name=
    'Z-Symm', region=mdb.models['Model-1'].rootAssembly.sets['XY Plane'])

# Face Equations

mdb.models['Model-1'].Equation(name='FrontFacePlanar', terms=((1.0, 'Front', 1), (
    -1.0, 'FrontPoint', 1)))
    
mdb.models['Model-1'].Equation(name='TopFacePlanar', terms=((1.0, 'Top', 3), (
    -1.0, 'TopPoint', 3)))
    
mdb.models['Model-1'].Equation(name='LeftFacePlanar', terms=((1.0, 'Left', 2), (
    -1.0, 'LeftPoint', 2)))
    
## Create Step

mdb.models['Model-1'].StaticStep(maxNumInc=1000, minInc=1e-08, name='Step-1', 
    previous='Initial')
    
## Create Loads

#E1 Case

#mdb.models['Model-1'].ConcentratedForce(cf1=Fapplied, createStepName='Step-1'
#    , distributionType=UNIFORM, field='', localCsys=None, name='FrontLoad', 
#    region=mdb.models['Model-1'].rootAssembly.sets['FrontPoint'])

#E2 Case

mdb.models['Model-1'].ConcentratedForce(cf2=Fapplied, createStepName='Step-1', 
    distributionType=UNIFORM, field='', localCsys=None, name='LeftLoad', region=
    mdb.models['Model-1'].rootAssembly.sets['LeftPoint'])

#E3 Case
    
#mdb.models['Model-1'].ConcentratedForce(cf3=Fapplied, createStepName='Step-1', 
#    distributionType=UNIFORM, field='', localCsys=None, name='TopLoad', region=
#    mdb.models['Model-1'].rootAssembly.sets['TopPoint'])

## Create History Output Requests

mdb.models['Model-1'].fieldOutputRequests['F-Output-1'].setValues(frequency=
    LAST_INCREMENT)

del mdb.models['Model-1'].historyOutputRequests['H-Output-1']

mdb.models['Model-1'].HistoryOutputRequest(createStepName='Step-1', frequency=
    LAST_INCREMENT, name='H-Output-1', rebar=EXCLUDE, region=
    mdb.models['Model-1'].rootAssembly.sets['FrontPoint'], sectionPoints=
    DEFAULT, variables=('U1',))
    
mdb.models['Model-1'].HistoryOutputRequest(createStepName='Step-1', frequency=
    LAST_INCREMENT, name='H-Output-2', rebar=EXCLUDE, region=
    mdb.models['Model-1'].rootAssembly.sets['LeftPoint'], sectionPoints=
    DEFAULT, variables=('U2',))
    
mdb.models['Model-1'].HistoryOutputRequest(createStepName='Step-1',frequency=
    LAST_INCREMENT, name='H-Output-3', rebar=EXCLUDE, region=
    mdb.models['Model-1'].rootAssembly.sets['TopPoint'], sectionPoints=DEFAULT, 
    variables=('U3',))   
    
## Create Job

mdb.Job(atTime=None, contactPrint=OFF, description='', echoPrint=OFF, 
    explicitPrecision=SINGLE, getMemoryFromAnalysis=True, historyPrint=OFF, 
    memory=90, memoryUnits=PERCENTAGE, model='Model-1', modelPrint=OFF, 
    multiprocessingMode=DEFAULT, name=jobname, 
    nodalOutputPrecision=FULL, numCpus=4, numDomains=4, numGPUs=0, queue=None
    , resultsFormat=ODB, scratch='', type=ANALYSIS, userSubroutine='', 
    waitHours=0, waitMinutes=0)
    
## Write Input

mdb.jobs[jobname].writeInput()

## Setup Extract File
extractname = jobname+ '_Extract.py'
