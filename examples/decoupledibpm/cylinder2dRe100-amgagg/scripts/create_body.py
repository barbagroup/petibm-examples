"""Create the body and write the coordinates to a file."""

import numpy
import pathlib

import petibmpy


# Create the coordinates of the circle.
R = 0.5
dx = 1.5 / 90
N = int(2 * numpy.pi * R / dx) + 1
N += N % 2
delta_x, delta_y = 0.01 * dx, 0.01 * dx
xc, yc = 0.0 + delta_x, 0.0 + delta_y  # slightly offset cylinder
theta = numpy.linspace(0.0, 2 * numpy.pi, num=N + 1)[:-1]
x, y = xc + R * numpy.cos(theta), yc + R * numpy.sin(theta)

# Save the coordinates into a file.
simudir = pathlib.Path(__file__).absolute().parents[1]
filepath = simudir / 'cylinder.body'
petibmpy.write_body(filepath, x, y)
