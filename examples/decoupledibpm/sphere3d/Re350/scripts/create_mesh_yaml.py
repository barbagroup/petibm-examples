"""Create a YAML file with info about the structured Cartesian mesh."""

import pathlib

import petibmpy


xlim, ylim, zlim = (-10.0, 10.0), (-10.0, 10.0), (-10.0, 10.0)
xbox, ybox, zbox = (-6.0, -4.0), (-1.0, 1.0), (-1.0, 1.0)
width = 0.025

config = [{'direction': 'x', 'start': xlim[0],
           'subDomains': [{'end': xbox[0],
                           'width': width,
                           'stretchRatio': 1.1,
                           'reverse': True},
                          {'end': xbox[1],
                           'width': width,
                           'stretchRatio': 1.0},
                          {'end': xlim[1],
                           'width': width,
                           'stretchRatio': 1.02}]},
          {'direction': 'y', 'start': ylim[0],
           'subDomains': [{'end': ybox[0],
                           'width': width,
                           'stretchRatio': 1.1,
                           'reverse': True},
                          {'end': ybox[1],
                           'width': width,
                           'stretchRatio': 1.0},
                          {'end': ylim[1],
                           'width': width,
                           'stretchRatio': 1.1}]},
          {'direction': 'z', 'start': zlim[0],
           'subDomains': [{'end': zbox[0],
                           'width': width,
                           'stretchRatio': 1.1,
                           'reverse': True},
                          {'end': zbox[1],
                           'width': width,
                           'stretchRatio': 1.0},
                          {'end': zlim[1],
                           'width': width,
                           'stretchRatio': 1.1}]}]

mesh = petibmpy.CartesianGrid(config=config)
print(mesh)
simudir = pathlib.Path(__file__).absolute().parents[1]
filepath = simudir / 'mesh.yaml'
mesh.write_yaml(filepath, ndigits=10)
