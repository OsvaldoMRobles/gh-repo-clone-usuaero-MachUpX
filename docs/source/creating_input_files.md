# Input Files
The basic input for MachUp contains a JSON object which describes the scene and which aircraft are in the scene, along with the state of those aircraft in the scene. A separate JSON object is used to specify the geometry and controls of each aircraft. These aircraft objects can reference other files that store information on airfoil properties, chord distributions, sweep, etc., as will be discussed. At a minimum, two JSON objects will be created by the user, a scene object and an aircraft object. These objects can be passed to MachUpX either as a .json file (this is the only way if MachUpX is being used through the command line) or as a Python dictionary, which is directly analagous to a .json file.

## JSON Format
The basic structure of a JSON object is a set of key-value pairs, analogous to a Python dictionary. Examples can be found in the examples/ directory. The following sections describe the structure of the JSON objects used to interface with MachUp. Only one JSON object is specified per .json file. When using the JSON objects, only the scene object is passed to MachUp. As long as the paths to all other JSON objects are properly specified in the scene object, MachUp will automatically load all other required objects.

## Coordinate Systems
MachUpX can accept inputs and output certain information in the wind and stability frames, along with the body frame. An aircraft's angular rate vector can be specified in the body, stability, or wind frame. In conjunction with this, MachUpX will calculate damping derivatives with respect to the frame the angular rates were originally specified in. Also, MachUpX can output forces an moments in any of these three frames.

## Scene Object
The following are keys which can be specified in the scene JSON object. NOTE: all keys not marked as optional are required. Key names typed in all capitals between carats (e.g. <KEY_VALUE>) are to be deterimined by the user.

Units of measurement may be specified for certain inputs. For information on how this is done, see [Units](units).

