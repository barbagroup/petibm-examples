"""Plot the steady-state drag coefficient on the sphere."""

from matplotlib import pyplot
import numpy
import pathlib

import petibmpy


Re = [50, 100, 150, 200, 250, 300]
show_figure = True  # display the Matplotlib figure
save_figure = True  # save the Matplotlib figure as PNG
rootdir = pathlib.Path(__file__).absolute().parents[1]

rho = 1.0
U_inf = 1.0
R = 0.5
A = numpy.pi * R**2
coeff = 1 / (0.5 * rho * U_inf**2 * A)

cd = []
for Re_ in Re:
    simudir = rootdir / f'Re{Re_}'
    filepath = simudir / 'forces-0.txt'
    _, fx, _, _ = petibmpy.read_forces(filepath)
    cd.append(coeff * fx[-1])

# Load experimental data from Roos & WIllmarth (1971).
datadir = rootdir.parents[2] / 'data'
filepath = datadir / 'roos_willmarth_1971_sphere_dragCoefficient.dat'
with open(filepath, 'r') as infile:
    data = numpy.loadtxt(infile, unpack=True)

# Plot the drag coefficient versus the Reynolds number.
pyplot.rc('font', family='serif', size=14)
fig, ax = pyplot.subplots(figsize=(6.0, 4.0))
ax.set_xlabel('Re')
ax.set_ylabel('$C_D$')
ax.plot(*data, label='Roos & Willmarth (1971)',
        linewidth=0, marker='o', markerfacecolor='none', color='black')
ax.plot(Re, cd, label='PetIBM', linewidth=0, marker='s')
ax.legend(frameon=False)
ax.set_xlim(0.0, 300.0)
ax.set_ylim(0.0, 4.0)
fig.tight_layout()

if save_figure:
    # Save figure as a PNG.
    figdir = pathlib.Path(__file__).absolute().parents[1] / 'figures'
    figdir.mkdir(parents=True, exist_ok=True)
    filepath = figdir / 'drag_coefficient.png'
    fig.savefig(filepath, dpi=300, bbox_inches='tight')

if show_figure:
    pyplot.show()
