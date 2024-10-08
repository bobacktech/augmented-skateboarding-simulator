from dataclasses import dataclass


"""
This class specifies the kinematic state of the electric skateboard. The coordinate 
reference frame for the data values is the skateboard itself, i.e. the body coordinate frame. 

x-axis is along the length of the skateboard.
y-axis is along the width of the skateboard.
z-axis is along the height of the skateboard.   

The velocity is the speed along the long axis, i.e. x-axis, of the electric skateboard.
"""


@dataclass
class EboardKinematicState:
    """Velocity is the speed along the long axis of the eboard. Units m/s"""

    velocity: float = 0.0

    """3-Dimensional linear acceleration vector. Units m/s^2"""
    acceleration_x: float = 0.0
    acceleration_y: float = 0.0
    acceleration_z: float = 0.0

    """Attitude - pitch, roll, yaw - in degrees"""
    pitch: float = 0.0
    roll: float = 0.0
    yaw: float = 0.0

    """Electric Motor State"""
    erpm: int = 0
    input_current: float = 0.0
