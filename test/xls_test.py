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

"""Unit test for proteomic_xls.py"""

__authors__ = "Pietro Brunetti"

from os import curdir, listdir
import os.path as path
from os.path import abspath

from xlrd import open_workbook
from EPPI.raw import proteomic_xls
from EPPI.raw import data_input
import unittest


DIR = abspath(path.join(curdir, "example_files", 'xls_testfiles'))

protpept_dir =   path.join(DIR, "five_right_protpept")
onlypept_dir =   path.join(DIR, "five_right_onlypept")
discoverer_dir = path.join(DIR, "five_right_discoverer")
wrong_format_dir = path.join(DIR, "wrong_format")
redundants_dir = path.join(DIR, "redundants")
without_fields_dir = path.join(DIR, "without_fields")
wrong_pepts_dir = path.join(DIR, "wrong_pepts")

class Wrong_header(unittest.TestCase):
    """
    Test for the when there is a wrong header in xls files.
    This tests prove xls_parser's methods.
    """

    def match_kof(self, dir, kof):
        xls_p = proteomic_xls.xls_parser()
        for file in listdir(dir):
            book = open_workbook(path.join(dir, file))
            sheet = book.sheet_by_index(0)
            res_type = xls_p.what_kind_of_file(sheet)
            self.assertEqual(res_type, kof, "%s != %s\nfile: %s" % (res_type, kof, file))

    def wkof_test(self):
        """
        What Kind of File Test
        Controlling if func return right wkof
        """
        self.match_kof(protpept_dir,   "protpep")
        self.match_kof(onlypept_dir,   "onlypep")
        self.match_kof(discoverer_dir, "discoverer")
        self.match_kof(wrong_format_dir, "wrongXLS")

    def match_ff(self, dir):
        xls_p = proteomic_xls.xls_parser()
        for f in listdir(dir):
            book = open_workbook(path.join(dir, f))
            sheet = book.sheet_by_index(0)
            res_type = xls_p.what_kind_of_file(sheet)
            a_d = dict(filename=f, xls_type=res_type, sheet=sheet)
            self.assertRaises(proteomic_xls.Without_Field, xls_p.find_fields, **a_d)

    def test_real_without_fileds(self):
        """
        File without Sequence or Accession column.
        """
        self.match_ff(without_fields_dir)

