"""Plot the steady-state drag coefficient on the sphere."""

from matplotlib import pyplot
import numpy
import pathlib

import petibmpy


def clift_correlation(Re_vals):
    """Compute the Re/Cd correlation from Clift et al. (1978)."""
    cd_vals = numpy.empty_like(Re_vals)
    for i, Re in enumerate(Re_vals):
        w = numpy.log10(Re)
        if 0.01 <= Re <= 20:
            cd = 24 / Re * (1 + 0.1315 * Re**(0.82 - 0.05 * w))
        elif 20 <= Re <= 260:
            cd = 24 / Re * (1 + 0.1935 * Re**0.6305)
        elif 260 <= Re <= 1500:
            cd = 10**(1.6435 - 1.1242 * w + 0.1558 * w**2)
        else:
            cd = None
        cd_vals[i] = cd
    return cd_vals


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

# Compute correlation equation from Clift et al. (1978).
Re_clift = numpy.arange(10.0, 300.0 + 0.5, 1.0)
cd_clift = clift_correlation(Re_clift)

# Plot the drag coefficient versus the Reynolds number.
pyplot.rc('font', family='serif', size=14)
fig, ax = pyplot.subplots(figsize=(6.0, 4.0))
ax.set_xlabel('Re')
ax.set_ylabel('$C_D$')
ax.plot(Re_clift, cd_clift, label='Clift et al. (1978)', color='C3')
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
