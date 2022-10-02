#!/usr/bin/env bash

descr="*** 2D lid-driven cavity flow at Reynolds number 100 ***"

export CUDA_VISIBLE_DEVICES=0
MPIEXEC_ARGS="-np 1 --allow-run-as-root"

scriptdir="$( cd "$(dirname "$0")" ; pwd -P )"
cd $scriptdir > /dev/null
printf "\n\n$descr\n\n"
mpiexec $MPIEXEC_ARGS petibm-navierstokes -options_left -log_view ascii:view.log
petibm-vorticity

exit 0
