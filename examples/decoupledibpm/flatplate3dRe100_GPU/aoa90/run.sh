#!/usr/bin/env bash
# Run simulation.

descr="*** 3D flow around inclined plate (AoA=90) at Reynolds number 100 ***"

# Hardware configuration
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


scriptdir="$( cd "$(dirname "$0")" ; pwd -P )"
simg=""
mpidir=""

while getopts 'm:p:s:h' flag; do
	case "${flag}" in
		m) mpidir=`realpath "${OPTARG}"` ;;
		s) simg=`realpath "${OPTARG}"` ;;
		p) petibmdir=`realpath "${OPTARGS}"` ;;
		h) print_usage
		   exit 0 ;;
		*) print_usage
		   exit 1 ;;
	esac
done

export PATH="$mpidir/bin":$PATH
export PATH="$petibmdir/bin":$PATH

echo ""
echo ""
echo $descr
echo ""
echo ""

mpiexec --version
nvidia-smi

cd $scriptdir
if [ -f "$simg" ]; then
	echo "[INFO] Running within Singularity container"
	mpiexec -np $np singularity exec --nv $simg \
		petibm-decoupledibpm \
		-options_left \
		-log_view ascii:view.log
else
	echo "[INFO] Running locally"
	mpiexec -np $np petibm-decoupledibpm \
		-options_left \
		-log_view ascii:view.log
fi

exit 0
