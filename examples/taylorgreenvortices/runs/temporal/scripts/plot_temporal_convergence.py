"""Plot the temporal convergence of the x-component of the velocity field."""

from matplotlib import pyplot
import numpy
import pathlib

import rodney


args = rodney.parse_command_line()
maindir = pathlib.Path(__file__).absolute().parents[1]

# Set parameters.
time = 0.2  # time
L = 2 * numpy.pi  # domain length
nu = 0.01  # coefficient of viscosity

# Reference solution at t=0.2
datadir = maindir / 'dt=0.0001' / 'output'
_, ref = rodney.petibm_load_grid_and_field(datadir, 2000, 'u')

# Time-step sizes to consider.
dt_values = (1e-2, 5e-3, 2.5e-3, 1.25e-3)

# Compute the L2 and Linf errors of the x-velocity for all grids
# for the simulation with and without the immersed body.
errors = {}
for label in ('ns',):  # 'ns' for Navier-Stokes, 'ib' for decoupled IBPM
    l2_errors, linf_errors = [], []
    for dt in dt_values:
        outname = 'output' + (label == 'ib') * '-with-ib'
        datadir = maindir / f'dt={dt}' / outname
        timestep = int(time / dt)
        grid, sol = rodney.petibm_load_grid_and_field(datadir, timestep, 'u')
        l2_errors.append(rodney.l2_norm(sol - ref))
        linf_errors.append(rodney.linf_norm(sol - ref))
    errors[label] = dict(l2=l2_errors, linf=linf_errors)

# Plot the errors versus the grid-spacing size.
# Only considering x-velocity due to symmetry of the problem.
pyplot.rc('font', family='serif', size=14)
fig, ax = pyplot.subplots(figsize=(4.0, 6.0))
ax.set_xlabel('Time-step size ($\Delta t$)')
ax.set_ylabel('Temporal error (u)')
ax.loglog(dt_values, errors['ns']['l2'], label='$L_2$ (NS)',
          color='C0', marker='o')
ax.loglog(dt_values, errors['ns']['linf'], label='$L_\infty$ (NS)',
          color='C0', marker='s')
# Add guide for second-order convergence.
markers = numpy.array([5e-4, 2e-2])
second = 1e-8 * (markers / markers[-1])**2
ax.loglog(markers, second, label='$2^{nd}$-order',
          color='gray', linestyle='-')
ax.legend(frameon=False, loc='upper right', fontsize=12)
ax.set_xlim(markers[::-1])
ax.set_ylim(1e-11, 1e-7)
for loc in ('right', 'top'):
    ax.spines[loc].set_visible(False)
fig.tight_layout()

if args.save_figures:
    # Save figure as a PNG file.
    figdir = maindir / 'figures'
    figdir.mkdir(parents=True, exist_ok=True)
    filepath = figdir / 'temporal_convergence.png'
    fig.savefig(filepath, dpi=300, bbox_inches='tight')

if args.show_figures:
    pyplot.show()
