#!/usr/bin/env bash
# Run simulations locally.

descr="*** 2D Taylor-Green vortices (Re=10) for convergence analysis ***"

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

declare -a folders=(
"spatial"
"temporal"
)

scriptdir="$( cd "$(dirname "$0")" ; pwd -P )"
cd $scriptdir > /dev/null
for folder in "${folders[@]}"
do
	$folder/run.sh "$@"
done

exit 0
