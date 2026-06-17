
# ============================================
# CST Studio Suite 2022 Double-Layer Metamaterial Unit Cell Modeling Script
# Author: CST EM Simulation Automation Specialist
# Date: 2024
# Function: Create a double-layer metal metamaterial unit cell for phase-encoding metasurface design
# ============================================

# Import CST interface
import sys
import os

# Try different path formats
cst_paths = [
    r"D:\Program Files (x86)\CST Studio Suite 2022\AMD64\python_cst_libraries",
    r"D:/Program Files (x86)/CST Studio Suite 2022/AMD64/python_cst_libraries",
    r"D:\Program Files (x86)\CST Studio Suite 2022\AMD64\python_cst_libraries"
]

for path in cst_paths:
    if os.path.exists(path):
        sys.path.insert(0, path)  # Use insert(0) to ensure highest priority
        break

# Attempt import
try:
    import cst
    print(f"Successfully imported CST library: {cst.__file__}")

    # View cst module contents
    print("\nCST module contents:")
    print(dir(cst))

    import cst.interface
    print("Successfully imported cst.interface")
except Exception as e:
    print(f"Import error: {e}")

    # Try direct import
    try:
        from cst import interface
        print("Successfully imported using 'from cst import interface'")
    except Exception as e2:
        print(f"Alternative import also failed: {e2}")
        sys.exit(1)

def setup_units(modeler):
    """Set global unit system"""
    print("Setting up unit system...")
    sCommand = ['With Units',
                '.Geometry "mm"',
                '.Frequency "GHz"',
                '.Time "ns"',
                'End With']
    sCommand = '\n'.join(sCommand)
    modeler.add_to_history('define units', sCommand)

def define_materials(modeler):
    """Define material properties"""
    print("Defining materials...")

    # Define F4B dielectric substrate material
    sCommand = [
        'With Material',
        '.Reset',
        '.Name "F4B"',
        '.Folder ""',
        '.FrqType "all"',
        '.Type "Normal"',
        '.SetMaterialUnit "GHz", "mm"',
        '.Epsilon "2.2"',
        '.Mue "1.0"',
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
        '.DispModelMue "None"',
        '.DispersiveFittingSchemeEps "General 1st"',
        '.DispersiveFittingSchemeMue "General 1st"',
        '.UseGeneralDispersionEps "False"',
        '.UseGeneralDispersionMue "False"',
        '.Rho "0.0"',
        '.ThermalType "Normal"',
        '.ThermalConductivity "0.20"',
        '.SetActiveMaterial "all"',
        '.Colour "0.6", "0.6", "0.6"',
        '.Wireframe "False"',
        '.Transparency "0"',
        '.Create',
        'End With'
    ]
    sCommand = '\n'.join(sCommand)
    modeler.add_to_history('define material: F4B', sCommand)

    # Use CST built-in Copper (annealed) material, as required
    print("Using CST built-in Copper (annealed) material...")
    sCommand = [
        'With Material',
        '.Reset',
        '.Name "Copper (annealed)"',
        '.Folder "Lossy metal"',
        '.FrqType "all"',
        '.Type "Lossy metal"',
        '.SetMaterialUnit "GHz", "mm"',
        '.Epsilon "1"',
        '.Mue "1.0"',
        '.Kappa "5.8e7"',
        '.TanD "0.0"',
        '.TanDFreq "0.0"',
        '.TanDGiven "False"',
        '.TanDModel "ConstTanD"',
        '.KappaM "0.0"',
        '.TanDM "0.0"',
        '.TanDMFreq "0.0"',
        '.TanDMGiven "False"',
        '.TanDMModel "ConstKappa"',
        '.DispModelEps "None"',
        '.DispModelMue "None"',
        '.DispersiveFittingSchemeEps "General 1st"',
        '.DispersiveFittingSchemeMue "General 1st"',
        '.UseGeneralDispersionEps "False"',
        '.UseGeneralDispersionMue "False"',
        '.Rho "8930.0"',
        '.ThermalType "Normal"',
        '.ThermalConductivity "401.0"',
        '.HeatCapacity "0.39"',
        '.MetabolicRate "0"',
        '.BloodFlow "0"',
        '.VoxelConvection "0"',
        '.MechanicsType "Isotropic"',
        '.YoungsModulus "120"',
        '.PoissonsRatio "0.33"',
        '.ThermalExpansionRate "17"',
        '.Colour "1", "0.65", "0"',
        '.Wireframe "False"',
        '.Transparency "0"',
        '.Create',
        'End With'
    ]
    sCommand = '\n'.join(sCommand)
    modeler.add_to_history('define material: Copper', sCommand)

