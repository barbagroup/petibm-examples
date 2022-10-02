# 2D flow around a stationary cylinder (Re=100)

A circular cylinder of diameter $D=1.0$ is placed at the origin of a two-dimensional domain spanning $\left[ -15, 35 \right] \times \left[ -25, 25 \right]$.
The initial velocity of the fluid in the domain is $\left( 1, 0 \right)$.
Dirichlet conditions for the velocity are set on all boundaries (velocity set to $\left( 1, 0 \right)$), except at the outlet where the fluid is convected outside the domain in the $x$-direction at speed $1.0$.
The Reynolds number (based on the freestream speed, the diameter of the circular cylinder, and the kinematic viscosity) is $100$.

The computational domain is discretized using an stretched Cartesian grid with $510 \times 298$ cells.
The mesh is kept uniform in the sub-domain $\left[ -0.75, 0.75 \right] \times \left[ -0.75, 0.75 \right]$ and stretched to the external boundaries with a constant ratio; we use a ratio of $1.04$ in the $y$ direction, $1.03$ in the $x$ direction upstream the cylinder, and $1.01$ in the $x$ direction downstream the cylinder.

For this example, we run the simulation with the immersed-boundary projection method implemented in PetIBM for $20000$ time steps with a time increment of $0.01$, saving the numerical solution every $1000$ time steps.

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
> For reference, the simulation completed 20,000 time steps in about 50 minutes using
>
> * 2 MPI processes (Intel(R) Core(TM) i7-3770 CPU @ 3.40GHz)
> * 1 NVIDIA K40 GPU device

## Post-processing

Activate your `conda` environment (see [instructions](../../../README.md)):

```shell
conda activate petibm-examples
```

Plot the history of the force coefficients:

```shell
python scripts/plot_force_coefficients.py
```

The figure is saved as a PNG file (`force_coefficients.png`) in the sub-folder `figures` of the present simulation directory.

<img src="figures/force_coefficients.png" alt="force_coefficients" width="400">

**Figure:** History of the force coefficients for the cylinder at Reynolds number $100$.

Plot the surface pressure coefficient and compare with numerical data from Li et al. (2016):

```shell
python scripts/plot_pressure_coefficient.py
```

The figure is saved as a PNG file (`pressure_coefficient.png`) in the sub-folder `figures` of the present simulation directory.

<img src="figures/pressure_coefficient.png" alt="drag_coefficient" width="400">

**Figure:** Pressure coefficient interpolated along the surface of the cylinder for Reynolds number $100$. Comparison with the numerical data reported in Li et al. (2016).

Plot the contours of the vorticity field after 20,000 time steps:

```shell
python scripts/plot_vorticity.py
```

The figure is saved as a PNG file (`wz_0020000.png`) in the sub-folder `figures` of the present simulation directory.

<img src="figures/wz_0020000.png" alt="vorticity" width="400">

**Figure:** Contours of the vorticity field at Reynolds number $100$ (contours between $-3$ and $3$ with increments of $0.4$).

---

## References

* Li, R. Y., Xie, C. M., Huang, W. X., & Xu, C. X. (2016). An efficient immersed boundary projection method for flow over complex/moving boundaries. Computers & Fluids, 140, 122-135.