>**"tag" : string, optional**
>>A note on the specific input. Does not affect execution.
>>
>**"run" : dict, optional**
>>Gives the analyses MachUp is to run. This must be specified if the input file is being passed as a command line argument to MachUp. Otherwise, MachUp will return without performing any calculations. **If the input file is used to initialize the Scene class within a script, rather than being passed as a command line argument, this set of run commands will be ignored.**
>>
>>The outputs from the analyses will be stored in files automatically. If no filename is given by the user, MachUpX will automatically specify a filename based on the name of the input file and the run command. This means that all output files will be stored in the same directory as the input file, with the exception of .stp and .dxf files.
>>
>>The availalbe run commands are the names of Scene functions, listed on the [Scene class page](scene_object), with the function arguments specified in the value dictionary. For example, the following set of commands would trim the aircraft in pitch, solve the current forces, and calculate derivatives:
>>
>>```json
>>{
>>    ...
>>    "run" : {
>>        "pitch_trim" : {
>>            "set_trim_state" : true,
>>            "verbose" : true
>>        },
>>        "solve_forces" : {
>>            "filename" : "my_forces.json",
>>            "dimensional" : false,
>>            "nondimensional" : false,
>>            "verbose" : true
>>        },
>>        "derivatives" : {
>>            "filename" : "my_derivatives.json"
>>        }
>>    },
>>    ...
>>}
>>```
>
>**"solver" : dict, optional**
>>Specifies parameters regarding how the lifting-line equation is solved.
>>
>>**"type" : string, optional**
>>>Can be "linear", "nonlinear", or "scipy_fsolve". The lifing-line equations are solved first by solving a linear approximation and then improving the result using the full nonlinear equations and Newton's method. The linear approximation is reasonably accurate for high aspect ratio lifting surfaces at low angles of attack. Alternately, if "scipy_fsolve" is selected, the scipy.optimize.fsolve function is used to calculate the solution. **We recommend the "nonlinear" solver.** The "linear" solver should be used if speed is preferred over accuracy and tests have shown the accuracy is not significantly affected. Using "scipy_fsolve" is almost equivalent to using "nonlinear", except the "nonlinear" solver will more reliably converge and find the solution more quickly in most cases. We thus discourage using "scipy_fsolve". Defaults to "nonlinear".
>>
>>**"convergence" : float, optional**
>>>Threshold for convergence of the nonlinear solution. The nonlinear solver is considered complete once the norm of the residuals falls below this threshold. Defaults to 1e-10. Has no effect on the linear solver. Can also be used to specify the 'xtol' argument for scipy.optimize.fsolve, if that is the selected solver. Note, this is not the same behavior between the nolinear solver and the scipy solver.
>>
>>**"relaxation" : float, optional**
>>>Relaxation factor for applying the calculated correction at each iteration of the nonlinear solver. A value of 1.0 applies the full correction. Defaults to 1.0. Has no effect on the linear solver or the scipy solver.
>>
>>**"max_iterations" : int, optional**
>>>Maximum number of iterations for the nonlinear solver. Rare cases may be poorly behaved and prevent the nonlinear solver from fully converging to the desired tolerance. Defaults to 100. Has no effect on the linear solver or the scipy solver.
>>
>>**"use_swept_sections" : int, optional**
>>>Whether to include corrections to section properties and local velocities for sweep. It is highly recommended that this not be turned off, even for straight wings. Defaults to True.
>>
>>**"use_total_velocity" : int, optional**
>>>Whether to include induced velocities when redimensionalizing section coefficients. It is highly recommended that this not be turned off. Defaults to True.
>>
>>**"use_in_plane" : int, optional**
>>>Whether to use only the in-plane velocity for determining airfoil section behavior. If True, the velocity in the plane normal to the lifting-line will be used to redimensionalize the section lift coefficient. If False, the true velocity is used for redimensionalization. Due to the definition of angle of attack from the section direction vectors, this does not affect swept section/original section angle of attack calculations. It is highly recommended that this not be turned off. Defaults to True.
>>
>>**"match_machup_pro" : int, optional**
>>>Changes how miscelaneous other aspects of NLL are handled to match the nondimensional derivation used in MachUp Pro. Defaults to False. **If you desire to match MachUp Pro exactly, "use_swept_sections", "use_total_velocity", "use_in_plane", "reid_corrections", and "flap_edge_cluster" must be set to False along with setting this to True (not recommended).** Even with this, MachUpX is unable to match MachUp Pro in the case of angular rates.
>>
>>**"impingement_threshold" : float, optional**
>>>Threshold for detecting whether trailing vortex filaments are impinging on aft lifting surfaces. Defaults to 1e-10.
>>
>>**"constrain_vortex_sheet" : bool, optional**
>>>Constrains the trailing vortices to be parallel to the aircraft's x-y plane (body-fixed). Defaults to False.
>
>**"units" : string, optional**
>>Specifies the unit system to be used for inputs and outputs. Can be "SI" or "English". Any units not explicitly defined for each value in the input objects will be assumed to be the default unit for that measurement in the system specified here. All outputs will be given in this unit system. Defaults to "English".
>
>**"scene" : dict**
>
>>**"atmosphere" : dict, optional**
>>>Specifies the atmosphere the aircraft exist in. If this dictionary is empty, the aircraft is assumed to be at sea-level in a standard Earth atmosphere. If you take the time to specify these keys, you can put your aircraft anywhere, even on Mars! Note that while viscosity and speed of sound are specified here, they will have no effect on computations unless the airfoil section properties are given as functions of Mach and Reynolds numbers. However, for many applications, it is appropriate to ignore Mach and Reynolds effects.
>>>
>>>**"rho" : float, array, or string, optional**
>>>>If a float, the atmospheric density is assumed constant. If an array is given, this is assumed to be either a density profile or a density field. MachUp will interpret a 2 column array as a profile where the first column is heights and the second column is densities. A 4 column array is a field where the first three columns are the position in earth-fixed coordinates and the fourth column is the density. MachUp will linearly interpolate these data. These arrays can alternatively be stored as a csv file, in which case, this value should be the path to the file. NOTE: Since MachUpX uses earth-fixed coordinates for position, altitude values should be negative (i.e. 1000 ft above sea level would be -1000 ft).
>>>>
>>>>If "rho" is a string, it is assumed the density is determined using an analytically defined atmosphere profile. The following profiles can be specified:
>>>>
>>>>>"standard" - Standard atmosphere profile.
>>>>
>>>>Defaults to density at sea-level.
>>>>
>>>**"V_wind" : vector, array, or string, optional**
>>>>If a vector is given, this is assumed to be the wind velocity vector given in earth-fixed coordinates which is constant throughout the scene. If an array is given, this is assumed to be either a wind profile or a wind field. MachUp will interpret a 4 column array as a velocity profile where the first column is heights and the last three columns are velocity components in earth-fixed coordinates. A 6 column array is a field where the first three columns are positions in earth-fixed coordinates and the fourth through sixth columns are velocity components in earth-fixed coordinates. These arrays can alternatively be stored as a csv file, in which case, this value should be the path to the file. Defaults to no wind.
>>>
>>>**"viscosity" : float or string**
>>>>*Kinematic* viscosity of the atmosphere. If a float, the viscosity is assumed to be constant. If a string, it is assumed the viscosity is determined using an analytically defined atmosphere profile. The following profiles can be specified:
>>>>
>>>>>"standard" - Standard atmosphere profile.
>>>>
>>>>Defaults to standard viscosity at sea-level.
>>>
>>**"aircraft" : dict**
>>>Lists the aircraft to be placed in the scene. At least one must be specified. Please note that MachUpX is able to model interactions between multiple aircraft within the limitations of lifting-line theory. It is assumed the user understands these limitations and will use MachUpX appropriately. If importing more than one aircraft, simply repeat the following structure:
>>>
>>>**"<AIRPLANE_NAME>" : dict**
>>>
>>>>**"file" : string**
>>>>>Path to file containing the JSON object describing the aircraft.
>>>>
>>>>**"state" : dict**
>>>>>Describes the state of the aircraft.
>>>>>
>>>>>**"position" : vector, optional**
>>>>>>Position of the origin of the aircraft's body-fixed coordinate system in earth-fixed coordinates. Defaults to [0.0, 0.0, 0.0]. It is recommended this only be used if multiple aircraft are being modeled and "position" is being used to specify separation between the aircraft. Otherwise, it is recommended the aircraft always be placed at the origin and the atmospheric properties changed accordingly.
>>>>>
>>>>>**"velocity" : float or vector**
>>>>>>Velocity vector of the aircraft in body-fixed coordinates (i.e. u, v, and w) or magnitude of the freestream velocity at the origin of the aircraft. In the case of a vector, "alpha" and "beta" may not be specified.
>>>>>
>>>>>**"alpha" : float, optional**
>>>>>>Aerodynamic angle of attack in degrees. Defaults to 0.
>>>>>
>>>>>**"beta" : float, optional**
>>>>>>Aerodynamic sideslip angle in degrees. Defaults to 0. NOTE: MachUpX defines this as the experimental sideslip angle, i.e. b = asin(Vy/V), rather than the analytic sideslip angle.
>>>>>
>>>>>**"orientation" : vector, optional**
>>>>>>Orientation of the aircraft, going from earth-fixed frame to body-fixed frame. If this is a 3-element vector it is assumed the ZYX Euler angle formulation in degrees is used (i.e. [bank angle, elevation angle, heading angle]). If this is a 4-element vector it is assumed the quaternion formulation is used where the first element is the scalar (i.e. [e0, ex, ey, ez]). Defaults to [1.0, 0.0, 0.0, 0.0], which will align the body-fixed frame with the earth-fixed frame.
>>>>>
>>>>>**"angular_rates" : vector, optional**
>>>>>>Angular rates of the aircraft about the center of gravity, corresponding to p, q, and r. These are dimensional angular rates (rad/s). Defaults to [0.0, 0.0, 0.0].
>>>>>
>>>>>**"angular_rate_frame" : str, optional**
>>>>>>Frame in which the angular rates are given. Can be "body", "stab" (stability coordinates), or "wind". Defaults to "body".
>>>>
>>>>**"control_state" : dict, optional**
>>>>>Describes the control deflections. The number and names of controls are arbitrary and may be specified by the user. This is discussed more in depth as part of the aircraft object. If the aircraft has controls but no state is specified, all deflections will be assumed to be zero.
>>>>
>>>>>**"<CONTROL_NAME>" : float or array, optional**
>>>>>>Control setting in degrees. If float, the setting is assumed constant across the control surface. If an array, then a distribution of deflections is assumed. This should be specified like "chord_fraction". Defaults to 0.0.

