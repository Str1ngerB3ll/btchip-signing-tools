#!/usr/bin/env python
from setuptools import setup, find_packages
from os.path import dirname, join

here = dirname(__file__)

setup(name='btchip-signer',
      version='0.1',
      description='Signing utilities for owners of BTChips',
      long_description=open(join(here, 'README.md')).read(),
      author='Samuel Reed',
      author_email='sam@bitmex.com',
      url='',
      install_requires=[
          'pycoin',
          'bitcoin-python',
          'mnemonic'
      ],
      dependency_links=['https://github.com/LedgerHQ/btchip-python/tarball/master#egg=package-1.0']
     )

print "Copy settings.py.example to settings.py and edit before getting started."
