# Collection of PetIBM examples

[![License](https://img.shields.io/badge/License-BSD%203--Clause-blue.svg)](https://github.com/mesnardo/petibm-examples/raw/master/LICENSE)
[![Docker Hub](https://img.shields.io/badge/hosted-docker--hub-informational.svg)](https://hub.docker.com/repository/docker/barbagroup/petibm)
[![Singularity Hub](https://www.singularity-hub.org/static/img/hosted-singularity--hub-%23e32929.svg)](https://singularity-hub.org/collections/3692)

The repository includes examples of flow simulation with [PetIBM](https://github.com/barbagroup/PetIBM).
Each example provides the set of input data and the python post-processing scripts.

## Requirements

To run the examples, you can either install PetIBM on your machine or use our Docker image.

To install PetIBM locally, please refer to [these instructions](https://barbagroup.github.io/PetIBM/dc/df1/md_doc_markdowns_installation.html).

To pull the Docker image (tag is last used to run these examples):

```shell
docker pull docker pull barbagroup/petibm:0.5.1-GPU-OpenMPI-xenial
```

To post-process the numerical solution, we provide python scripts.
To install the packages required to execute the scripts, we recommend creating a `conda` environment with:

```
conda env create --name=petibm-example --file=environment.yml
```

Note that most examples are set to solve the Poisson system on a GPU using the NVIDIA AmgX library and require a CUDA-capable GPU device.
Of course, you can always modify the configuration files to run all solvers on CPUs.

## List of examples

* [2D array of decaying vortices at Re=10](examples/taylorgreenvortices) (convergence analysis)
* Navier-Stokes solver
  * [2D lid-driven cavity flow at Re=100, 1000, 3200, and 5000](examples/navierstokes)
* Immersed boundary projection method (IBPM)
  * [2D flow around an impulsively started circular cylinder at Re=40, 550, and 3000](examples/ibpm)
  * [2D unsteady flow past a stationary circular cylinder at Re=100](examples/ibpm/cylinder2dRe100)
* Decoupled IBPM
  * [2D flow around an impulsively started circular cylinder at Re=40 and 550](examples/decoupledibpm)
  * [2D unsteady flow past a stationary circular cylinder at Re=100](examples/decoupledibpm/cylinder2dRe100)
  * [2D flapping wing at Re=75](examples/decoupledibpm/flapping2dRe75)
  * [2D flow around an inline oscillating cylinder at Re=100 and KC=5](examples/decoupledibpm/oscillatingcylinder2dRe100)
  * [3D steady flow around an inclined flat plate at Re=100](examples/decoupledibpm/flatplate3dRe100)
  * [3D steady flow around a sphere at Re=50, 100, 150, 200, 250, and 300](examples/decoupledibpm/sphere3d)
  * [3D unsteady flow around a sphere at Re=350](examples/decoupledibpm/sphere3d/Re350)

To report bugs or ask questions, please use the GitHub issue tracking system.
We also welcome pull-requests.
