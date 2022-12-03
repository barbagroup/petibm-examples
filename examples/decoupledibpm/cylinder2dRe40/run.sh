#!/usr/bin/env bash

descr="*** 2D flow past a circular cylinder at Reynolds number 40 ***"

export CUDA_VISIBLE_DEVICES=0
MPIEXEC_ARGS="-np 2 --allow-run-as-root"
export OMPI_MCA_btl_vader_single_copy_mechanism=none

scriptdir="$( cd "$(dirname "$0")" ; pwd -P )"
cd $scriptdir > /dev/null
printf "\n\n$descr\n\n"
mpiexec $MPIEXEC_ARGS petibm-decoupledibpm -options_left -log_view ascii:view.log
petibm-vorticity

exit 0
