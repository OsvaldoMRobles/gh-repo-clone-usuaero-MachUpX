#Tests the state of the aircraft is properly set

import machupX as MX
import numpy as np
import json

input_file = "test/input_for_testing.json"


def test_aerodynamic_velocity_with_wind():
    # Tests the aircraft's velocity is properly determined from an aerodynamic state with wind in the scene

    # Load input
    with open(input_file, 'r') as input_handle:
        input_dict = json.load(input_handle)

    input_dict["scene"]["atmosphere"]["V_wind"] = [100, 0, 0]
    
    aircraft_state = {}
    aircraft_state["type"] = "aerodynamic"
    aircraft_state["velocity"] = 100
    aircraft_state["alpha"] = 0.0
    aircraft_state["beta"] = 0.0
    input_dict["scene"]["aircraft"]["test_plane"]["state"] = aircraft_state

    scene = MX.Scene(input_dict)

    assert np.allclose(scene.airplanes["test_plane"].v, [200, 0, 0], rtol=0.0, atol=1e-10)


def test_complex_aerodynamic_velocity_with_wind():
    # Tests the aircraft's velocity is properly determined from an aerodynamic state with wind in the scene

    # Load input
    with open(input_file, 'r') as input_handle:
        input_dict = json.load(input_handle)

    input_dict["scene"]["atmosphere"]["V_wind"] = [100, 100, 0]
    
    aircraft_state = {}
    aircraft_state["type"] = "aerodynamic"
    aircraft_state["velocity"] = 100
    aircraft_state["alpha"] = 5.0
    aircraft_state["beta"] = 5.0
    input_dict["scene"]["aircraft"]["test_plane"]["state"] = aircraft_state

    scene = MX.Scene(input_dict)

    assert np.allclose(scene.airplanes["test_plane"].v, [199.24325091, 108.682659390, 8.682659390], rtol=0.0, atol=1e-8)


def test_rigid_body_velocity_with_wind():
    # Tests the aircraft's velocity is properly determined from a rigid body state with wind in the scene

    # Load input
    with open(input_file, 'r') as input_handle:
        input_dict = json.load(input_handle)

    input_dict["scene"]["atmosphere"]["V_wind"] = [100, 100, 0]
    
    aircraft_state = {}
    aircraft_state["type"] = "rigid-body"
    aircraft_state["velocity"] = [100, 100, 0]
    input_dict["scene"]["aircraft"]["test_plane"]["state"] = aircraft_state

    scene = MX.Scene(input_dict)

    assert np.allclose(scene.airplanes["test_plane"].v, [100, 100, 0], rtol=0.0, atol=1e-8)


def test_get_alpha_and_beta():
    # Tests the alpha and beta that are input are what are returned

    # Load input
    with open(input_file, 'r') as input_handle:
        input_dict = json.load(input_handle)

    v_wind = [100, 100, 0]
    input_dict["scene"]["atmosphere"]["V_wind"] = v_wind
    
    aircraft_state = {}
    aircraft_state["type"] = "aerodynamic"
    aircraft_state["velocity"] = 100
    aircraft_state["alpha"] = 5.0
    aircraft_state["beta"] = 5.0
    input_dict["scene"]["aircraft"]["test_plane"]["state"] = aircraft_state

    scene = MX.Scene(input_dict)

    assert abs(scene.airplanes["test_plane"].get_alpha(v_wind)-5.0)<1e-10
    assert abs(scene.airplanes["test_plane"].get_beta(v_wind)-5.0)<1e-10