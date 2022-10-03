"""Plot the history of the force coefficients."""

from matplotlib import pyplot
import numpy
import pathlib
from scipy import signal

import petibmpy


show_figure = True  # if True, display the figure(s).

maindir = pathlib.Path(__file__).absolute().parents[1]

cases = {
    'Aggregation AMG': {
        'directory': maindir,
        'plt_kwargs': dict(color='C0', linestyle='-')
    },
    'Classical AMG': {
        'directory': maindir.parent / 'cylinder2dRe100',
        'plt_kwargs': dict(color='C1', linestyle='--')
    }
}

for label, cfg in cases.items():
    print(f'[{label}] Processing ...')

    data = {}

    # Load forces from file.
    datadir = cfg['directory'] / 'output'
    filepath = datadir / 'forces-0.txt'
    t, fx, fy = petibmpy.read_forces(filepath)
    data['t'] = t

    # Convert forces to force coefficients.
    rho, U_inf, D = 1.0, 1.0, 1.0
    coeff = 1 / (0.5 * rho * U_inf**2 * D)
    cd, cl = petibmpy.get_force_coefficients(fx, fy, coeff=coeff)
    data['cd'], data['cl'] = cd, cl

    # Get index of the minima of the lift coefficient curve.
    idx_min = signal.argrelextrema(cl, numpy.less_equal, order=10)[0][:-1]

    # Get time limits covering the last N sheddin cycles.
    n_cycles = 10
    idx_min = idx_min[-(n_cycles + 1):]
    time_limits = (t[idx_min[0]], t[idx_min][-1])
    data['time_limits'] = time_limits

    # Compute the time-averaged force coefficients.
    cd_mean, cl_mean = petibmpy.get_time_averaged_values(
        t, cd, cl, limits=time_limits
    )
    data['cd_mean'], data['cl_mean'] = cd_mean, cl_mean

    # Compute the RMS of the lift coefficient.
    cl_window = cl[idx_min[0]:idx_min[-1] + 1]
    rms = numpy.sqrt(numpy.mean(numpy.square(cl_window)))
    data['cl_rms'] = rms

    # Compute the maximum deviation of the lift coefficient from mean value.
    cl_max_dev = max(abs(cl_window - cl_mean))
    data['cl_max_dev'] = rms

    # Compute the Strouhal number
    # (using the averaged valley-to-valley time length).
    t_minima = t[idx_min]
    strouhal = D / U_inf / numpy.mean(t_minima[1:] - t_minima[:-1])
    data['strouhal'] = strouhal

    cases[label]['data'] = data

    print('Time limits:', data['time_limits'])
    print(f"Time length: {time_limits[1] - time_limits[0]}")
    print(f"<C_D> = {data['cd_mean']}")
    print(f"<C_L> = {data['cl_mean']}")
    print(f"rms(C_L) = {data['cl_rms']}")
    print(f"max_dev(C_L) = {data['cl_max_dev']}")
    print(f"St = {data['strouhal']}")

# Plot the history of the force coefficients.
pyplot.rc('font', family='serif', size=14)
fig, ax = pyplot.subplots(figsize=(8.0, 4.0))
ax.set_xlabel('Non-dimensional time')
ax.set_ylabel('Force coefficients')
for label, case in cases.items():
    data = case['data']
    plt_kwargs = case['plt_kwargs']
    ax.plot(data['t'], data['cd'], label=label, **plt_kwargs)
    ax.plot(data['t'], data['cl'], label=None, **plt_kwargs)
ax.annotate('$C_D$', xy=(130.0, 1.3), xytext=(150.0, 1.1),
            arrowprops=dict(arrowstyle='->'))
ax.annotate('$C_L$', xy=(130.0, 0.4), xytext=(150.0, 0.6),
            arrowprops=dict(arrowstyle='->'))
ax.legend(ncol=1, frameon=False, fontsize=14)
ax.set_xlim(0.0, 200.0)
ax.set_ylim(-0.5, 1.5)
ax.spines['right'].set_visible(False)
ax.spines['top'].set_visible(False)
fig.tight_layout()

# Save the figure.
figdir = maindir / 'figures'
figdir.mkdir(parents=True, exist_ok=True)
filepath = figdir / 'force_coefficients_compare_amg.png'
fig.savefig(filepath, dpi=300, bbox_inches='tight')

if show_figure:
    pyplot.show()
