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

""" Maps coding aminoacids informations """

__authors__ = "Pietro Brunetti"

import string

# the twenty knowed aminoacids
IUPAC = ['M', 'I', 'P', 'V', 'G', 'A', 'L', \
         'W', 'Y', 'F', \
         'C', 'N', 'Q', 'T', 'S', \
         'D', 'E', \
         'H', 'R', 'K']


Other = ['B', 'Z', 'J', 'X', 'U', 'O']

Groups = [
             "Al",  # Aliphatic 
             "Ar",  # Aromatic
             "NC",  # No-Charged
             "Neg", # Negative-Charged
             "Pos", # Positive-Charged
             "NU"   # No-Iupac 
            ]

# Aminoacids divided by chemical propriety
to_group  =  {'A':'Al',  'B':'NU', 'C':'NC', 'D':'Neg', 'E':'Neg', 'F':'Ar', 'G':'Al', 'H':'Pos', 
              'I':'Al',  'J':'NU', 'K':'Pos','L':'Al',  'M':'Al',  'N':'NC', 'O':'NU', 'P':'Al',
              'Q':'NC',  'R':'Pos','S':'NC', 'T':'NC',  'U':'NU',  'V':'Al', 'W':'Ar', 'X':'NU',
              'Y':'Ar',  'Z':'NU'}

names = {'A':('Ala','Alanine'),
         'R':('Arg','Arginine'),
         'N':('Asn','Asparagine'),
         'D':('Asp','Aspartic Acid'),
         'C':('Cys','Cysteine'),
         'E':('Glu','Glutamic acid'),
         'Q':('Gln','Glutamine'),
         'G':('Gly','Glycine'),
         'H':('His','Histidine'),
         'I':('Ile','Isoleucine'),
         'L':('Leu','Leucine'),
         'K':('Lys','Lysine'),
         'M':('Met','Methionine'),
         'F':('Phe','Phenilalanine'),
         'P':('Pro','Proline'),
         'S':('Ser','Serine'),
         'T':('Thr','Threonine'),
         'W':('Trp','Tryptophan'),
         'Y':('Tyr','Tyrosine'),
         'V':('Val','Valine'),
         
         'B':('Asx','Asparagine or aspartic acid'),
         'Z':('Glx','Glutamine or glutamic acid'),
         'J':('Xle','Leucine or Isoleucine'),
         'X':('Xaa','Unspecified or Unknow'),
         
         'U':('Sel','Selenocysteine'),
         'O':('Pyl','Pirrolysine')}

#no_std_trns_table = {ord('N'):'B', ord('D'):'B',
#                     ord('Q'):'Z', ord('E'):'Z',
#                     ord('L'):'J', ord('I'):'J'}
# The last one is a random deliberate author choice
#                     ord('G'):'X', ord('P'):'X'

no_std_trns_table = string.maketrans('NDQELI','BBZZJJ')