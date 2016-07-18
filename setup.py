#!/usr/bin/env python

from distutils.core import setup

setup(name='gcalendar',
      version='0.1',
      description='Python Distribution Utilities',
      author='Tay Frost',
      author_email='tay@taybird.com',
      url='https://github.com/tay-bird/Gcalendar/',
      packages=[
          'uritemplate.py==0.3.0',
          'google-api-python-client==1.5.1'],
     )
