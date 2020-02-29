"""Create coordinates of immersed boundary and save them to file."""

import math
import numpy
import pathlib

import petibmpy


# Simulation directory.
simudir = pathlib.Path(__file__).absolute().parents[1]

# Set parameters.
L, n = 1.0, 180  # Length of the domain and number of cells along a direction
R = 0.25  # radius of the cylinder
xc, yc = 0.5, 0.5  # center of the cylinder
ds = L / n  # approximate distance between two adjacent markers
N = math.ceil(2 * numpy.pi * R / ds)  # number of segments on boundary

# Create the cylinder coordinates.
theta = numpy.linspace(0.0, 2 * numpy.pi, num=N + 1)[:-1]
x, y = xc + R * numpy.cos(theta), yc + R * numpy.sin(theta)

# Save the coordinates into file.
filepath = simudir / 'cylinder.body'
petibmpy.write_body(filepath, x, y)
