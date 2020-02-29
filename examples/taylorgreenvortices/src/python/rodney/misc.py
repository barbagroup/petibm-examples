"""Miscellaneous helper functions."""

import argparse
import numpy
import pathlib

import petibmpy


def parse_command_line():
    """Parse the command-line options."""
    formatter_class = argparse.ArgumentDefaultsHelpFormatter
    descr = 'Generic command-line parser for the rolling-piching application.'
    parser = argparse.ArgumentParser(description=descr,
                                     formatter_class=formatter_class)
    parser.add_argument('--no-show', dest='show_figures',
                        action='store_false',
                        help='Do not display Matplotlib figures')
    parser.add_argument('--no-save', dest='save_figures',
                        action='store_false',
                        help='Do not save Matplotlib figures')
    parser.add_argument('--data-dir', dest='data_dir',
                        type=str,
                        default='output',
                        help='Directory with data to load')
    parser.add_argument('--body', dest='body_path',
                        type=str,
                        default=None,
                        help='Path of the file with body coordinates')
    # Cast data directory into a pathlib.Path object.
    args = parser.parse_args()
    args.data_dir = pathlib.Path(args.data_dir)
    return args


def petibm_load_grid_and_field(datadir, timestep, name):
    """Load the gridlines and values of a field at a given time step.

    Parameters
    ----------
    datadir : pathlib.Path
        Directory with the data to load.
    timestep : int
        Time-step index.
    name : str
        Name of the field to read, e.g. 'u', 'v', or 'p'.

    Returns
    -------
    tuple
        Gridline locations in each direction as a tuple of 1D arrays of floats.
    numpy.ndarray
        Field values at given time step.

    """
    grid = petibmpy.read_grid_hdf5(datadir / 'grid.h5', name)
    field = petibmpy.read_field_hdf5(datadir / f'{timestep:0>7}.h5', name)
    return grid, field


def l2_norm(u):
    """Compute and return the L_2 norm of the a given array u."""
    return numpy.sqrt(numpy.sum(u**2) / u.size)


def linf_norm(u):
    """Compute and return the L_inf norm of the a given array u."""
    return numpy.max(numpy.abs(u))
