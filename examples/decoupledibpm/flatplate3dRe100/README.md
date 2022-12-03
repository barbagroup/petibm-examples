# 3D flow around inclined flat plate (Re=100, AR=2)

The simulations compute the flow past an inclined flat plate, with aspect ratio $AR=2$, at Reynolds number $100$ (based on the chord length of the plate, the freestream velocity, and the kinematic viscosity) in the domain $left[ -4, 6.1 \right] \times \left[-5, 5 \right] \times \left[-5, 5 \right]$.
The fluid velocity is initially set to the freestream velocity.
The mesh contains $129 \times 56 \times 86$ cells and is uniform in the sub-domain $\left[ -0.5, 0.7] \times \left[ -0.6, 0.6 \right] \times \left[ -1.2, 1.2 \right]$ with a grid cell-width of $0.04$ in the three directions and stretched to the external boundaries with a geometric ratio of $1.03$ in the $x$ direction and $1.3$ in the $y$ and $z$ directions.
We set freestream conditions for the velocity at the on all boundaries, except at the outlet where we use a convective conditions.

The flat plate has an aspect ratio of 2 ,is centered in the computational domain, and is uniformly discretized with the same resolution than the background Eulerian mesh.
For this study, the angle of attack of the plate varies from $0^o$ to $90^o$ degrees by $10$-degree increments.

The convective and diffusive terms are temporally integrated with a second-order Adams-Bashforth scheme and a second-order Crank-Nicolson scheme, respectively.
Each configuration was run for $2000$ time steps with a time-step size of $0.01$.

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
> For reference, each simulation completed in less than 8 minutes using
>
> * 4 MPI processes (Intel(R) Core(TM) i7-3770 CPU @ 3.40GHz)
> * 1 NVIDIA K40 GPU device

## Post-processing

Activate your `conda` environment (see [instructions](../../../README.md)):

```shell
conda activate petibm-examples
```

Plot the instantaneous force coefficients and compare with the experimental results from Taira et al. (2007):

```shell
python scripts/plot_force_coefficients.py
```

The figure is saved as a PNG file (`force_coefficients.png`) in the sub-folder `figures` of the present simulation directory.

<img src="figures/force_coefficients.png" alt="force_coefficients" width="400">

**Figure:** Time-averaged lift and drag coefficients for angles of attack of the flat plate between $0^o$ and $90^o$ ($10^o$ increments). We compare the results with the experimental data reported in Taira et al. (2007).

## References

* Taira, K., Dickson, W. B., Colonius, T., Dickinson, M. H., & Rowley, C. W. (2007). "Unsteadiness in flow over a flat plate at angle-of-attack at low Reynolds numbers." AIAA Paper, 710, 2007.
