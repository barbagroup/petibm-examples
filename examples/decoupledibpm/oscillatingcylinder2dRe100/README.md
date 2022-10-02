# 2D flow around an inline oscillating cylinder (Re=100)

> :warning:
>
> All commands displayed below assume you are in the directory containing the present README file.

## Run the example

```shell
docker pull barbagroup/petibm:0.5.1-GPU-OpenMPI-xenial

nvidia-docker create --name=oscillating -v $(pwd):/data -v $(pwd)/../../cmake-modules:/tmp/cmake-modules barbagroup/petibm:0.5.1-GPU-OpenMPI-xenial

nvidia-docker start oscillating
nvidia-docker exec oscillating /data/build.sh
nvidia-docker exec oscillating /data/run.sh
nvidia-docker stop oscillating

nvidia-docker rm oscillating
```

> :information_source:
>
> For reference, the simulation completed 10,000 time steps in about 50 minutes using
>
> * 2 MPI processes (Intel(R) Core(TM) i7-3770 CPU @ 3.40GHz)
> * 1 NVIDIA K40 GPU device

## Post-processing

Activate your `conda` environment (see [instructions](../../../README.md)):

```shell
conda activate petibm-examples
```

Plot the history of the drag coefficient:

```shell
python run/scripts/plot_drag_coefficient.py
```

The figure is saved as a PNG file (`drag_coefficient.png`) in the sub-folder `figures` of the simulation directory.

<img src="run/figures/drag_coefficient.png" alt="drag_coefficient" width="400">

**Figure:** History of the drag coefficient on an inline oscillating cylinder at Reynolds number $100$.

Plot the vertical profiles of the velocity components at different position along the horizontal axis:

```shell
python scripts/plot_velocity_profiles.py
```

The figure is saved as a PNG file (`velocity_profiles.png`) in the sub-folder `figures` of the simulation directory.

<img src="run/figures/velocity_profiles.png" alt="velocity_profiles" width="400">

**Figure:** Vertical profiles of the velocity components ($u$: left; $v$: right) at different locations along the $x$ axis and at phase angles $\phi = 180^o$, $210^o$, and $330^o$. We compare the PetIBM solution with the experimental data from Dutsch et al. (1998).

Plot the vorticity field at phase angles $\phi = 0^o$ and $288^o$:

```shell
python scripts/plot_vorticity.py
```

The figure is saved as a PNG file (`vorticity.png`) in the sub-folder `figures` of the simulation directory.

<img src="run/figures/vorticity.png" alt="vorticity" width="400">

**Figure:** Vorticity field around an inline oscillating cylinder at Reynolds number $100$ at phase angles $\phi = 0^o$ (left) and $\phi = 288^o$ (right).

Plot the pressure field at phase angles $\phi = 0^o$ and $288^o$:

```shell
python scripts/plot_pressure.py
```

The figure is saved as a PNG file (`pressure.png`) in the sub-folder `figures` of the simulation directory.

<img src="run/figures/pressure.png" alt="pressure" width="400">

**Figure:** Pressure field around an inline oscillating cylinder at Reynolds number $100$ at phase angles $\phi = 0^o$ (left) and $\phi = 288^o$ (right).

---

## References

* Dütsch, H., Durst, F., Becker, S., & Lienhart, H. (1998). Low-Reynolds-number flow around an oscillating circular cylinder at low Keulegan–Carpenter numbers. Journal of Fluid Mechanics, 360, 249-271.
