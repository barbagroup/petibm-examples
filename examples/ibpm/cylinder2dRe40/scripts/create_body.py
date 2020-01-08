"""Create a 2D circle."""

import pathlib
import numpy

import petibmpy


# Set parameters of the circle.
R = 0.5  # radius
xc, yc = 0.0, 0.0  # center's coordinates
ds = 0.025  # distance between two consecutive points

# Create coordinates of the circle.
n = numpy.ceil(2 * numpy.pi * R / ds)  # number of divisions
theta = numpy.linspace(0.0, 2.0 * numpy.pi, num=n + 1)[:-1]
x, y = xc + R * numpy.cos(theta), yc + R * numpy.sin(theta)

# Save coordinates into file.
simudir = pathlib.Path(__file__).absolute().parents[1]
filepath = simudir / 'circle.body'
petibmpy.write_body(filepath, x, y)
