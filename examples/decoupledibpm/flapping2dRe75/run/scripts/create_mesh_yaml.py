"""Create a YAML file with info about the structured Cartesian mesh."""

import pathlib

import petibmpy


# Info about the 2D structured Cartesian grid.
xlim, ylim = (-15.0, 15.0), (-15.0, 15.0)
xbox, ybox = (-2.0, 2.0), (-3.0, 1.0)
width = 0.025  # minimum grid spacing in the x- and y- directions
ratio = 1.05  # stretching ratio

info = [{'direction': 'x', 'start': xlim[0],
         'subDomains': [{'end': xbox[0],
                         'width': width,
                         'stretchRatio': ratio,
                         'reverse': True},
                        {'end': xbox[1],
                         'width': width,
                         'stretchRatio': 1.0},
                        {'end': xlim[1],
                         'width': width,
                         'stretchRatio': ratio}]},
        {'direction': 'y', 'start': ylim[0],
         'subDomains': [{'end': ybox[0],
                         'width': width,
                         'stretchRatio': ratio,
                         'reverse': True},
                        {'end': ybox[1],
                         'width': width,
                         'stretchRatio': 1.0},
                        {'end': ylim[1],
                         'width': width,
                         'stretchRatio': ratio}]}]

mesh = petibmpy.CartesianGrid(info)
print(mesh)
simudir = pathlib.Path(__file__).absolute().parents[1]
filepath = simudir / 'mesh.yaml'
mesh.write_yaml(filepath, ndigits=10)
