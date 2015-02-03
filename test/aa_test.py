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

__author__ = 'Pietro Brunetti'

from EPPI.peptidome.commons import aa
from EPPI.peptidome.commons import aaData

import unittest
import string

class aaRECases(unittest.TestCase):

    No_Standard = "B Z J X".split()
    Special = ['O', 'U']

    IUPACSequences = [
        ''.join(aaData.IUPAC), # the twenty know aminoacids
        # random sequences from Aspergillus sojae fasta
        "GGEQPQIVKGVTTQIADDTARTIEKWEIKKAYKFGGD",
        "QYQRYMHMSNTNIIIAQRANDKAALALSSFIHALFELECYAVARLVVKENKPPVIVLLAG",
        "RRKIALVTNGQGRMSDEDLGEIVKKVKEDNIE",
        "VVSAAEKRGIKLLIPLVNNWDDYGGMNAYV",
        "KGAIDTFVRCMAIDCGDKKITVNAVAPGAIKTDMFLAVSREYIPNG",
        "PENAHEPALQLSEKLLASVGKGWASRVYFSDDGSTAVEVA",
        "QGNHAKSLRLSVKASLQKLQTDYIDLLYVHMWDFTTSVEEVMRSLNHLVANG"
    ]
    
    No_std_IUPAC_examples = [
        ("XGGEQPQIVKGVTTQIADDTARTIEKWEIKKAYKFGGD",0),
        #("GXGEQPQIVKGVTTQIADDTARTIEKWEIKKAYKFGGD",1),
        ("GGXEQPQIVKGVTTQIADDTARTIEKWEIKKAYKFGGD",2),
        ("GGEXQPQIVKGVTTQIADDTARTIEKWEIKKAYKFGGD",3),
        ("GGEQXPQIVKGVTTQIADDTARTIEKWEIKKAYKFGGD",4),
        ("GGEQPXQIVKGVTTQIADDTARTIEKWEIKKAYKFGGD",5),
        ("XGGEQPQIVKGVTTQIADDTARTIEXKWEIKKAYKFGGD",0),
        ("GXGEQPQIVKGVTTQIADDTARTIEKWXEIKKAYKFGGD",1),
        ("GGXEQPQIVKGVTTQIADDTARTIEKWEIXKKAYKFGGD",2),
        ("GGEXQPQIVKGVTTQIADDTARTIEKWEIKKXAYKFGGD",3),
        ("GGEQXPQIVKGVTTQIADDTARTIEKWEIKKAYXKFGGD",4),
        ("GGEQPXQIVKGVTTQIADDTARTIEKWEIKKAYKFXGGD",5),
        
        ]

    no_standard_Sequences = [s.translate(aaData.no_std_trns_table) for s in IUPACSequences]

    spl_trns_table = string.maketrans('CGL','UUO')
    special_Sequences = [s.translate(spl_trns_table) for s in IUPACSequences]

    wrongSequences = [(s.lower(),
                      s.replace('G', '@', 1),
                      s.replace('G', ' ', 1),
                      s.replace('G', '7', 1)) for s in IUPACSequences]

    def test_NoIUPAC_RE_right(self):
        for c in self.Special:
            self.assertRegexpMatches(c, aa.NoIUPAC)
        for c in self.No_Standard:
            self.assertRegexpMatches(c, aa.NoIUPAC)
        for s in self.no_standard_Sequences:
            self.assertRegexpMatches(s, aa.NoIUPAC)
        for s in self.special_Sequences:
            self.assertRegexpMatches(s, aa.NoIUPAC)

    def test_NoIUPAC_RE_wrong(self):
        for c in aaData.IUPAC:
            self.assertNotRegexpMatches(c, aa.NoIUPAC)
        for c in string.lowercase:
            self.assertNotRegexpMatches(c, aa.NoIUPAC)
        for c in string.digits:
            self.assertNotRegexpMatches(c, aa.NoIUPAC)
        for c in string.punctuation:
            self.assertNotRegexpMatches(c, aa.NoIUPAC)
        for c in string.whitespace:
            self.assertNotRegexpMatches(c, aa.NoIUPAC)
        for q in self.wrongSequences:
            for s in q:
                self.assertNotRegexpMatches(s, aa.NoIUPAC)
        for s in self.IUPACSequences:
            self.assertNotRegexpMatches(s, aa.NoIUPAC)

    def test_Standard_RE_right(self):
        for c in aaData.IUPAC:
            self.assertRegexpMatches(c, aa.standard)
        for s in self.IUPACSequences:
            self.assertRegexpMatches(s, aa.standard)

    def test_Standard_RE_wrong(self):
        for c in self.Special:
            self.assertNotRegexpMatches(c, aa.standard)
        for c in self.No_Standard:
            self.assertNotRegexpMatches(c, aa.standard)
        for c in string.lowercase:
            self.assertNotRegexpMatches(c, aa.standard)
        for c in string.digits:
            self.assertNotRegexpMatches(c, aa.standard)
        for c in string.punctuation:
            self.assertNotRegexpMatches(c, aa.standard)
        for c in string.whitespace:
            self.assertNotRegexpMatches(c, aa.standard)

    def test_NoStandard_RE_right(self):
        for c in self.No_Standard:
            self.assertRegexpMatches(c, aa.no_standard)
        for s in self.no_standard_Sequences:
            self.assertRegexpMatches(s, aa.no_standard)

    def test_NoStandard_RE_wrong(self):
        for c in self.Special:
            self.assertNotRegexpMatches(c, aa.no_standard)
        for c in aaData.IUPAC:
            self.assertNotRegexpMatches(c, aa.no_standard)
        for c in string.lowercase:
            self.assertNotRegexpMatches(c, aa.no_standard)
        for c in string.digits:
            self.assertNotRegexpMatches(c, aa.no_standard)
        for c in string.punctuation:
            self.assertNotRegexpMatches(c, aa.no_standard)
        for c in string.whitespace:
            self.assertNotRegexpMatches(c, aa.no_standard)

    def test_special_RE_right(self):
        for c in self.Special:
            self.assertRegexpMatches(c, aa.special)
        for s in self.special_Sequences:
            self.assertRegexpMatches(s, aa.special)

    def test_special_RE_wrong(self):
        for c in self.No_Standard:
            self.assertNotRegexpMatches(c, aa.special)
        for c in aaData.IUPAC:
            self.assertNotRegexpMatches(c, aa.special)
        for c in string.lowercase:
            self.assertNotRegexpMatches(c, aa.special)
        for c in string.digits:
            self.assertNotRegexpMatches(c, aa.special)
        for c in string.punctuation:
            self.assertNotRegexpMatches(c, aa.special)
        for c in string.whitespace:
            self.assertNotRegexpMatches(c, aa.special)

    def test_wrong_RE_right(self):
        for c in string.lowercase:
            self.assertRegexpMatches(c, aa.wrong)
        for c in string.digits:
            self.assertRegexpMatches(c, aa.wrong)
        for c in string.punctuation:
            self.assertRegexpMatches(c, aa.wrong)
        for c in string.whitespace:
            self.assertRegexpMatches(c, aa.wrong)
        for q in self.wrongSequences:
            for s in q:
                self.assertRegexpMatches(s, aa.wrong)

    def test_wrong_RE_wrong(self):
        for c in self.No_Standard:
            self.assertNotRegexpMatches(c, aa.wrong)
        for c in aaData.IUPAC:
            self.assertNotRegexpMatches(c, aa.wrong)
        for c in self.Special:
            self.assertNotRegexpMatches(c, aa.wrong)

