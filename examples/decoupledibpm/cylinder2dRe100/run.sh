#!/usr/bin/env bash

descr="*** 2D flow past a circular cylinder at Reynolds number 100 ***"

export CUDA_VISIBLE_DEVICES=0
MPIEXEC_ARGS="-np 2 --allow-run-as-root"
export OMPI_MCA_btl_vader_single_copy_mechanism=none
PETIBM_ARGS="-options_left -log_view ascii:view.log"

scriptdir="$( cd "$(dirname "$0")" ; pwd -P )"
cd $scriptdir > /dev/null
printf "\n\n$descr\n\n"
mpiexec $MPIEXEC_ARGS petibm-decoupledibpm $PETIBM_ARGS
petibm-vorticity

exit 0
