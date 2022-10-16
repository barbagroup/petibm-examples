"""Kinematic parameters for the oscillating 2D cylinder."""

import math


# Set parameters.
Re = 100.0  # Reynolds number
KC = 5.0  # Keulegan-Carpenter number
D = 1.0  # cylinder diameter
Um = 1.0  # maximum translational velocity

# Set fluid properties.
nu = Um * D / Re  # kinematic viscosity
rho = 1.0  # density

# Set kinematic parameters.
f = Um / D / KC  # oscillation frequency
w = 2 * math.pi * f  # angular frequency
Am = Um / w  # oscillation amplitude


if __name__ == '__main__':
    print(locals())
