"""Plot the history of the drag coefficient.

Compare with the numerical results reported in Koumoutsakos & Leonard (1995).

_References:_

* Koumoutsakos, P., & Leonard, A. (1995).
  High-resolution simulations of the flow around an impulsively started
  cylinder using vortex methods.
  Journal of Fluid Mechanics, 296, 1-38.

"""

from matplotlib import pyplot
import numpy
import pathlib

import petibmpy


# Set directories and parameters.
simudir = pathlib.Path(__file__).absolute().parents[1]
rootdir = simudir.parents[2]
datadir = rootdir / 'data'
show_figure = True  # display the Matplotlib figure
save_figure = True  # save the Matplotlib figure as PNG

# Load drag force from file and compute drag coefficient.
filepath = simudir / 'output' / 'forces-0.txt'
t, fx, _ = petibmpy.read_forces(filepath)
cd = 2 * fx

# Load drag coefficient from Koumoutsakos & Leonard (1995).
filename = 'koumoutsakos_leonard_1995_cylinder_dragCoefficientRe40.dat'
filepath = datadir / filename
t2, cd2 = petibmpy.read_forces(filepath)
t2 *= 0.5

# Plot the history of the drag coefficient.
pyplot.rc('font', family='serif', size=14)
fig, ax = pyplot.subplots(figsize=(8.0, 4.0))
ax.set_xlabel('Non-dimensional time')
ax.set_ylabel('Drag coefficient')
ax.plot(t, cd, label='PetIBM')
ax.plot(t2, cd2, label='Koumoutsakos & Leonard (1995)',
        marker='o', linewidth=0, color='black')
ax.axis((0.0, 20.0, 0.0, 5.0))
ax.legend(frameon=False)
fig.tight_layout()

if show_figure:
    pyplot.show()

if save_figure:
    figdir = simudir / 'figures'
    figdir.mkdir(parents=True, exist_ok=True)
    filepath = figdir / 'drag_coefficient.png'
    fig.savefig(filepath, dpi=300, bbox_inches='tight')
