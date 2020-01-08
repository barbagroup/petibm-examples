"""Plot the history of the force coefficients.

Compared results with numerical data reported in Li et al. (2015).

*References:*

* Li, C., Dong, H., & Liu, G. (2015).
  Effects of a dynamic trailing-edge flap on the aerodynamic performance
  and flow structures in hovering flight.
  Journal of Fluids and Structures, 58, 49-65.

"""

from matplotlib import pyplot
import pathlib

import flapping


save_figure = True  # save Matplotlib figure as PNG
show_figure = True  # display Matplotlib figure
data = {}

# Load the force from the present simulation and get force coefficients.
key = 'PetIBM'
simudir = pathlib.Path(__file__).absolute().parents[1]
datadir = simudir / 'output'
filepath = datadir / 'forces-0.txt'
bodypath = simudir / 'ellipse.body'
data[key] = flapping.get_CD_CL('petibm', filepath, bodypath)
data[key]['kwargs'] = {'color': 'C0', 'linestyle': '-', 'linewidth': 1,
                       'zorder': 4}

# Load numerical data from Li et al. (2015).
key = 'Li et al. (2015)'
data[key] = flapping.get_CD_CL(key)
data[key]['kwargs'] = {'color': 'C1', 'linestyle': '-', 'linewidth': 1,
                       'zorder': 3}

# Load experimental data from Wang et al. (2004).
# Data were digitized Li and co-workers from Wang et al. (2004).
key = 'Wang et al. (2004)'
data[key] = flapping.get_CD_CL(key)
data[key]['kwargs'] = {'marker': 'o', 'color': 'black',
                       'markerfacecolor': 'none', 'markersize': 4,
                       'linewidth': 0,
                       'zorder': 2}

# Load numerical data from Eldredge (2007).
# Data were digitized Li and co-workers from Eldredge (2007).
key = 'Eldredge (2007)'
data[key] = flapping.get_CD_CL(key)
data[key]['kwargs'] = {'color': 'black', 'linestyle': '--', 'linewidth': 1,
                       'zorder': 1}

# Plot the lift and drag coefficients.
pyplot.rc('font', family='serif', size=12)
fig, (ax1, ax2) = pyplot.subplots(nrows=2, figsize=(8.0, 6.0), sharex=True)
ax1.set_ylabel('$C_L$')
for label, subdata in data.items():
    ax1.plot(*subdata['CL'], label=label, **subdata['kwargs'])
ax1.set_ylim(-1.0, 2.0)
ax1.legend(ncol=4, frameon=False, prop={'size': 10})
ax2.set_xlabel('$t / T$')
ax2.set_ylabel('$C_D$')
for label, subdata in data.items():
    ax2.plot(*subdata['CD'], label=label, **subdata['kwargs'])
ax2.set_xlim(0.0, 4.0)
ax2.set_ylim(-1.5, 2.0)
fig.tight_layout()

if save_figure:
    # Save the Matplotlib figure as a PNG.
    figdir = simudir / 'figures'
    figdir.mkdir(parents=True, exist_ok=True)
    filepath = figdir / 'force_coefficients.png'
    fig.savefig(filepath, dpi=300, bbox_inches='tight')

if show_figure:
    pyplot.show()
