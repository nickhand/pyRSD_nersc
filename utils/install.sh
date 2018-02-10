#!/bin/bash

build_dir=$HOME/pyrsd-build

# create the directory, if it does not exist
if [[ ! -d "${build_dir}" ]]
then
  mkdir $build_dir
fi

# cd to the directory
cd $build_dir

# download and install miniconda (if we need to)
if [[ ! -d "anaconda3" ]]
then
  # download
  wget https://repo.continuum.io/miniconda/Miniconda3-latest-Linux-x86_64.sh

  # install Miniconda
  bash Miniconda3-latest-Linux-x86_64.sh -p anaconda3 -b -f
fi

# download scripts
wget https://raw.githubusercontent.com/nickhand/pyRSD_nersc/master/utils/tar-anaconda.sh
wget https://raw.githubusercontent.com/nickhand/pyRSD_nersc/master/utils/install-pyRSD.sh
wget https://raw.githubusercontent.com/nickhand/pyRSD_nersc/master/utils/environment.yml

# activate the new environment
source anaconda3/bin/activate root

# install pyRSD dependencies into new environment
if [[ ! -d "anaconda3/envs/pyrsd-anaconda-3.6" ]]
then
  conda env create --name pyrsd-anaconda-3.6 -f environment.yml
fi
source activate pyrsd-anaconda-3.6

# install pyRSD_nersc
pip install --no-deps -I git+git://github.com/nickhand/pyRSD_nersc.git

# install pyRSD
bash install-pyRSD.sh

# tar anaconda
bash tar-anaconda.sh
