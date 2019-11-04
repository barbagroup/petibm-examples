#!/usr/bin/env bash

#SBATCH --job-name="sphRe250"
#SBATCH --output=slurm-%j.out
#SBATCH --error=slurm-%j.err
#SBATCH --partition=small-gpu
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=20
#SBATCH --time=00:20:00

module load singularity/3.4.2
module load openmpi/gcc/64/3.1.4

printf "\n*** SLURM JOB SCRIPT ***\n"
cat pegasus.slurm

printf "\n*** PRESENT WORKING DIRECTORY  ***\n"
pwd

printf "\n*** NVIDIA-SMI ***\n"
export CUDA_VISIBLE_DEVICES=0,1
nvidia-smi

simudir="/lustre/groups/barbalab/Re250"
indir="/mnt"
image="/SEAS/home/mesnardo/images/petibm-0.4.2_xenial.sif"

mpirun singularity exec \
	--bind $simudir:$indir \
	--nv $image petibm-decoupledibpm \
	-directory $indir \
	-options_left \
	-log_view ascii:$indir/view.log
