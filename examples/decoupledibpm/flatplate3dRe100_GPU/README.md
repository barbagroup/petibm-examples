# 3D flow around inclined flat plate (Re=100, AR=2)

Run the example using 1 GPU device and 4 MPI processes:

```shell
export CUDA_VISIBLE_DEVICES=<idx1>
# Declare list of angles of attack to run
angles=(0 10 20 30 40 50 60 70 80 90)
for angle in ${angles[@]}; do
    echo "*** Angle of attack: $angle degrees ***"
    mpiexec -np 4 petibm-decoupledibpm \
        -directory "aoa$angle" \
        -options_left \
        -log_view ascii:"aoa$angle/stdout.txt"
done
```

Each simulation completes in about 10 minutes when using:

* 4 MPI processes (Intel(R) Core(TM) i7-3770 CPU @ 3.40GHz),
* 1 NVIDIA K40 GPU device.

Plot the instantaneous force coefficients and compare with the experimental results from Taira et al. (2007):

```shell
python scripts/plot_force_coefficients.py
```

The figure is saved as a PNG file (`force_coefficients.png`) in the sub-folder `figures` of the present simulation directory.

<img src="figures/force_coefficients.png" alt="force_coefficients" widht="400">

**Figure:** Time-averaged lift and drag coefficients for angles of attack of the flat plate between $0$ and $90^o$ ($10$-degree increments). We compare the results with the experimental data reported in Taira et al. (2007).

## References

* Taira, K., Dickson, W. B., Colonius, T., Dickinson, M. H., & Rowley, C. W. (2007). "Unsteadiness in flow over a flat plate at angle-of-attack at low Reynolds numbers." AIAA Paper, 710, 2007.
