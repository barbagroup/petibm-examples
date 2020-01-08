# 2D flow around a flapping wing (Re = 100)

Run the simulation locally from the current directory:

```shell
./run.sh -m /home/mesnardo/software/openmpi/3.1.4/linux-gnu-opt -p .. > stdout.txt 2> stderr.txt
```

The simulation completes 3200 time steps in about 8 minutes when using:

* 2 CPU processes (Intel(R) Core(TM) i7-3770 CPU @ 3.40GHz),
* 1 NVIDIA K40 GPU device.

To visualize the instantaneous force coefficients:

```shell
python scripts/plot_force_coefficients.py
```

(The Matplotlib figure is saved as a PNG file in the sub-folder `figures` of the simulation directory.)

<img src="figures/force_coefficients.png" alt="force_coefficients" width="400">

**Figure:** History of the lift (top) and drag (bottom) coefficients over 4 periods. We compare the forces obtained with PetIBM to the results from Li et al. (2015), Wang et al. (2004), and Eldredge (2007).

To plot the contours of the vorticity field:

To plot the contour of the vorticity field using VisIt:

```shell
petibm-vorticity
python scripts/plot_vorticity.py
```

(The PNG files are saved in the sub-folder `figures` of the simulation directory.)

## References

* Eldredge, J. D. (2007). Numerical simulation of the fluid dynamics of 2D rigid body motion with the vortex particle method. Journal of Computational Physics, 221(2), 626-648.
* Li, C., Dong, H., & Liu, G. (2015). Effects of a dynamic trailing-edge flap on the aerodynamic performance and flow structures in hovering flight. Journal of Fluids and Structures, 58, 49-65.
* Wang, Z. J., Birch, J. M., & Dickinson, M. H. (2004). Unsteady forces and flows in low Reynolds number hovering flight: two-dimensional computations vs robotic wing experiments. Journal of Experimental Biology, 207(3), 449-460.
