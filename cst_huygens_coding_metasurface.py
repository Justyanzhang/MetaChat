# Call CST interface
import sys
cst_lib_path = r"d:\\Program Files (x86)\\CST Studio Suite 2022\\AMD64\\python_cst_libraries"
sys.path.append(cst_lib_path)

import pandas as pd
import os
import cst.interface
import random
# Generate 1 row with 32x32 = 1024 random 0/1 values
sequence = [random.randint(0, 1) for _ in range(5 * 5)]

# Write to CSV file (1 row, elements separated by commas)
with open("SaveMat_total.csv", "w") as f:
    f.write(",".join(map(str, sequence)) + "\n")

csv_path = "SaveMat_total.csv"  # CSV file path
output_folder = "F:\\CSTProjects"  # Your output directory (example)
if not os.path.exists(output_folder):
    os.makedirs(output_folder)
tmpPrjFile = os.path.join(output_folder, 'CSTfile.cst')

################################################################
num = 5
pattern = 1
num_points = 21
################################################################
index = pattern - 1  # The row number from filter_top.py minus 1 equals the index of the pattern to be modeled, everything else remains unchanged
data = pd.read_csv(csv_path, header=None).to_numpy().astype(int)
code = data[index].reshape(num, num)

cst = cst.interface.DesignEnvironment()
mws = cst.new_mws()
mws.save(tmpPrjFile)
modeler = mws.modeler

p = 16.17
h = 0.48
ts = 0.035
h_add = 3.72
da = 10
d = 0.76*20/num
l = d*1.2
freq = [8, 12]

# Enable Bounding Box display
sCommand = 'Plot.DrawBox "True"'
modeler.add_to_history('switch bounding box', sCommand)

# Add structural parameters to CST for easy manual operations in the CST file later
modeler.add_to_history('StoreParameter', 'StoreParameter "p", "%.3f"' % p)
modeler.add_to_history('StoreParameter', 'StoreParameter "h", "%.3f"' % h)
modeler.add_to_history('StoreParameter', 'StoreParameter "ts", "%.3f"' % ts)
modeler.add_to_history('StoreParameter', 'StoreParameter "h_add", "%.3f"' % h_add)
modeler.add_to_history('StoreParameter', 'StoreParameter "da", "%.3f"' % da)
modeler.add_to_history('StoreParameter', 'StoreParameter "l", "%.3f"' % l)
modeler.add_to_history('StoreParameter', 'StoreParameter "d", "%.3f"' % d)
for i in range(num):
    for j in range(num):
        modeler.add_to_history('StoreParameter', f'StoreParameter "a_{i+1}_{j+1}", "%d"' % int(code[i][j]))

line_break = '\n'  # Newline character, used later for VBA string concatenation
# Global unit initialization
sCommand = ['With Units',
            '.Geometry "mm"',
            '.Frequency "GHz"',
            '.Time "ns"',
            'End With']
sCommand = line_break.join(sCommand)
modeler.add_to_history('define units', sCommand)

# Switch to F solver
sCommand = ['ChangeSolverType "HF Frequency Domain"'
            ]
sCommand = line_break.join(sCommand)
modeler.add_to_history('change solver type', sCommand)

# Frequency range setup
sCommand = 'Solver.FrequencyRange "%.1f","%.1f"'  % (freq[0], freq[1])
modeler.add_to_history('define frequency range', sCommand)

sCommand = [
    'With Material',
    '.Reset',
    '.Name "Rogers RT5880 (lossy)"',
    '.Folder ""',
    '.FrqType "all"',
    '.Type "Normal"',
    '.SetMaterialUnit "GHz", "mm"',
    '.Epsilon "2.2"',
    '.Mu "1.0"',
    '.Kappa "0.0"',
    '.TanD "0.0009"',
    '.TanDFreq "10.0"',
    '.TanDGiven "True"',
    '.TanDModel "ConstTanD"',
    '.KappaM "0.0"',
    '.TanDM "0.0"',
    '.TanDMFreq "0.0"',
    '.TanDMGiven "False"',
    '.TanDMModel "ConstKappa"',
    '.DispModelEps "None"',
    '.DispModelMu "None"',
    '.DispersiveFittingSchemeEps "General 1st"',
    '.DispersiveFittingSchemeMu "General 1st"',
    '.UseGeneralDispersionEps "False"',
    '.UseGeneralDispersionMu "False"',
    '.Rho "0.0"',
    '.ThermalType "Normal"',
    '.ThermalConductivity "0.20"',
    '.SetActiveMaterial "all"',
    '.Colour "0.94", "0.82", "0.76"',
    '.Wireframe "False"',
    '.Transparency "0"',
    '.Create',
    'End With'
]
sCommand = line_break.join(sCommand)
modeler.add_to_history('define material: Rogers RT5880 (lossy)', sCommand)

