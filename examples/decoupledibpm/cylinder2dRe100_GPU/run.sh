#!/usr/bin/env bash
# Run simulation.

# Hardware configuration
np=2  # number of MPI processes
export CUDA_VISIBLE_DEVICES=0  # GPU device indices
execname="petibm-decoupledibpm"

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

if [ -d "$mpidir" ]; then
	export PATH="$mpidir/bin":$PATH
fi
if [ -d "$petibmdir" ]; then
	export PATH="$petibmdir/bin":$PATH
fi

scriptdir="$( cd "$(dirname "$0")" ; pwd -P )"

echo ""
echo ""
cat  $scriptdir/README.md | head -n 1
echo ""
echo ""

mpiexec --version
nvidia-smi

petibmcmd="$execname -options_left -log_view ascii:view.log"

cd $scriptdir
if [ -f "$simg" ]; then
	echo "[INFO] Running within Singularity container"
	mpiexec -np $np singularity exec --nv $simg $petibmcmd
else
	echo "[INFO] Running locally"
	mpiexec -np $np $petibmcmd
fi

exit 0
