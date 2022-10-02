# 3D unsteady flow around a stationary sphere (Re=350)

> :warning:
>
> All commands displayed below assume you are in the directory containing the present README file.

## Run the example

Submit the job on Pegasus:

```shell
sbatch pegasus.slurm
```

> :information_source:
>
> For reference, each simulation completed 2,500 time steps in about 1 hour using
>
> * 20 MPI processes (Dual 20-Core 3.70GHz Intel Xeon Gold 6148)
> * 2 NVIDIA Tesla V100 GPU devices

## Post-processing

Activate your `conda` environment (see [instructions](../../../README.md)):

```shell
conda activate petibm-examples
```

To plot the history of the force coefficients:

```shell
python scripts/plot_force_coefficients.py
```

The figure is saved as a PNG file (`force_coefficients.png`) in the sub-folder `figures` on the present directory.

<img src="figures/force_coefficients.png" alt="force_coefficients" width="400">

**Figure:** History of the force coefficients on a sphere at Reynolds number $350$.