# Model the dielectric substrate
Str_Name = 'sub'
Str_Component = 'Sub'
Str_Material = 'Rogers RT5880 (lossy)'
# The following block can be written as a function
sCommand = ['With Brick',
            '.Reset',
            '.Name "%s"' % Str_Name,
            '.Component "%s"' % Str_Component,
            '.Material "%s"' % Str_Material,
            '.Xrange "-p/2","p/2"',
            '.Yrange "-p/2","p/2"',
            '.Zrange "h_add/2","h_add/2 + h"',
            '.Create',
            'End With']
sCommand = line_break.join(sCommand)
modeler.add_to_history('define brick:%s:%s' % (Str_Component, Str_Name,), sCommand)
# Change the substrate color
sCommand = [
    'With Material',
    '.Name "%s"' % Str_Material,
    '.Folder ""',
    '.Colour "0.94", "0.82", "0.76"',
    '.Wireframe "False"',
    '.Reflection "False"',
    '.Allowoutline "True"',
    '.Transparentoutline "False"',
    '.Transparency "40"',
    '.ChangeColour',
    'End With'
]
sCommand = line_break.join(sCommand)
modeler.add_to_history('define material colour:%s' % Str_Material, sCommand)

# Zoom to fit size, same effect as pressing spacebar in CST
sCommand = 'Plot.ZoomToStructure'
modeler.add_to_history('ZoomToStructure', sCommand)

# Metal patches
for i in range(num):
    for j in range(num):
        Str_Name = f'a_{i+1}_{j+1}'
        Str_Component = 'Metal'
        Str_Material = 'PEC'
        # Create metal patch
        sCommand = ['With Brick',
                    '.Reset',
                    '.Name "%s"' % Str_Name,
                    '.Component "%s"' % Str_Component,
                    '.Material "%s"' % Str_Material,
                    '.Xrange "-l/2","l/2"',
                    '.Yrange "-l/2 + d*9.5","l/2 + d*9.5"',
                    '.Zrange "h_add/2 + h","h_add/2 + h + ts"',
                    '.Create',
                    'End With']
        sCommand = line_break.join(sCommand)
        modeler.add_to_history('define brick:%s:%s' % (Str_Component, Str_Name,), sCommand)
        # Move metal patch
        move_X = f'd*{i + 1 - num / 2 - 0.5}'
        move_Y = f'd*{j + 1 - num / 2 - 0.5}'
        move_Z = 0
        sCommand = ['With Transform',
                    '.Reset',
                    f'.Name "{Str_Component}:{Str_Name}"',
                    f'.Vector "{move_X}", "{move_Y}", "{move_Z}"',
                    '.UsePickedPoints "False"',
                    '.InvertPickedPoints "False"',
                    '.Repetitions "1"',
                    '.MultipleSelection "False"',
                    '.Transform "Shape", "Translate"',
                    'End With']
        sCommand = line_break.join(sCommand)
        modeler.add_to_history('transform: %s:%s' % (Str_Component, Str_Name,), sCommand)

# Merge metal patches vertically
for i in range(num - 1):
    for j in range(num):
        Str_Component = 'Metal'
        name1 = "a_" + str(1) + "_" + str(j+1)
        name2 = "a_" + str(i + 1 + 1) + "_" + str(j+1)
        sCommand = [f'Solid.Add "Metal:{name1}", "Metal:{name2}"'
                    ]
        sCommand = line_break.join(sCommand)
        modeler.add_to_history('boolean add shapes: %s:%s, %s:%s' %
                               (Str_Component, name1, Str_Component, name2,), sCommand)

# Merge metal patches horizontally
for j in range(num - 1):
    name1 = "a_" + str(1) + "_" + str(1)
    name2 = "a_" + str(1) + "_" + str(j + 1 + 1)
    sCommand = [f'Solid.Add "Metal:{name1}", "Metal:{name2}"'
                ]
    sCommand = line_break.join(sCommand)
    modeler.add_to_history('boolean add shapes: %s:%s, %s:%s' %
                           (Str_Component, name1, Str_Component, name2,), sCommand)

