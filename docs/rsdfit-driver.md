# Calling rsdfit from a Python script

To more easily submit pyRSD ``rsdfit`` jobs on NERSC, it is necessary
to be able to execute ``rsdfit`` commands from within a Python script (rather than on the command-line using the ``rsdfit`` executable).

In this guide, we'll walk through two example files that are
included in the [examples](../examples) directory:

1. [run_rsdfit.py](../examples/run_rsdfit.py)
2. [run_batch_rsdfit.py](../examples/run_batch_rsdfit.py)


## Running a single fit

The file ["run_rsdfit.py"](../examples/run_rsdfit.py) uses the class
``RSDFitDriver`` to execute the ``rsdfit`` command from within
a Python script. This class can be imported from ``pyRSD_nersc`` using

```python
from pyRSD_nersc import RSDFitDriver
```

The arguments needed to initialize this object are:


- **mode** : str; "mcmc" or "nlopt"<br>
    the type of fit we want to run
- **param_file** : str <br>
    the name of an existing parameter file that will be passed to ``rsdfit``; this replaces the ``-p`` argument of ``rsdfit``
- **model_file** : str <br>
    the name of an existing model file to load and pass to ``rsdfit``;
    this replaces the ``-m`` argument of ``rsdfit``
- **output_dir** : str <br>
    the name of the directory to save the output of ``rsdfit`` to; this
    replaces the ``-o`` argument of ``rsdfit``
- **iterations** : int <br>
    the number of iterations to run during the fit; this replaces the
    ``-i`` argument of ``rsdfit``
- **walkers** : int, optional <br>
  the number of walkers to use when running in "mcmc" mode; this replaces
  the ``-w`` argument of ``rsdfit``
- **nchains** : int, optional <br>
    the number of independent chains to run in "mcmc" mode; this replaces
    the ``--nchains`` argument of ``rsdfit``

Once initialized, the fit can be executed the ``run()`` function,

```python
driver = RSDFitDriver(...)
driver.run()
```

The [run_rsdfit.py](../examples/run_rsdfit.py) file provides a full working
example. Users can run the example fit by executing the script,


```bash
cd examples
python run_rsdfit.py
```

## Iterating through multiple fits

The file ["run_batch_rsdfit.py"](../examples/run_batch_rsdfit.py)
provides an example of iterating through multiple pyRSD fits from within
a Python script. In this example, we have three sets of input data
and parameters that we wish to fit, located in ``examples/box1``,
``examples/box2``, and ``examples/box2``. In this case, everything is the
same except for the box number (1, 2, or 3). The ``BatchRSDFitDriver``
object provides the user with functionality to iterate through these
fits, updating the box number for each iteration and running ``rsdfit``.

The user must supply a **template parameter file** to initialize a ``BatchRSDFitDriver`` object. Then, the template parameter file is updated
after each iteration with the key/value pairs specified by the user. For example, in [run_rsdfit.py](../examples/run_rsdfit.py), we specify the iteration key to be ``"box"``, with values ``[1, 2, 3]``.

The template parameter file uses Jinja syntax to update the key/values
for each iteration. This means that anything between double curly
brackets will be updated. For example,
[the example template file](../examples/params.template) includes the
line

```bash
data.data_file = 'box{{ box }}/poles.dat'
```

which specifies that the data file name should be updated during
each iteration. At each iteration, a new parameter file will be generated
with the keys filled in with the appropriate value. For example on the
first iteration, the data file name will be set to "box1/poles.dat".

Once initialized, the fit can be executed the ``run()`` function, and
the user must supply the key/value pairs to iterate through

```python
driver = BatchRSDFitDriver(...)
driver.run("box", [1, 2, 3])
```

Multiple keys can also be updated in the template parameter file
at each iteration. In this case, the values should be a list of tuples,

```python
driver.run(['key1', 'key2'], [(1, 'value1'), (2, 'value2')])
```
In this example, the first iteration is updated using
``{'key1': 1, 'key2': 'value1'}`` and the second iteration uses
``{'key1': 2, 'key2': 'value2'}``.

**Note: currently only "nlopt" fits can be executed when using the
BatchRSDFitDriver object**.

The ``BatchRSDFitDriver`` object can iterate through the fits in parallel,
running each fit with a single process. For example, we can run the
example using

```bash
cd examples/
mpirun -n 4 python run_batch_rsdfit.py
```

With 4 total processes and 3 total fits (``box=[1, 2, 3]``), the fits will
be run in parallel. 
