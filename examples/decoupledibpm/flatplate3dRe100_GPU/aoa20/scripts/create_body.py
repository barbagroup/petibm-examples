"""Create a flat plate with aspect ratio 2 and a 20-degree inclination."""

import numpy
import pathlib

import petibmpy


# Flat-plate's parameters.
L = 1.0  # chord length
AR = 2.0  # aspect ratio
xc, yc, zc = 0.0, 0.0, 0.0  # center's coordinates
aoa = 20.0  # angle of inclination in degrees
ds = 0.04  # mesh spacing

# Generate coordinates of an inclined line.
n = numpy.ceil(L / ds)
s = numpy.linspace(xc - L / 2, xc + L / 2, num=n + 1)
x = xc + numpy.cos(numpy.radians(-aoa)) * s
y = yc + numpy.sin(numpy.radians(-aoa)) * s

# Extrude the line along the z direction.
zlim = (zc - L * AR / 2, zc + L * AR / 2)
nz = numpy.ceil(L * AR / ds)
x, y, z = petibmpy.extrude2d(x, y, zlim, n=nz, force=True)

# Save coordinates to file.
simudir = pathlib.Path(__file__).absolute().parents[1]
filepath = simudir / f'flatplate_aoa{int(aoa)}.body'
petibmpy.write_body(filepath, x, y, z)
