#!/usr/bin/env bash
# Run simulations.

descr="*** Examples using the IBPM solver ***"

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

while getopts 'm:s:h' flag; do
	case "${flag}" in
		m) mpidir=`realpath "${OPTARG}"` ;;
		s) simg=`realpath "${OPTARG}"` ;;
		h) print_usage
		   exit 0 ;;
		*) print_usage
		   exit 1 ;;
	esac
done


declare -a folders=(
"cylinder2dRe40"
"cylinder2dRe550"
"cylinder2dRe550_GPU"
"cylinder2dRe3000_GPU"
"cylinder2dRe100_GPU"
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
	cd $folder && ./run.sh "$@"
done

exit 0
