# Used to define versioning, package name, and other details for package distribution on PyPi
# This file is used to build the package and upload it to PyPi so that it can be installed using pip
# TBD if I even want this

from setuptools import setup, find_packages

setup(
  name='TBD',
  version='0.1',
  packages=find_packages(),
  install_requires=[
    # add all package dependencies here
    'numpy',
    
  ],
  author='John Dunn',
  author_email='johnwdunn20@gmail.com',
  description='TBD',
  license='MIT',
  keywords='TBD',
)