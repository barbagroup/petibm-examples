"""Create a YAML file with info about the structured Cartesian mesh."""

import pathlib

import petibmpy


xlim, ylim, zlim = (-4.0, 6.1), (-5.0, 5.0), (-5.0, 5.0)
xbox, ybox, zbox = (-0.5, 0.7), (-0.6, 0.6), (-1.2, 1.2)
width = 0.04

config = [{'direction': 'x', 'start': xlim[0],
           'subDomains': [{'end': xbox[0],
                           'width': width,
                           'stretchRatio': 1.03,
                           'reverse': True},
                          {'end': xbox[1],
                           'width': width,
                           'stretchRatio': 1.0},
                          {'end': xlim[1],
                           'width': width,
                           'stretchRatio': 1.03}]},
          {'direction': 'y', 'start': ylim[0],
           'subDomains': [{'end': ybox[0],
                           'width': width,
                           'stretchRatio': 1.3,
                           'reverse': True},
                          {'end': ybox[1],
                           'width': width,
                           'stretchRatio': 1.0},
                          {'end': ylim[1],
                           'width': width,
                           'stretchRatio': 1.3}]},
          {'direction': 'z', 'start': zlim[0],
           'subDomains': [{'end': zbox[0],
                           'width': width,
                           'stretchRatio': 1.3,
                           'reverse': True},
                          {'end': zbox[1],
                           'width': width,
                           'stretchRatio': 1.0},
                          {'end': zlim[1],
                           'width': width,
                           'stretchRatio': 1.3}]}]

mesh = petibmpy.CartesianGrid(config=config)
print(mesh)
simudir = pathlib.Path(__file__).absolute().parents[1]
filepath = simudir / 'mesh.yaml'
mesh.write_yaml(filepath, ndigits=10)
