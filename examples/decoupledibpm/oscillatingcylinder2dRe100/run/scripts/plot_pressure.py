"""Plot the pressure at phase 0 and 288 degrees."""

from matplotlib import pyplot
import numpy
import pathlib

import petibmpy


show_figure = True  # if True, display the figure(s)
simudir = pathlib.Path(__file__).absolute().parents[1]
datadir = simudir / 'solution'

# Load the grid from file.
name = 'p'  # name of the pressure variable
filepath = simudir / 'grid.h5'
x, y = petibmpy.read_grid_hdf5(filepath, name)

# Load the pressure at phase angles 0 deg during the last period.
timestep = 7500
filepath = datadir / '{:0>7}.h5'.format(timestep)
p1 = petibmpy.read_field_hdf5(filepath, name)
# Load the body coordinates at the same time.
filepath = datadir / 'circle_{:0>7}.2D'.format(timestep)
body1 = petibmpy.read_body(filepath)

# Load the pressure at phase angles 288 deg during the last period.
timestep = 9500
filepath = datadir / '{:0>7}.h5'.format(timestep)
p2 = petibmpy.read_field_hdf5(filepath, name)
# Load the body coordinates at the same time.
filepath = datadir / 'circle_{:0>7}.2D'.format(timestep)
body2 = petibmpy.read_body(filepath)

# Plot the contours of the pressure at the two time steps.
pyplot.rc('font', family='serif', size=16)
fig, (ax1, ax2) = pyplot.subplots(ncols=2, figsize=(8.0, 4.0))
levels = numpy.linspace(-1.0, 1.0, num=50)
ax1.set_xlabel('x')
ax1.set_ylabel('y')
ax1.contour(x, y, p1, levels=levels, colors='black', linewidths=0.75)
ax1.plot(*body1, color='red')
ax1.axis('scaled', adjustable='box')
ax1.set_xlim(-1.0, 1.5)
ax1.set_ylim(-1.2, 1.2)
ax2.set_xlabel('x')
ax2.set_ylabel('y')
ax2.contour(x, y, p2, levels=levels, colors='black', linewidths=0.75)
ax2.plot(*body2, color='red')
ax2.axis('scaled', adjustable='box')
ax2.set_xlim(-1.0, 1.5)
ax2.set_ylim(-1.2, 1.2)
fig.tight_layout()

# Save the figure.
figdir = simudir / 'figures'
figdir.mkdir(parents=True, exist_ok=True)
filepath = figdir / 'pressure.png'
fig.savefig(filepath, dpi=300, bbox_inches='tight')

if show_figure:
    pyplot.show()
