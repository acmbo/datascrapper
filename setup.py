#!/usr/bin/env python

from distutils.core import setup

setup(name='datascrapper',
      version='0.5',
      description='Python Scrapper for DW',
      author='acmbo',
      author_email='',
      url='',
      packages=['pymongo', 
                'random',
                'urllib',
                'beautifulsoup4',
                'torpy',
                'redis',
                'datetime'],
     )