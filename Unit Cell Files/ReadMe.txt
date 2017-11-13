##Nathan Phelps##
##UT Knoxville##
##Hex Unit Cell Model Sobol Analysis Read Me##

This set of files generates Sobol Indexes for various geometry and material property inputs for a
hexagonal unit cell model made up of a non-homogeneous fiber and a homogeneous matrix materials.

TO RUN MODEL:
1. Run "filemaker.py", setting the desired input variables in the main() portion of the function.
The default setup runs a +-30% sweep around central estimated values for a carbon/epoxy laminate.
By default, the number of base samples is set to n=12. This is extremely low and is only useful
for demonstration of the process. For actual analysis, this should be set to n~=1000-5000 depending
on desired level of accuracy.

2. Run "Runscriptnew.py", with start=1 and end=nsamples. Leave runtype='separate' to performa full 
analysis. Set desired values for cpucount, cores_per_job, and cae_cpu_limit. Default values are 
set based off of the author's computing and license resources and may not be appropriate for
 your workstation or cluster.

3. Inside the results folder, run "CSVreader.py". This simply collects all of the outputs into a
single CSV file.

4. Run "Compute Sobol Results.py". View results in the console.h

NOTES:
2. Element type may be switched between reduced and full integration by commenting/uncommenting
sections in the Model Generation Python code. Reduced integration is used by default.

3. Boundary conditions are periodic and enforced using equation constraints. The current model
does not model shear loadings as the boundary condition formulation does not allow for out of
plane deformations.

SETTING MATERIAL PROPERTIES AND RETRIEVING OUTPUTS:
1. Material proprties and cell geometry is set in the python script.

2. The fiber is modelled as a non-isotropic elastic solid. The matrix is modelled as an isotropic
elastic solid.

3. Realistic volume fractions are between roughly .4 and .7. Choosing a range between .4 and .85
is safe for the current mesh controls. Values above .85 will cause problems with sliver elements.

4. All material properties are currently in metric units. Length is in mm, pressure is in MPa.
All other units follow keeping proper scaling to mm as the base unit.

5. Model inputs:

	Basic Geometry:

		FiberDiameter=Diameter of fiber (mm)
		VolumeFraction=Volume Fraction in Decimal Form

	Material Properties

		Fiber:
			E1, E2, E3 = Fiber Tensile Moduli (MPa)
			Nu12f, Nu13f, Nu23f = Fiber Poisson's Ratios
			G12f, G13f, G23f = Fiber Shear Moduli
		Matrix:
			
			Ema = Matrix Tensile Modulus
			Numa = Matrix Poisson's Ratio

6. The model outputs the input properties as well as the Young's Modulus and Poisson's Ratio to a CSV file.

USEFUL CODE LOCATIONS:

UnitCellProbabilistic.py:

Line #		Note:
36-54		Material Property and Geometry Inputs. Do NOT change material properties elsewhere.
68-78		Mesh Control Settings
82		Magnitude of Applied Force
532-565		Element Integration Settings--Full or Reduced Integration
730-749		Loading Choice. E1, E2, E3 cases. NOTE: Current model only setup to extract E and nu from E2 case.

Filemaker.py:

Line #		Note:
25-29		Setup file naming convention
32		Set Applied Force. Stock value is tuned for stock dimensions
40~51		Setup Sobol problem Dict

Runscriptnew.py

Line #		Note:
28-30		Setup run parameters

