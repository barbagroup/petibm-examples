"""Plot the vorticity at saved time steps."""


from matplotlib import pyplot
import numpy
import pathlib
import yaml

import petibmpy


simudir = pathlib.Path(__file__).absolute().parents[1]  # simulation directory
datadir = simudir / 'output'  # directory with field solution files
name = 'wz'  # name of the variable to load and plot

# Load the grid from file.
filepath = datadir / 'grid.h5'
grid = petibmpy.read_grid_hdf5(filepath, name)

# Load the time parameters from YAML configuration file.
filepath = simudir / 'config.yaml'
with open(filepath, 'r') as infile:
    config = yaml.load(infile, Loader=yaml.FullLoader)
f = config['bodies'][0]['kinematics']['f']
T = 1 / f  # flapping period
config = config['parameters']
nstart, nt, nsave = config['startStep'], config['nt'], config['nsave']
dt = config['dt']

times = numpy.array([3.0, 3.25, 3.5, 3.75, 4.0])
timesteps = numpy.array(times * T / dt, dtype='int')

pyplot.rc('font', family='serif', size=14)
levels = numpy.linspace(-20.0, 20.0, num=40)  # contour levels
figdir = simudir / 'figures'  # folder to contain PNG files
figdir.mkdir(parents=True, exist_ok=True)
for timestep in timesteps:
    print(f'[time step {timestep}] Load and plot contours of {name}')
    # Load data from file.
    filepath = datadir / f'{timestep:0>7}.h5'
    data = petibmpy.read_field_hdf5(filepath, name)
    # Load body coordinates from file.
    filepath = datadir / f'ellipse_{timestep:0>7}.2D'
    body = petibmpy.read_body(filepath)
    # Plot the contour of the field variable.
    fig, ax = pyplot.subplots(figsize=(6.0, 6.0))
    ax.text(-3.5, 0.5, f't / T = {timestep * dt / T:g}', fontsize=16)
    ax.set_xlabel('x/c')
    ax.set_ylabel('y/c')
    ax.contour(*grid, data, levels=levels, extend='both')
    ax.plot(*body, color='black')
    ax.axis('scaled', adjustable='box')
    ax.set_xlim(-4.0, 3.0)
    ax.set_ylim(-5.0, 1.0)
    ax.get_xaxis().set_visible(False)
    ax.get_yaxis().set_visible(False)
    fig.tight_layout()
    # Save the figure as PNG.
    filepath = figdir / f'wz_{timestep:0>7}.png'
    fig.savefig(filepath, dpi=300, bbox_inches='tight')
    pyplot.close(fig)
