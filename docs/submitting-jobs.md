# Submitting pyRSD jobs on NERSC

The ``NERSCManager`` object provides functionality for submitting
jobs to NERSC. It can be imported in a Python script using

```python
from pyRSD_nersc import NERSCManager
```

The file ["nersc_submit.py"](../examples/nersc_submit.py) provides an example
use case for submitting jobs to NERSC. In this case, the ``rsdfit`` job is the
same batch job from [run_batch_rsdfit.py](../examples/run_batch_rsdfit.py).
In this case, we initialize an ``NERSCManager`` object and make sure to
only execute the main function if we are on the NERSC compute nodes.
This is achieved in a few lines of code:

```python
# initialize NERSC manager
manager = NERSCManager(output_dir='job_output')

# run the job! (will only run on compute nodes)
if manager.on_compute_node():
    main()
```

Here, the ``main()`` function iterates through the
desired set of ``rsdfit`` commands using the ``BatchRSDFitDriver`` object.
See the [guide to calling ``rsdfit`` from a Python script](rsdfit-driver.md)
for notes on how to use the ``BatchRSDFitDriver`` object.

**Note:** the ``output_dir`` keyword above specifies the directory where the
output log file from the NERSC job will be stored. This directory must
already exist when running the script, or an exception will be raised.

The ``NERSCManager`` object has two modes: "submit" and "run". Users will
always use it in the "submit" mode, which allows users to specify the
NERSC job specifics: time length, partition name, and number of cores. These
options are all specified via command-line arguments. When the user
specifies these values, the ``NERSCManager`` object will
automatically generate the necessary job script. This generated job
script will
include a command that re-runs the Python script in "run" mode using the
requested number of CPUs. When in "run" mode, the script will simply
execute the ``main()`` function, which runs the desired ``rsdfit`` commands.

As an example, we can submit the batch ``rsdfit`` example job to
the "debug" queue on Cori using 32 cores (1 node) for 30 minutes using:

```bash
python nersc_submit.py submit -n 32 -p debug -t 30 --dry-run
```

**Note**: when actually submitting on NERSC, remove the "--dry-run" flag.

This command will automatically generate and submit
(using the ``sbatch`` command) the following job script:

```
#!/bin/bash

#SBATCH -p debug
#SBATCH -J rsdfit.32
#SBATCH -o job_output/cori-%j.out.32
#SBATCH -N 1
#SBATCH -t 00:30:00
#SBATCH -C haswell

# user-defined preamble (loading, etc)

# activate environment
source /usr/common/contrib/bccp/conda-activate.sh 3.6

# install pyRSD
bcast $HOME/local-python/pyrsd-anaconda.tar.gz

# install NERSC specific environment
bcast /usr/common/contrib/bccp/anaconda3/envs/bcast-anaconda-3.6.tar.gz

# change to the correct directory
cd /Users/nhand/Research/Programs/pyRSD_nersc/examples

# run the script with the desired number of cores
echo ===== Running with 32 cores =====
srun -n 32 python nersc_submit.py run
```

The job script first loads ``nbodykit`` and ``pyRSD`` on the compute
nodes. Be sure to see [the setup instructions](setup.md) to make sure
the file ``$HOME/local-python/pyrsd-anaconda.tar.gz`` exists. Finally,
we see that the same Python script that we called to submit the job  (``"nersc_submit.py"``) is executed in "run" mode,
using the 32 cores that we requested when we submitted the job.
