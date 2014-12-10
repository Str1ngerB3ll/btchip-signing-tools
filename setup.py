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
          'mnemonic==0.9',
          'btchip-python==0.1.11',
          'hidapi',
          'simplejson',
          'requests',
          'click',
          'pycoin',
          'python-dateutil'
      ],
      dependency_links=[
        'https://github.com/LedgerHQ/btchip-python/tarball/master#egg=btchip-python-0.1.11',
        'https://github.com/STRML/python-mnemonic/tarball/master#egg=mnemonic-0.9',
      ]
     )

print "Copy settings.py.example to settings.py and edit before getting started."
