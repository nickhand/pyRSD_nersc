from setuptools import setup, find_packages
import os
from glob import glob

# the package data
package_data = glob('examples/*') + glob('utils/*')

setup(
    name='pyRSD_nersc',
    version='0.0.1',
    author='Nick Hand',
    package_data = {'pyRSD_nersc': package_data},
    packages=find_packages(),
    description="Utilities for running pyRSD on NERSC",
    install_requires=['pyRSD']
)
