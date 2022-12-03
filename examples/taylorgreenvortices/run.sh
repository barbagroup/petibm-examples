#!/usr/bin/env bash

scriptdir="$( cd "$(dirname "$0")" ; pwd -P )"
rootdir=$scriptdir

# Set up run arguments
export CUDA_VISIBLE_DEVICES=0
MPIEXEC_ARGS="-np 1 --allow-run-as-root"
PETIBM_ARGS="-options_left"

# 2D Taylor-Green vortices for spatial convergence
declare -a folders=(
"20x20"
"60x60"
"180x180"
"540x540"
)
for folder in "${folders[@]}"
do
    cd $rootdir/runs/spatial/$folder
    printf "\n\n*** Grid size: $folder ***\n\n"
    printf "\n\t- Navier-Stokes solver\n"
    mpiexec $MPIEXEC_ARGS petibm-taylorgreen $PETIBM_ARGS
    printf "\n\t- Decoupled IBPM solver\n"
    mpiexec $MPIEXEC_ARGS petibm-taylorgreen $PETIBM_ARGS \
        -with-ib -output output-with-ib
done

# 2D Taylor-Green vortices for temporal convergence
declare -a folders=(
"dt=0.01"
"dt=0.005"
"dt=0.0025"
"dt=0.00125"
"dt=0.0001"
)
for folder in "${folders[@]}"
do
    cd $rootdir/runs/temporal/$folder
    printf "\n\n*** Time-step size: $folder ***\n\n"
    printf "\n\t- Navier-Stokes solver\n"
    mpiexec $MPIEXEC_ARGS petibm-taylorgreen $PETIBM_ARGS
done

exit 0
