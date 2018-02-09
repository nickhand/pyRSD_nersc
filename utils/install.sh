#!/bin/bash

python_dir=$HOME/local-python

# create the directory, if it does not exist
if [[ ! -d "${python_dir}" ]]
then
  mkdir $python_dir
fi

# cd to the directory
cd $python_dir

# download and install miniconda (if we need to)
if [[ ! -d "anaconda3" ]]
then
  # download
  wget https://repo.continuum.io/miniconda/Miniconda3-latest-Linux-x86_64.sh

  # install Miniconda
  bash Miniconda3-latest-Linux-x86_64.sh -p anaconda3 -b -f
fi

# download tar-anaconda.sh
wget https://raw.githubusercontent.com/nickhand/pyRSD_nersc/master/utils/tar-anaconda.sh

# activate the new environment
source anaconda3/bin/activate root

# install pyrsd
conda install --yes -c nickhand pyrsd

# install pyRSD_nersc