class Xls_occurences(unittest.TestCase):
    """
    Is the occurrence evaluation rights?
    """
    prots = [
        ("4502027", xrange(1,6)),
        ("56550049", xrange(1,6)),
        ("4504943", xrange(1,6)),
        ("992949", xrange(1,6)),
        ("15029677", [1 for i in xrange(5)] )
    ]

    pepts =[
        ("4502027", [
            ("AEFAEVSK", xrange(1,6),  [3*i for i in xrange(1,6)]),
            ("DDNPNLPR", xrange(1,6),  [1*i for i in xrange(1,6)]),
            ("DLGEENFK", xrange(1,6),  [1*i for i in xrange(1,6)]),
            ("KQTALVELVK", xrange(1,6),  [4*i for i in xrange(1,6)]),
            ("KVPQVSTPTLVEVSR", xrange(1,6),  [6*i for i in xrange(1,6)]),
            ("KYLYEIAR", xrange(1,6),  [1*i for i in xrange(1,6)]),
            ("LVAASQAALGL", xrange(1,6),  [2*i for i in xrange(1,6)]),
            ("LVNEVTEFAK", xrange(1,6),  [3*i for i in xrange(1,6)]),
            ("LVTDLTK", xrange(1,6),  [1*i for i in xrange(1,6)]),
            ("SLHTLFGDK", xrange(1,6),  [2*i for i in xrange(1,6)]),
            ("VFDEFKPLVEEPQNLIK", xrange(1,6),  [1*i for i in xrange(1,6)]),
            ("YLYEIAR", xrange(1,6),  [1*i for i in xrange(1,6)]),
            ("FKDLGEENFK", xrange(1,6),  [3*i for i in xrange(1,6)]),
            ("HPDYSVVLLLR", xrange(1,6),  [2*i for i in xrange(1,6)]),
            ("FYAPELLFFA", xrange(1,6),  [1*i for i in xrange(1,6)]),
            ("FYAPELLFFAK", xrange(1,6),  [2*i for i in xrange(1,6)])
        ]),
        ("56550049", [
            ("STIQVVENGESSQGR",	xrange(1,6),  [1*i for i in xrange(1,6)]),
            ("TALQPMVSALNIR",	xrange(1,6),  [5*i for i in xrange(1,6)]),
            ("VFMYLSDSR",	xrange(1,6),  [2*i for i in xrange(1,6)]),
            ("YFIIQDR",	xrange(1,6),  [3*i for i in xrange(1,6)]),
            ("VSALNIR", xrange(1,6),  [1*i for i in xrange(1,6)]),
            ("DSTIQVVENGESSQGR", xrange(1,6),  [20*i for i in xrange(1,6)]),
            ("DWVSVVTPAR", xrange(1,6),  [5*i for i in xrange(1,6)]),
            ("FSVQMFR",	xrange(1,6),  [1*i for i in xrange(1,6)]),
            ("TLDEYWR",	xrange(1,6),  [2*i for i in xrange(1,6)]),
            ("VGGTGMFTVR", xrange(1,6),  [2*i for i in xrange(1,6)]),
            ("LADEIIIR", xrange(1,6),  [2*i for i in xrange(1,6)])
        ]),
        ("4504943", [
            ("IDSVSEGNAGPYR", xrange(1,6),  [1*i for i in xrange(1,6)]),
            ("GPVGVQTFR", xrange(1,6),  [1*i for i in xrange(1,6)]),
            ("WSEQSDYLELLVK", xrange(1,6),  [2*i for i in xrange(1,6)])
        ]),
        ("992949", [
            ("ISHELDSASSEVN", xrange(1,6),  [2*i for i in xrange(1,6)]),
            ("AIPVAQDLNAPSDWDSR", xrange(1,6),  [3*i for i in xrange(1,6)]),
            ("YPDAVATWLNPDPSQK", xrange(1,6),  [3*i for i in xrange(1,6)])
        ]),
        ("15029677",[
            ("EDQTSPAPGLR",  [1 for i in xrange(1,6)],  [2 for i in xrange(1,6)]),
            ("SEAAAVQPVIGISQR", [1 for i in xrange(1,6)], [2 for i in xrange(1,6)]),
            ("SEAAAVQPVIGISQ", [1 for i in xrange(1,6)], [1 for i in xrange(1,6)])
        ])
    ]

    onlypepts =[
        ("4502027", [
            ("AEFAEVSK", xrange(1,6),  [3*i for i in xrange(1,6)]),
            ("DDNPNLPR", xrange(1,6),  [1*i for i in xrange(1,6)]),
            ("DLGEENFK", xrange(1,6),  [1*i for i in xrange(1,6)]),
            ("KQTALVELVK", xrange(1,6),  [4*i for i in xrange(1,6)]),
            ("KVPQVSTPTLVEVSR", xrange(1,6),  [1*i for i in xrange(1,6)]), #changed
            ("KYLYEIAR", xrange(1,6),  [1*i for i in xrange(1,6)]),
            ("LVAASQAALGL", xrange(1,6),  [2*i for i in xrange(1,6)]),
            ("LVNEVTEFAK", xrange(1,6),  [3*i for i in xrange(1,6)]),
            #("LVTDLTK", xrange(1,6),  [1*i for i in xrange(1,6)]),
            ("SLHTLFGDK", xrange(1,6),  [2*i for i in xrange(1,6)]),
            ("VFDEFKPLVEEPQNLIK", xrange(1,6),  [1*i for i in xrange(1,6)]),
            ("YLYEIAR", xrange(1,6),  [1*i for i in xrange(1,6)]),
            ("FKDLGEENFK", xrange(1,6),  [3*i for i in xrange(1,6)]),
            ("HPDYSVVLLLR", xrange(1,6),  [2*i for i in xrange(1,6)]),
            ("FYAPELLFFA", xrange(1,6),  [1*i for i in xrange(1,6)]),
            ("FYAPELLFFAK", xrange(1,6),  [2*i for i in xrange(1,6)])
        ]),
        ("56550049", [
            ("STIQVVENGESSQGR",	xrange(1,6),  [1*i for i in xrange(1,6)]),
            ("TALQPMVSALNIR",	xrange(1,6),  [5*i for i in xrange(1,6)]),
            ("VFMYLSDSR",	xrange(1,6),  [2*i for i in xrange(1,6)]),
            ("YFIIQDR",	xrange(1,6),  [3*i for i in xrange(1,6)]),
            ("VSALNIR", xrange(1,6),  [1*i for i in xrange(1,6)]),
            ("DSTIQVVENGESSQGR", xrange(1,6),  [20*i for i in xrange(1,6)]),
            ("DWVSVVTPAR", xrange(1,6),  [5*i for i in xrange(1,6)]),
            ("FSVQMFR",	xrange(1,6),  [1*i for i in xrange(1,6)]),
            ("TLDEYWR",	xrange(1,6),  [2*i for i in xrange(1,6)]),
            ("VGGTGMFTVR", xrange(1,6),  [2*i for i in xrange(1,6)]),
            ("LADEIIIR", xrange(1,6),  [2*i for i in xrange(1,6)])
        ]),
        ("4504943", [
            ("IDSVSEGNAGPYR", xrange(1,6),  [1*i for i in xrange(1,6)]),
            ("GPVGVQTFR", xrange(1,6),  [1*i for i in xrange(1,6)]),
            ("WSEQSDYLELLVK", xrange(1,6),  [2*i for i in xrange(1,6)])
        ]),
        ("992949", [
            ("ISHELDSASSEVN", xrange(1,6),  [2*i for i in xrange(1,6)]),
            ("AIPVAQDLNAPSDWDSR", xrange(1,6),  [3*i for i in xrange(1,6)]),
            ("YPDAVATWLNPDPSQK", xrange(1,6),  [3*i for i in xrange(1,6)])
        ]),
        ("15029677",[
            ("EDQTSPAPGLR",  [1 for i in xrange(1,6)],  [2 for i in xrange(1,6)]),
            ("SEAAAVQPVIGISQR", [1 for i in xrange(1,6)], [2 for i in xrange(1,6)]),
            ("SEAAAVQPVIGISQ", [1 for i in xrange(1,6)], [1 for i in xrange(1,6)])
        ])
    ]

    files =[
        "A1.xls",
        "B1.xls",
        "B2.xls",
        "B3.xls",
        "B4.xls"
    ]

    def test_proteins_protpept(self):
        """
        proteins occurrence during parsing the five file
        """
        p = proteomic_xls.sequest_protpept_parser()
        for i, f in enumerate(self.files):
            try:
                p.parse(path.join(protpept_dir, f))
            except proteomic_xls.EmptyCell:
                pass
            for acc, occs in self.prots:
                self.assertEqual(occs[i], p.proteins[acc])

    def test_peptides_protpept_nored(self):
        """
        peptides occurrence during parsing the five file
        Spectral count False
        """
        p = proteomic_xls.sequest_protpept_parser()
        for i, f in enumerate(self.files):
            try:
                p.parse(path.join(protpept_dir, f))
            except proteomic_xls.EmptyCell:
                pass
            for acc, pepts in self.pepts:
                for seq, occs_nr, occs_r in pepts:
                    self.assertEqual(occs_nr[i], p.peptides[acc][seq], "%d, %s, %s" %(i, acc, seq))

    def test_peptides_protpept_red(self):
        """
        peptides occurrence during parsing the five file
        Spectral Count True
        """
        p = proteomic_xls.sequest_protpept_parser(mode=True)
        for i, f in enumerate(self.files):
            try:
                p.parse(path.join(protpept_dir, f))
            except proteomic_xls.EmptyCell:
                pass
            for acc, pepts in self.pepts:
                for seq, occs_nr, occs_r in pepts:
                    self.assertEqual(occs_r[i], p.peptides[acc][seq], "%d, %s, %s" %(i, acc, seq))

    def test_proteins_onlypept(self):
        """
        proteins occurrence during parsing the five file
        """
        p = proteomic_xls.sequest_onlypept_parser()
        for i, f in enumerate(self.files):
            try:
                p.parse(path.join(onlypept_dir, f))
            except proteomic_xls.EmptyCell:
                pass
            for acc, occs in self.prots:
                self.assertEqual(occs[i], p.proteins[acc], "%d != %d @prot: %s, @time: %d"\
                    %(occs[i], p.proteins[acc], acc, i))

    def test_peptides_onlypept_nored(self):
        """
        peptides occurrence during parsing the five file
        Spectral count False
        """
        p = proteomic_xls.sequest_onlypept_parser()
        for i, f in enumerate(self.files):
            try:
                p.parse(path.join(onlypept_dir, f))
            except proteomic_xls.EmptyCell:
                pass
            for acc, pepts in self.onlypepts:
                for seq, occs_nr, occs_r in pepts:
                    try:
                        self.assertEqual(occs_nr[i], p.peptides[acc][seq], "%d, %s, %s" %(i, acc, seq))
                    except KeyError:
                        print "KeyError: %s, %s" %(acc, seq)

    def test_peptides_onlypept_red(self):
        """
        peptides occurrence during parsing the five file
        Spectral Count True
        """
        p = proteomic_xls.sequest_onlypept_parser(mode=True)
        for i, f in enumerate(self.files):
            try:
                p.parse(path.join(onlypept_dir, f))
            except proteomic_xls.EmptyCell:
                pass
            for acc, pepts in self.onlypepts:
                for seq, occs_nr, occs_r in pepts:
                    self.assertEqual(occs_r[i], p.peptides[acc][seq], "%d, %s, %s" %(i, acc, seq))

    def test_file_source_store_op(self):
        """
        testing the original seq storage
        """
        p = proteomic_xls.sequest_onlypept_parser(mode=True)
        for f in self.files:
            try:
                p.parse(path.join(onlypept_dir, f))
            except proteomic_xls.EmptyCell:
                pass
        self.assertListEqual([path.join(onlypept_dir, f) for f in self.files],
                             p.sources)

    def test_file_source_store_pp(self):
        """
        testing the original seq storage
        """
        p = proteomic_xls.sequest_protpept_parser(mode=True)
        for f in self.files:
            try:
                p.parse(path.join(protpept_dir, f))
            except proteomic_xls.EmptyCell:
                pass
        self.assertListEqual([path.join(protpept_dir, f) for f in self.files],
                             p.sources)

