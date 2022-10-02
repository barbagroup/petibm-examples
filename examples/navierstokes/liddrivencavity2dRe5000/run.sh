#!/usr/bin/env bash

descr="*** 2D lid-driven cavity flow at Reynolds number 5000 ***"

export CUDA_VISIBLE_DEVICES=0
MPIEXEC_ARGS="-np 4 --allow-run-as-root"
export OMPI_MCA_btl_vader_single_copy_mechanism=none

scriptdir="$( cd "$(dirname "$0")" ; pwd -P )"
cd $scriptdir > /dev/null
printf "\n\n$descr\n\n"
mpiexec $MPIEXEC_ARGS petibm-navierstokes -options_left -log_view ascii:view.log
petibm-vorticity

exit 0
