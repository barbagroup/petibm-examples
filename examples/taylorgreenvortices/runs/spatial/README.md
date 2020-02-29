# Spatial convergence analysis using the example of the Taylor-Green vortices

We consider the example of a two-dimensional array of decaying vortices to report the temporal convergence of the Navier-Stokes solver with and without an immersed body in the domain.

The computational domain is $\left[ 0, 1 \right]^2$.
The Reynolds number (based on the domain length $L$, a characteristic velocity of $U = 1$, and the kinematic viscosity) is set to $Re = 10$ and we advance the solution in time to $t = 0.2$, with time-step size $\Delta t = 10^{-4}$.

The solution is computed on $4$ uniform grids with sizes $20^2$, $60^2$, $180^2$, and $540^2$.
We run simulations with and without an immersed body to assess the temporal convergence of the Navier-Stokes solver and the decoupled IBPM.
For cases with an body, we use a cylinder with radius $R = 0.25 L$, centered at $\left( 0.5, 0.5 \right)$, discretized with a similar resolution as the background grid ($\Delta s \approx \Delta x$).

The velocity system is solved on CPU with a stabilized bi-conjugate gradient method with a diagonal preconditioner.
The Poisson system is solved on a GPU device with a conjugate-gradient method and a classical algebraic multigrid technique for the preconditioner.
Each time step, we consider the iterative solvers to have converged when the absolute size of the residual norm is lower than $10^{-12}$.
(When the immersed body is present, the system for the Lagrangian forces is solved with a direct solver.)

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
export PYTHONPATH=../../src/python
python scripts/plot_spatial_convergence.py
```

The output file `spatial_convergence.png` is saved in the sub-folder `figures` of the present directory.

<img src="figures/spatial_convergence.png" alt="spatial_convergence" width="600">

**Figure:** Spatial errors in the x-component of the velocity field for the case a two-dimensional array of decaying vortices with and without a boundary immersed ("IB") in the domain.