## Aircraft Object
Describes an aircraft. Stored as a .json file or a Python dictionary.

>**"CG" : vector, optional**
>>Location of the aircraft's center of gravity in body-fixed coordinates. Defaults to [0.0, 0.0, 0.0], as the origin of the body-fixed coordinate system is typically the aircraft's center of gravity.
>
>**"weight" : float**
>>Weight of the aircraft.
>
>**"reference" : dict, optional**
>>Specifies the reference lengths and areas used for nondimensional analysis. Any or none of these may be specified. If not specified, MachUp will select appropriate values based on the geometry of the main wing.
>
>>**"area" : float, optional**
>>>The reference area. Defaults to the main wing planform area.
>>
>>**"longitudinal_length" : float, optional**
>>>Longitudinal reference length. Defaults to the reference area divided by the lateral reference length.
>>
>>**"lateral_length" : float, optional**
>>>Lateral reference length. Defaults to the main wing span.
>
>**"controls" : dict, optional**
>>Defines the controls of the aircraft. The number and names of controls are arbitrary and may be specified by the user. A simple aircraft, such as a chuck glider may have no controls, whereas a more complex aircraft may have controls for aileron, elevator, rudder, and multiple flaps. Defining the controls here can be thought of as deciding which control knobs/switches/sticks you want to make available to the pilot.
>
>>**"<CONTROL_NAME>" : dict**
>>
>>>**"is_symmetric" : bool**
>>>>Specifies whether this control causes symmetric or asymmetric control surface deflections (e.g. for a typical aircraft, the elevator control causes symmetric deflections whereas the aileron causes asymmetric deflections).
>
>**"airfoils" : dict or str**
>>Defines the airfoils used on the aircraft. Any number of airfoils can be defined for the aircraft and MachUpX will pull from these airfoil definitions as needed, depending on which airfoils are specified for each wing segment. If no airfoils are listed here MachUp will automatically generate a default airfoil and use it on all lifting surfaces. The default values listed are for a flat plate as predicted by thin airfoil theory. Do not expect these to give you accurate results.
>>
>>This may also be the path to a JSON object containing the airfoils.
>>
>>MachUpX uses the AirfoilDatabase package ([link](https://www.github.com/usuaero/AirfoilDatabase)) to calculate section properties. This package allows for generating nonlinear coefficient databases for a given airfoil. It's full capabilities are explained in the [documentation](https://airfoildatabase.readthedocs.io/en/latest/). Please note that MachUpX does not have the capability to generate these databases. It can only read in a previously generated database.
>>
>>**IMPORTANT:** If you are using multiple nonlinear databases for multiple spanwise airfoils, then the nonlinear databases must be generated for the range of Reynolds number *seen by the whole wing*. E.g. if you have a tapered wing, then the root will see a higher Reynolds number than the tip; despite this fact, the root airfoil database must span the range of Reynolds numbers expected at the tip and vice versa. Please also note that the Reynolds number used to extract coefficients from the database is calculated using the total (freestream plus induced) velocity. Thus it is a good rule of thumb to generate a database which goes a little above and a little below the expected freestream Reynolds numbers.
>>
>>The input for a single airfoil has the following structure:
>
>>**"<AIRFOIL_NAME>" : dict or str**
>>>Input for a given airfoil. As a dictionary, it should have the following keys. If this is a string, it should be the path to a JSON object containing the same information. The name of the airfoil should not be repeated in the file; only the coefficients and geometry information should be listed.
>>
>>>**"type" : string**
>>>>The type of data used to calculate section properties for the airfoil. Can be "linear", "database", or "poly_fit". For a "database" or "poly_fit" airfoil, "input_file" must be specified. A "linear" airfoil assumes linear lift and moment curves and a quadratic drag polar. In this case, the following keys must be defined. UNITS MAY NOT BE SPECIFIED BY THE USER FOR ANY AIRFOIL PARAMETERS. THESE VALUES MUST BE SPECIFIED IN THE UNITS GIVEN HERE.
>>>
>>>**"aL0" : float, optional**
>>>>The zero-lift angle of attack in radians. Defaults to 0.0.
>>>
>>>**"CLa" : float, optional**
>>>>The lift slope in radians^-1. Defaults to 2pi
>>>
>>>**"CmL0" : float, optional**
>>>>Pitching moment at zero lift. Defaults to 0.0.
>>>
>>>**"Cma" : float, optional**
>>>>The moment slope in radians^-1. Defaults to 0.0.
>>>
>>>**"CD0" : float, optional**
>>>>Constant coefficient in the quadratic fit of the CD/CL curve. MachUpX assumes section drag is modelled by 
>>>>
>>>>CD = CD0 + CD1\*CL + CD2\*CL^2
>>>>
>>>>Defaults to 0.0.
>>>
>>>**"CD1" : float, optional**
>>>>Linear coefficient in the quadratic fit of the CD/CL curve. Defaults to 0.0.
>>>
>>>**"CD2" : float, optional**
>>>>Quadratic coefficient in the quadratic fir of the CD/CL curve. Defaults to 0.0.
>>>
>>>**"CL_max" : float, optional**
>>>>Maximum lift coefficient. Defaults to infinity.
>>>
>>>**"input_file" : str, optional**
>>>>File containing the coefficient database or polynomial fit information for the airfoil. Required if "type" is "database" or "poly_fit".
>>>
>>>**"geometry" : dict, optional**
>>>>Describes the geometry of the airfoil.
>>>>
>>>>**"outline_points" : str or array, optional**
>>>>>Path to a file containing airfoil outline points or array of outline points. The first column contains x-coordinates and the second column contains y-coordinates, where x originates at the leading edge and points back along the chord line and y points up. If a file, it should be comma-delimited. The trailing edge should be sealed and points should be listed starting at the trailing edge. The geometry specified here will only be used in generating 3D models and will not affect the aerodynamics. Cannot be specified along with "NACA".
>>>>
>>>>**"NACA" : str, optional**
>>>>>NACA designation for the airfoil. If given, MachUpX will automatically generate outline points using the NACA equations. Can only be NACA 4-digit series. Cannot be specified along with "outline_points". Will not affect aerodynamics.
>>>>
>>>**"camber_solver_kwargs" : dict, optional**
>>>>A dictionary of kwargs to pass to the Airfoil class initializer for this airfoil. These affect how the camber line solver runs for an airfoil where "ouline_points" is given. Has no effect is this is not given. The kwargs that can be specified are "verbose", "camber_relaxation", "le_loc", "max_iterations", and "camber_termination_tol". More information on each of these can be found [here](https://airfoildatabase.readthedocs.io/en/latest/airfoil_class.html).
>
>**"wings" : dict**
>>Gives the lifting surfaces for the aircraft. Wings, stabilizers, fins, etc. are all treated the same in numerical lifting-line and so should be included here as wing segments. MachUp is set up so the user can define complex geometries by attaching the ends of different wing segments together (for an example, see the examples/ directory). The user can define any number of wing segments within this dict. Note that each wing segment can only have one control surface, therefore, a wing with multiple control surfaces must be created from multiple wing segments.
>
>>**"<WING_SEGMENT_NAME>" : dict**
>>
>>>**"ID" : uint**
>>>>ID tag of the wing segment, used for specifying which other wing segments are defined relative to it. MAY NOT BE 0.
>>>
>>>**"is_main" : bool**
>>>>Specifies whether this wing segment is part of the main wing (used for determining reference lengths and areas).
>>>
>>>**"side" : string**
>>>>May be "right", "left", or "both". Defines which side(s) of the aircraft the wing segment appears on. If "both", the wing segment will be mirrored across the x-z plane.
>>>
>>>**"connect_to" : dict**
>>>>Places the origin for the wing segment. This can be defined relative to the aircraft's body-fixed origin, or the root or tip of any other wing segment.
>>>>
>>>>**"ID" : uint, optional**
>>>>>ID of the wing segment this wing segment's origin is being defined relative to. If 0, this wing segment's origin will be defined relative to the aircraft's body-fixed origin. Defaults to 0.
>>>>
>>>>**"location" : string, optional**
>>>>>May be "root" or "tip". Defines whether this wing segment's origin should be defined relative to the root or tip of the other wing segment. Defaults to "tip"
>>>>
>>>>**"dx" : float, optional**
>>>>>Displacement of the origin from the selected reference point in the body-fixed x- direction. Defaults to 0.
>>>>
>>>>**"dy" : float, optional**
>>>>>Displacement of the origin from the selected reference point in the body-fixed y- direction. NOTE: If "side" is specified as "both", changing this value will shift both sides of the wing segment in the SAME direction. The effect is not mirrored. Defaults to 0.
>>>>
>>>>**"dz" : float, optional**
>>>>>Displacement of the origin from the selected reference point in the body-fixed z- direction. Defaults to 0.
>>>>
>>>>**"y_offset" : float, optional**
>>>>>Distance the origin should be shifted from the centerline (positive offset corresponds to outward from the x-z plane). If "side" is specified as "both", this effect is mirrored. Defaults to 0.
>>>
>>>**"semispan" : float**
>>>>Length of the wing segment in the y-direction (i.e. discounting sweep). If "side" is specified as "both", the total span of the segment is twice this value. May not be specified if "quarter_chord_locs" is specified.
>>>
>>>**"twist" : float, array, string, or func, optional**
>>>>Gives the **geometric** twist of the wing, meaning the angle of the chord line of each airfoil section relative to the body x-axis in degrees. If specified as a float, then all sections will make that angle with the horizontal and it will be as if the wing is untwisted but mounted at that angle. If specified as an array, the array gives the local twist as a function of span. The first column gives the span location as a fraction of the total span. This column must have values going from 0.0 to 1.0. The second column gives the twist at that span location. If specified as a string, this string must contain the path to a csv file containing the twist data formatted in columns, as with the array. For properties as a function of span, MachUp will linearly interpolate intermediate values. If a step change in distribution is needed, this can be done by specifying the span location where the step change occurs twice, once with each value, as below:
>>>>
>>>>>**"twist" : [[0.0, 0.0], [0.5, 0.0], [0.5, 2.0], [1.0, 2.0]]**
>>>>
>>>>In the above example, the twist will be 0 degrees for the inner half of the wing and 2 degrees for the outer half of the wing. Note that this parameter also determines the mounting angle and washout of the wing segment. Defaults to 0.
>>>>
>>>>Alternatively, if MachUpX is being used as a module imported into a script, this value can be a function which accepts an array of span fractions and returns the corresponding twist angles *in radians*.
>>>
>>>**"dihedral" : float, array, string, or func optional**
>>>>Gives the dihedral of the wing segment in degrees. Defined the same as "twist". If defined as a distribution, this specifies the local dihedral angle at each point along the wing. Defaults to 0.
>>>
>>>**"shear_dihedral" : bool, optional**
>>>>Whether the dihedral should be viewed as a solid-body rotation (standard) or a shear transformation (nonstandard), similar to sweep, for the purpose of exporting 3D models. Has no effect on aerodynamics. Defaults to False, corresponding to a solid-body rotation.
>>>
>>>**"sweep" : float, array, string, or func optional**
>>>>Gives the sweep angle of the wing segment in degrees. Sweeping the wing is a shear transformation, rather than a solid-body rotation. This means the amount of sweep will not affect the distance of the wingtip from thex-z plane. Defined the same as "twist". Defaults to 0.
>>>
>>>**"chord" : float, array, string, or func optional**
>>>>Gives the chord length of the wing segment. Defined the same as "twist", except that it can also be specified as elliptic using the following definition:
>>>
>>>>>**"chord" : ["elliptic", 1.0]**
>>>
>>>>Where the second list element is the root chord length. Units can be specified using:
>>>
>>>>>**"chord" : ["elliptic", 1.0, "ft"]**
>>>
>>>>Defaults to 1.0.
>>>
>>>**"quarter_chord_locs" : array or string, optional**
>>>>Gives locations of the wing quarter chord **relative to the wing root**, as opposed to relative to the aircraft origin. The first column should be body-x coordinates, the second column should be body-y coordinates, and the third column should be body-z coordinates. MachUpX will linearly interpolate between the given points to determine the locations of control points and vortex nodes. Points should be given progressing from root to tip. If only one point is given, this will be taken as the tip location relative to the root, and the wing will be straight. Not that the corresponding span fraction for each point *does not* need to be specified here. MachUpX will automatically calculate that from the point locations.
>>>>
>>>>If "quarter_chord_locs" is given, "sweep", "dihedral", and "semispan" may not be specified.
>>>>
>>>>These locations should only be given for the *right* half of the wing and MachUpX will mirror them for the left half, *even for a wing where "side" is "left"*.
>>>
>>>**"ll_offset" : float, array, string, or func optional**
>>>>Gives the offset of the lifting-line from the wing quarter-chord. By default, MachUpX assumes the lifting-line for a given wing segment falls on the quarter chord line. This parameter allows shifting the lifting-line along the chord line, if desired. This shift is given as a fraction of the local chord. A positive value shifts the lifting-line back. This is defined the same as "twist", except that it may also be specified as "kuchemann" *for wings of constant sweep, including zero sweep*, in which case the lifting-line will be placed on the locus of aerodynamic centers as predicted by Kuchemann's equations. Specifying "kuchemann" for a wing segment with variable sweep will result in an error. If Kuchemann's equations are selected, the user should ensure the number of control points for this wing is large enough to capture the nonlinear locus of aerodynamic centers at the wing root and tips. MachUpX will cosine cluster these points by default, but a very small number of control points may still fail to sufficiently capture Kuchemann's correction. Defaults to 0. The developers consider placing the lifting-line using Kuchemann's equations to be inappropriate; see Goates et al. "Practical Implementation of a General Numerical Lifting-Line Theory", *AIAA SciTech Forum*, 2021, for further discussion of this.
>>>
>>>**"airfoil" : string or array, optional**
>>>>Gives the section airfoil(s) of the wing segment. Can be the name of any airfoil defined under "airfoils" within the parent aircraft object, in which case the section properties will be constant across the span. If specified as an array, the array gives the airfoil as a function of span. The first column gives the span location, as with "twist", and the second column gives the name of the airfoil at that location. MachUpX will interpolate airfoil properties between the given points. Can also be the path to a csv file containing the airfoil distribution formatted in columns, as with the array. Cannot have units. If no airfoil is specified here, it will default to the first airfoil given under "airfoils" (aircraft scope).
>>>
>>>**"grid" : dict, optional**
>>>>Describes the distribution of control points along the wing and certain corrections to the structure of the grid.
>>>>
>>>>**"N" : int, optional**
>>>>>Number of horseshoe vortices used to model the wing segment in the numerical lifting-line algorithm. This is the number of horseshoe vortices per semispan. Defaults to 40.
>>>>
>>>>**"distribution" : str or list, optional**
>>>>>Specifies how vortex nodes and control points are to be distributed along the wing segment. Can be "linear", "cosine_cluster", or a list of span locations. "linear" will distribute the control points and vortex nodes evenly along the span. "cosine_cluster" will implement traditional cosine clustering, where points are spaced evenly in theta causing them to cluster at the tips of each segment. Defaults to "cosine_cluster".
>>>>>
>>>>>If this is a list, it must be an ordered list of span locations of length 2N+1 explicitly giving the span fraction location of each vortex node and control point. Should be arranged as ```[node_0_loc, cp_0_loc, node_1_loc, cp_1_loc,..., node_N_loc, cp_N_loc, node_N+1_loc]```. The list should begin at 0.0 and end at 1.0 and be monotonically increasing.
>>>>
>>>>**"flap_edge_cluster" : bool, optional**
>>>>>If true, control points will be clustered around the edges of control surfaces. Can only be used if "distribution" is "cosine_cluster". Defaults to True.
>>>>
>>>>**"cluster_points" : list, optional**
>>>>>If extra clustering is desired (for example at a sharp change in geometry) the user can specify a list of additional span fractions here about which control points should be clustered. Can only be used if "distribution" is "cosine_cluster". Defaults to no extra clustering.
>>>>
>>>>**"reid_corrections" : bool, optional**
>>>>>Whether to apply corrections to this wing segment to implement the general approach to lifting-line developed by Reid (Reid, et al. "A General Approach to Lifting-Line Theory, Applied to Wings with Sweep," *AIAA SciTech Forum*, 2020.). For those not familiar with the general implementation of numerical lifting-line, it is highly recommended to read the paper. These analytic corrections increase accuracy and ensure grid convergence for swept wings and wings in sideslip. Should not be set to False unless you know what you're doing. Defaults to True.
>>>>
>>>>**"joint_length" : float, optional**
>>>>>Non-dimensional joint length, as a fraction of the chord, of the jointed horseshoe vortices. Defaults to 0.15. Note that any joint length less than the default is considered by Reid to be numerically sensitive, leading to poor grid convergence. Final results are mildly sensitive to this parameter.
>>>>
>>>>**"blending_distance" : float, optional**
>>>>>Non-dimensional lifting-line blending distance to be used in setting conditional concavity. Defaults to 1.0. Note that any blending distance less than the default is considered by Reid to be numerically sensitive, leading to poor grid convergence. Final results are mildly sensitive to this parameter.
>>>>
>>>>**"wing_ID" : int, optional**
>>>>>ID of the wing this wing segment belongs to. This is not the same as the ID of the wing segment that this wing segment connects to. Rather, this parameter is used to group wing segments into contiguous wings that share a single lifting-line. If this is not specified, MachUpX will assume this wing segment is isolated in space, except from its mirror image if the two halves are contiguous. Must be positive. Defaults to None. Not required if "reid_corrections" is False.
>>>
>>>**"control_surface" : dict, optional**
>>>>Defines a control surface on the trailing edge of the wing segment. The flap aerodynamics are determined by the airfoil type given for the wing segment. A "linear" airfoil will use Phillips' approximations for trailing-edge flaps (Mechanics of Flight, ed. 2, Ch. 1.7).
>>>>
>>>>**"root_span" : float, optional**
>>>>>The span location, as a fraction of total span, where the control surface begins. Defaults to 0.0.
>>>>
>>>>**"tip_span" : float, optional**
>>>>>The span location, as a fraction of total span, where the control surface ends. Defaults to 1.0.
>>>>
>>>>**"chord_fraction" : float, array, or string, optional**
>>>>>The depth of the control surface, as a fraction of the local chord length. Defined the same as "twist". If an array or file is specified, however, the start and end of the data must coincide with "root_span" and "tip_span", respectively. Defaults to 0.25.
>>>>
>>>>**"saturation_angle" : float, optional**
>>>>>Positive angle (in degrees) at which this control surface saturates. It is assumed the control surface also saturates at the negative of this angle. Defaults to infinite (no saturation).
>>>>
>>>>**"is_sealed" : bool, optional**
>>>>>Whether or not the flap is sealed. Affects the effectiveness of the flap. Defaults to true.
>>>>
>>>>**"control_mixing" : dict**
>>>>>Determines which control inputs move this control surface. A control surface can be affected by any number of controls.
>>>>>
>>>>>**"<CONTROL_NAME>" : float**
>>>>>>Linearly maps the control deflection to the control surface deflection. The control deflection will be multiplied by this value and then applied to the control surface.
>>>
>>>**"CAD_options" : dict, optional**
>>>>Contains options for how this wing segment is to be treated when exporting in a CAD-type file (STL, STP, DXF).
>>>>
>>>>**"close_wing_tip" : bool, optional**
>>>>>Whether to close the tip of the wing when exporting an STL or VTK file. Does so using a flat surface of the same shape as the tip airfoil section. Defaults to False.
>>>>
>>>>**"close_wing_root" : bool, optional**
>>>>>Same as "close_wing_root", but for the root.
>>>>
>>>>**"round_wing_tip" : bool, optional**
>>>>>Whether to close the tip of the wing when exporting an STL or VTK file. Does so by rotating and blending the airfoil outline about the chord. Defaults to False.
>>>>
>>>>**"round_wing_root" : bool, optional**
>>>>>Same as "round_wing_root", but for the root.