def create_substrate(modeler, p, h_sub):
    """Create dielectric substrate"""
    print("Creating dielectric substrate...")

    # Substrate center at z=0, thickness h_sub
    z_min = -h_sub / 2
    z_max = h_sub / 2

    sCommand = [
        'With Brick',
        '.Reset',
        '.Name "substrate"',
        '.Component "substrate"',
        '.Material "F4B"',
        '.Xrange "-p/2", "p/2"',
        '.Yrange "-p/2", "p/2"',
        f'.Zrange "{z_min}", "{z_max}"',
        '.Create',
        'End With'
    ]
    sCommand = '\n'.join(sCommand)
    modeler.add_to_history('define brick:substrate', sCommand)

    print(f"Dielectric substrate created: dimensions {p}x{p}x{h_sub} mm")

def create_bottom_metal(modeler, w_bot, t_metal, h_sub):
    """Create bottom metal patch"""
    print("Creating bottom metal patch...")

    # Bottom metal on the lower surface of substrate, z = -h_sub/2
    z_min = -h_sub/2 - t_metal
    z_max = -h_sub/2

    sCommand = [
        'With Brick',
        '.Reset',
        '.Name "bottom_patch"',
        '.Component "metal"',
        '.Material "Copper (annealed)"',
        f'.Xrange "-{w_bot}/2", "{w_bot}/2"',
        f'.Yrange "-{w_bot}/2", "{w_bot}/2"',
        f'.Zrange "{z_min}", "{z_max}"',
        '.Create',
        'End With'
    ]
    sCommand = '\n'.join(sCommand)
    modeler.add_to_history('define brick:bottom_patch', sCommand)

    print(f"Bottom metal patch created: dimensions {w_bot}x{w_bot}x{t_metal} mm")

def create_top_metal(modeler, w_top, t_metal, h_sub):
    """Create top metal patch"""
    print("Creating top metal patch...")

    # Top metal on the upper surface of substrate, z = h_sub/2
    z_min = h_sub/2
    z_max = h_sub/2 + t_metal

    sCommand = [
        'With Brick',
        '.Reset',
        '.Name "top_patch"',
        '.Component "metal"',
        '.Material "Copper (annealed)"',
        f'.Xrange "-{w_top}/2", "{w_top}/2"',
        f'.Yrange "-{w_top}/2", "{w_top}/2"',
        f'.Zrange "{z_min}", "{z_max}"',
        '.Create',
        'End With'
    ]
    sCommand = '\n'.join(sCommand)
    modeler.add_to_history('define brick:top_patch', sCommand)

    print(f"Top metal patch created: dimensions {w_top}x{w_top}x{t_metal} mm")

def set_background(modeler, air_thickness):
    """Set background material"""
    print(f"Setting background material, air layer thickness: {air_thickness} mm...")

    sCommand = [
        'With Background',
        '.ResetBackground',
        '.Type "Normal"',
        '.XminSpace "0.0"',
        '.XmaxSpace "0.0"',
        '.YminSpace "0.0"',
        '.YmaxSpace "0.0"',
        f'.ZminSpace "{air_thickness}"',
        f'.ZmaxSpace "{air_thickness}"',
        '.ApplyInAllDirections "False"',
        'End With'
    ]
    sCommand = '\n'.join(sCommand)
    modeler.add_to_history('define background', sCommand)

