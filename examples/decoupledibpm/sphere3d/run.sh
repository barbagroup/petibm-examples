#!/usr/bin/env bash

descr="*** 3D steady flow around a stationary sphere ***"

scriptdir="$( cd "$(dirname "$0")" ; pwd -P )"
rootdir=$scriptdir

# Set up run arguments
export CUDA_VISIBLE_DEVICES=0
MPIEXEC_ARGS="-np 4 --allow-run-as-root"
export OMPI_MCA_btl_vader_single_copy_mechanism=none
PETIBM_ARGS="-options_left -log_view ascii:view.log"

declare -a folders=(
"Re50"
"Re100"
"Re150"
"Re200"
"Re250"
"Re300"
)

printf "\n\n$descr\n\n"

for folder in "${folders[@]}"
do
    cd $rootdir/$folder
    printf "\n\n*** Case: $folder ***\n\n"
    mpiexec $MPIEXEC_ARGS petibm-decoupledibpm $PETIBM_ARGS
done

exit 0