class Xls_occurences_discoverer(unittest.TestCase):
    """
    Is the occurrence evaluation rights?
    """
    prots = [
        ("386599560", xrange(1,6)),
        ("386601074", xrange(1,6)),
        ("386601333", xrange(1,6)),
        ("386602367", xrange(1,6)),
        ("386601051", [1 for i in xrange(5)] )
    ]

    pepts =[
        ("386599560", [("VITASDSSGTVVDESGFTK",
                        xrange(1,6),
                        [2*i for i in xrange(1,6)]),
                       ("VSVSGSGNVAQYAIEK",
                        xrange(1,6),
                        [2*i for i in xrange(1,6)]),
         ]),
        ("386601074", [("TIAAAEGPYGEEGMIVQQFHPLPK",
                        xrange(1,6),
                        [2*i for i in xrange(1,6)]),
                       ("GQFTDLQDQVISNLFK",
                        xrange(1,6),
                        [1*i for i in xrange(1,6)]),
        ]),
        ("386601333", [("QHVPVFVTDEMVGHK",
                        xrange(1,6),
                        [3*i for i in xrange(1,6)]),
        ]),
         ("386602367", [("NIIAGLPGAEEGYTLDQFR",
                        xrange(1,6),
                        [2*i for i in xrange(1,6)]),
                       #only A1 has this peptide
                       ("AIIPVAEEVGVR",
                        [1 for i in xrange(1,6)],
                        [1 for i in xrange(1,6)]),
        ]),
        #only A1 has this protein
        ("386601051", [("TTLDQLLDIVQGPDYPTEAEIITSR",
                       [1 for i in xrange(1,6)],
                       [2 for i in xrange(1,6)]),
                      ("MLMFPVSDLPQLSK",
                      [1 for i in xrange(1,6)],
                      [2 for i in xrange(1,6)]),
        ])
    ]

    files =[
        "A1.xls",
        "B1.xls",
        "B2.xls",
        "B3.xls",
        "B4.xls"
    ]

    def test_proteins(self):
        """
        proteins occurrence during parsing the five file
        """
        p = proteomic_xls.discoverer_parser()
        msg = "{0}: predicted {1} != counted {2}"
        for i, f in enumerate(self.files):
            try:
                p.parse(path.join(discoverer_dir, f))
            except proteomic_xls.EmptyCell:
                pass
            for acc, occs in self.prots:
                self.assertEqual(occs[i], p.proteins[acc], msg.format(acc, occs[i], p.proteins[acc]))

    def test_peptides_protpept_nored(self):
        """
        peptides occurrence during parsing the five file
        Spectral count False
        """
        p = proteomic_xls.discoverer_parser()
        for i, f in enumerate(self.files):
            try:
                p.parse(path.join(discoverer_dir, f))
            except proteomic_xls.EmptyCell:
                pass
            for acc, pepts in self.pepts:
                for seq, occs_nr, occs_r in pepts:
                    self.assertEqual(occs_nr[i], p.peptides[acc][seq], "{0} - {1}:{2} aspected {3} != retrived {4}".format(
                    f, acc, seq, occs_nr[i], p.peptides[acc][seq]))

    def test_peptides_protpept_red(self):
        """
        peptides occurrence during parsing the five file
        Spectral Count True
        """
        p = proteomic_xls.discoverer_parser(mode=True)
        for i, f in enumerate(self.files):
            try:
                p.parse(path.join(discoverer_dir, f))
            except proteomic_xls.EmptyCell:
                pass
            for acc, pepts in self.pepts:
                for seq, occs_nr, occs_r in pepts:
                    print occs_r[i]
                    self.assertEqual(occs_r[i], p.peptides[acc][seq],
                    "{0} - {1}:{2} aspected {3} != retrived {4}".format(
                    f, acc, seq, occs_r[i], p.peptides[acc][seq]))

    def test_file_source_store(self):
        """
        testing the original seq storage
        """
        p = proteomic_xls.discoverer_parser(mode=True)
        for f in self.files:
            try:
                p.parse(path.join(discoverer_dir, f))
            except proteomic_xls.EmptyCell:
                pass
        self.assertListEqual([path.join(discoverer_dir, f)\
            for f in self.files], p.sources)

