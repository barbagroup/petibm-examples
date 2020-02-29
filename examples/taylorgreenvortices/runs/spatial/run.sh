#!/usr/bin/env bash
# Run simulations locally.

descr="*** 2D Taylor-Green vortices (Re=10) for spatial convergence ***"

# Hardware configuration.
np=1  # number of MPI processes
export CUDA_VISIBLE_DEVICES=0  # GPU device indices

print_usage() {
	printf "usage: ./run.sh [-h] [-p DIR] [-m DIR]\n\n"
	printf "Run the simulation locally or within a Singularity container.\n\n"
	printf "Options:\n\n"
	printf "  -h          Show this message and exit.\n"
	printf "  -m DIR      MPI installation directory.\n"
	printf "  -p DIR      PetIBM app installation directory.\n"
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
while getopts 'm:p:h' flag; do
	case "${flag}" in
		m) mpidir=`realpath "${OPTARG}"` ;;
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

declare -a folders=(
"20x20"
"60x60"
"180x180"
"540x540"
)

scriptdir="$( cd "$(dirname "$0")" ; pwd -P )"
cd $scriptdir > /dev/null
for folder in "${folders[@]}"
do
	cd $folder
	printf "\nGrid size: $folder\n"
	printf "\n\t- Navier-Stokes solver\n"
	mpiexec -np $np petibm-taylorgreen -options_left
	printf "\n\t- Decoupled IPBM\n"
	mpiexec -np $np petibm-taylorgreen -with-ib -output output-with-ib -options_left
	cd $scriptdir
done

exit 0
