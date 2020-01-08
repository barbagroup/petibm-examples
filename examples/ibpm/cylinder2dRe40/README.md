# 2D flow around stationary cylinder (Re=40)

Run the example:

```shell
mpiexec -np 2 petibm-ibpm -options_left -log_view ascii:view.log
```

The simulation completed 2,000 time steps in about 3 minutes using:

* 2 MPI processes (Intel(R) Core(TM) i7-3770 CPU @ 3.40GHz)

Plot the history of the drag coefficient and compare with numerical data from Koumoutsakos and Leonard (1995):

```shell
python scripts/plot_drag_coefficient.py
```

The figure is saved as a PNG file (`drag_coefficient.png`) in the sub-folder `figures` of the present simulation directory.

<img src="figures/drag_coefficient.png" alt="drag_coefficient" widht="400">

**Figure:** History of the drag coefficient for the cylinder at Reynolds number $40$. Comparison with the numerical data of reported by Koumoutsakos & Leonard (1995).

Compute the vorticity field at saved time steps:

```shell
petibm-vorticity
```

Plot the contours of the vorticity field at the final time step:

```shell
python scripts/plot_vorticity.py
```

The figure is saved as a PNG file (`wz_0002000.png`) in the sub-folder `figures` of the present simulation directory.

<img src="figures/wz_0002000.png" alt="vorticity" widht="400">

**Figure:** Contours of the vorticity field at Reynolds number $40$ ($16$ contours between $-3$ and $+3$).

---

## References

* Koumoutsakos, P., & Leonard, A. (1995). High-resolution simulations of the flow around an impulsively started cylinder using vortex methods. Journal of Fluid Mechanics, 296, 1-38.
