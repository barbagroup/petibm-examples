"""Plott the velocities along the centerlines of the 2D cavity.

Compare results with numerical data reported in Ghia et al. (1982).

_References:_

* Ghia, U. K. N. G., Ghia, K. N., & Shin, C. T. (1982).
  High-Re solutions for incompressible flow using the Navier-Stokes equations
  and a multigrid method.
  Journal of computational physics, 48(3), 387-411.

"""

from matplotlib import pyplot
import numpy
import os
import pathlib

import petibmpy


def load_data_ghia_et_al_1982(filepath, Re):
    """Load numerical data from Ghia et al. (1982) at given Re.

    Parameters
    ----------
    filepath : string or pathlib.Path object
        The path of the file containing data from Ghia et al. (1982).
    Re : str
        Reynolds number.

    Returns
    -------
    dict
        2-item dictionary with the data along the `vertical` and
        `horizontal` centerlines.

    """
    with open(filepath, 'r') as infile:
        data = numpy.loadtxt(infile, dtype=numpy.float64, unpack=True)
    yu, xv = data[0], data[6]
    re2col = {'100': (1, 7), '1000': (2, 8), '3200': (3, 9),
              '5000': (4, 10), '10000': (5, 11)}
    idx_u, idx_v = re2col[Re]
    u, v = data[idx_u], data[idx_v]
    return yu, u, xv, v


# Parameters.
Res = [100, 1000, 3200, 5000]  # Reynolds numbers
# Res = [100, 1000, 5000]  # Reynolds numbers
timesteps = [1000, 10000, 25000, 60000]  # time step to read the solution
# timesteps = [1000, 10000, 60000]  # time step to read the solution
show_figure = True  # display the Matplotlib figure
save_figure = True  # save the Matplotlib figure

maindir = pathlib.Path(__file__).absolute().parents[1]
rootdir = maindir.parents[1]

# Initialize the figure.
pyplot.rc('font', family='serif', size=12)
fig, (ax1, ax2) = pyplot.subplots(ncols=2, figsize=(8.0, 4.0))
ax1.set_xlabel('y')
ax1.set_ylabel('u')
ax2.set_xlabel('x')
ax2.set_ylabel('v')

for Re, timestep in zip(Res, timesteps):
    # Load data from Ghia et al. (1982).
    datadir = rootdir / 'data'
    filepath = datadir / 'ghia_et_al_1982_lid_driven_cavity.dat'
    yu_g, uc_g, xv_g, vc_g = load_data_ghia_et_al_1982(filepath, str(Re))

    # Load gridlines and velocity fields.
    simudir = maindir / f'liddrivencavity2dRe{Re}'
    filepath = simudir / 'grid.h5'
    xu, yu = petibmpy.read_grid_hdf5(filepath, 'u')
    xv, yv = petibmpy.read_grid_hdf5(filepath, 'v')
    filepath = simudir / 'solution' / f'{timestep:0>7}.h5'
    u = petibmpy.read_field_hdf5(filepath, 'u')
    v = petibmpy.read_field_hdf5(filepath, 'v')

    # Interpolate solution at centerlines of the cavity.
    uc = petibmpy.linear_interpolation(u.T, xu, 0.5)
    vc = petibmpy.linear_interpolation(v, yv, 0.5)

    # Plot the velocity profiles.
    ax1.plot(yu, uc, label=f'Re = {Re}')
    label = ('Ghia et al. (1982)' if Re == Res[-1] else None)
    ax1.plot(yu_g, uc_g, label=label, linewidth=0,
             color='black', marker='o', markerfacecolor='none')
    ax2.plot(xv, vc, label=f'Re = {Re}')
    ax2.plot(xv_g, vc_g, label='Ghia et al. (1982)', linewidth=0,
             color='black', marker='o', markerfacecolor='none')

# Finalize the figure.
ax1.legend(loc='upper left', frameon=False)
ax1.axis((0.0, 1.0, -0.75, 1.0))
ax2.axis((0.0, 1.0, -0.75, 1.0))
fig.tight_layout()

if show_figure:
    pyplot.show()

if save_figure:
    # Save the figure as a PNG.
    figdir = maindir / 'figures'
    figdir.mkdir(parents=True, exist_ok=True)
    filepath = figdir / 'liddrivencavity2d_centerline_velocities.png'
    fig.savefig(filepath, dpi=300, bbox_inches='tight')
