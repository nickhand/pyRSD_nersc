# Setup instructions

## Environment Setup and Installation

The bulk of the setup is performed by the [utils/install.sh](../utils/install.sh) script. After logging into NERSC, users should download this script using

```bash
wget https://raw.githubusercontent.com/nickhand/pyRSD_nersc/master/utils/install.sh
```

And then execute the script using

```bash
bash install.sh
```

This script performs the following steps:

- Creates a new directory: ``$HOME/pyrsd-build``
- Downloads and installs a fresh Anaconda environment to the directory
``$HOME/pyrsd-build/anaconda3``
- Activates the new conda environment and installs ``pyRSD`` and ``pyRSD_nersc``
- Downloads the script [tar-anaconda.sh](../utils/tar-anaconda.sh) to the ``$HOME/pyrsd-build`` directory (see the section on bundling pyRSD)

## Updating pyRSD

When the version of pyRSD is updated, users can update their version using

```bash
# re-install a fresh pyRSD with the latest version
bash $HOME/pyrsd-build/install-pyRSD.sh
```

## Bundling pyRSD

To efficiently use pyRSD on the computing nodes, we need to bundle pyRSD and
its dependencies into a tar file that will be loaded in the job script. The
loading mechanism uses ``python-mpi-bcast`` and is similar to how ``nbodykit``
is loaded in job scripts.

To create the tar file, users should execute the following command:

```bash
bash $HOME/pyrsd-build/tar-anaconda.sh
```

This will create the tar file:
``$HOME/pyrsd-build/anaconda3/envs/pyrsd-anaconda-3.6.tar.gz``.
It typically takes ~2-3 minutes to build the tar file.

**Note: whenever the version of pyRSD is updated, users should re-run the
above script to create a new tar file.**
