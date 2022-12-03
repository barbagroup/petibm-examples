"""Plot filled contours of the velocity and pressure fields."""

import argparse
from matplotlib import pyplot
import numpy
import pathlib

import petibmpy

import rodney


args = rodney.parse_command_line()
timestep, dt = 160, 1.25e-3  # time-step index and time-step size
time = timestep * dt  # time value
nu = 0.1  # coefficient of viscosity

# Change default font size and family for Matplotlib figures.
pyplot.rc('font', family='serif', size=14)

# If path to file with immersed body is provided, load coordinates.
body = None
if args.body_path is not None:
    body = petibmpy.read_body(args.body_path, skiprows=1)

# Load x-velocity, compute reference solution, and plot side by side.
grid_u, u = rodney.petibm_load_grid_and_field(args.data_dir, timestep, 'u')
u_ref, _, _ = rodney.taylor_green_vortex(*grid_u, time, nu)
levels = numpy.linspace(-0.5, 0.5, num=21)
fig, ax = rodney.plot_contourf_field(grid_u, u, 'u', ref=u_ref, body=body,
                                     levels=levels, figsize=(8.0, 4.0))

# Load y-velocity, compute reference solution, and plot side by side.
grid_v, v = rodney.petibm_load_grid_and_field(args.data_dir, timestep, 'v')
_, v_ref, _ = rodney.taylor_green_vortex(*grid_v, time, nu)
levels = numpy.linspace(-0.5, 0.5, num=21)
fig, ax = rodney.plot_contourf_field(grid_v, v, 'v', ref=v_ref, body=body,
                                     levels=levels, figsize=(8.0, 4.0))

# Load pressure, compute reference solution, and plot side by side.
grid_p, p = rodney.petibm_load_grid_and_field(args.data_dir, timestep, 'p')
_, _, p_ref = rodney.taylor_green_vortex(*grid_p, time, nu)
levels = numpy.linspace(-0.5, 0.5, num=21)
fig, ax = rodney.plot_contourf_field(grid_p, p, 'p', ref=p_ref, body=body,
                                     levels=levels, figsize=(8.0, 4.0))

if args.show_figures:
    pyplot.show()
