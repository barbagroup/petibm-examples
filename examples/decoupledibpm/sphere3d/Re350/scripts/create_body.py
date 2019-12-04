"""Create a sphere."""

import pathlib
import sys

import petibmpy


rootdir = pathlib.Path(__file__).absolute().parents[5]
sys.path.insert(0, str(rootdir / 'misc'))
import icosphere


R = 0.5
sphere = icosphere.create_icosphere(25)
sphere.vertices *= R
sphere.print_info()
x, y, z = sphere.vertices.T

# Center the sphere at (-5.0, 0.0, 0.0)
x += -5.0

simudir = pathlib.Path(__file__).absolute().parents[1]
filepath = simudir / 'sphere.body'
petibmpy.write_body(filepath, x, y, z)
