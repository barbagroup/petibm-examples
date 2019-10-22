#!/usr/bin/env bash
# Run simulations.

descr="*** 3D flow around inclined flate plate at Reynolds number 100 ***"

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
"aoa0"
"aoa10"
"aoa20"
"aoa30"
"aoa40"
"aoa50"
"aoa60"
"aoa70"
"aoa80"
"aoa90"
)

scriptdir="$( cd "$(dirname "$0")" ; pwd -P )"

echo ""
echo ""
echo $descr
echo ""
echo ""

cd $scriptdir
for folder in "${folders[@]}"
do
	$folder/run.sh "$@"
done

exit 0