class Kind_of_file(unittest.TestCase):
    """
    Unit test for the format of xls file
    """

    def match_format_parser(self, pars, dir):
        for file in listdir(dir):
            path_ = path.join(dir, file)
            a_d = dict(fileName=path_)
            self.assertRaises(proteomic_xls.wrongFile, pars, **a_d)

    def test_bad_format_real_protpept(self):
        """
        Should fail with format no protpept using
        wrong protpept analysis files
        """
        p = proteomic_xls.sequest_protpept_parser()
        self.match_format_parser(p.parse, onlypept_dir)
        self.match_format_parser(p.parse, discoverer_dir)


    def test_bad_format_real_onlypept(self):
        """
        Should fail with format no onlypept using
        wrong onlypept analysis files
        """
        p = proteomic_xls.sequest_onlypept_parser()
        self.match_format_parser(p.parse, protpept_dir)
        self.match_format_parser(p.parse, discoverer_dir)

    def test_bad_format_real_discoverer(self):
        """
        Should fail with format no data_discoverer using
        wrong data_discoverer analysis files
        """
        p = proteomic_xls.sequest_onlypept_parser()
        self.match_format_parser(p.parse, protpept_dir)
        self.match_format_parser(p.parse, discoverer_dir)

class Redundancies_Accession_number(unittest.TestCase):
    """
    Test for the xls files.
    It evaluates when  there's more than
    one time the same Accession number

    This test is not thought for onlypept, were
    redundant accessions are of course allowed.
    """

    def test_real_redundant_protpept(self):
        """
        When there aren't redundancy in proptpept
        """
        path_ = path.join(redundants_dir,
            "redundant_accessions_protpept.xls")
        p = proteomic_xls.sequest_protpept_parser()
        a_d = dict(fileName=path_)
        self.assertRaises(proteomic_xls.Same_Accession, p.parse, **a_d)

    def test_real_redundant_discoverer(self):
        """
        When there aren't redundancy data_discoverer
        """
        path_ = path.join(redundants_dir,
            "redundant_accessions_discoverer.xls")
        p = proteomic_xls.discoverer_parser()
        a_d = dict(fileName=path_)
        self.assertRaises(proteomic_xls.Same_Accession, p.parse, **a_d)

