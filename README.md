# Collection of PetIBM examples

[![License](https://img.shields.io/badge/License-BSD%203--Clause-blue.svg)](https://github.com/mesnardo/petibm-examples/raw/master/LICENSE)
[![Docker Hub](https://img.shields.io/badge/hosted-docker--hub-informational.svg)](https://hub.docker.com/repository/docker/barbagroup/petibm)
[![Singularity Hub](https://www.singularity-hub.org/static/img/hosted-singularity--hub-%23e32929.svg)](https://singularity-hub.org/collections/3692)

## Dependencies

Package version last used indicated between parenthesis.

* [PetIBM](https://github.com/barbagroup/PetIBM) (`0.4.2`)
  * [OpenMPI](https://www.open-mpi.org) (`3.1.4`)
  * [PETSc](https://www.mcs.anl.gov/petsc) (`3.11.4`)
  * [CUDA Toolkit](https://developer.nvidia.com/cuda-toolkit-archive) (`10.1`)
  * [AmgX](https://github.com/NVIDIA/AMGX) (commit `cf285c1`)
* [PetibmPy](https://github.com/mesnardo/petibmpy) (`develop`)

## List of examples

* Navier-Stokes solver
  * Convergence analysis (2D lid-driven cavity flow at Reynolds number 100)
  * 2D lid-driven cavity flow at Reynolds numbers 100, 1000, 3200, and 5000
* IBPM
  * 2D flow around a stationary cylinder at Reynolds numbers 40, 550, and 3000
  * 2D unsteady flow around a stationary cylinder at Reynolds number 100
* Decoupled IBPM
  * 2D unsteady flow around a stationary cylinder at Reynolds number 100
  * 2D flapping wing at Reynolds number 75
  * 2D flow around an inline oscillating cylinder at Reynolds number 100
  * 3D steady flow around an inclined flat plate at Reynolds number 100
  * 3D steady-flow around a sphere

## Contact

Please e-mail [Olivier Mesnard](mailto:mesnardo@gwu.edu) if you have any questions, suggestions, or feedback.

To report bugs, please use the GitHub issue tracking system.
We also welcome pull-requests.
