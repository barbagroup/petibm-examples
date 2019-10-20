"""Compute the observed order of convergence for the velocity and pressure."""


import numpy
import pathlib

import petibmpy


def observed_order_convergence(fields, grids, grid_ref, ratio):
    """Compute the observed order of convergence.

    Parameters
    ----------
    fields : tuple of numpy.ndarray objects
        The field values on three consistently refined grids.
    grids : tuple of tuple of numpy.ndarray objects
        The gridline locations for three consistently refined grids.
    grid_ref : tuple of numpy.ndarray objects
        The reference gridlines used for interpolation.
    ratio : float
        The grid refinement ratio.

    Returns
    -------
    float
        The observed order of convergence.

    """
    coarse = petibmpy.interpolate2d(fields[0], grids[0], grid_ref)
    medium = petibmpy.interpolate2d(fields[1], grids[1], grid_ref)
    fine = petibmpy.interpolate2d(fields[2], grids[2], grid_ref)
    alpha = (numpy.log(numpy.linalg.norm(medium - coarse, ord=None) /
                       numpy.linalg.norm(fine - medium, ord=None)) /
             numpy.log(ratio))
    return alpha


# Set parameters.
rootdir = pathlib.Path(__file__).absolute().parents[1]
timestep = 500  # solution time-step index
field_names = ['p', 'u', 'v']  # name of the fields
ncells = [30, 90, 270, 810]  # number of cells in each direction
ratio = 3  # refinement ratio between two consecutive grids

# Load the grid and field from files.
data = {}
for name in field_names:
    subdata = {'grids': [], 'fields': []}
    for n in ncells:
        simudir = rootdir / str(n)
        grid = petibmpy.read_grid_hdf5(simudir / 'grid.h5', name)
        filepath = simudir / 'solution' / f'{timestep:0>7}.h5'
        field = petibmpy.read_field_hdf5(filepath, name)
        subdata['grids'].append(grid)
        subdata['fields'].append(field)
    data[name] = subdata

# Compute the observed orders of convergence.
alphas = {}
for name in field_names:
    grids, fields = data[name]['grids'], data[name]['fields']
    # Compute order of convergence using the three coarsest grids.
    # Fields are interpolated on the first grid.
    alpha1 = observed_order_convergence(fields[:3], grids[:3], grids[0], ratio)
    # Compute order of convergence using the three finest grids.
    # Fields are interpolated on the first grid.
    alpha2 = observed_order_convergence(fields[1:], grids[1:], grids[0], ratio)
    alphas[name] = (alpha1, alpha2)

print(alphas)
