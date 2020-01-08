"""Plot the history of the force coefficients."""

from matplotlib import pyplot
import numpy
import pathlib

import petibmpy


simudir = pathlib.Path(__file__).absolute().parents[1]
datadir = simudir / 'output'
show_figure = True  # display the Matplotlib figure
save_figure = True  # save the Matplotlib figure as PNG

rho = 1.0
U_inf = 1.0
R = 0.5
A = numpy.pi * R**2
coeff = 1 / (0.5 * rho * U_inf**2 * A)

# Load forces from file and compute force coefficients.
filepath = datadir / 'forces-0.txt'
t, fx, fy, fz = petibmpy.read_forces(filepath)
cd, cl, cz = petibmpy.get_force_coefficients(fx, fy, fz, coeff=coeff)

# Plot history of the force coefficients.
pyplot.rc('font', family='serif', size=14)
fig, ax = pyplot.subplots(figsize=(6.0, 4.0))
ax.set_xlabel('Non-dimensional time')
ax.set_ylabel('Force coefficient')
ax.plot(t, cd, label='$C_D$')
ax.plot(t, cl, label='$C_L$')
ax.plot(t, cz, label='$C_Z$')
ax.legend(frameon=False)
ax.set_ylim(-0.1, 1.0)
fig.tight_layout()

if save_figure:
    # Save figure as a PNG.
    figdir = simudir / 'figures'
    figdir.mkdir(parents=True, exist_ok=True)
    filepath = figdir / 'force_coefficients.png'
    fig.savefig(filepath, dpi=300, bbox_inches='tight')

if show_figure:
    pyplot.show()
