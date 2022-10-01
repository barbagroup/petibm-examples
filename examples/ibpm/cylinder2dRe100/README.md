# 2D flow around a stationary cylinder (Re=100)

Run the example from the present directory:

```shell
export CUDA_VISIBLE_DEVICES=0
mpiexec -np 2 petibm-ibpm -options_left -log_view ascii:view.log
```

The simulation completed 20,000 time steps in about $50$ minutes using:

* 2 MPI processes (Intel(R) Core(TM) i7-3770 CPU @ 3.40GHz)
* 1 NVIDIA K40 GPU device

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

**Figure:** Pressure coefficient interpolated along the surface of the cylinder for Reynolds number $100$. Comparison with the numerical data reported by Li et al. (2016).

Compute the vorticity field at saved time steps:

```shell
petibm-vorticity
```

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
