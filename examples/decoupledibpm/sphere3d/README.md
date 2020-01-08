# 3D steady flow around a stationary sphere (Re=50, 100, 150, 200, 250, 300)

Submit the job on Pegasus:

```shell
sbatch pegasus.slurm
```

Each simulation computes 2,500 time steps in about 16 minutes using one `small-gpu` node on Pegasus

* 20 MPI processes (Dual 20-Core 3.70GHz Intel Xeon Gold 6148)
* 2 NVIDIA Tesla V100 GPU devices

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

