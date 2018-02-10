from __future__ import print_function
import os
import sys
import tempfile
import subprocess
from argparse import ArgumentParser
from jinja2 import Environment, BaseLoader, Template
import textwrap

# the current directory
toplevel = os.path.split(os.path.abspath(__file__))[0]

class NERSCManager(object):
    """
    A manager to submit :mod:`pyRSD` jobs on NERSC.

    Parameters
    ----------
    job_preamble : str
        a string specifying the commands to run in the job script before
        executing the ``rsdfit`` command; these are meant to be the commands
        that load the relevant packages
    output_dir : str, optional
        the name of the directory to write the output log from the batch job
    """
    def __init__(self, job_preamble=None, output_dir='output'):

        # the job preamble string
        if job_preamble is not None:
            self.job_preamble = textwrap.dedent(job_preamble).strip()
        else:
            self.job_preamble = self.default_job_preamble

        # the output directory to store the log
        if not os.path.isdir(output_dir):
            raise ValueError(("the output directory '%s' does not exist; " %output_dir +
                              "create it to store the output job log"))
        self.output_dir = output_dir

        # parse the command-line arguments
        self.args = self.parse_args()

    def parse_args(self):
        """
        Parse command-line arguments.
        """
        # get the parser
        parser = self.parser

        # get known and unknown args
        ns, unknown = parser.parse_known_args()

        # just return the args if we are running and not submitting
        if ns.subparser_name == 'run':
            return ns

        # build the command to run the job
        command = [os.path.basename(sys.executable), sys.argv[0]] + ['run'] + unknown

        # determine the NERSC host
        host = os.environ.get('NERSC_HOST', None)
        if host is None:
             raise RuntimeError("jobs should be executed on NERSC")

        # load the template job script
        env = Environment(loader=BaseLoader())
        tpl = env.from_string(self.job_template)

        # create the output file name
        output_file = "{host}-%j.out.{cores}".format(host=host, cores=ns.cores)
        output_file = os.path.join(self.output_dir, output_file)

        # the configuration to pass to the template
        config = {}
        config['job_preamble'] = self.job_preamble
        config['output_file'] = output_file
        config['command'] = " ".join(command)
        config['partition'] = ns.partition
        config['time'] = minutes_to_job_time(ns.time)
        config['cores'] = ns.cores
        config['nodes'] = get_nodes_from_cores(ns.cores, host)
        config['haswell_config'] = "#SBATCH -C haswell" if host == 'cori' else ""
        config['job'] = 'rsdfit'

        # render the template
        rendered = tpl.render(**config)

        # echo the job script
        print(rendered)

        # submit the job!
        if not ns.dry_run:

            # write to temp file and call
            with tempfile.NamedTemporaryFile(mode='w') as ff:

                # write to temp file (and rewind)
                ff.write(rendered)
                ff.seek(0)

                # and call
                subprocess.call(["sbatch", ff.name])

        return ns

    def on_compute_node(self):
        """
        Whether we are executing on the NERSC compute node
        """
        return self.args.subparser_name == 'run'

    def add_argument(self, *args, **kwargs):
        """
        Add a command-line argument.
        """
        parser = self.parser
        self._run.add_argument(*args, **kwargs)

    @property
    def default_job_preamble(self):
        """
        The default loading preamble to use in the job script.
        """
        s = """
            # activate default environment
            source /usr/common/contrib/bccp/conda-activate.sh 3.6

            # install pyRSD and dependencies
            bcast $HOME/pyrsd-build/$NERSC_HOST/pyRSD*

            # install pyRSD_nersc
            bcast-pip git+git://github.com/nickhand/pyRSD_nersc.git
            """
        return textwrap.dedent(s)

    @property
    def job_template(self):
        """
        The jinja template string used to generate the batch job script.
        """
        # the directory where the calling script lives
        dirname = os.path.dirname(os.path.abspath(sys.argv[0]))

        s = """
            #!/bin/bash

            #SBATCH -p {{ partition }}
            #SBATCH -J {{ job }}.{{ cores }}
            #SBATCH -o {{ output_file }}
            #SBATCH -N {{ nodes }}
            #SBATCH -t {{ time }}
            {{ haswell_config }}

            # user-defined preamble (loading, etc)
            {{ job_preamble }}

            # change to the correct directory
            cd %s

            # run the script with the desired number of cores
            echo ===== Running with {{ cores }} cores =====
            srun -n {{ cores }} {{ command }}
            """ %(dirname)
        return textwrap.dedent(s).strip()

    @property
    def parser(self):
        """
        The command-line argument parser.
        """
        try:
            return self._parser
        except AttributeError:

            desc = 'submit a pyRSD rsdfit job to NERSC'
            parser = ArgumentParser(description=desc)

            # initialize the sub parsers
            subparsers = parser.add_subparsers(dest='subparser_name')

            h = 'submit the job to NERSC'
            submit = subparsers.add_parser('submit', help=h)

            h = 'the number of nodes to request'
            submit.add_argument('-n', '--cores', type=int, help=h, required=True)

            h = 'the NERSC partition to submit to'
            choices=['debug', 'regular']
            submit.add_argument('-p', '--partition', type=str, choices=choices, default='debug', help=h)

            h = 'the requested amount of time (in minutes)'
            submit.add_argument('-t', '--time', type=int, default=30, help=h)

            h = 'do a dry run -- just print the job script'
            submit.add_argument('--dry-run', action='store_true', help=h)

            self._run = subparsers.add_parser('run', help='run the job')
            self._parser = parser

        return self._parser

def minutes_to_job_time(minutes):
    """
    Convert integer minutes to the proper batch job time string.
    """
    h, m = divmod(minutes, 60)
    return "%02d:%02d:00" % (h, m)

def get_nodes_from_cores(cores, host):
    """
    Get the necessary number of nodes based on the number of cores and
    NERSC host.
    """
    if host == 'cori':
        nodes, extra = divmod(cores, 32)
    elif host == 'edison':
        nodes, extra = divmod(cores, 24)
    else:
        raise ValueError("bad host name '%s'" %host)
    # account for remainder cores
    if extra > 0: nodes += 1
    return nodes