class aaFunctionCases(unittest.TestCase):

    no_std_subPep = (("BGGEQPQ", ["B"]),
                     ("GGEQPQZ", ["GGEQPQZ"]),
                     ("GGEZQPQ", ["GGEZ"]),
                     ("GGEJXQPQ", ["GGEJ", "X"]),
                     ("GJGEXQPBQ", ["GJ", "GEX", "QPB"]))

    no_std_poz = (("BGGEQPQ", [0]),
                  ("GGEQPQZ", [6]),
                  ("GGEZQPQ", [3]),
                  ("GGEJXQPQ", [3, 4]),
                  ("GJGEXQPBQ", [1, 4, 7]))

    symbols = (("BGGEQPQ", "^------"),
               ("GGEQPQZ", "------^"),
               ("GGEZQPQ", "---^---"),
               ("GGEJXQPQ", "---^^---"),
               ("GJGEXQPBQ", "-^--^--^-"),
               ("PVPDPIU", "------!"),
               ("GGEOQPQ", "---!---"),
               ("XMASLLKVDOQEVKLKVDSFRERITSEABEDLVANFFPKKLLELDSFLKEPILNIHDLTQIHSDMNLPVPDPIU",
                "^--------!------------------^--------------------------------------------!"))

    sights = (("BGGEQPQ", "BGGEQPQ\n^------"),
               ("GGEQPQZ", "GGEQPQZ\n------^"),
               ("GGEZQPQ", "GGEZQPQ\n---^---"),
               ("GGEJXQPQ", "GGEJXQPQ\n---^^---"),
               ("GJGEXQPBQ", "GJGEXQPBQ\n-^--^--^-"),
               ("PVPDPIU", "PVPDPIU\n------!"),
               ("GGEOQPQ", "GGEOQPQ\n---!---"),
               ("XMASLLKVDOQEVKLKVDSFRERITSEABEDLVANFFPKKLLELDSFLKEPILNIHDLTQIHSDMNLPVPDPIU",
                "XMASLLKVDOQEVKLKVDSFRERITSEABEDLVANFFPKKLLELDSFLKE\n^--------!------------------^---------------------\nPILNIHDLTQIHSDMNLPVPDPIU\n-----------------------!"))

    def test_badFormatRaises(self):
        for q in aaRECases.wrongSequences:
            for s in q:
                self.assertRaises(aa.wrongFormat, aa._bad_format, s)

    def test_noStandard_SubPep_result(self):
        for s,r in self.no_std_subPep:
            self.assertEqual(aa.noStandard_SubPep(s), r)

    def test_find_noStandards(self):
        for s in aaRECases.IUPACSequences:
            self.assertEqual(aa.find_noStandards(s), -1)
        for s, v in aaRECases.No_std_IUPAC_examples:
            self.assertEqual(aa.find_noStandards(s), v, msg="seq: %s\nexpected: %d\nresult: %d" %(s, v, aa.find_noStandards(s)))

    def test_Poz_noStandards(self):
        for s,r in self.no_std_poz:
            self.assertEqual(aa.Poz_noStandards(s), r)

    def test__seq2tags(self):
        for s,r in self.symbols:
            self.assertEqual(aa._seq2tags(s), r)

    def test_noStandardSeq(self):
        for s,r in self.sights:
            self.assertEqual(aa.noStandardSeq(s), r)

if __name__ == '__main__':
    unittest.main()