def set_boundary_conditions(modeler):
    """Set boundary conditions"""
    print("Setting boundary conditions...")

    # X and Y directions set to periodic boundary conditions, Z direction open
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
        '.SetPeriodicBoundaryAngles "0", "0"',
        '.SetPeriodicBoundaryAnglesDirection "outward"',
        '.UnitCellFitToBoundingBox "True"',
        '.UnitCellDs1 "0.0"',
        '.UnitCellDs2 "0.0"',
        '.UnitCellAngle "90.0"',
        'End With'
    ]
    sCommand = '\n'.join(sCommand)
    modeler.add_to_history('define boundaries', sCommand)

def set_floquet_ports(modeler, air_thickness):
    """Set Floquet ports"""
    print("Setting Floquet ports...")

    # Set Floquet ports in Zmin and Zmax directions
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
        f'.SetDistanceToReferencePlane "-{air_thickness}"',
        '.SetUseCircularPolarization "False"',
        '.Port "Zmax"',
        '.SetNumberOfModesConsidered "2"',
        f'.SetDistanceToReferencePlane "-{air_thickness}"',
        '.SetUseCircularPolarization "False"',
        'End With'
    ]
    sCommand = '\n'.join(sCommand)
    modeler.add_to_history('define Floquet port boundaries', sCommand)

def set_solver_parameters(modeler, freq_min, freq_max):
    """Set solver parameters"""
    print("Setting solver parameters...")

    # Set frequency domain solver
    sCommand = 'ChangeSolverType "HF Frequency Domain"'
    modeler.add_to_history('change solver type', sCommand)

    # Set frequency range
    sCommand = f'Solver.FrequencyRange "{freq_min}", "{freq_max}"'
    modeler.add_to_history('define frequency range', sCommand)

    # Set solver parameters
    sCommand = [
        'With FDSolver',
        '.Reset',
        '.SetMeshType "Hex"',
        '.AutoNormImpedance "False"',
        '.NormingImpedance "50"',
        '.UseDistributedComputing "False"',
        '.UseParallelization "True"',
        '.SetShield "PEC"',
        '.SetShieldType "None"',
        '.SetCreateSMatrix "True"',
        '.SetCreateSMatrixOnly "False"',
        '.SetSMatrixSamplingRange "False"',
        '.SetSMatrixSymmetry "False"',
        '.SetUseFastRCSSweep "False"',
        '.SweepWeightEvanescent "1.0"',
        '.SetAccuracyEnhanced "False"',
        '.SetAccuracyGH "0.0001"',
        '.SweepConsiderAll "True"',
        '.SweepError "1e-3"',
        '.SweepMinimumSamples "3"',
        '.SweepConsiderAll "False"',
        '.SweepConsiderProp "False"',
        '.SweepConsiderEvan "True"',
        '.SweepMinFreqScale "1.0"',
        '.SweepWeightEvanescent "1.0"',
        '.UseDoublePrecision "True"',
        '.MixedOrderSweep "False"',
        '.SetUseDoublePrecision "True"',
        '.SetUseMixedOrder "False"',
        '.SetPreconditionerAccuracy "0.15"',
        '.UseIEGroundPlane "False"',
        '.SetUseIEGroundPlane "False"',
        '.UseRobustSMatrixSweepMode "True"',
        '.SetRobustSMatrixSweepMode "True"',
        '.SetRobustSMatrixSweepModeGerm "0"',
        '.SetRobustSMatrixSweepModeMaxPass "20"',
        '.SetRobustSMatrixSweepModeMaxIter "10"',
        '.SetRobustSMatrixSweepModeConvergence "1e-3"',
        '.SetRobustSMatrixSweepModeThreshold "1e-6"',
        'End With'
    ]
    sCommand = '\n'.join(sCommand)
    modeler.add_to_history('define FDSolver settings', sCommand)

