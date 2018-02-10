#!/bin/bash

build_dir=$HOME/pyrsd-build

# create the directory, if it does not exist
[ -d "${build_dir}" ] || mkdir $build_dir

# cd to the directory
cd $build_dir

# download and install miniconda (if we need to)
[ -f "Miniconda3-latest-Linux-x86_64.sh" ] || wget https://repo.continuum.io/miniconda/Miniconda3-latest-Linux-x86_64.sh

# install
[ -d "anaconda3" ] || bash Miniconda3-latest-Linux-x86_64.sh -p anaconda3 -b -f

# download scripts
[ -f "tar-anaconda.sh" ] || wget https://raw.githubusercontent.com/nickhand/pyRSD_nersc/master/utils/tar-anaconda.sh
[ -f "install-pyRSD.sh" ] || wget https://raw.githubusercontent.com/nickhand/pyRSD_nersc/master/utils/install-pyRSD.sh
[ -f "environment.yml" ] || wget https://raw.githubusercontent.com/nickhand/pyRSD_nersc/master/utils/environment.yml

# activate the new environment
source anaconda3/bin/activate root
[ -d "anaconda3/envs/pyrsd-anaconda-3.6" ] || conda env create --name pyrsd-anaconda-3.6 -f environment.yml

# activate new environment
source anaconda3/bin/activate pyrsd-anaconda-3.6

# install pyRSD_nersc
pip install --no-deps -I git+git://github.com/nickhand/pyRSD_nersc.git

# install pyRSD
bash install-pyRSD.sh

# tar anaconda
bash tar-anaconda.sh
