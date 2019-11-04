"""Plot the history of the drag coefficient."""

from matplotlib import pyplot
import numpy
import pathlib
from scipy import signal

import petibmpy

from kinematics import Am, D, f, rho, Um, w


show_figure = True  # if True, display the figure(s)

# Load drag force from file.
simudir = pathlib.Path(__file__).absolute().parents[1]
filepath = simudir / 'forces-0.txt'
t, fx, _ = petibmpy.read_forces(filepath)

# Convert drag to drag coefficient.
V = numpy.pi * D**2 / 4  # body volume
ax = w**2 * Am * numpy.sin(w * t)
fx += rho * V * ax
cd = fx / (0.5 * rho * Um**2 * D)

# Plot the history of the drag coefficient.
pyplot.rc('font', family='serif', size=16)
fig, ax = pyplot.subplots(figsize=(8.0, 4.0))
ax.grid()
ax.set_xlabel('$t / T$')
ax.set_ylabel('$C_D$')
ax.plot(f * t, cd)
ax.axis((0.0, 4.0, -6.0, 6.0))
fig.tight_layout()

# Save the figure.
figdir = simudir / 'figures'
figdir.mkdir(parents=True, exist_ok=True)
filepath = figdir / 'drag_coefficient.png'
fig.savefig(filepath, dpi=300)

if show_figure:
    pyplot.show()
