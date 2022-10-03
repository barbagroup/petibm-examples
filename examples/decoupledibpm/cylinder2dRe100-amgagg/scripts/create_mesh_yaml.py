"""Create a YAML file with info about the structured Cartesian mesh."""

import pathlib

import petibmpy


xlim, ylim = (-15.0, 35.0), (-25.0, 25.0)
xbox, ybox = (-0.75, 0.75), (-0.75, 0.75)
width = (xbox[1] - xbox[0]) / 90

info = [{'direction': 'x', 'start': xlim[0],
         'subDomains': [{'end': xbox[0],
                         'width': width,
                         'stretchRatio': 1.03,
                         'reverse': True},
                        {'end': xbox[1],
                         'width': width,
                         'stretchRatio': 1.0},
                        {'end': xlim[1],
                         'width': width,
                         'stretchRatio': 1.01}]},
        {'direction': 'y', 'start': ylim[0],
         'subDomains': [{'end': ybox[0],
                         'width': width,
                         'stretchRatio': 1.04,
                         'reverse': True},
                        {'end': ybox[1],
                         'width': width,
                         'stretchRatio': 1.0},
                        {'end': ylim[1],
                         'width': width,
                         'stretchRatio': 1.04}]}]

mesh = petibmpy.CartesianGrid(info)
print(mesh)
simudir = pathlib.Path(__file__).absolute().parents[1]
filepath = simudir / 'mesh.yaml'
mesh.write_yaml(filepath, ndigits=10)
