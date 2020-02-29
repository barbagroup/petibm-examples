"""Plot the spatial convergence of the x-component of the velocity field."""

from matplotlib import pyplot
import numpy
import pathlib

import petibmpy

import rodney


args = rodney.parse_command_line()
maindir = pathlib.Path(__file__).absolute().parents[1]

# Set parameters.
timestep, dt = 2000, 1e-4  # time-step index and time-step size
time = timestep * dt  # time value
L, nu = 1.0, 0.1  # length of the domain and coefficient of viscosity

# Grid sizes to consider (set a number of cells in one direction).
nx_values = (20, 60, 180, 540)
dx_values = L / numpy.array(nx_values)  # grid-spacing sizes

# Compute the L2 and Linf errors of the x-velocity for all grids
# for the simulation with and without the immersed body.
errors = {}
for label in ('ns', 'ib'):  # 'ns' for Navier-Stokes, 'ib' for decoupled IBPM
    l2_errors, linf_errors = [], []
    for n in nx_values:
        outname = 'output' + (label == 'ib') * '-with-ib'
        datadir = maindir / f'{n}x{n}' / outname
        grid, sol = rodney.petibm_load_grid_and_field(datadir, timestep, 'u')
        ref, _, _ = rodney.taylor_green_vortex(*grid, time, nu)
        l2_errors.append(rodney.l2_norm(sol - ref))
        linf_errors.append(rodney.linf_norm(sol - ref))
    errors[label] = dict(l2=l2_errors, linf=linf_errors)

# Plot the errors versus the grid-spacing size.
# Only considering x-velocity due to symmetry of the problem.
pyplot.rc('font', family='serif', size=14)
fig, ax = pyplot.subplots(figsize=(6.0, 6.0))
ax.set_xlabel(r'$\Delta x$')
ax.set_ylabel('Spatial error (u)')
ax.loglog(dx_values, errors['ns']['l2'], label='$L_2$-norm',
          color='C0', marker='x')
ax.loglog(dx_values, errors['ns']['linf'], label=r'$L_\infty$-norm',
          color='C0', marker='s')
ax.loglog(dx_values, errors['ib']['l2'], label='$L_2$-norm (IB)',
          color='black', linestyle=':', marker='x')
ax.loglog(dx_values, errors['ib']['linf'], label=r'$L_\infty$-norm (IB)',
          color='black', linestyle=':', marker='s')
# Add guide for second-order convergence.
markers = numpy.array([5e-4, 1e-1])
second = 1e-4 * (markers / markers[-1])**2
ax.loglog(markers, second, label=r'$2^{nd}$-order',
          color='black', linestyle='--')
ax.legend(frameon=False)
ax.set_xlim(markers)
for loc in ('right', 'top'):
    ax.spines[loc].set_visible(False)
fig.tight_layout()

if args.save_figures:
    # Save figure as a PNG file.
    figdir = maindir / 'figures'
    figdir.mkdir(parents=True, exist_ok=True)
    filepath = figdir / 'spatial_convergence.png'
    fig.savefig(filepath, dpi=300, bbox_inches='tight')

if args.show_figures:
    pyplot.show()
