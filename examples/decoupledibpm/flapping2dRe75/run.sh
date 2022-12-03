#!/usr/bin/env bash

descr="*** 2D flapping wing at Reynolds number 75 ***"

scriptdir="$( cd "$(dirname "$0")" ; pwd -P )"
rootdir=$scriptdir

# Set up run arguments
export CUDA_VISIBLE_DEVICES=0
MPIEXEC_ARGS="-np 2 --allow-run-as-root"
export OMPI_MCA_btl_vader_single_copy_mechanism=none
PETIBM_ARGS="-options_left -log_view ascii:view.log"

printf "\n\n$descr\n\n"

cd $rootdir/run
mpiexec $MPIEXEC_ARGS petibm-flapping $PETIBM_ARGS
petibm-vorticity

exit 0
