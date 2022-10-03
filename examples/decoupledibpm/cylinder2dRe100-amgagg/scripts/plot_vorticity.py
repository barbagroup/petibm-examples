"""Plot the contours of the vorticity field at final time step."""

from matplotlib import pyplot
import numpy
import pathlib

import petibmpy


name = 'wz'  # name of the vorticity variable
timestep = 20000  # final time-step index
show_figure = True  # if True, display the figure

# Set the simulation and data directories.
simudir = pathlib.Path(__file__).absolute().parents[1]
datadir = simudir / 'output'

# Load the gridlines from file.
filepath = datadir / 'grid.h5'
x, y = petibmpy.read_grid_hdf5(filepath, name)
# Load the vorticity field from file.
filepath = datadir / f'{timestep:0>7}.h5'
wz = petibmpy.read_field_hdf5(filepath, name)
# Load the boundary coordinates from file.
filepath = simudir / 'cylinder.body'
xb, yb = petibmpy.read_body(filepath, skiprows=1)

# Plot the contours of the vorticity field.
pyplot.rc('font', family='serif', size=16)
fig, ax = pyplot.subplots(figsize=(6.0, 6.0))
ax.set_xlabel('x / D')
ax.set_ylabel('y / D')
levels = numpy.arange(-3.0, 3.0 + 0.4 / 2, 0.4)
ax.contour(x, y, wz, levels=levels, colors='black')
ax.plot(xb, yb, color='red')
ax.axis('scaled', adjustable='box')
ax.set_xlim(-1.0, 5.0)
ax.set_ylim(-2.0, 2.0)
fig.tight_layout()

# Save the figure.
figdir = simudir / 'figures'
figdir.mkdir(parents=True, exist_ok=True)
filepath = figdir / f'{name}_{timestep:0>7}.png'
fig.savefig(filepath, dpi=300, bbox_inches='tight')

if show_figure:
    pyplot.show()