# Mirror the metal structure
Str_Name = 'a_1_1'
Str_Component = 'Metal'
sCommand = ['With Transform',
                    '.Reset',
                    f'.Name "{Str_Component}:{Str_Name}"',
                    '.Origin "Free"',
                    '.Center "0", "0", "0"',
                    '.PlaneNormal "0", "0", "-1"',
                    '.MultipleObjects "True"',
                    '.GroupObjects "False"',
                    '.Repetitions "1"',
                    '.MultipleSelection "False"',
                    '.Transform "Shape", "Mirror"',
                    'End With']
sCommand = line_break.join(sCommand)
modeler.add_to_history('transform: mirror %s:%s' % (Str_Component, Str_Name,), sCommand)

# Mirror the substrate
Str_Name = 'sub'
Str_Component = 'Sub'
sCommand = ['With Transform',
                    '.Reset',
                    f'.Name "{Str_Component}:{Str_Name}"',
                    '.Origin "Free"',
                    '.Center "0", "0", "0"',
                    '.PlaneNormal "0", "0", "-1"',
                    '.MultipleObjects "True"',
                    '.GroupObjects "False"',
                    '.Repetitions "1"',
                    '.MultipleSelection "False"',
                    '.Transform "Shape", "Mirror"',
                    'End With']
sCommand = line_break.join(sCommand)
modeler.add_to_history('transform: mirror %s:%s' % (Str_Component, Str_Name,), sCommand)

# Rotate the mirrored metal structure
Str_Name = 'a_1_1_1'
Str_Component = 'Metal'
sCommand = ['With Transform',
                    '.Reset',
                    f'.Name "{Str_Component}:{Str_Name}"',
                    '.Origin "Free"',
                    '.Center "0", "0", "0"',
                    '.Angle "0", "0", "180"',
                    '.MultipleObjects "False"',
                    '.GroupObjects "False"',
                    '.Repetitions "1"',
                    '.MultipleSelection "False"',
                    '.Transform "Shape", "Rotate"',
                    'End With']
sCommand = line_break.join(sCommand)
modeler.add_to_history('transform: rotate %s:%s' % (Str_Component, Str_Name,), sCommand)

# Background material settings
sCommand = ['With Background',
            '.ResetBackground',
            '.XminSpace "0.0"',
            '.XmaxSpace "0.0"',
            '.YminSpace "0.0"',
            '.YmaxSpace "0.0"',
            '.ZminSpace "da"',
            '.ZmaxSpace "da"',
            '.ApplyInAllDirections "False"',
            '.Type "Normal"',
            'End With']
sCommand = line_break.join(sCommand)
modeler.add_to_history('define background', sCommand)

# Boundary conditions
sCommand = [
    f'Solver.FrequencyRange "{freq[0]}", "{freq[1]}"'
]
sCommand = line_break.join(sCommand)
modeler.add_to_history('define frequency range', sCommand)

sCommand = [
    'With FloquetPort',
    '.Reset',
    '.SetDialogTheta "0"',
    '.SetDialogPhi "0"',
    '.SetPolarizationIndependentOfScanAnglePhi "0.0", "False"',
    '.SetSortCode "+beta/pw"',
    '.SetCustomizedListFlag "False"',
    '.Port "Zmin"',
    '.SetNumberOfModesConsidered "2"',
    '.SetDistanceToReferencePlane "-da"',
    '.SetUseCircularPolarization "False"',
    '.Port "Zmax"',
    '.SetNumberOfModesConsidered "2"',
    '.SetDistanceToReferencePlane "-da"',
    '.SetUseCircularPolarization "False"',
    'End With'
]
sCommand = line_break.join(sCommand)
modeler.add_to_history('define Floquet port boundaries', sCommand)

sCommand = [
    'With Boundary',
    '.Xmin "unit cell"',
    '.Xmax "unit cell"',
    '.Ymin "unit cell"',
    '.Ymax "unit cell"',
    '.Zmin "open"',
    '.Zmax "open"',
    '.Xsymmetry "none"',
    '.Ysymmetry "none"',
    '.Zsymmetry "none"',
    '.ApplyInAllDirections "False"',
    '.XPeriodicShift "0.0"',
    '.YPeriodicShift "0.0"',
    '.ZPeriodicShift "0.0"',
    '.PeriodicUseConstantAngles "False"',
    '.SetPeriodicBoundaryAngles "0.0", "0.0"',
    '.SetPeriodicBoundaryAnglesDirection "outward"',
    '.UnitCellFitToBoundingBox "True"',
    '.UnitCellDs1 "0.0"',
    '.UnitCellDs2 "0.0"',
    '.UnitCellAngle "90.0"',
    'End With'
]

sCommand = line_break.join(sCommand)
modeler.add_to_history('define boundaries', sCommand)

mws.save(tmpPrjFile)  # Save