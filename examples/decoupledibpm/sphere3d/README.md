# 3D steady flow around a stationary sphere (Re=50, 100, 150, 200, 250, 300)

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
> For reference, each simulation completed 2,500 time steps in about 1 hour using
>
> * 4 MPI processes (Intel(R) Core(TM) i7-3770 CPU @ 3.40GHz)
> * 1 NVIDIA K40 GPU device

## Post-processing

Activate your `conda` environment (see [instructions](../../../README.md)):

```shell
conda activate petibm-examples
```

To plot the drag coefficient versus the Reynolds number

```shell
python scripts/plot_drag_coefficient.py
```

We compare the drag coefficient with the correlation from Clift et al. (1978) and the experimental data from Roos & Willmarth (1971).
The figure is saved as a PNG file (`drag_coefficient.png`) in the sub-folder `figures` on the present directory.

<img src="figures/drag_coefficient.png" alt="drag_coefficient" width="400">

**Figure:** Drag coefficient on the sphere versus the Reynolds number. Comparison with the correlation from Clift et al. (1978) and the experimental data from Roos & Willmarth (1971).

---

## References

* Clift, R., Grace, J. R., & Weber, M. E. (1978). Bubbles, drops, and particles–Academic Press. New York, 510.
* Roos, F. W., & Willmarth, W. W. (1971). Some experimental results on sphere and disk drag. AIAA journal, 9(2), 285-291.

