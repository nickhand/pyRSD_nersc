#!/bin/bash

build_dir=$HOME/pyrsd-build

# create the directory, if it does not exist
if [[ ! -d "${build_dir}" ]]
then
  mkdir $build_dir
fi

# cd to the directory
cd $build_dir

# download tar scripts
wget https://raw.githubusercontent.com/nickhand/pyRSD_nersc/master/utils/tar-pyRSD.sh
wget https://raw.githubusercontent.com/nickhand/pyRSD_nersc/master/utils/tar-pyRSD-deps.sh

# load python
module load python/3.6-anaconda-4.4

# install pyRSD_nersc locally
pip install --no-deps git+git://github.com/nickhand/pyRSD_nersc.git --user

# tar pyrsd
bash tar-pyRSD.sh

# tar pyrsd dependencies
bash tar-pyRSD-deps.sh
