"""Create a sphere."""

import pathlib
import sys

import petibmpy


rootdir = pathlib.Path(__file__).absolute().parents[5]
sys.path.insert(0, str(rootdir / 'misc'))
import icosphere


R = 0.5
sphere = icosphere.create_icosphere(15)
sphere.vertices *= R
sphere.print_info()

simudir = pathlib.Path(__file__).absolute().parents[1]
filepath = simudir / 'sphere.body'
petibmpy.write_body(filepath, *sphere.vertices.T)
