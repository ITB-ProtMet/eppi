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

cimport cython

class Param_Error(Exception): pass
class wrongSequence(Param_Error): pass


# Monoisotopic Molecular Weight.
# all these seq are by 10^5 !!!!
mw_map={          'A': 7103711, \
                  'R':15610111, \
                  'N':11404293, \
                  'D':11502694, \
                  'C':10300919, \
                  'E':12904259, \
                  'Q':12805858, \
                  'G': 5702146, \
                  'H':13705891, \
                  'I':11308406, \
                  'L':11308406, \
                  'K':12809496, \
                  'M':13104049, \
                  'F':14706841, \
                  'P': 9705276, \
                  'S': 8703203, \
                  'T':10104768, \
                  'W':18607931, \
                  'Y':16306333, \
                  'V': 9906841
           # we are not sure of wikipedia seq about
               # 'O':25515829
               # 'U':16896420
               }

OH = 1700274
H  =  100782
H2O = OH + H

def mi_mw(seq):
    """
    Return Monoisotopic mass for sequence passed.
    """
    cdef unsigned long mw
    try:
        mw = sum([mw_map[aa] for aa in seq])
    except KeyError:
        raise wrongSequence, "No standard AminoAcid in {0}\n".format(seq)
    else:
        return mw + H2O + H

