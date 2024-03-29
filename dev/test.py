# This script is for me to test the functionality of whatever I'm working on at the moment.
import machupX as MX
import pypan as pp
import json
import numpy as np
import subprocess as sp
import matplotlib.pyplot as plt
from stl import mesh
from mpl_toolkits import mplot3d

if __name__=="__main__":
    
    # Specify input
    input_dict = {
        "solver" : {
            "type" : "nonlinear"
        },
        "units" : "English",
        "scene" : {
            "atmosphere" : {
            }
        }
    }

    # Specify airplane
    airplane_dict = {
        "weight" : 50.0,
        "units" : "English",
        "controls" : {
            "aileron" : {
                "is_symmetric" : False
            },
            "elevator" : {
                "is_symmetric" : True
            },
            "rudder" : {
                "is_symmetric" : False
            }
        },
        "airfoils" : {
            "NACA_2410" : {
                "CLa" : 6.28,
                "geometry" : {
                    "NACA" : "2410"
                }
            }
        },
        "plot_lacs" : False,
        "wings" : {
            "main_wing" : {
                "ID" : 1,
                "side" : "both",
                "is_main" : True,
                "airfoil" : [[0.0, "NACA_2410"],
                             [1.0, "NACA_2410"]],
                "semispan" : 10.0,
                "dihedral" : [[0.0, 0.0],
                              [1.0, 0.0]],
                "chord" : [[0.0, 1.0],
                           [1.0, 1.0]],
                "sweep" : [[0.0, 30.0],
                           [1.0, 30.0]],
                "grid" : {
                    "N" : 5
                },
                "CAD_options" :{
                    "round_wing_tip" : True,
                    "round_wing_root" : False,
                    "n_rounding_sections" : 20
                }
            #},
            #"h_stab" : {
            #    "ID" : 2,
            #    "connect_to" : {
            #        "ID" : 1,
            #        "location" : "root",
            #        "dx" : -5.0,
            #        "dz" : -0.5
            #    },
            #    "side" : "both",
            #    "is_main" : False,
            #    "airfoil" : [[0.0, "NACA_2410"],
            #                 [1.0, "NACA_2410"]],
            #    "semispan" : 4.0,
            #    "dihedral" : [[0.0, 0.0],
            #                  [1.0, 0.0]],
            #    "chord" : [[0.0, 1.0],
            #               [1.0, 1.0]],
            #    "sweep" : [[0.0, 30.0],
            #               [1.0, 30.0]],
            #    "grid" : {
            #        "N" : 30
            #    },
            #    "control_surface" : {
            #        "control_mixing" : {
            #            "elevator" : 1.0
            #        }
            #    }
            }
        }
    }

    # Specify state
    state = {
        "position" : [0.0, 0.0, 0.0],
        "velocity" : 10.0,
        "alpha" : 5.0,
        "orientation" : [0.0, 0.0, 0.0]
    }
    control_state = {
    }

    # Load scene
    scene = MX.Scene(input_dict)
    scene.add_aircraft("plane", airplane_dict, state=state, control_state=control_state)
    FM = scene.solve_forces(verbose=True)
    print(json.dumps(FM["plane"]["total"], indent=4))
    state["alpha"] = 5.5
    scene.set_aircraft_state(state=state)
    FM = scene.solve_forces(initial_guess='previous', verbose=True)
    print(json.dumps(FM["plane"]["total"], indent=4))
    state["alpha"] = 0.0
    scene.set_aircraft_state(state=state)
    FM = scene.solve_forces(initial_guess='previous', verbose=True)
    print(json.dumps(FM["plane"]["total"], indent=4))