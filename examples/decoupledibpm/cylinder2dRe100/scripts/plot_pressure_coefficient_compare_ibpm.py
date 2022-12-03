"""Plot the surface pressure coefficient from last probe record."""

import numpy
import pathlib
from matplotlib import pyplot

import petibmpy


name = 'p'  # name of the field variable to load
time = 200.0  # final probe record
show_figure = True  # if True, display the figure
maindir = pathlib.Path(__file__).absolute().parents[1]

cases = {
    'Decoupled IBPM': {
        'directory': maindir,
        'plt_kwargs': dict(color='C0', linestyle='-')
    },
    'IBPM': {
        'directory': maindir.parents[1] / 'ibpm' / 'cylinder2dRe100',
        'plt_kwargs': dict(color='C1', linestyle='--')
    }
}

for label, cfg in cases.items():
    print(f'[{label}] Processing ...')

    # Load data from last record of the probe.
    datadir = cfg['directory'] / 'output'
    filepath = datadir / 'probe-p.h5'
    probe = petibmpy.ProbeVolume(name, name)
    (x, y), p = probe.read_hdf5(filepath, time)

    # Define circle outside support region of delta function.
    dx = 1.5 / 90  # grid-spacing in the uniform region
    R = 0.5 + 3 * dx  # radius 3 cells away from real boundary
    nb = 100
    theta = numpy.linspace(0.0, 2 * numpy.pi, num=nb + 1)[:-1]
    xc, yc = 0.0, 0.0
    xb, yb = xc + R * numpy.cos(theta), yc + R * numpy.sin(theta)

    # Interpolate the field on extended boundary.
    pb = numpy.empty_like(xb)
    for i, (xbi, ybi) in enumerate(zip(xb, yb)):
        pi = petibmpy.linear_interpolation(p, y, ybi)
        pb[i] = petibmpy.linear_interpolation(pi, x, xbi)

    # Compute the pressure coefficient.
    rho = 1.0  # fluid density
    U_inf = 1.0  # freestream speed
    p_inf = 0.0  # far-away pressure
    cp = (pb - p_inf) / (0.5 * rho * U_inf**2)

    # Re-arrange values to split apart lower and upper surfaces.
    cp_lower = numpy.append(cp[nb // 2:], [cp[-1]])
    theta_lower = numpy.linspace(0.0, 180.0, num=cp_lower.size)
    cp_upper = cp[:nb // 2 + 1][::-1]
    theta_upper = numpy.linspace(0.0, 180.0, num=cp_upper.size)

    data = {}
    data['theta_lower'], data['cp_lower'] = theta_lower, cp_lower
    data['theta_upper'], data['cp_upper'] = theta_upper, cp_upper

    cases[label]['data'] = data

# Load digitized values from Li et al. (2016).
rootdir = pathlib.Path(__file__).absolute().parents[4]
filepath = rootdir / 'data' / 'li_et_al_2016_cylinder2dRe100_cp.csv'
with open(filepath, 'r') as infile:
    theta_li, cp_li = numpy.loadtxt(infile, delimiter=',', unpack=True)

# Plot the distribution of the surface pressure coefficient.
pyplot.rc('font', family='serif', size=16)
fig, ax = pyplot.subplots(figsize=(6.0, 4.0))
ax.set_xlabel(r'$\theta$')
ax.set_ylabel('$C_p$')
for label, case in cases.items():
    data = case['data']
    plt_kwargs = case['plt_kwargs']
    ax.plot(data['theta_upper'], data['cp_upper'], label=label, **plt_kwargs)
ax.plot(theta_li, cp_li, label='Li et al. (2016)',
        color='black', linestyle='-', linewidth=0.75)
ax.legend(frameon=False, fontsize=12)
ax.set_xlim(0.0, 180.0)
ax.set_ylim(-1.5, 1.5)
ax.spines['right'].set_visible(False)
ax.spines['top'].set_visible(False)
fig.tight_layout()

# Save the figure.
figdir = maindir / 'figures'
figdir.mkdir(parents=True, exist_ok=True)
filepath = figdir / 'pressure_coefficient_compare_ibpm.png'
fig.savefig(filepath, dpi=300, bbox_inches='tight')

if show_figure:
    pyplot.show()
