#!/usr/bin/env bash
# Run simulation locally or within Singularity container.

descr="*** 3D flow around inclined plate (AoA=0) at Reynolds number 100 ***"

# Hardware configuration.
np=4  # number of MPI processes
export CUDA_VISIBLE_DEVICES=0  # GPU device indices

print_usage() {
	printf "usage: ./run.sh [-h] [-p DIR] [-m DIR] [-s IMAGE]\n\n"
	printf "Run the simulation locally or within a Singularity container.\n\n"
	printf "Options:\n\n"
	printf "  -h          Show this message and exit.\n"
	printf "  -m DIR      MPI installation directory.\n"
	printf "  -p DIR      PetIBM installation directory.\n"
	printf "  -s IMAGE    Path of the Singularity image.\n"
	printf "\n"
}

prepend_path() {
	if [ -d "$1" ]; then
		export PATH="$1:"$PATH
	else
		printf "[WARNING] $1: not a valid directory"
	fi
}

# Parse command-line options.
while getopts 'm:p:s:h' flag; do
	case "${flag}" in
		m) mpidir=`realpath "${OPTARG}"` ;;
		s) simg=`realpath "${OPTARG}"` ;;
		p) petibmdir=`realpath "${OPTARG}"` ;;
		h) print_usage
		   exit 0 ;;
		*) print_usage
		   exit 1 ;;
	esac
done

printf "\n\n$descr\n\n"

prepend_path $mpidir/bin

printf "\n[INFO] MPI version:\n"
mpiexec --version
printf "\n[INFO] nvidia-smi output:\n"
nvidia-smi

scriptdir="$( cd "$(dirname "$0")" ; pwd -P )"
cd $scriptdir > /dev/null
if [ -f "$simg" ]; then
	printf "\n[INFO] Running within Singularity container\n"
	mpiexec -np $np singularity exec --nv --bind $scriptdir:/mnt $simg \
		petibm-decoupledibpm \
		-directory /mnt \
		-options_left \
		-log_view ascii:view.log
else
	printf "\n[INFO] Running locally\n"
	prepend_path $petibmdir/bin
	mpiexec -np $np petibm-decoupledibpm \
		-options_left \
		-log_view ascii:view.log
fi

exit 0
