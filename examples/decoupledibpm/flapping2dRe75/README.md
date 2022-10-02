# 2D flow around a flapping wing (Re = 100)

> :warning:
>
> All commands displayed below assume you are in the directory containing the present README file.

## Run the example

```shell
docker pull barbagroup/petibm:0.5.1-GPU-OpenMPI-xenial

nvidia-docker create --name=flapping -v $(pwd):/data -v $(pwd)/../../cmake-modules:/tmp/cmake-modules barbagroup/petibm:0.5.1-GPU-OpenMPI-xenial

nvidia-docker start flapping
nvidia-docker exec flapping /data/build.sh
nvidia-docker exec flapping /data/run.sh
nvidia-docker stop flapping

nvidia-docker rm flapping
```

> :information_source:
>
> For reference, the simulation completed 3,200 time steps in about 5 minutes using
>
> * 2 MPI processes (Intel(R) Core(TM) i7-3770 CPU @ 3.40GHz)
> * 1 NVIDIA K40 GPU device

## Post-processing

Activate your `conda` environment (see [instructions](../../../README.md)):

```shell
conda activate petibm-examples
```

To visualize the instantaneous force coefficients:

```shell
python run/scripts/plot_force_coefficients.py
```

(The figure is saved as a PNG file in the sub-folder `figures` of the simulation directory.)

<img src="run/figures/force_coefficients.png" alt="force_coefficients" width="400">

**Figure:** History of the lift (top) and drag (bottom) coefficients over 4 periods. We compare the forces obtained with PetIBM to the results from Li et al. (2015), Wang et al. (2004), and Eldredge (2007).

To plot the contours of the vorticity field:

```shell
python run/scripts/plot_vorticity.py
```

(The PNG files are saved in the sub-folder `figures` of the simulation directory.)

<img src="run/figures/wz_0002600.png" alt="wz_0002600" width="800">

**Figure:** Contours of the vorticity field at $t/T = 3.25$ (40 levels uniformly distributed between $-20$ and $20$).

## References

* Eldredge, J. D. (2007). Numerical simulation of the fluid dynamics of 2D rigid body motion with the vortex particle method. Journal of Computational Physics, 221(2), 626-648.
* Li, C., Dong, H., & Liu, G. (2015). Effects of a dynamic trailing-edge flap on the aerodynamic performance and flow structures in hovering flight. Journal of Fluids and Structures, 58, 49-65.
* Wang, Z. J., Birch, J. M., & Dickinson, M. H. (2004). Unsteady forces and flows in low Reynolds number hovering flight: two-dimensional computations vs robotic wing experiments. Journal of Experimental Biology, 207(3), 449-460.
