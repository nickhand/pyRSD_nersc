#!/bin/bash

build_dir=$HOME/pyrsd-build

# create the directory, if it does not exist
if [[ ! -d "${build_dir}" ]]
then
  mkdir $build_dir
fi

# cd to the directory
cd $build_dir

# create the directory, if it does not exist
if [[ ! -d "${NERSC_HOST}" ]]
then
  mkdir $NERSC_HOST
fi

# load fftw
module load fftw

# install
fname=$NERSC_HOST/pyRSD.tar.gz
CFLAGS=-fPIC /usr/common/contrib/bccp/python-mpi-bcast/tar-pip.sh $fname --global-option=build_ext --global-option="-I$FFTW_INC" pyRSD
