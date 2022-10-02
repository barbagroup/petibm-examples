"""Plot the contours of the vorticity field at the final time step."""

from matplotlib import pyplot
import numpy
import pathlib

import petibmpy


# Set parameters and directory.
show_figure = True  # display the Matplotlib figure
save_figure = True  # save the Matplotlib figure as PNG
simudir = pathlib.Path(__file__).absolute().parents[1]
datadir = simudir / 'output'

# Load vorticity grid and field at final time step.
name = 'wz'
filepath = datadir / 'grid.h5'
x, y = petibmpy.read_grid_hdf5(filepath, name)
timestep = 2000
filepath = datadir / f'{timestep:0>7}.h5'
wz = petibmpy.read_field_hdf5(filepath, name)

# Load coordinates of the immersed boundary.
filepath = simudir / 'circle.body'
xb, yb = petibmpy.read_body(filepath, skiprows=1)

# Plot the contours of the vorticity field.
pyplot.rc('font', family='serif', size=14)
fig, ax = pyplot.subplots(figsize=(6.0, 6.0))
ax.set_xlabel('x')
ax.set_ylabel('y')
levels = numpy.linspace(-3.0, 3.0, 16)
ax.contour(x, y, wz, levels=levels, colors='black')
ax.plot(xb, yb, color='red')
ax.set_xlim(-1.0, 4.0)
ax.set_ylim(-2.0, 2.0)
ax.set_aspect('equal')
fig.tight_layout()

if show_figure:
    pyplot.show()

if save_figure:
    figdir = simudir / 'figures'
    figdir.mkdir(parents=True, exist_ok=True)
    filepath = figdir / f'{name}_{timestep:0>7}.png'
    fig.savefig(filepath, dpi=300, bbox_inches='tight')
