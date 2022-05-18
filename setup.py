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
                'datetime',
                'setuptools',
                'wheel',
                'spacy'],
      install_requires=['spacy',
                        'en_core_web_sm @ https://github.com/explosion/spacy-models/releases/download/en_core_web_sm-2.0.0/en_core_web_sm-2.0.0.tar.gz',],
     )