def set_mesh_settings(modeler, t_metal):
    """Set mesh parameters, with special handling for thin metal layers"""
    print("Setting mesh parameters...")

    # Set global mesh properties
    sCommand = [
        'With Mesh',
        '.MeshType "PBA"',
        '.SetCreator "High Frequency"',
        '.Automesh "True"',
        '.AutomeshRefineAt "Pec"',
        '.AutomeshRefineAt "Material"',
        '.AutomeshRefineAt "Dielectric"',
        '.AutomeshAccuracy "2"',
        '.MinStep "0"',
        '.RatioLimit "20"',
        '.UseAnisotropicCurveRefinement "True"',
        '.UseDivergedCurveRefinement "False"',
        '.SnapToAxialLines "True"',
        '.SnapToMagneticCenterLines "False"',
        '.SnapToElectricCenterLines "False"',
        '.SnapToEndPoints "True"',
        '.SnapToCentralPoints "True"',
        '.SnapToIntersectionPoints "True"',
        '.CurveRefinementControlPoints "3"',
        '.CurveRefinementUseSameAs "2"',
        '.CurveRefinementCount "10"',
        '.SurfaceRefinement "True"',
        '.SurfaceRefinementAspectRatio "10"',
        '.SurfaceRefinementGrading "1.3"',
        '.SurfaceRefinementMaxDev "0.025"',
        '.VolumeRefinement "True"',
        '.VolumeRefinementAspectRatio "10"',
        '.VolumeRefinementGrading "1.3"',
        '.VolumeRefinementMaxDev "0.025"',
        '.SrfAndVolRefinementSame "True"',
        '.SmallFeatureSize "0"',
        '.SmallFeatureRatio "0.01"',
        '.UsePecEdgeModel "True"',
        '.PecEdgeModelAbsoluteWidth "0"',
        '.PecEdgeModelRelativeWidth "0.0001"',
        '.PecEdgeModelMinAbsoluteWidth "0"',
        '.PecEdgeModelMinRelativeWidth "1e-06"',
        '.UseThinSheetVolumeMesh "True"',
        '.ThinSheetVolumeMeshAbsoluteThickness "0.01"',
        '.ThinSheetVolumeMeshRelativeThickness "0.01"',
        '.ThinSheetVolumeMeshSnap "True"',
        '.ThinSheetVolumeMeshPriority "0"',
        '.UseThinSheetModel "True"',
        '.ThinSheetModelAbsoluteThickness "0.01"',
        '.ThinSheetModelRelativeThickness "0.01"',
        '.ThinSheetModelSnap "True"',
        '.ThinSheetModelPriority "0"',
        'End With'
    ]
    sCommand = '\n'.join(sCommand)
    modeler.add_to_history('define mesh settings', sCommand)

    # Set thin layer mesh refinement (for 0.018 mm metal layer)
    print(f"Setting thin metal layer mesh refinement (thickness: {t_metal} mm)...")

    # Add local mesh settings for metal layers
    sCommand = [
        'With MeshAdaption3D',
        '.Reset',
        '.SetType "General"',
        '.Add "metal:bottom_patch"',
        '.Add "metal:top_patch"',
        '.SetMeshType "Hex"',
        '.SetMethod "Standard"',
        '.SetMaxPasses "10"',
        '.SetMaxRefineSteps "5"',
        '.SetUseControl "True"',
        '.SetControl "S-Parameter"',
        '.SetErrorLimit "0.02"',
        '.SetStep "0.1"',
        '.SetRatioLimit "20"',
        '.SetMinPasses "2"',
        '.SetRefinementType "h-adaptation"',
        '.SetRefinementStrategy "Gradient"',
        '.SetUseAnisotropicRefinement "True"',
        '.SetAnisotropicRatio "10"',
        '.SetAnisotropicRatioLimit "100"',
        '.SetUseMaxElementLength "False"',
        '.SetMaxElementLength "1"',
        '.SetUseTargetElementLength "False"',
        '.SetTargetElementLength "1"',
        '.SetUseVolumeSensitiveRefinement "False"',
        '.SetUseTwoLevelRefinement "False"',
        '.SetTwoLevelRefinementRatio "0.3"',
        '.SetTwoLevelRefinementStrategy "Convergence"',
        '.SetUseMultiplePassesAdaption "False"',
        '.SetUseSensitivityAnalysis "False"',
        '.SetStopAtOptimalPass "False"',
        'End With'
    ]
    sCommand = '\n'.join(sCommand)
    modeler.add_to_history('define mesh adaption', sCommand)

