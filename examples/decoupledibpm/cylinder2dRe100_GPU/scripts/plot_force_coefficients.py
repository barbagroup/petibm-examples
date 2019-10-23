"""Plot the history of the force coefficients."""

import math
from matplotlib import pyplot
import numpy
import pathlib
import scipy
from scipy import fftpack, signal

import petibmpy


show_figure = True  # if True, display the figure(s).

# Load forces from file.
simudir = pathlib.Path(__file__).absolute().parents[1]
filepath = simudir / 'forces-0.txt'
t, fx, fy = petibmpy.read_forces(filepath)

# Convert forces to force coefficients.
rho, U_inf, D = 1.0, 1.0, 1.0
coeff = 1 / (0.5 * rho * U_inf**2 * D)
cd, cl = petibmpy.get_force_coefficients(fx, fy, coeff=coeff)

# Define time interval used to compute stats.
time_limits = (150.0, 200.0)
print('Initial time interval: {}'.format(time_limits))
mask = numpy.where((t >= time_limits[0]) & (t <= time_limits[1]))[0]

# Compute the minima and maxima of the lift coefficient.
idx_min = signal.argrelextrema(cl, numpy.less_equal, order=5)[0][:-1]
idx_min = numpy.intersect1d(idx_min, mask, assume_unique=True)
print('min(CL) = {}'.format(cl[idx_min]))
idx_max = signal.argrelextrema(cl, numpy.greater_equal, order=5)[0][:-1]
idx_max = numpy.intersect1d(idx_max, mask, assume_unique=True)
print('max(CL) = {}'.format(cl[idx_max]))

# Redefine time interval between first minima and last maxima.
time_limits = (t[idx_min[0]], t[idx_max[-1]])
print('Time interval: {}'.format(time_limits))

# Compute the time-averaged force coefficients.
cd_mean, cl_mean = petibmpy.get_time_averaged_values(t, cd, cl,
                                                     limits=time_limits)
print('<CD> = {:.4f}'.format(cd_mean))
print('<CL> = {:.4f}'.format(cl_mean))

# Compute the RMS of the lift coefficient.
cl2 = cl[idx_min[0]:idx_max[-1] + 1]
rms = numpy.sqrt(numpy.mean(numpy.square(cl2)))
print('rms(CL) = {:.4f}'.format(rms))

# Compute the Strouhal number.
dt = t[1] - t[0]
fft = scipy.fft(cl2)
freqs = fftpack.fftfreq(len(cl2), dt)
idx = numpy.argmax(abs(fft))
strouhal = freqs[idx]
print('St = {:.4}'.format(strouhal))

# Plot the history of the force coefficients.
pyplot.rc('font', family='serif', size=16)
fig, ax = pyplot.subplots(figsize=(8.0, 4.0))
ax.set_xlabel('Non-dimensional time')
ax.set_ylabel('Force coefficients')
ax.grid()
ax.plot(t, cd, label='$C_D$')
ax.plot(t, cl, label='$C_L$')
ax.axvline(t[idx_min[0]], color='grey', linestyle='--')
ax.axvline(t[idx_max[-1]], color='grey', linestyle='--')
ax.axhline(cl[idx_min[-1]], color='grey', linestyle='--')
ax.axhline(cl[idx_max[-1]], color='grey', linestyle='--')
ax.scatter(t[idx_min], cl[idx_min], c='C3')
ax.scatter(t[idx_max], cl[idx_max], c='C3')
ax.legend(ncol=2)
ax.set_xlim(t[0], t[-1])
ax.set_ylim(-0.5, 1.5)
fig.tight_layout()

# Save the figure.
figdir = simudir / 'figures'
figdir.mkdir(parents=True, exist_ok=True)
filepath = figdir / 'force_coefficients.png'
fig.savefig(filepath, dpi=300, bbox_inches='tight')

if show_figure:
    pyplot.show()
