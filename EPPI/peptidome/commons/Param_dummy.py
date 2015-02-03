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

""" Module to calculate the monisotopic molecular weight
   from peptide sequence"""

__authors__ = "Pietro Brunetti"

import ParamData



class Param_Error(Exception): pass
class wrongSequence(Param_Error): pass

mw_map = ParamData.Monoisotopic_AA
odd = ParamData.H2O + ParamData.H


def mi_mw(seq):
    """
    Return Monoisotopic mass for sequence passed.
    """
    try:
        mw = sum([mw_map[aa] for aa in seq])
    except KeyError:
        raise wrongSequence, "No standard AminoAcid in {0}\n".format(seq)
    else:
        return mw + odd
    
def mi_mw_np(seq):
    """
    Return Monoisotopic mass for sequence passed.
    """
    import numpy as np
    try:
        mw = np.sum([mw_map[aa] for aa in seq])
    except KeyError:
        raise wrongSequence, "No standard AminoAcid in {0}\n".format(seq)
    else:
        return mw + odd
    
if __name__ == '__main__':
    seq = 'DAGNIIIDDDDISLLPLHAR'
    print mi_mw(seq)
    print mi_mw_np(seq)
    #print mi_mw_c(seq)
    
    