class distinct_peptides(unittest.TestCase):
    """
    Test to evaluate the correctness of computation
    of the parsers with distinct peptides and with spectral count
    """
    def test_spectral_count_false_proppept(self):
        """
        Using a protpept file with peptides no-distinct,
        the frequencies must be equal to one.
        """
        chase1 = path.join(redundants_dir, "redundant_protpept.xls")
        #assert(os.path.isfile(chase1))
        p = proteomic_xls.sequest_protpept_parser()
        try:
            p.parse(chase1)
        except proteomic_xls.EmptyCell:
            pass
        finally:
            for acc, pepts in p.peptides.iteritems():
                for seq, occ in pepts.iteritems():
                    self.assertEqual(occ, 1)

    def test_spectral_count_false_onlypept(self):
        """
        Using a onlypept file with peptides no-distinct,
        the frequencies must be equal to one.
        """
        chase2 = path.join(redundants_dir, "redundant_onlypept.xls")
        p = proteomic_xls.sequest_onlypept_parser()
        try:
            p.parse(chase2)
        except proteomic_xls.EmptyCell:
            pass
        finally:
            for acc, pepts in p.peptides.iteritems():
                for seq, occ in pepts.iteritems():
                    self.assertEqual(occ, 1)

    def test_spectral_count_false_discoverer(self):
        """
        Using a data_discoverer file with peptides no-distinct,
        the frequencies must be equal to one.
        """
        chase2 = path.join(redundants_dir, "redundant_discoverer.xls")
        p = proteomic_xls.discoverer_parser()
        try:
            p.parse(chase2)
        except proteomic_xls.EmptyCell:
            pass
        finally:
            for acc, pepts in p.peptides.iteritems():
                for seq, occ in pepts.iteritems():
                    self.assertEqual(occ, 1)

class wrong_peptides(unittest.TestCase):
    """
    strange peptides inside
    """
    def test_wrong_peptides_protpept(self):
        """
        When protpept file has wrong peptides
        """
        path_ = path.join(wrong_pepts_dir, "wrong_pepts_protpept.xls")
        p = proteomic_xls.sequest_protpept_parser()
        a_d = dict(fileName=path_)
        self.assertRaises(data_input.bad_format_peptide, p.parse, **a_d)

    def test_wrong_peptides_onlypept(self):
        """
        When onlypept file has wrong peptides
        """
        path_ = path.join(wrong_pepts_dir, "wrong_pepts_onlypept.xls")
        p = proteomic_xls.sequest_onlypept_parser()
        a_d = dict(fileName=path_)
        self.assertRaises(data_input.bad_format_peptide, p.parse, **a_d)

    def test_wrong_peptides_discoverer(self):
        path_ = path.join(wrong_pepts_dir, "wrong_pepts_discoverer.xls")
        p = proteomic_xls.discoverer_parser()
        a_d = dict(fileName=path_)
        self.assertRaises(data_input.bad_format_peptide, p.parse, **a_d)

if __name__ == "__main__":
    unittest.main()
