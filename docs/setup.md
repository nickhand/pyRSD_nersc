# Setup instructions

## Environment Setup and Installation

The bulk of the setup is performed by the [utils/install.sh](https://github.com/nickhand/pyRSD_nersc/blob/master/utils/install.sh) script. After logging into NERSC, users should download this script using

```bash
wget https://raw.githubusercontent.com/nickhand/pyRSD_nersc/master/utils/install.sh
```

And then execute the script using

```bash
bash install.sh
```

This script performs the following steps:

- Creates a new directory: ``$HOME/local-python``
- Downloads and installs a fresh Anaconda environment to the directory ``
``$HOME/local-python/anaconda3``
- Activates the new conda environment and installs ``pyRSD`` and ``pyRSD_nersc``
- Downloads the script ``tar-anaconda.sh`` to ``$HOME/local-python`` (see the section on bundling pyRSD)

## Updating pyRSD

When the version of pyRSD is updated, users can update their version using

```bash
# activate the conda environment
source $HOME/local-python/anaconda3/bin/activate root

# update pyRSD
conda update -c nickhand pyRSD
```

## Bundling pyRSD

To efficiently use pyRSD on the computing nodes, we need to bundle pyRSD and its dependencies into a tar file that will be loaded in the job script. The loading mechanism uses ``python-mpi-bcast`` and is similar to how ``nbodykit`` is loaded in job scripts.

To create the tar file, users should execute the following command:

```bash
bash $HOME/local-python/tar-anaconda.sh
```

This will create the tar file: ``$HOME/local-python/pyrsd-anaconda.tar.gz``.
It typically takes ~2-3 minutes to build the tar file. 

**Note: whenever the version of pyRSD is updated, users should re-run the above script to create a new tar file.**
