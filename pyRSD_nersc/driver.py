import os
from mpi4py import MPI
from jinja2 import Environment, PackageLoader, meta, FileSystemLoader
import tempfile
import six

class RSDFitDriver(object):
    """
    A driver class to run execute ``rsdfit`` from the :mod:`pyRSD` package.

    Parameters
    ----------
    mode : str, {'mcmc', 'nlopt'}
        the type of fit we want to run
    param_file : str
        the name of an existing parameter file to pass to ``rsdfit``
    model_file : str
        the name of an existing model file to load and pass to ``rsdfit``
    output_dir : str
        the name of the directory to save the output of ``rsdfit`` to
    iterations : int
        the number of iterations to run
    walkers : int, optional
        the number of walkers to use when running in 'mcmc' mode
    nchains : int, optional
        the number of independent chains to run in 'mcmc' mode
    comm : optional
        the MPI communicator to use
    """
    def __init__(self, mode, param_file, model_file, output_dir,
                    iterations, walkers=None, nchains=None, comm=None):

        if mode not in ['mcmc', 'nlopt']:
            raise ValueError("'mode' should be 'mcmc' or 'nlopt'")

        if mode == 'mcmc' and walkers is None:
            raise ValueError("'walkers' should be specified for mcmc runs")

        for f in [param_file, model_file]:
            if not os.path.isfile(f):
                raise ValueError("no such file '%s'" %f)

        self.mode = mode
        self.param_file = param_file
        self.model_file = model_file
        self.output_dir = output_dir
        self.iterations = iterations
        self.walkers = walkers
        self.nchains = nchains

        # determine the communicator
        if comm is None:
            comm = MPI.COMM_WORLD
        self.comm = comm

    def run(self):
        """
        Call the ``rsdfit`` command.
        """
        from pyRSD.rsdfit.util import rsdfit_parser
        from pyRSD.rsdfit import rsdfit

        # build the rsdfit argument list
        args = [self.mode, '-p', self.param_file, '-m', self.model_file]
        args += ['-i', str(self.iterations), '-o', self.output_dir]
        if self.walkers is not None:
            args += ['-w', str(self.walkers)]
        if self.nchains is not None:
            args += ['--nchains', str(self.nchains)]

        # parse the args passed to rsdfit
        print(args)
        args = rsdfit_parser().parse_args(args)
        args = vars(args)

        # initialize and run the RSDFit driver
        mode = args.pop('subparser_name')
        driver = rsdfit.RSDFitDriver(self.comm, mode, **args)
        driver.run()

class BatchRSDFitDriver(object):
    """
    A driver class to iterate through a set of ``rsdfit`` commands.

    .. note::
        This only runs ``rsdfit`` in "nlopt" mode (not "mcmc") mode.

    Parameters
    ----------
    param_template : str
        the name of an existing template parameter file; this file should
        use jinja syntax (i.e., ``{{ key }}``) to specify the keys that
        will be updated for each iteration
    model_file : str
        the name of an existing model file to load and pass to ``rsdfit``
    base_output : str
        the base name of the results directory; for each iteration, the 
        results name will be the concatenation of this base name and the
        key/value pairs being iterated over
    iterations : int
        the number of iterations to run for each fit
    """
    def __init__(self, param_template, model_file, base_output, iterations):

        for f in [param_template, model_file]:
            if not os.path.isfile(f):
                raise ValueError("no such file '%s'" %f)

        self.mode = 'nlopt'
        self.param_template = os.path.abspath(param_template)
        self.model_file = model_file
        self.base_output = base_output
        self.iterations = iterations

    def _make_param_file(self, kws):
        """
        Internal function to create a temporary file holding the parameters
        to pass to ``rsdfit``

        Parameters
        ----------
        kws : dict
            the parameters to pass to the jinja template file

        Returns
        -------
        filename : str
            the name of the temporay parameter file
        """
        # jinja environ
        dirname, filename = os.path.split(self.param_template)
        env = Environment(loader=FileSystemLoader(dirname))

        # render the template
        tpl = env.get_template(filename)
        params = tpl.render(**kws)

        # make the parameter file
        with tempfile.NamedTemporaryFile(mode='wb', delete=False) as ff:
            ff.write(params.encode())

        return ff.name

    def _verify_template(self, keys):
        """
        Internal function that verifies all of the necessary keys in the
        template file were input by the user.
        """
        # jinja environ
        dirname, filename = os.path.split(self.param_template)
        env = Environment(loader=FileSystemLoader(dirname))

        # read the template source and extract keys
        template_source = env.loader.get_source(env, filename)[0]
        parsed_content = env.parse(template_source)
        needed = meta.find_undeclared_variables(parsed_content)

        missing = needed - set(keys)
        if len(missing):
            msg = "the following keys in the template file have not been declared: "
            msg += str(missing)
            raise ValueError(msg)

    def run(self, keys, values):
        """
        Iterate through a set of values, generating a new parameter file on
        each iteration, and then running the ``rsdfit`` nlopt command.

        Given a set of MPI ranks, a single rank is assigned to each
        task and all the tasks are iterated through until none are left.

        See "batch-example" directory for example use.

        Parameters
        ----------
        keys : str or list of str
            the name or list of names of the keys in the template parameter
            file that we are replacing on each iteration
        values : list
            the list of values to iterate through, where each value
            corresponds to the names in ``keys``
        """
        try:
            from nbodykit.lab import TaskManager
        except:
            raise ImportError("please install nbodykit!")

        if isinstance(keys, six.string_types):
            keys = [keys]

        # verify the template
        self._verify_template(keys)

        # run with 1 core per task
        with TaskManager(cpus_per_task=1, use_all_cpus=True) as tm:

            # iterate through the values in parallel
            for value in tm.iterate(values):

                # make into tuple
                if not isinstance(value, tuple):
                    value = (value,)

                # check length consistency
                if len(value) != len(keys):
                    raise ValueError("mismatch between length of keys and values when iterating")

                # make the parameter file
                kws = dict(zip(keys, value))
                param_file = self._make_param_file(kws)

                # tag the output file
                tag = '_'.join(['%s-%s' %(k,v) for (k,v) in kws.items()])
                output_dir = self.base_output + '_' + tag

                # the driver arguments
                args = {}
                args['mode'] = self.mode
                args['param_file'] = param_file
                args['model_file'] = self.model_file
                args['output_dir'] = output_dir
                args['iterations'] = self.iterations
                args['comm'] = tm.comm

                # initialize and run
                driver = RSDFitDriver(**args)
                driver.run()

                # remove the temporary parameter file
                if os.path.exists(param_file):
                    os.remove(param_file)
