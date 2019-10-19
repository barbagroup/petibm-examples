# 2D lid-driven cavity flow at Re=5000

Run the example:

```shell
mpiexec -np 4 petibm-navierstokes -options_left -log_view ascii:view.log
```

Plot the centerline velocity components and compare with the numerical results from Ghia et al. (1982):

```shell
python scripts/plot_centerline_velocities.py
```

The figure is saved as a PNG file (`centerline_velocities_0060000.png`) in the sub-folder `figures` of the present simulation directory.

Plot the contours of the vorticity field:

```shell
petibm-vorticity
python scripts/plot_vorticity.py
```

The figure is saved as a PNG file (`wz_0060000.png`) in the sub-folder `figures` of the present simulation directory.

---

## References

* Ghia, U. K. N. G., Ghia, K. N., & Shin, C. T. (1982). High-Re solutions for incompressible flow using the Navier-Stokes equations and a multigrid method. Journal of computational physics, 48(3), 387-411.
