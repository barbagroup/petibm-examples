# 2D lid-driven cavity flow at Re=5000

Run the example:

```shell
mpiexec -np 4 petibm-navierstokes -options_left -log_view ascii:view.log
```

The simulation completed $60,000$ time steps in about $24$ minutes on Hopper:

* 4 MPI processes (Intel(R) Core(TM) i5-8250U CPU @ 1.60GHz)

Plot the centerline velocity components and compare with the numerical results from Ghia et al. (1982):

```shell
python scripts/plot_centerline_velocities.py
```

The figure is saved as a PNG file (`centerline_velocities_0060000.png`) in the sub-folder `figures` of the present simulation directory.

<img src="figures/centerline_velocities_0060000.png" alt="velocity_profiles" widht="400">

**Figure:** Velocity profiles of the $x$ component along a vertical line at $x=0.5$ (left) and of the $y$ component along an horizontal line at $y=0.5$ and (right).

Plot the contours of the vorticity field:

```shell
petibm-vorticity
python scripts/plot_vorticity.py
```

The figure is saved as a PNG file (`wz_0060000.png`) in the sub-folder `figures` of the present simulation directory.

<img src="figures/wz_0060000.png" alt="wz" width="400"/>

**Figure:** Contours the vorticity ($21$ contours between $-5$ and $+5$).

---

## References

* Ghia, U. K. N. G., Ghia, K. N., & Shin, C. T. (1982). High-Re solutions for incompressible flow using the Navier-Stokes equations and a multigrid method. Journal of computational physics, 48(3), 387-411.
