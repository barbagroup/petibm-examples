#!/usr/bin/env bash
# Run simulations locally or within a Singularity container.

descr="*** Examples using the Navier-Stokes solver ***"

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
"liddrivencavity2dRe100"
"liddrivencavity2dRe1000"
"liddrivencavity2dRe3200"
"liddrivencavity2dRe5000"
)

printf "\n\n$descr\n\n"

scriptdir="$( cd "$(dirname "$0")" ; pwd -P )"
cd $scriptdir > /dev/null
for folder in "${folders[@]}"
do
	$folder/run.sh "$@"
done

exit 0
