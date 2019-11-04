#!/usr/bin/env bash
# Run simulations locally or within a Singularity container.

descr="*** Convergence analysis for the Navier-Stokes solver ***"

# Hardware configuration.
np=1  # number of MPI processes

print_usage() {
	printf "usage: ./run.sh [-h] [-p DIR] [-m DIR] [-s IMAGE]\n\n"
	printf "Run the simulations locally or within a Singularity container.\n\n"
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

declare -a folders=(
"30"
"90"
"270"
"810"
)

printf "\n\n$descr\n\n"

prepend_path $mpidir/bin

printf "\n[INFO] MPI version:\n"
mpiexec --version

scriptdir="$( cd "$(dirname "$0")" ; pwd -P )"
cd $scriptdir > /dev/null
if [ -f "$simg" ]; then
	printf "\n[INFO] Running within Singularity container\n"
	for folder in "${folders[@]}"; do
		cd $folder > /dev/null
		mpiexec -np $np singularity exec --bind $scriptdir/$folder:/mnt $simg \
			petibm-navierstokes \
			-directory /mnt \
			-options_left \
			-log_view ascii:view.log
		cd $scriptdir > /dev/null
	done
else
	printf "\n[INFO] Running locally\n"
	prepend_path $petibmdir/bin
	for folder in "${folders[@]}"; do
		cd $folder > /dev/null
		mpiexec -np $np petibm-navierstokes \
			-options_left \
			-log_view ascii:view.log
		cd $scriptdir > /dev/null
	done
fi

exit 0
