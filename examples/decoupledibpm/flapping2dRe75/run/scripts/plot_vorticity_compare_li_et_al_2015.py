"""Plot the vorticity at saved time steps."""


from matplotlib import pyplot, image
import numpy
import pathlib

import petibmpy


simudir = pathlib.Path(__file__).absolute().parents[1]  # simulation directory
datadir = simudir / 'output'  # directory with field solution files
name = 'wz'  # name of the variable to load and plot
save_figure = True  # save Matplotlib figure as PNG
show_figure = True  # show Matplotlib figure

# Load the grid from file.
filepath = datadir / 'grid.h5'
grid = petibmpy.read_grid_hdf5(filepath, name)

states = [2400, 2600, 2800, 3000, 3200]
pyplot.rc('font', family='serif', size=14)
fig, (ax1, ax2) = pyplot.subplots(nrows=2, ncols=5, figsize=(10.0, 5.0))
levels = numpy.linspace(-20.0, 20.0, num=40)  # contour levels
for i, state in enumerate(states):
    print(f'[time step {state}] Load and plot contours of {name}')
    # Load data from file.
    filepath = datadir / f'{state:0>7}.h5'
    data = petibmpy.read_field_hdf5(filepath, name)
    # Load body coordinates from file.
    filepath = datadir / f'ellipse_{state:0>7}.2D'
    body = petibmpy.read_body(filepath)
    # Plot the contour of the field variable.
    ax1[i].contour(*grid, data, levels=levels, linewidths=0.5, extend='both')
    ax1[i].plot(*body, color='black', linewidth=0.5)
    ax1[i].axis('scaled', adjustable='box')
    ax1[i].set_xlim(-3.5, 2.5)
    ax1[i].set_ylim(-5.0, 1.0)
    ax1[i].axis('off')

# Add images from Li et al. (2015) to the figure.
datadir = simudir.parent / 'data'
times = [3.0, 3.25, 3.5, 3.75, 4.0]
for i, time in enumerate(times):
    print(f'[time {time}] Display image from Li et al. (2015)')
    filepath = datadir / f'li_et_al_2015_flapping_wz_{time:.2f}.png'
    im = image.imread(str(filepath))
    ax2[i].imshow(im)
    ax2[i].axis('off')

fig.tight_layout()

if save_figure:
    figdir = simudir / 'figures'  # folder to contain PNG files
    figdir.mkdir(parents=True, exist_ok=True)
    filepath = figdir / f'wz_compare_li_et_al_2015.png'
    fig.savefig(filepath, dpi=300, bbox_inches='tight')

if show_figure:
    pyplot.show()
