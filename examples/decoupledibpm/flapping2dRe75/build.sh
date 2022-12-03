#!/usr/bin/env bash

scriptdir="$( cd "$(dirname "$0")" ; pwd -P )"
rootdir=$scriptdir

# Install make and cmake to build the petibm application
apt-get update
apt-get install --yes make cmake

# Build/install petibm application
builddir="$rootdir/build"
mkdir -p $builddir
cd $builddir
cmake $rootdir \
    -DCMAKE_INSTALL_PREFIX=$PETIBM_DIR \
    -DCMAKE_C_COMPILER=mpicc \
    -DCMAKE_CXX_COMPILER=mpicxx \
    -DPETIBM_DIR=$PETIBM_DIR \
    -DPETSC_DIR=$PETSC_DIR \
    -DPETSC_ARCH="" \
    -DYAMLCPP_DIR=$PETIBM_DIR \
    -DCMAKE_INSTALL_RPATH_USE_LINK_PATH=ON \
    -DCMAKE_BUILD_TYPE=RELEASE
make all
make install
rm -rf $builddir
