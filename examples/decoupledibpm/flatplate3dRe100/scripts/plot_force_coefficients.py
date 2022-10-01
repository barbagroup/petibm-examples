"""Plot the steady-state force coefficients of an inclined flat-plate.

Reynolds number 100 and the rectangular plate has an aspect ratio of 2.
We compare the results from data reported in Taira et al. (2007).

_References:_

* Taira, K., Dickson, W. B., Colonius,
  T., Dickinson, M. H., & Rowley, C. W. (2007).
  Unsteadiness in flow over a flat plate at angle-of-attack at low Reynolds
  numbers.
  AIAA Paper, 710, 2007.

"""

from matplotlib import pyplot
import numpy
import pathlib

import petibmpy


show_figure = True  # display the Matplotlib figure
save_figure = True  # save the Matplotlib figure as PNG
rootdir = pathlib.Path(__file__).absolute().parents[1]

# Load forces and compute mean values for each angle of inclination.
time_limits = (15.0, 20.0)
angles = numpy.arange(0, 90 + 1, 10, dtype=numpy.int32)
cd, cl = [], []
for angle in angles:
    simudir = rootdir / f'aoa{angle}'
    filepath = simudir / 'output' / 'forces-0.txt'
    t, fx, fy, _ = petibmpy.read_forces(filepath)
    fx_mean, fy_mean = petibmpy.get_time_averaged_values(t, fx, fy,
                                                         limits=time_limits)
    cd.append(fx_mean)
    cl.append(fy_mean)

# Load experimental data from Taira et al. (2007).
datadir = rootdir.parents[2] / 'data'
filepath = datadir / 'taira_et_al_2007_flatplateRe100AR2_cd_exp.dat'
with open(filepath, 'r') as infile:
    cd_taira_exp = numpy.loadtxt(infile, unpack=True)
filepath = datadir / 'taira_et_al_2007_flatplateRe100AR2_cl_exp.dat'
with open(filepath, 'r') as infile:
    cl_taira_exp = numpy.loadtxt(infile, unpack=True)

# Load numerical data from Taira et al. (2007).
filepath = datadir / 'taira_et_al_2007_flatplateRe100AR2_cd_num.dat'
with open(filepath, 'r') as infile:
    cd_taira_num = numpy.loadtxt(infile, delimiter=',', unpack=True)
filepath = datadir / 'taira_et_al_2007_flatplateRe100AR2_cl_num.dat'
with open(filepath, 'r') as infile:
    cl_taira_num = numpy.loadtxt(infile, delimiter=',', unpack=True)

# Plot the force coefficients versus the angle-of-attack and compare with
# experimental results reported in Taira et al. (2007).
pyplot.rc('font', family='serif', size=12)
fig, (ax1, ax2) = pyplot.subplots(nrows=2, figsize=(6.0, 6.0), sharex=True)
ax1.set_ylabel('Drag coefficient')
ax1.scatter(angles, cd, label='PetIBM',
            marker='s', s=40, facecolor='C0', zorder=3)
ax1.scatter(*cd_taira_exp, label='Taira et al. (2007) - exp.',
            marker='o', s=40, facecolor='none', edgecolor='black')
ax1.scatter(*cd_taira_num, label='Taira et al. (2007) - num.',
            marker='o', s=40, facecolor='black')
ax1.set_ylim(0.0, 2.0)
ax1.legend(loc='upper left', frameon=False)
ax2.set_xlabel('Angle of attack (deg)')
ax2.set_ylabel('Lift coefficient')
ax2.scatter(angles, cl, label='PetIBM',
            marker='s', s=40, facecolor='C0', zorder=3)
ax2.scatter(*cl_taira_exp, label='Taira et al. (2007) - exp.',
            marker='o', s=40, facecolor='none', edgecolor='black')
ax2.scatter(*cl_taira_num, label='Taira et al. (2007) - num.',
            marker='o', s=40, facecolor='black')
ax2.set_xlim(0.0, 90.0)
ax2.set_ylim(0.0, 1.5)
fig.tight_layout()

if show_figure:
    pyplot.show()

if save_figure:
    figdir = rootdir / 'figures'
    figdir.mkdir(parents=True, exist_ok=True)
    filepath = figdir / 'force_coefficients.png'
    fig.savefig(filepath, dpi=300, bbox_inches='tight')
