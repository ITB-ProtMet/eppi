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

from distutils.core import setup

#import sys
#sys.path.insert(0, os.path.abspath('../EPPI/'))
#import EPPI

setup(name='EPPI',
      version='1.0',
      author='Pietro Brunetti',
      author_email='pietro.brunetti@itb.cnr.it',
      #url='',
      #download_url='',
      description='Experimental Proteotypic Peptides Investigator',
      #long_description=EPPI.EPPI.__doc__,
      # <- some  problems with relative importing?
      packages=['EPPI', 'EPPI.raw', 'EPPI.peptidome',
                'EPPI.peptidome.commons', 'test', 'doc'],
      #package_dir={'EPPI': 'EPPI'},
      #package_data={'EPPI': ['EPPI/faceglasses.ico']},
      data_files=[('icon', ['EPPI/faceglasses.ico']),
                  ('doc_index', ['doc/index.rst']),
                  ('fasta_ex', ['test/Cypselurus_Hbps.fasta'])],
      provides=['EPPI'],
      keywords='Mass-Spectrometry Proteomic Proteotypic',
      license='',
      classifiers=['Development Status :: 1 - Planning',
                   'Intended Audience :: Science/Research',
                   'Natural Language :: English',
                   'Operating System :: OS Independent',
                   'Programming Language :: Python :: 2',
                   'License :: OSI Approved :: Academic Free License (AFL)',
                   'Topic :: Scientific/Engineering :: Bio-Informatics',
                   'Topic :: Scientific/Engineering :: Information Analysis',
                   'Topic :: Scientific/Engineering :: Medical Science Apps.',
                  ],
     )

# setup.py

# for notes on compiler flags see:
# http://docs.python.org/install/index.html




