"""Plot the history of the force coefficients."""

from matplotlib import pyplot
import numpy
import pathlib
from scipy import signal

import petibmpy


show_figure = True  # if True, display the figure(s).

# Load forces from file.
simudir = pathlib.Path(__file__).absolute().parents[1]
datadir = simudir / 'output'
filepath = datadir / 'forces-0.txt'
t, fx, fy = petibmpy.read_forces(filepath)

# Convert forces to force coefficients.
rho, U_inf, D = 1.0, 1.0, 1.0
coeff = 1 / (0.5 * rho * U_inf**2 * D)
cd, cl = petibmpy.get_force_coefficients(fx, fy, coeff=coeff)

# Get index of the minima of the lift coefficient curve.
idx_min = signal.argrelextrema(cl, numpy.less_equal, order=10)[0][:-1]

# Get time limits covering the last N sheddin cycles.
n_cycles = 10
idx_min = idx_min[-(n_cycles + 1):]
time_limits = (t[idx_min[0]], t[idx_min][-1])

# Compute the time-averaged force coefficients.
cd_mean, cl_mean = petibmpy.get_time_averaged_values(
    t, cd, cl, limits=time_limits
)

# Compute the RMS of the lift coefficient.
cl_window = cl[idx_min[0]:idx_min[-1] + 1]
cl_rms = numpy.sqrt(numpy.mean(numpy.square(cl_window)))

# Compute the maximum deviation of the lift coefficient from mean value.
cl_max_dev = max(abs(cl_window - cl_mean))

# Compute the Strouhal number
# (using the averaged valley-to-valley time length).
t_minima = t[idx_min]
strouhal = D / U_inf / numpy.mean(t_minima[1:] - t_minima[:-1])

print('Time limits:', time_limits)
print(f"Time length: {time_limits[1] - time_limits[0]}")
print(f"<C_D> = {cd_mean}")
print(f"<C_L> = {cl_mean}")
print(f"rms(C_L) = {cl_rms}")
print(f"max_dev(C_L) = {cl_max_dev}")
print(f"St = {strouhal}")

# Plot the history of the force coefficients.
pyplot.rc('font', family='serif', size=14)
fig, ax = pyplot.subplots(figsize=(8.0, 4.0))
ax.set_xlabel('Non-dimensional time')
ax.set_ylabel('Force coefficients')
ax.plot(t, cd, label='$C_D$')
ax.plot(t, cl, label='$C_L$')
ax.legend(ncol=2, frameon=False, fontsize=14)
ax.set_xlim(0.0, 200.0)
ax.set_ylim(-0.5, 1.5)
fig.tight_layout()

# Save the figure.
figdir = simudir / 'figures'
figdir.mkdir(parents=True, exist_ok=True)
filepath = figdir / 'force_coefficients.png'
fig.savefig(filepath, dpi=300, bbox_inches='tight')

if show_figure:
    pyplot.show()
