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
#

"""
It contains functions that recognize if a seq is made by  IUPAC aminoacids
"""

__authors__ = "Pietro Brunetti"

import re
import itertools

NoIUPAC = re.compile(r'[AC-IK-NP-TVWY]*[BZJXUO]{1}')
standard   = re.compile(r'[AC-IK-NP-TVWY]')
no_standard = re.compile(r'[BZJX]')
special    = re.compile(r'[OU]')
wrong = re.compile(r'[^A-Z]')

class aaError(Exception): pass
class wrongFormat(aaError): pass

def _bad_format(seq):
    """
    raises an Error if the sequence is not UPPERCASE

    :param seq: peptide or protein sequence
    :type seq: str
    """
    wrongs = wrong.findall(seq)
    if wrongs:
        raise wrongFormat, "Find {0} : {1} in {2}".format(wrongs[0],
                                                          seq.find(wrongs[0]),
                                                          seq)

def noStandard_SubPep(seq):
    """
    From a sequence returns all No IUPAC sub sequences

    >>> noStandard_SubPep('XMASLLKVDOQEVKLKVDSFRERITSEABEDLVANFFPKKLLELDSFLKEPILNIHDLTQIHSDMNLPVPDPIU')
    ['X', 'MASLLKVDO', 'QEVKLKVDSFRERITSEAB', 'EDLVANFFPKKLLELDSFLKEPILNIHDLTQIHSDMNLPVPDPIU']
    >>> noStandard_SubPep('MASLLKVDQEVKLKVDSFRERITSEAEDLVANFFPKKLLELDSFLKEPILNIHDLTQIHSDMNLPVPDPI')
    []

    :param seq: peptide or protein sequence
    :type seq: str
    :return: a list of noIupac SubPeptides
    :rtype: list
    """
    _bad_format(seq)
    return NoIUPAC.findall(seq)

def find_noStandards(seq):
    """
    From a sequence returns if it is No-IUPAC formatted

    >>> find_noStandards('XMASLLKVDOQEVKLKVDSFRERITSEABEDLVANFFPKKLLELDSFLKEPILNIHDLTQIHSDMNLPVPDPIU')
    0
    >>> find_noStandards('MASLLKVDQEVKLKVDSFRERITSEAEDLVANFFPKKLLELDSFLKEPILNIHDLTQIHSDMNLPVPDPI')
    -1

    :param seq: peptide or protein sequence
    :typeseq: str
    :return: if there are no standard aminoacids
    :rtype: bool
    """

    _bad_format(seq)
    matchy = NoIUPAC.match(seq)
    if matchy == None: 
        return -1
    else: 
        return matchy.end()-1

def Poz_noStandards(seq):
    """
    Positions of No Standard aminoacids inside a given sequence

    >>> Poz_noStandards('XMASLLKVDOQEVKLKVDSFRERITSEABEDLVANFFPKKLLELDSFLKEPILNIHDLTQIHSDMNLPVPDPIU')
    [0, 9, 28, 73]
    >>> Poz_noStandards('MASLLKVDQEVKLKVDSFRERITSEAEDLVANFFPKKLLELDSFLKEPILNIHDLTQIHSDMNLPVPDPI')
    []

    :param seq: peptide or protein sequence
    :typeseq: str
    :return: a list of position of all no-stardard aminoacids
    :rtype: list
    """
    _bad_format(seq)
    subpepts = noStandard_SubPep(seq)
    positions = []
    p = 0
    for subpept in subpepts:
        p += len(subpept)
        positions.append(p)
    return [paa-1 for paa in positions]

def _seq2tags(seq, minus=standard, caret=no_standard, bang=special):
    """
    From a sequence returns a new string that use:
    * '-' that accounts for standard aa
    * '^' that accounts for ambiguous aa
        * B - Asparagine or aspartic acid
        * Z - Glutamine or glutamic acid
        * J - Leucine or Isoleucine
        * X - Unspecified or unknown amino acid
    * '!' that accounts for special aa
        * O - Pyrrolysine
        * U stands for Selenocysteine.

    >>> _seq2tags('XMASLLKVDOQEVKLKVDSFRERITSEABEDLVANFFPKKLLELDSFLKEPILNIHDLTQIHSDMNLPVPDPIU')
    '^--------!------------------^--------------------------------------------!'
    >>> _seq2tags('MASLLKVDQEVKLKVDSFRERITSEAEDLVANFFPKKLLELDSFLKEPILNIHDLTQIHSDMNLPVPDPI')
    '----------------------------------------------------------------------'

    :param seq: peptide or protein sequence
    :typeseq: str
    :param minus: regular expression accounting for IUPAC standard amminoacids
    :typeminus: re
    :param caret: regular expression accounting for ambiguous amminoacids
    :typecaret: re
    :param bang: regular expression accounting for special amminoacids
    :typeminus: re
    :return: a string that encode where are different type of aminoacids
    :rtype: string
    """
    _bad_format(seq)
    s1 = minus.sub('-', seq)
    s1 = caret.sub('^', s1)
    s1 = bang.sub('!', s1)
    return s1

def noStandardSeq(seq):
    """
    Nice print for sequence with No Standard aminoacids

    >>> print noStandardSeq('MASLLKVDQEVKLKVDSFRERITSEAEDLVANFFPKKLLELDSFLKEPIL')
    MASLLKVDQEVKLKVDSFRERITSEAEDLVANFFPKKLLELDSFLKEPIL
    --------------------------------------------------
    >>> print noStandardSeq('XMASLLKVDOQEVKLKVDSFRERITSEABEDLVANFFPKKLLELDSFLKE')
    XMASLLKVDOQEVKLKVDSFRERITSEABEDLVANFFPKKLLELDSFLKE
    ^--------!------------------^---------------------

    :param seq: peptide or protein sequence
    :typeseq: str
    :return: a multi-line string that encode where are different type of aminoacids
    :rtype: string
    """
    _bad_format(seq)
    import textwrap as tw
    s = tw.wrap(seq, width=50)
    si= tw.wrap(_seq2tags(seq), width=50)
    tot = []
    for pieces in itertools.izip(s, si):
        tot.extend(pieces)
    return  "\n".join(tot)

if __name__ == "__main__":
    import doctest
    doctest.testmod()
