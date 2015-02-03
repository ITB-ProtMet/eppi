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

try:
    import unittest2 as unittest
except ImportError:
    import unittest

from EPPI.peptidome import fasta_indx
from EPPI.peptidome.commons import peptidases

from os import curdir, listdir
import os.path as path
from os.path import abspath

file1 = path.join(curdir, "example_files", "Cypselurus_Hbps.fasta")
file2 = path.join(curdir, "example_files", "Ecoli_K12_IV.fasta")

sequence1 = "GAGAMSSRKKPSRRTRVLVGGAALAVLGAGVVGTVAANAADTTEATPAAAPVAARGGELTQSTHLTLEAATKAARAAVEAAEKDGRHVSVAVVDRNGNTLVTLRGDGAGPQSYESAERKAFTAVSWNAPTSELAKRLAQAPTLKDIPGTLFLAGGTPVTAKGAPVAGIGVAGAPSGDLDEQYARAGAAVLGH"
sequence2 = "LGAGVVGTVAANAADTT"
sequence3 = "VAGAPSGDLDEQYARAGAAVLGH"
sequence4 = "EAATKAARAAVE"

class Test_functions(unittest.TestCase):
    other_res = [("29420777", ">gi|29420777|dbj|BAC66610.1| T cell receptor alpha chain [Sus scrofa]"),
                 ("29788996", ">gi|29788996|ref|NP_000931.1| paraoxonase 3 [Homo sapiens] gi|114614590|ref|XP_519212.2| PREDICTED: paraoxonase 3 isoform 4 [Pan troglodytes] gi|50403778|sp|Q15166|PON3_HUMAN Serum paraoxonase/lactonase 3 gi|27462186|gb|AAO15365.1|AF329433_1 paraoxonase 3 [Homo sapiens] gi|51094887|gb|EAL24132.1| paraoxonase 3 [Homo sapiens] gi|55375975|gb|AAV50000.1| paraoxonase 3 [Homo sapiens] gi|119597174|gb|EAW76768.1| hCG2023324, isoform CRA_a [Homo sapiens]"),
                 #("P69905", ">sp|P69905|HBA_HUMAN Hemoglobin subunit alpha OS=Homo sapiens GN=HBA1 PE=1 SV=2")
                 ]
    wrong_res = bad_cases = [
                ">TR|F4YGV3|F4YGV3_9CARY Maturase K OS=Lophophora williamsii GN=matK PE=3 SV=1",
                ">gI|330887539|gb|AEC47541.1| maturase K [Lophophora williamsii]",
                 "O48111 CYB_PYTSE Cytochrome b [Python sebae]",
                 "UniRef100_O48111 Cytochrome b n=1 Tax=Python sebae RepID=CYB_PYTSE",
                 " ;LCBO - Prolactin precursor - Bovine",
                 "MCHU - Calmodulin - Human, rabbit, bovine, rat, and chicken",
                 "sp|P143&09|PHI0_HOLTU Sperm-specific protein Phi-0 OS=Holothuria tubulosa PE=4 SV=1",
                 "gi|2099A61650|gb|ACJ02073.1| cytochrome c oxidase subunit I [Holothuria leucospilota]",
                 "sp|Q9U#VX6|AXHA_ASPSO Alpha-L-arabinofuranosidase axhA OS=Aspergillus sojae GN=axhA PE=2 SV=1",]

