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
clz = numpy.sqrt(cl**2 + cz**2)

# Compute the time-averaged force coefficients.
time_limits = (200.0, 250.0)
cd_mean, clz_mean = petibmpy.get_time_averaged_values(t, cd, clz,
                                                      limits=time_limits)
print('Time-averaged force coefficients:\n')
print(f'* <CD> = {cd_mean:0.4f}')
print(f'* <sqrt(CL^2 + CZ^2)> = {clz_mean:0.4f}')
print(f'\n(Time limits: {time_limits})')


# Plot history of the force coefficients.
pyplot.rc('font', family='serif', size=14)
fig, ax = pyplot.subplots(figsize=(6.0, 4.0))
ax.set_xlabel('Non-dimensional time')
ax.set_ylabel('Force coefficients')
ax.plot(t, cd, label='$C_D$')
ax.plot(t, clz, label='$\sqrt{C_L^2 + C_z^2}$')
ax.legend(frameon=False)
ax.set_xlim(200.0, 250.0)
ax.set_ylim(-0.2, 0.7)
fig.tight_layout()

if save_figure:
    # Save figure as a PNG.
    figdir = simudir / 'figures'
    figdir.mkdir(parents=True, exist_ok=True)
    filepath = figdir / 'force_coefficients.png'
    fig.savefig(filepath, dpi=300, bbox_inches='tight')

if show_figure:
    pyplot.show()
