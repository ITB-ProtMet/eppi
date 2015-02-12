# -*- coding: utf-8 -*-

# Copyright 2015 Pietro Brunetti <pietro.brunetti@itb.cnr.it>
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from setuptools import setup
from setuptools import find_packages

setup(name='EPPI',
      version='2.0',
      author='Pietro Brunetti',
      author_email='pietro.brunetti@itb.cnr.it',
      url='https://github.com/ITB-ProtMet/eppi',
      license='Apache2',
      description='Experimental Proteotypic Peptides Investigator',
      packages=find_packages(),
      package_data={'EPPI': ['EPPI/faceglasses.ico']},
      install_requires=[
          'xlrd',
          'matplotlib',
          'wx',
          'jinja2',
          'ctypes'
      ]
      #provides=['EPPI'],
      #keywords='Mass-Spectrometry Proteomic Proteotypic',
      # classifiers=['Development Status :: 1 - Planning',
      #             'Intended Audience :: Science/Research',
      #             'Natural Language :: English',
      #             'Operating System :: OS Independent',
      #             'Programming Language :: Python :: 2',
      #             'License :: OSI Approved :: Academic Free License (AFL)',
      #             'Topic :: Scientific/Engineering :: Bio-Informatics',
      #             'Topic :: Scientific/Engineering :: Information Analysis',
      #             'Topic :: Scientific/Engineering :: Medical Science Apps.'],
     )