#    ["gi|29420777|dbj|BAC66610.1| T cell receptor alpha chain [Sus scrofa]",
#                 ">GI|29788996|ref|NP_000931.1| paraoxonase 3 [Homo sapiens] gi|114614590|ref|XP_519212.2| PREDICTED: paraoxonase 3 isoform 4 [Pan troglodytes] gi|50403778|sp|Q15166|PON3_HUMAN Serum paraoxonase/lactonase 3 gi|27462186|gb|AAO15365.1|AF329433_1 paraoxonase 3 [Homo sapiens] gi|51094887|gb|EAL24132.1| paraoxonase 3 [Homo sapiens] gi|55375975|gb|AAV50000.1| paraoxonase 3 [Homo sapiens] gi|119597174|gb|EAW76768.1| hCG2023324, isoform CRA_a [Homo sapiens]",
#                 ">sp|P69905|HBA_HUMAN Hemoglobin subunit alpha OS=Homo sapiens GN=HBA1 PE=1 SV=2",
#                 ">Hb|Chongquing|alpha|2 Leu-Arg|1-7",
#                 ">gi|2942O777|dbj|BAC66610.1| T cell receptor alpha chain [Sus scrofa]",
#                 ">sp|P05100|3MG1_ECOLI DNA-3-methyladenine glycosylase 1 OS=Escherichia coli (strain K12) GN=tag PE=1 SV=1"
#                 ]
#
    text = "Nel mezzo di cammin di nostra vita"

    slices  = ["Nel ", "el m", "l me", " mez", "mezz",
               "ezzo", "zzo ", "zo d", "o di", " di ",
               "di c", "i ca", " cam", "camm", "ammi",
               "mmin", "min ", "in d", "n di", " di ",
               "di n", "i no", " nos", "nost", "ostr",
               "stra", "tra ", "ra v", "a vi", " vit",
               "vita"]

    paradigm  = "LucyintheSkywithDiamonds"

    anagramms = ["LucyintheSkywithDiamonds",
                 "SkyintheDiamondswithLucy",
                 "DiamondsintheSkywithLucy",
                 "LucyintheDiamondswithSky",
                 "DiamondsintheLucywithSky",
                 "IucyintheSkywithDiamonds",
                 ]

    alterations = ["LucyintheSkywithRubies",
                   "PaintItBlack",
                   "LucyintheSkywithSky",
                   "LucyintheSkywithDiamondsSky",
                   "LucyintheSkywith",]

    def test__gi_from_ref(self):
        for acc, ref in self.other_res:
            self.assertEqual(acc, fasta_indx.gi_from_ref(ref))

    def test_raise__gi_from_ref(self):
        for ref in self.wrong_res:
            print ref
            self.assertRaises(fasta_indx.WrongReference, fasta_indx.gi_from_ref, ref)

    def test__iterslice(self):
        for i, each in enumerate(fasta_indx._iterslice(self.text, 4)):
            self.assertEqual(each, self.slices[i])

    def test__compare_composition(self):
        for each in self.anagramms:
            self.assertTrue(fasta_indx._compare_composition(self.paradigm, each),
                             msg="%s"%each)
        for each in self.alterations:
            self.assertFalse(fasta_indx._compare_composition(self.paradigm, each),
                             msg="%s"%each)

