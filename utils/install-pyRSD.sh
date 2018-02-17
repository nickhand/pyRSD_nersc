#!/bin/bash

build_dir=$HOME/pyrsd-build

# create the directory, if it does not exist
[ -d "${build_dir}" ] || mkdir $build_dir

# cd to the directory
cd $build_dir

# load fftw
module unload fftw || true
module load fftw/3.3.4.6

# load gnu environment
module unload PrgEnv-intel || true
module load PrgEnv-gnu

# load swig
module load swig

# tar pyRSD
pip install -vvv -I --no-deps --global-option=build_ext --global-option="-I$FFTW_INC" pyRSD