def zoom_to_structure(modeler):
    """Zoom view to structure"""
    print("Zooming view to structure...")
    sCommand = 'Plot.ZoomToStructure'
    modeler.add_to_history('ZoomToStructure', sCommand)

def main():
    """Main function: Create double-layer metamaterial unit cell model"""

    # ================================
    # Define structural parameters (per verification report)
    # ================================
    print("Defining structural parameters...")

    # Unit cell period (mm)
    period_x = 12.0
    period_y = 12.0
    period = 12.0  # Use unified period variable

    # Dielectric substrate parameters
    h_sub = 2.0  # Dielectric substrate thickness (mm)
    epsilon_r = 2.2  # Relative permittivity
    tan_delta = 0.0009  # Loss tangent

    # Metal layer parameters
    t_metal = 0.018  # Metal layer thickness (mm) - corrected to finite thickness
    conductivity = 5.8e7  # Conductivity (S/m)

    # Patch dimensions (mm)
    w_bot = 11.7  # Bottom patch width (fixed)
    w_top = 9.6   # Top patch width (default value, can be parametrically scanned)

    # Operating frequency range (GHz)
    freq_min = 8.0
    freq_max = 12.0
    freq_center = 10.0  # Center frequency

    # Background / air layer thickness (mm) - set to 10 mm per recommendations
    air_thickness = 10.0

    # Project save path
    project_path = "F:\\CSTProjects\\DoubleLayerMetasurface_UnitCell.cst"

    # Create output directory
    output_folder = os.path.dirname(project_path)
    if not os.path.exists(output_folder):
        try:
            os.makedirs(output_folder)
            print(f"Created output directory: {output_folder}")
        except Exception as e:
            print(f"Failed to create directory: {e}")
            project_path = os.path.join(os.getcwd(), "DoubleLayerMetasurface_UnitCell.cst")
            print(f"Using current directory: {project_path}")

    # Initialize CST design environment
    print("Initializing CST design environment...")
    try:
        cst_env = cst.interface.DesignEnvironment()
        mws = cst_env.new_mws()
        modeler = mws.modeler
        print("CST design environment initialized successfully")
    except Exception as e:
        print(f"CST design environment initialization failed: {e}")
        return

    # Save project file
    print(f"Saving project to: {project_path}")
    try:
        mws.save(project_path)
        print("Project saved successfully")
    except Exception as e:
        print(f"Project save failed: {e}")
        print("Continuing modeling process...")

    # Store parameters to CST project
    print("Storing structural parameters...")
    try:
        modeler.add_to_history('StoreParameter', 'StoreParameter "period", "%.3f"' % period)
        modeler.add_to_history('StoreParameter', 'StoreParameter "period_x", "%.3f"' % period_x)
        modeler.add_to_history('StoreParameter', 'StoreParameter "period_y", "%.3f"' % period_y)
        modeler.add_to_history('StoreParameter', 'StoreParameter "h_sub", "%.3f"' % h_sub)
        modeler.add_to_history('StoreParameter', 'StoreParameter "t_metal", "%.6f"' % t_metal)
        modeler.add_to_history('StoreParameter', 'StoreParameter "w_bot", "%.3f"' % w_bot)
        modeler.add_to_history('StoreParameter', 'StoreParameter "w_top", "%.3f"' % w_top)
        modeler.add_to_history('StoreParameter', 'StoreParameter "epsilon_r", "%.1f"' % epsilon_r)
        modeler.add_to_history('StoreParameter', 'StoreParameter "tan_delta", "%.6f"' % tan_delta)
        modeler.add_to_history('StoreParameter', 'StoreParameter "freq_min", "%.1f"' % freq_min)
        modeler.add_to_history('StoreParameter', 'StoreParameter "freq_max", "%.1f"' % freq_max)
        modeler.add_to_history('StoreParameter', 'StoreParameter "freq_center", "%.1f"' % freq_center)
        modeler.add_to_history('StoreParameter', 'StoreParameter "air_thickness", "%.1f"' % air_thickness)
        print("Parameters stored successfully")
    except Exception as e:
        print(f"Parameter storage failed: {e}")

    # Set unit system
    setup_units(modeler)

    # Define materials
    define_materials(modeler)

    # Create dielectric substrate
    create_substrate(modeler, period, h_sub)

    # Create bottom metal patch
    create_bottom_metal(modeler, w_bot, t_metal, h_sub)

    # Create top metal patch
    create_top_metal(modeler, w_top, t_metal, h_sub)

    # Set background material
    set_background(modeler, air_thickness)

    # Set boundary conditions
    set_boundary_conditions(modeler)

    # Set Floquet ports
    set_floquet_ports(modeler, air_thickness)

    # Set solver parameters
    set_solver_parameters(modeler, freq_min, freq_max)

    # Set mesh parameters
    set_mesh_settings(modeler, t_metal)

    # Zoom view to structure
    zoom_to_structure(modeler)

    # Save project again
    print("Saving complete project...")
    try:
        mws.save(project_path)
        print("Project saved successfully")
    except Exception as e:
        print(f"Project save failed: {e}")

    # Print modeling completion summary
    print("\n" + "="*60)
    print("Double-Layer Metamaterial Unit Cell Modeling Summary")
    print("="*60)
    print(f"1. Unit cell period: {period_x} x {period_y} mm")
    print(f"2. Dielectric substrate: {period} x {period} x {h_sub} mm, Material: F4B (epsilon_r={epsilon_r}, tand={tan_delta})")
    print(f"3. Metal layer thickness: {t_metal} mm, Material: Copper (annealed) (sigma={conductivity:.1e} S/m)")
    print(f"4. Bottom patch: {w_bot} x {w_bot} mm (fixed dimensions)")
    print(f"5. Top patch: {w_top} x {w_top} mm (default value, can be parameterized)")
    print(f"6. Operating frequency: {freq_min}-{freq_max} GHz")
    print(f"7. Air layer thickness: {air_thickness} mm (each side)")
    print(f"8. Boundary conditions: X/Y directions - periodic unit cell, Z direction - open")
    print(f"9. Excitation: z-direction normal incidence y-polarized plane wave")
    print(f"10. Port setup: Zmin/Zmax directions - Floquet ports")
    print(f"11. Solver: Frequency domain solver")
    print(f"12. Project file: {project_path}")
    print("="*60)

    print("\nNext steps:")
    print("1. Check the model structure in CST")
    print("2. Run initial simulation to verify settings")
    print("3. Set w_top as a variable for parametric sweep")
    print("4. Study phase response at different w_top values")

    print("\nModeling complete! You can further adjust parameters or run simulation in CST Studio Suite.")

    # Keep CST process alive
    print("\nCST process is still running, please close CST software manually...")
    try:
        input("Press Enter to exit the script (CST software will remain open)...")
    except:
        print("Script execution complete, CST process continues running.")

    # Clean up resources (optional, if user wants to close)
    # mws.close()
    # cst_env.close()

# Error handling
if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nUser interrupted script execution.")
    except Exception as e:
        print(f"Error occurred during script execution: {e}")
        import traceback
        traceback.print_exc()
    finally:
        print("Script execution finished.")
