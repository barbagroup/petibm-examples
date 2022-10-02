# 2D flow around an inline oscillating cylinder (Re=100)

Run the example from the present directory:

```shell
export CUDA_VISIBLE_DEVICES=0
mpiexec -np 2 petibm-oscillating \
	-probes probes.yaml \
	-options_left \
	-log_view ascii:view.log
```

The simulation completed 10,000 time steps in about 50 minutes using:

* 2 MPI processes (Intel(R) Core(TM) i7-3770 CPU @ 3.40GHz)
* 1 NVIDIA K40 GPU device

Plot the history of the drag coefficient:

```shell
python scripts/plot_drag_coefficient.py
```

The figure is saved as a PNG file (`drag_coefficient.png`) in the sub-folder `figures` of the present simulation directory.

<img src="figures/drag_coefficient.png" alt="drag_coefficient" width="400">

**Figure:** History of the drag coefficient on an inline oscillating cylinder at Reynolds number $100$.

Plot the vertical profile of the velocity components at different position along the horizontal axis:

```shell
python scripts/plot_velocity_profiles.py
```

The figure is saved as a PNG file (`velocity_profiles.png`) in the sub-folder `figures` of the present simulation directory.

<img src="figures/velocity_profiles.png" alt="velocity_profiles" width="400">

**Figure:** Vertical profiles of the velocity components ($u$: left; $v$: right) at different locations along the $x$ axis and at phase angles $\phi = 180^o$, $210^o$, and $330^o$.

Plot the vorticity field at phase angles $\phi = 0^o$ and $288^o$:

```shell
petibm-vorticity
python scripts/plot_vorticity.py
```

The figure is saved as a PNG file (`vorticity.png`) in the sub-folder `figures` of the present simulation directory.

<img src="figures/vorticity.png" alt="vorticity" width="400">

**Figure:** Vorticity field around an inline oscillating cylinder at Reynolds number $100$ at phase angles $\phi = 0^o$ (left) and $\phi = 288^o$ (right).

Plot the pressure field at phase angles $\phi = 0^o$ and $288^o$:

```shell
python scripts/plot_pressure.py
```

The figure is saved as a PNG file (`pressure.png`) in the sub-folder `figures` of the present simulation directory.

<img src="figures/pressure.png" alt="pressure" width="400">

**Figure:** Pressure field around an inline oscillating cylinder at Reynolds number $100$ at phase angles $\phi = 0^o$ (left) and $\phi = 288^o$ (right).

