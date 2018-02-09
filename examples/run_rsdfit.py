"""
An example script to show how to iterate through a set of rsdfit "nlopt"
commands.

As an example, this can be executed from the command line:

>> mpirun -n 4 python run_rsdfit.py
"""
from pyRSD_nersc import RSDFitDriver

def main():

    # the parameter file
    params = 'params.dat'

    # the name of the model to load
    model_file = 'model.npy'

    # the output directory
    output = 'results'

    # number of iterations to run
    iterations = 10

    # run in mcmc mode (can also do nlopt here)
    mode = 'mcmc'

    # initialize the driver
    d = RSDFitDriver(mode, params, model_file, output, iterations, walkers=30)

    # run 10 MCMC iterations
    d.run()


if __name__ == '__main__':
    main()
