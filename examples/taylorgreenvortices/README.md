# Convergence analysis using the example of the 2D decaying Taylor-Green vortices

We consider the example of a two-dimensional array of decaying vortices to report the temporal convergence of the Navier-Stokes solver with and without an immersed body in the domain.

The computational domain is $\left[ 0, 1 \right]^2$.
The Reynolds number (based on the domain length $L$, a characteristic velocity of $U = 1$, and the kinematic viscosity) is set to $Re = 10$ and we advance the solution in time to $t = 0.2$, with time-step size $\Delta t = 10^{-4}$.

All commands displayed below assume you are in the directory containing the present README file.

## Run the simulations

```shell
docker pull barbagroup/petibm:0.5.1-GPU-OpenMPI-xenial

nvidia-docker create --name=tgv10 -v $(pwd):/data -v $(pwd)/../../cmake-modules:/tmp/cmake-modules barbagroup/petibm:0.5.1-GPU-OpenMPI-xenial

nvidia-docker start tgv10
nvidia-docker exec tgv10 /data/build.sh
nvidia-docker exec tgv10 /data/run.sh
nvidia-docker stop tgv10

nvidia-docker rm tgv10
```

## Post-processing

Activate your `conda` environment (see [instructions](../../README.md)):

```shell
conda activate petibm-examples
```

To plot the $L_2$ and $L\infty$ norms of the error in the x-component of the velocity field versus the grid-spacing size:

```shell
export PYTHONPATH=src/python
python runs/spatial/scripts/plot_spatial_convergence.py
```

The output file `spatial_convergence.png` is saved in the sub-folder `runs/spatial/figures` of the present directory.

To plot the $L_2$ and $L\infty$ norms of the error in the x-component of the velocity field versus the time-step size:

```shell
export PYTHONPATH=src/python
python runs/temporal/scripts/plot_temporal_convergence.py
```

The output file `temporal_convergence.png` is saved in the sub-folder `runs/temporal/figures` of the present directory.

<img src="runs/spatial/figures/spatial_convergence.png" alt="spatial_convergence" width="600">

**Figure:** Spatial errors in the x-component of the velocity field for the case a two-dimensional array of decaying vortices with ("IB") and without ("NS") an immersed boundary.

<img src="runs/temporal/figures/temporal_convergence.png" alt="temporal_convergence" width="600">

**Figure:** Temporal errors in the x-component of the velocity field for the case a two-dimensional array of decaying vortices with ("IB") and without ("NS") an immersed boundary.
