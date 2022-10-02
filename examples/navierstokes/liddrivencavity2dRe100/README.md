# 2D lid-driven cavity flow at Re=100

This example solves the flow in a 2D square cavity of unit length with the top wall moving in the positive $x$ direction at speed $1$.
The Reynolds number (based on the kinematic viscosity, the length of the cavity, and the speed of the moving wall) is $100$.
The fluid is initially at rest and the top wall impulsively starts moving.

The computational domain $\left[ 0, 1 \right] \times \left[0, 1 \right]$ is uniformly discretized with $32$ cells in each direction.

We run $1000$ time steps with a time increment of $0.01$ and save the numerical solution at the end.

> :warning:
>
> All commands displayed below assume you are in the directory containing the present README file.

## Run the example

```shell
docker pull barbagroup/petibm:0.5.1-GPU-OpenMPI-xenial
nvidia-docker run --rm -it -v $(pwd):/data barbagroup/petibm:0.5.1-GPU-OpenMPI-xenial /data/run.sh
```

> :information_source:
>
> For reference, the simulation completed 1,000 time steps in a few second using
>
> * 1 MPI process (Intel(R) Core(TM) i7-3770 CPU @ 3.40GHz)
> * 1 NVIDIA K40 GPU device

## Post-processing

Activate your `conda` environment (see [instructions](../../../README.md)):

```shell
conda activate petibm-examples
```

Plot the centerline velocity components and compare with the numerical results from Ghia et al. (1982):

```shell
python scripts/plot_centerline_velocities.py
```

The figure is saved as a PNG file (`centerline_velocities_0001000.png`) in the sub-folder `figures` of the present simulation directory.

<img src="figures/centerline_velocities_0001000.png" alt="velocity_profiles" width="400">

**Figure:** Velocity profiles of the $x$ component along a vertical line at $x=0.5$ (left) and of the $y$ component along an horizontal line at $y=0.5$ and (right).

Plot the contours of the vorticity field:

```shell
python scripts/plot_vorticity.py
```

The figure is saved as a PNG file (`wz_0001000.png`) in the sub-folder `figures` of the present simulation directory.

<img src="figures/wz_0001000.png" alt="wz" width="400"/>

**Figure:** Contours the vorticity ($21$ contours between $-5$ and $+5$).

---

## References

* Ghia, U. K. N. G., Ghia, K. N., & Shin, C. T. (1982). High-Re solutions for incompressible flow using the Navier-Stokes equations and a multigrid method. Journal of computational physics, 48(3), 387-411.
