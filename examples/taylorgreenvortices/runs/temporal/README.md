# Temporal convergence analysis using the example of the Taylor-Green vortices

We consider the example of a two-dimensional array of decaying vortices to report the temporal convergence of the Navier-Stokes solver.

The computational domain ($\left[ 0, 2 \pi \right]^2$) contains $540 \times 540$ cells.
The Reynolds number (based on the domain length $L$, a characteristic velocity of $U = 1$, and the kinematic viscosity) is set to $Re = 10$ and we advance the solution in time to $t = 0.2$.

The solution is computed on $4$ time grids with $\Delta t = 0.01$, $0.005$, $0.0025$, and $0.00125$ and compared in the $L_2$ and $L_\infty$ norms with a reference solution obtained with a smaller time-step size $\Delta t = 10^{-4}$.

The velocity system is solved on CPU with a stabilized bi-conjugate gradient method with a diagonal preconditioner.
The Poisson system is solved on a GPU device with a conjugate-gradient method and a classical algebraic multigrid technique for the preconditioner.
Each time step, we consider the iterative solvers to have converged when the absolute size of the residual norm is lower than $10^{-14}$.

## Post-processing

To plot the $L_2$ and $L\infty$ norms of the error in the x-component of the velocity field versus the time-step size:

```shell
export PYTHONPATH=../../src/python
python scripts/plot_temporal_convergence.py
```

The output file `temporal_convergence.png` is saved in the sub-folder `figures` of the present directory.

<img src="figures/temporal_convergence.png" alt="temporal_convergence" width="600">

**Figure:** Temporal errors in the x-component of the velocity field for the case a two-dimensional array of decaying vortices.
