"""Plot the velocity profiles at 4 cross-sections and 3 phase angles."""

from matplotlib import pyplot
import numpy
import pathlib

import petibmpy

from kinematics import D, Um


display_figure = True  # if True, display the figure(s).
simudir = pathlib.Path(__file__).absolute().parents[1]
rootdir = simudir.parents[3]
datadir = simudir / 'output'

pyplot.rc('font', family='serif', size=12)
nrows, ncols = 3, 2
fig, ax = pyplot.subplots(nrows=nrows, ncols=ncols, figsize=(10.0, 10.0))
phases = [180, 210, 330]  # phase angles (in degrees)
times = [17.5, 17.916, 19.584]  # corresponding time units
x_locs = [-0.6, 0.0, 0.6, 1.2]  # cross-section locations
for row in range(nrows):
    for col in range(ncols):
        name = 'u' if col == 0 else 'v'
        time, phase = times[row], phases[row]
        filepath = datadir / f'probe{phase}-{name}.h5'
        for i, xi in enumerate(x_locs):
            probe = petibmpy.ProbeVolume(name, name)
            (x, y), u = probe.read_hdf5(filepath, time)
            ui = petibmpy.linear_interpolation(u.T, x, xi)
            ax[row, col].plot(ui / Um, y / D, label=f'{xi}')

            # Load and plot experimental data from Dutsch et al. (1998).
            exp_filename = f'{name}_phi={phase}_x={xi}.csv'
            exp_filepath = (rootdir / 'data' / 'dutsch_et_al_1998' /
                            exp_filename)
            with open(exp_filepath, 'r') as f:
                u_exp, y_exp = numpy.loadtxt(f, unpack=True, delimiter=',')
            ax[row, col].plot(u_exp, y_exp, linewidth=0,
                              color=f'C{i}', marker='o',
                              markerfacecolor='none', markersize=4)

        ax[row, col].set_xlabel('$u / U_m$' if col == 0 else '$v / U_m$')
        ax[row, col].set_ylabel('$y / D$')
        ax[row, col].set_xlim(-1.5, 1.5)
        ax[row, col].set_ylim(-1.1, 1.1)
        ax[row, col].text(0.7, 0.8, r'$\phi = {}^o$'.format(phases[row]))
        ax[row, col].spines['right'].set_visible(False)
        ax[row, col].spines['top'].set_visible(False)
ax[0, 1].legend(title='$x/D$', loc='center left',
                prop={'size': 12}, frameon=False)
fig.tight_layout()

# Save the figure.
figdir = simudir / 'figures'
figdir.mkdir(parents=True, exist_ok=True)
filepath = figdir / 'velocity_profiles.png'
fig.savefig(filepath, dpi=300, bbox_inches='tight')

if display_figure:
    pyplot.show()
