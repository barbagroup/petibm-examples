# Convergence analysis using the example of the decaying Taylor-Green vortices

We consider the example of a two-dimensional array of decaying vortices to report the temporal convergence of the Navier-Stokes solver with and without an immersed body in the domain.

The computational domain is $\left[ 0, 1 \right]^2$.
The Reynolds number (based on the domain length $L$, a characteristic velocity of $U = 1$, and the kinematic viscosity) is set to $Re = 10$ and we advance the solution in time to $t = 0.2$, with time-step size $\Delta t = 10^{-4}$.

All commands displayed in this README assumes you are in the directory containing the present README file.

## Run the simulations

If the binary folder with the executable `petibm-taylorgreen` is already in your search path (as well as `mpiexec`), you can run the simulations with

```shell
./run.sh
```

Otherwise, you can use the command-line options to provide the MPI installation directory and the application directory:

```shell
./run.sh -m "<MPI installation directory>" -p "<Taylor-Green vortices application directory>"
```

## Post-processing

To plot the $L_2$ and $L\infty$ norms of the error in the x-component of the velocity field versus the grid-spacing size:

```shell
export PYTHONPATH=../src/python
python spatial/scripts/plot_spatial_convergence.py
```

The output file `spatial_convergence.png` is saved in the sub-folder `spatial/figures` of the present directory.

To plot the $L_2$ and $L\infty$ norms of the error in the x-component of the velocity field versus the time-step size:

```shell
export PYTHONPATH=../src/python
python temporal/scripts/plot_temporal_convergence.py
```

The output file `temporal_convergence.png` is saved in the sub-folder `temporal/figures` of the present directory.

<img src="spatial/figures/spatial_convergence.png" alt="spatial_convergence" width="600">

**Figure:** Spatial errors in the x-component of the velocity field for the case a two-dimensional array of decaying vortices with and without a boundary immersed ("IB") in the domain.

<img src="temporal/figures/temporal_convergence.png" alt="temporal_convergence" width="600">

**Figure:** Temporal errors in the x-component of the velocity field for the case a two-dimensional array of decaying vortices with and without a boundary immersed ("IB") in the domain.
