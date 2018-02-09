#!/bin/bash

# the anaconda directory
conda_dir=$HOME/local-python/anaconda3

# the output filename
fname=pyrsd-anaconda.tar.gz

OUTPUT=`readlink -f $conda_dir/envs/$fname`
(
cd $conda_dir
list=
for dir in bin lib include share; do
    if [ -d $dir ]; then
        list="$list $dir"
    fi
done
tar -h --hard-dereference -czf $OUTPUT \
    --exclude='*.html' \
    --exclude='*.jpg' \
    --exclude='*.jpeg' \
    --exclude='*.png' \
    --exclude='*.pyc' \
    --exclude='*.pyo' \
    --exclude='mpl_toolkits/basemap/data/*' \
    --exclude='pandas/io/tests/data/*' \
    --exclude='*.csv' \
    --exclude='*.dta' \
    --exclude='*.xls' \
    --exclude='*.mat' \
    --exclude='*.arff' \
    --exclude='*.h5' \
    --exclude='*.ipynb' \
    --exclude='*.svg' \
    --exclude='libreadline.so.6' \
    --exclude='libreadline.so' \
    $list
)
# black-list readline due to https://github.com/ContinuumIO/anaconda-issues/issues/1701
exit 0
