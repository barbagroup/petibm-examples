#!/usr/bin/env bash
# Configure, build, and install `petibm-flapping`.

scriptdir="$( cd "$(dirname "$0")" ; pwd -P )"
rootdir=$scriptdir

installdir=$rootdir
builddir="$rootdir/build"
rm -rf $builddir
mkdir -p $builddir

MPI_DIR="$HOME/software/openmpi/3.1.4/linux-gnu-opt"
export PATH="$MPI_DIR/bin":$PATH
export PETSC_DIR="$HOME/software/petsc/3.11.4"
export PETSC_ARCH="linux-gnu-openmpi-opt"
PETIBM_DIR="$HOME/software/petibm/0.4.2/linux-gnu-openmpi-opt"
YAMLCPP_DIR="$HOME/software/yaml-cpp/0.6.2/linux-gnu-opt"


cd $builddir
cmake $rootdir -DCMAKE_INSTALL_PREFIX=$installdir \
	-DCMAKE_C_COMPILER=mpicc \
	-DCMAKE_CXX_COMPILER=mpicxx \
	-DPETIBM_DIR=$PETIBM_DIR \
	-DPETSC_DIR=$PETSC_DIR \
	-DPETSC_ARCH=$PETSC_ARCH \
	-DYAMLCPP_DIR=$YAMLCPP_DIR \
	-DCMAKE_INSTALL_RPATH_USE_LINK_PATH=ON \
	-DCMAKE_BUILD_TYPE=RELEASE
