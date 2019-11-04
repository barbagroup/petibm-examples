"""Create and plot an icosphere."""

from matplotlib import pyplot
from mpl_toolkits.mplot3d import Axes3D
import numpy
import pathlib

import petibmpy

from icosphere import create_icosphere, create_polyhedron


def plot_trisurf(vertices, triangles):
    """Plot the triangular mesh."""
    fig = pyplot.figure(figsize=(8.0, 8.0))
    ax = fig.gca(projection='3d')
    ax.plot_trisurf(*vertices.T, triangles=triangles,
                    linewidth=0.5, edgecolor='black')
    ax.axis('scaled', adjustable='box')
    fig.tight_layout()


simudir = pathlib.Path(__file__).absolute().parent

icosphere = create_icosphere(25)
# print(icosphere)
R = 0.5
icosphere.vertices *= R
icosphere.print_info()

filepath = simudir / 'sphere.body'
petibmpy.write_body(filepath, *icosphere.vertices.T)

# plot_trisurf(icosphere.vertices, icosphere.triangles)
# pyplot.show()
