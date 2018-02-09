"""
An example script to show submit an rsdfit job script to NERSC.

This can be executed via:

>>> python nersc_submit.py submit -n 32 -p debug -t 30 --dry-run

Note: when actually submitting, remove the "--dry-run" flag.

The help message for submitting jobs can be displayed using:

>>> python nersc_submit.py submit -h
"""
import os
from pyRSD_nersc import BatchRSDFitDriver, NERSCManager

# define the host so script will work not on NERSC (for testing)
os.environ['NERSC_HOST'] = 'cori'

def main():

    # the template parameter file
    template = 'params.template'

    # the name of the model to load
    model_file = 'model.npy'

    # the base output directory
    # results will be saved to results_box-1, results_box-2, etc..
    output = 'results'

    # number of iterations to run
    iterations = 10

    # initialize the batch driver
    d = BatchRSDFitDriver(template, model_file, output, iterations)

    # run 3 rsdfit tasks, updating the "box" value in the template file
    d.run('box', [1, 2, 3])

if __name__ == '__main__':

    # initialize NERSC manager
    manager = NERSCManager(output_dir='job_output')

    # run the job! (will only run from job script)
    if manager.on_compute_node():
        main()