class Test_Saf(unittest.TestCase):

    results = [
        ("221046910", ">gi|221046910|pdb|3FPV|A Chain A, Crystal Structure Of Hbps"),
        ("221046911", ">gi|221046911|pdb|3FPV|B Chain B, Crystal Structure Of Hbps"),
        ("221046912", ">gi|221046912|pdb|3FPV|C Chain C, Crystal Structure Of Hbps"),
        ("221046913", ">gi|221046913|pdb|3FPV|D Chain D, Crystal Structure Of Hbps"),
        ("221046914", ">gi|221046914|pdb|3FPV|E Chain E, Crystal Structure Of Hbps"),
        ("221046915", ">gi|221046915|pdb|3FPV|F Chain F, Crystal Structure Of Hbps"),
        ("221046916", ">gi|221046916|pdb|3FPV|G Chain G, Crystal Structure Of Hbps"),
        ("221046917", ">gi|221046917|pdb|3FPV|H Chain H, Crystal Structure Of Hbps"),
        ("221046918", ">gi|221046918|pdb|3FPW|A Chain A, Crystal Structure Of Hbps With Bound Iron")
        ]

    @classmethod
    def setUpClass(cls):
        global READER
        READER = fasta_indx.Saf(file1)
        global READER2
        READER2 = fasta_indx.Saf(file2)

    def test_get_reference(self):
        for acc, ref in self.results:
            self.assertEqual(READER.get_reference(acc), ref)

    def test_get_sequence(self):
        for res in self.results[1:]:
            print res, READER.get_sequence(res[0])
            self.assertEqual(READER.get_sequence(res[0]), sequence1)

    def test_search_peptide(self):
        prots = [each[1] for each in self.results]
        self.assertEqual([res for res in READER.search_peptide(sequence1)], prots)
        self.assertEqual([res for res in READER.search_peptide(sequence2)], prots)
        self.assertEqual([res for res in READER.search_peptide(sequence3)], prots)
        self.assertEqual([res for res in READER.search_peptide(sequence4)], prots)

    def test_search_composition(self):
        prots = [each[1] for each in self.results]
        self.assertEqual([res for res in READER.search_composition(sequence1)], prots)
        self.assertEqual([res for res in READER.search_composition(sequence2)], prots)
        self.assertEqual([res for res in READER.search_composition(sequence3)], prots)

        res_list = list(set([res for res in READER.search_composition(sequence4)]))
        self.assertItemsEqual(res_list, prots)

        self.assertEqual([res for res in READER.search_composition(sequence1[::-1])], prots)
        self.assertEqual([res for res in READER.search_composition(sequence2[::-1])], prots)
        self.assertEqual([res for res in READER.search_composition(sequence3[::-1])], prots)
        res_list = list(set([res for res in READER.search_composition(sequence4[::-1])]))
        self.assertItemsEqual(res_list, prots)

    exam_peptides_NR = [(265329699, #"HSQVFSTAEDNQSAVTIHVLQGER",
                         [('33347764', "DAMVASGVTTTRPQDNDTFTRLTR", 2653.30037,
                           ">gi|33347764|ref|NP_417987.2| putative oxidoreductase subunit [Escherichia coli K12]"),
                          ('16129979',"SNYAVTGLYFYDNDVVQMAKNLK", 2653.29718,
                           ">gi|16129979|ref|NP_416543.1| glucose-1-phosphate thymidylyltransferase [Escherichia coli K12]"),
                          ('16129045', "AGFDANGDAGEDFFAIGKPAVLQNTK", 2653.28974,
                           ">gi|16129045|ref|NP_415600.1| hook-filament junction protein 1 [Escherichia coli K12]"),
                          ('16128008',"HSQVFSTAEDNQSAVTIHVLQGER", 2653.29699,
                           ">gi|16128008|ref|NP_414555.1| chaperone Hsp70 [Escherichia coli K12]")]),
                        (228409933, #"VPYIAQVMNDAPAVASTDYMK",
                         [('16129246',"LTESSDVLRFSTTETTEPDR",  2284.09444,
                           ">gi|16129246|ref|NP_415801.1| hypothetical protein b1285 [Escherichia coli K12]"),
                          ('16128107',"VPYIAQVMNDAPAVASTDYMK", 2284.09933,
                           ">gi|16128107|ref|NP_414656.1| pyruvate dehydrogenase [Escherichia coli K12]")]),
                        (257923708, #"LTACNTTRGVGEDISDGGNAISGAATK",
                         [('16128388', "LVLDGVFNHSGDSHAWFDRHNR", 2579.22917,
                           ">gi|16128388|ref|NP_414937.1| maltodextrin glucosidase [Escherichia coli K12]")])
                        ]

    def test_search_by_mw(self):
        for exa in self.exam_peptides_NR:
            results = list(READER2.search_by_mw(exa[0], peptidases.tryp_simp_pro, miscut=2))
            self.assertListEqual(results, exa[1])


    exam_peptides_seq = [("HSQVFSTAEDNQSAVTIHVLQGER",
                         [('16128008',"HSQVFSTAEDNQSAVTIHVLQGER", 2653.29699,
                           ">gi|16128008|ref|NP_414555.1| chaperone Hsp70 [Escherichia coli K12]")]),
                        ("VPYIAQVMNDAPAVASTDYMK",
                         [('16128107',"VPYIAQVMNDAPAVASTDYMK", 2284.09933,
                           ">gi|16128107|ref|NP_414656.1| pyruvate dehydrogenase [Escherichia coli K12]")]),
                        ("LTACNTTRGVGEDISDGGNAISGAATK",
                        [('33347826', 'LTACNTTRGVGEDISDGGNAISGAATK', 2579.23708,
                          '>gi|33347826|ref|NP_877565.1| entericidin B precursor [Escherichia coli K12]')]),
                        ("DAGNIIIDDDDISLLPLHAR",
                         [('16131091', 'DAGNIIIDDDDISLLPLHAR', 2176.12492,
                           '>gi|16131091|ref|NP_417668.1| putative ATP-binding component of a transport system [Escherichia coli K12]')]),
                         ]

    def test_search_by_sequence(self):
        for exa in self.exam_peptides_seq:
            results = list(READER2.search_by_sequence(exa[0]))
            self.assertListEqual(results, exa[1])
#        READER1 = fasta_indx.Saf(file1)
#        prots = [each[1] for each in self.results]
#        self.assertEqual([res for res in READER1.search_by_peptide(sequence1)], prots)
#        self.assertEqual([res for res in READER1.search_by_peptide(sequence2)], prots)
#        self.assertEqual([res for res in READER1.search_by_peptide(sequence3)], prots)
#        self.assertEqual([res for res in READER1.search_by_peptide(sequence4)], prots)

if __name__ == '__main__':
    unittest.main()

