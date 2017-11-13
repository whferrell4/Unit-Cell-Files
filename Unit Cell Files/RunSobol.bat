@echo off
python filemaker.py
python Runscriptnew.py
copy CSVreader.py "./Results/CSVreader.py"
copy "Compute Sobol Results.py" "./Results/Compute Sobol Results.py"
cd Results
python CSVreader.py
python "Compute Sobol Results.py"
cmd /k