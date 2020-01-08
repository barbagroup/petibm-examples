# 3D unsteady flow around a stationary sphere (Re=350)

Submit the job on Pegasus:

```shell
sbatch pegasus.slurm
```

The simulation computed 50,000 time steps in about 7.1 hours using one `small-gpu` node on Pegasus

* 20 MPI processes (Dual 20-Core 3.70GHz Intel Xeon Gold 6148)
* 2 NVIDIA Tesla V100 GPU devices

To plot the history of the force coefficients:

```shell
python scripts/plot_force_coefficients.py
```

The figure is saved as a PNG file (`force_coefficients.png`) in the sub-folder `figures` on the present directory.

<img src="figures/force_coefficients.png" alt="force_coefficients" width="400">

**Figure:** History of the force coefficients on a sphere at Reynolds number $350$.
