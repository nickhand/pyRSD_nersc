"""
An example script to show how to iterate through a set of rsdfit "nlopt"
commands.

As an exmplae, this can be executed from the command line:

>> mpirun -n 4 python run_batch_rsdfit.py
"""
from pyRSD_nersc import BatchRSDFitDriver

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
    main()
