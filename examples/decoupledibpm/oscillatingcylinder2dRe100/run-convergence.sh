#!/usr/bin/env bash

scriptdir="$( cd "$(dirname "$0")" ; pwd -P )"
rootdir=$scriptdir

# Set up run arguments
export CUDA_VISIBLE_DEVICES=0
MPIEXEC_ARGS="-np 2 --allow-run-as-root"
export OMPI_MCA_btl_vader_single_copy_mechanism=none
PETIBM_ARGS="-options_left"

# Spatial convergence analysis
declare -a folders=(
"64x64"
"128x128"
"256x256"
"512x512"
"1024x1024"
)
for folder in "${folders[@]}"
do
    cd $rootdir/convergence/spatial/$folder
    printf "\n\n*** Grid size: $folder ***\n\n"
    mpiexec $MPIEXEC_ARGS petibm-oscillating $PETIBM_ARGS
done

# Temporal convergence analysis
declare -a folders=(
"dt=0.01"
"dt=0.005"
"dt=0.002"
"dt=0.001"
"dt=0.0005"
)
for folder in "${folders[@]}"
do
    cd $rootdir/convergence/temporal/$folder
    printf "\n\n*** Time-step size: $folder ***\n\n"
    mpiexec $MPIEXEC_ARGS petibm-oscillating $PETIBM_ARGS
done

exit 0
