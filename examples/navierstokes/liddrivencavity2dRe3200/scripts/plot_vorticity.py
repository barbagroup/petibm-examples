"""Plot the final time step vorticity field."""

from matplotlib import pyplot
import numpy
import pathlib

import petibmpy


show_figure = True  # display the Matplotlib figure
save_figure = True  # save the Matplotlib figure
simudir = pathlib.Path(__file__).absolute().parents[1]

# Load the grid lines from file.
filepath = simudir / 'grid.h5'
x, y = petibmpy.read_grid_hdf5(filepath, 'wz')

# Load the vorticity field from file.
timestep = 25000
filepath = simudir / 'solution' / f'{timestep:0>7}.h5'
wz = petibmpy.read_field_hdf5(filepath, 'wz')

# Plot the contours of the vorticity.
pyplot.rc('font', family='serif', size=14)
fig, ax = pyplot.subplots(figsize=(6.0, 6.0))
ax.set_xlabel('x')
ax.set_ylabel('y')
levels = numpy.linspace(-5.0, 5.0, num=21)
ax.contourf(x, y, wz, levels=levels, extend='both')
ax.contour(x, y, wz, levels=levels, colors='black')
ax.set_xlim(0.0, 1.0)
ax.set_ylim(0.0, 1.0)
ax.axis('scaled', adjust='box')
fig.tight_layout()

if show_figure:
    pyplot.show()

if save_figure:
    figdir = simudir / 'figures'
    figdir.mkdir(parents=True, exist_ok=True)
    filepath = figdir / 'wz_{:0>7}.png'.format(timestep)
    fig.savefig(filepath, dpi=300, bbox_inches='tight')
