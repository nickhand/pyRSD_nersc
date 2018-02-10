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

# needed to build george
pip install pybind11 --user

# tar pyRSD dependencies
fname=$NERSC_HOST/pyRSD-deps.tar.gz
/usr/common/contrib/bccp/python-mpi-bcast/tar-pip.sh $fname -v emcee autograd lmfit xarray pybind11 george
