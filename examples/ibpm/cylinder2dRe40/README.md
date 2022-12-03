# 2D flow around stationary cylinder (Re=40)

A circular cylinder of diameter $D=1.0$ is placed at the center of a two-dimensional domain spanning $\left[ -15, 15 \right] \times \left[ -15, 15 \right]$.
The initial velocity of the fluid in the domain is $\left( 1, 0 \right)$.
Dirichlet conditions for the velocity are set on all boundaries (velocity set to $\left( 1, 0 \right)$), except at the outlet where the fluid is convected outside the domain in the $x$-direction at speed $1.0$.
The Reynolds number (based on the freestream speed, the diameter of the circular cylinder, and the kinematic viscosity) is $40$.

The computational domain is discretized using an stretched Cartesian grid with $186 \times 186$ cells.
The mesh is kept uniform in the sub-domain $\left[ -0.6, 0.6 \right] \times \left[ -0.6, 0.6 \right]$ and stretched to the external boundaries with a constant ratio of $1.05$.

For this example, we run the simulation with the immersed-boundary projection method implemented in PetIBM for $2000$ time steps with a time increment of $0.01$ and save the numerical solution at the end.

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
> For reference, the simulation completed 2,000 time steps in less than 2 minutes using
>
> * 2 MPI processes (Intel(R) Core(TM) i7-3770 CPU @ 3.40GHz)
> * 1 NVIDIA K40 GPU device

## Post-processing

Activate your `conda` environment (see [instructions](../../../README.md)):

```shell
conda activate petibm-examples
```

Plot the history of the drag coefficient and compare with numerical data from Koumoutsakos and Leonard (1995):

```shell
python scripts/plot_drag_coefficient.py
```

The figure is saved as a PNG file (`drag_coefficient.png`) in the sub-folder `figures` of the present simulation directory.

<img src="figures/drag_coefficient.png" alt="drag_coefficient" width="400">

**Figure:** History of the drag coefficient for the cylinder at Reynolds number $40$. Comparison with the numerical data of reported by Koumoutsakos & Leonard (1995).

Plot the contours of the vorticity field at the final time step:

```shell
python scripts/plot_vorticity.py
```

The figure is saved as a PNG file (`wz_0002000.png`) in the sub-folder `figures` of the present simulation directory.

<img src="figures/wz_0002000.png" alt="vorticity" width="400">

**Figure:** Contours of the vorticity field at Reynolds number $40$ ($16$ contours between $-3$ and $+3$).

---

## References

* Koumoutsakos, P., & Leonard, A. (1995). High-resolution simulations of the flow around an impulsively started cylinder using vortex methods. Journal of Fluid Mechanics, 296, 1-38.
