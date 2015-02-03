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

from EPPI.raw import proteomic_xml

import nose
import unittest


from os import curdir
import os.path as path
from os.path import abspath

class tpath():
    base = ""
    files = []
    ROOT = abspath(path.join(curdir, "example_files", 'xml_testfiles'))

    def get_file(self):
        for file in self.files:
            yield  path.join(self.ROOT, self.base, file)

class data_sequest():
    data = (("7019519", 2,  "DHDVGSELPPEGVLGALLR", 2),
            ("56550049", 2, "VGGTGMFTVR",2),
            ("56550049", 2, "DWVSVVTPAR",2),
            ("56550049", 2, "LADEIIIR", 2),
            ("56550049", 2, "FSVQMFR", 2),
            ("56550049", 2, "VSALNIR", 2),
            ("56550049", 2, "TALQPMVSALNIR", 2),
            ("56550049", 2, "YFIIQDR", 2),
            ("56550049", 2, "DSTIQVVENGESSQGR", 2),
            ("56550049", 2, "TLDEYWR", 2),
            ("56550049", 2, "STIQVVENGESSQGR", 2),
            ("56550049", 2, "VFMYLSDSR", 2),
            ("7934572", 2, "PPSLKKKQTTKKPTETPPVKETQQEPDEESLV", 2),
            ("15029677", 2, "SEAAAVQPVIGISQR", 2),
            ("15029677", 2, "EDQTSPAPGLR", 2),
            ("15029677", 2, "SEAAAVQPVIGISQ", 2),
            ("1155011", 2, "SDIDAVYVTTNGIIATSEPPAK", 2),
            ("1335344", 2, "LAACLEGNCAEGLGTNYR", 2)
            )
    
class data_discoverer():
    """
    Extract random data from a discoverer output excell file.
    """
    import disco
    path = "example_files/xls_testfiles/template_disco.xls"
    data = disco.xls_extract(path)
    

class data_sequest_pep(tpath, data_sequest):
    base = "sequest_pep"
    files = ["pep_file1.xml",
             "pep_file1_bis.xml"]

class data_sequest_pep_dist(tpath, data_sequest):
    base = "sequest_pep_dist"
    files = ["pep_file1_dist.xml", "pep_file1_bis_dist.xml"]

class data_sequest_pro(tpath, data_sequest):
    base ="sequest_seq_prot_pep"
    files = ["prot_pep_file1.xml",
             "prot_pep_file1_bis.xml"]

class data_sequest_pro_dist(tpath, data_sequest):
    base = "sequest_seq_prot_pep_dist"
    files = ["prot_pep_file1_dist.xml", "prot_pep_file1_bis_dist.xml"]
    
class data_discoverer_prot(tpath, data_discoverer):
    base = "disco_prot"
    files = ["file1.prot.xml", "file1_bis.prot.xml"]

class data_discoverer_pept(tpath, data_discoverer):
    base = "disco_pept"
    files = ["file1.pep.xml", "file1_bis.pep.xml"]

class data_mzIdent(tpath):
    data = (
            ('HSP70_ECHGR', 2, 'DAGTISGLNVLR', 2),
            ('HSP70_ONCMY', 2, 'DAGTISGLNVLR', 2),
            ('HSP7C_ICTPU', 2, 'DAGTISGLNVLR', 2),
            ('HSP7C_ORYLA', 2, 'DAGTISGLNVLR', 2),
            ('HSP7D_MANSE', 2, 'DAGTISGLNVLR', 2),
            ('HS70A_BOVIN', 2, 'TTPSYVAFTDTER', 2),
            ('HS70A_MOUSE', 2, 'TTPSYVAFTDTER', 2),
            ('HS70B_BOSMU', 2, 'TTPSYVAFTDTER', 2),
            ('HS70B_BOVIN', 2, 'TTPSYVAFTDTER', 2),
            ('HS70B_MOUSE', 2, 'TTPSYVAFTDTER', 2),
            ('HS70B_PIG', 2, 'TTPSYVAFTDTER', 2),
            ('HS70L_HUMAN', 2, 'TTPSYVAFTDTER', 2),
            ('HS70L_MOUSE', 2, 'TTPSYVAFTDTER', 2),
            ('HS70L_RAT', 2, 'TTPSYVAFTDTER', 2),
            ('HSP70_BRUMA', 2, 'TTPSYVAFTDTER', 2),
            ('HSP70_CHICK', 2, 'TTPSYVAFTDTER', 2),
            ('HSP70_ECHGR', 2, 'TTPSYVAFTDTER', 2),
            ('HSP70_HYDMA', 2, 'TTPSYVAFTDTER', 2),
            ('HSP70_ONCTS', 2, 'TTPSYVAFTDTER', 2),
            ('HSP70_PLEWA', 2, 'TTPSYVAFTDTER', 2),
            ('HSP70_XENLA', 2, 'TTPSYVAFTDTER', 2),
            ('HSP71_CANFA', 2, 'TTPSYVAFTDTER', 2),
            ('HSP71_CERAE', 2, 'TTPSYVAFTDTER', 2),
            ('HSP71_HUMAN', 2, 'TTPSYVAFTDTER', 2),
            ('HSP71_ORYLA', 2, 'TTPSYVAFTDTER', 2),
            ('HSP71_RAT', 2, 'TTPSYVAFTDTER', 2),
            ('HSP72_HUMAN', 2, 'TTPSYVAFTDTER', 2),
            ('HSP72_MOUSE', 2, 'TTPSYVAFTDTER', 2),
            ('HSP72_PARLI', 2, 'TTPSYVAFTDTER', 2),
            ('HSP72_RAT', 2, 'TTPSYVAFTDTER', 2),
            ('HSP73_BOVIN', 2, 'TTPSYVAFTDTER', 2),
            ('HSP76_HUMAN', 2, 'TTPSYVAFTDTER', 2),
            ('HSP76_PIG', 2, 'TTPSYVAFTDTER', 2),
            ('HSP76_SAGOE', 2, 'TTPSYVAFTDTER', 2),
            ('HSP77_HUMAN', 2, 'TTPSYVAFTDTER', 2),
            ('HSP7A_CAEEL', 2, 'TTPSYVAFTDTER', 2),
            ('HSP7C_BOVIN', 2, 'TTPSYVAFTDTER', 2),
            ('HSP7C_BRARE', 2, 'TTPSYVAFTDTER', 2),
            ('HSP7C_CRIGR', 2, 'TTPSYVAFTDTER', 2),
            ('HSP7C_HUMAN', 2, 'TTPSYVAFTDTER', 2),
            ('HSP7C_MOUSE', 2, 'TTPSYVAFTDTER', 2),
            ('HSP7C_ORYLA', 2, 'TTPSYVAFTDTER', 2),
            ('HSP7C_PONPY', 2, 'TTPSYVAFTDTER', 2),
            ('HSP7C_RAT', 2, 'TTPSYVAFTDTER', 2),
            ('HSP7C_SAGOE', 2, 'TTPSYVAFTDTER', 2),
            ('HSP7D_DROME', 2, 'TTPSYVAFTDTER', 2),
            ('HSP7A_DROME', 2, 'TTPSYVAFTESER', 2),
            ('HSP7A_DROSI', 2, 'TTPSYVAFTESER', 2),
            ('HSP7A_DROME', 2, 'NQVAMNPNNTIFDAK', 2),
            ('HSP7A_DROSI', 2, 'NQVAMNPNNTIFDAK', 2),
            ('HSP7D_MANSE', 2, 'NQVAMNPNNTIFDAK', 2),
            ('HS70L_HUMAN', 2, 'NQVAMNPQNTVFDAK', 2),
            ('HS70L_MOUSE', 2, 'NQVAMNPQNTVFDAK', 2),
            ('HS70L_RAT', 2, 'NQVAMNPQNTVFDAK', 2),
            ('HSP70_XENLA', 2, 'NQVAMNPQNTVFDAK', 2),
            ('HSP7D_DROME', 2, 'NQVAMNPTQTIFDAK', 2)
    )

    base = "mzIdent"
    files = ["Mascott_file1.mzid", "Mascott_file2.mzid"]
    
class data_mascot(tpath):
    data = (("28590", 2, "AWAVAR", 2),
            ("28590", 2, "YLYEIAR", 2),
            ("28590", 2, "FQNALLVR", 2),
            ("28590", 2, "KQTALVELVK", 2),
            ("78101694", 2, "AWAVAR", 2),
            ("78101694", 2, "YLYEIAR", 2),
            ("386854", 2, "SLNNQFASFIDK", 2),
            ("992948", 2, "YPDAVATWLNPDPSQK", 2),
            ("4504943", 2, "GPVGVQTFR", 2),
            ("165761385", 2, "QFLIEIPEINEK", 2))

    base = "mascot"
    files = ["Mascot1.xml", "Mascot2.xml"]


class data_pride(tpath):
    data = (("IPI00448095.3", 2, "SGMTTGSTLPVEGGFWAC", 2),
            ("IPI00032179.2", 2, "TSDQIHFFFAK", 2),
            ("IPI00414283.1", 2, "TNTNVNCPIECFMPLDVQA", 2),
            ("IPI00414283.1", 2, "TNTNVNCPIECFMPLDV", 2),
            ("IPI00219344.3", 2, "LLQCDPSSASQF", 2),
            ("IPI00472718.1", 2, "ITIADCGQLE", 2),
            ("IPI00418163.3", 2, "AACAQLNDFLQEYGTQGCQV", 2))

    base = "PRIDE"
    files = ["PRIDE_Exp_Complete_Ac_8172.xml.gz", 
             "PRIDE_Exp_IdentOnly_Ac_8172.xml.gz"]

form = "%d != %d\nprotein %s, peptide %s" 
form2 = "%d != %d\nprotein %s"
            
class SequestPeptide_Case(unittest.TestCase):

    def test_xml_peptide(self):
        p = proteomic_xml.sequest_pep_parser()
        examples = data_sequest_pep()
        for file in examples.get_file():
            p.parse(file)
        
        for (acc, prot_occs, seq, pept_occs,) in examples.data:
            self.assertEqual(prot_occs, p.proteins[acc],
                msg=form2 % (prot_occs, p.proteins[acc],acc))
            
            self.assertEqual(pept_occs, p.peptides[acc][seq],
                msg= form % (pept_occs, p.peptides[acc][seq],acc, seq))

    def test_xml_dist_peptide(self):
        p = proteomic_xml.sequest_pep_parser()
        examples = data_sequest_pep_dist()
        for file in examples.get_file():
            p.parse(file)
        for (acc, prot_occs, seq, pept_occs,) in examples.data:
            self.assertEqual(prot_occs, p.proteins[acc],
                msg = form2 % (prot_occs, p.proteins[acc],acc))
            
            self.assertEqual(pept_occs, p.peptides[acc][seq],
                msg = form % (pept_occs, p.peptides[acc][seq],acc, seq))

    def test_wrong_files(self):
        p = proteomic_xml.sequest_pep_parser()
        objs = [
                #data_sequest_pep(),
                #data_sequest_pep_dist(),
                data_sequest_pro(),
                data_sequest_pro_dist(),
                data_discoverer_pept(),
                data_discoverer_prot(),
                data_mascot(),
                data_pride(),
                data_mzIdent()
        ]
        for obj in objs:
            for file in obj.get_file():
                print file
                self.assertRaises(proteomic_xml.wrongFile, p.parse, file)

class SequestProtPept_Case(unittest.TestCase):

    def test_xml_protein(self):
        p = proteomic_xml.sequest_prot_parser()
        examples = data_sequest_pro()
        for file in examples.get_file():
            p.parse(file)
        for (acc, prot_occs, seq, pept_occs,) in examples.data:
            try:
                self.assertEqual(prot_occs, p.proteins[acc],
                    msg = form2 % (prot_occs, p.proteins[acc],acc))
            except KeyError:
                print acc
            self.assertEqual(pept_occs, p.peptides[acc][seq],
                msg=form % (pept_occs, p.peptides[acc][seq],acc, seq))

    def test_xml_dist_protein(self):
        p = proteomic_xml.sequest_prot_parser()
        examples = data_sequest_pro_dist()
        for file in examples.get_file():
            p.parse(file)
        for (acc, prot_occs, seq, pept_occs,) in examples.data:
            self.assertEqual(prot_occs, p.proteins[acc],
                msg = form2 %(prot_occs, p.proteins[acc],acc))
            
            self.assertEqual(pept_occs, p.peptides[acc][seq],
                msg = form %(pept_occs, p.peptides[acc][seq],acc, seq))

    def test_wrong_files(self):
        p = proteomic_xml.sequest_prot_parser()
        #Todo: Fix this
        objs = [
                data_sequest_pep(),
                data_sequest_pep_dist(),
                #data_sequest_pro(),
                #data_sequest_pro_dist(),
                data_discoverer_pept(),
                data_discoverer_prot(),
                data_mascot(),
                data_pride(),
                data_mzIdent()
                ]
        for obj in objs:
            for file in obj.get_file():
                self.assertRaises(proteomic_xml.wrongFile, p.parse, file)

class Mascot_Case(unittest.TestCase, data_mascot):

    def test_mascot(self):
        p = proteomic_xml.mascot_parser()
        examples = data_mascot()
        for file in examples.get_file():
            p.parse(file)
        for (acc, prot_occs, seq, pept_occs,) in examples.data:
            self.assertEqual(prot_occs, p.proteins[acc],
                msg = form2 % (prot_occs, p.proteins[acc],acc))
            self.assertEqual(pept_occs, p.peptides[acc][seq],
                msg = form % (pept_occs, p.peptides[acc][seq],acc, seq))

    def test_wrong_files(self):
        p = proteomic_xml.mascot_parser()
        objs = [
                data_sequest_pep(),
                data_sequest_pep_dist(),
                data_sequest_pro(),
                data_sequest_pro_dist(),
                data_discoverer_pept(),
                data_discoverer_prot(),
                #data_mascot(),
                data_pride(),
                data_mzIdent()
        ]
        for obj in objs:
            for file in obj.get_file():
                print file
                self.assertRaises(proteomic_xml.wrongFile, p.parse, file)

class PRIDE_Case(unittest.TestCase, data_pride):

    def test_pride(self):
        p = proteomic_xml.pride_parser(compressed = True)
        examples = data_pride()
        for file in examples.get_file():
            p.parse(file)
        for (acc, prot_occs, seq, pept_occs,) in examples.data:
            self.assertEqual(prot_occs, p.proteins[acc],
                msg = form2 % (prot_occs, p.proteins[acc],acc))
            self.assertEqual(pept_occs, p.peptides[acc][seq],
                msg = form %(pept_occs, p.peptides[acc][seq],acc, seq))

    def test_wrong_files(self):
        p = proteomic_xml.pride_parser()
        objs = [
                data_sequest_pep(),
                data_sequest_pep_dist(),
                data_sequest_pro(),
                data_sequest_pro_dist(),
                data_discoverer_pept(),
                data_discoverer_prot(),
                data_mascot(),
                #data_pride(),
                data_mzIdent()
        ]
        for obj in objs:
            for file in obj.get_file():
                print file
                self.assertRaises(proteomic_xml.wrongFile, p.parse, file)

class MzIdent_Case(unittest.TestCase, data_mzIdent):

    def test_mzIdent(self):
        p = proteomic_xml.mzIdent_parser()
        examples = data_mzIdent()
        for file in examples.get_file():
            p.parse(file)

        for (acc, prot_occs, seq, pept_occs, ) in examples.data:
            self.assertEqual(prot_occs, p.proteins[acc],
                msg=form2 % (prot_occs, p.proteins[acc], acc))
            self.assertEqual(pept_occs,p.peptides[acc][seq],
                msg= form % (pept_occs, p.peptides[acc][seq], acc, seq))

    def test_wrong_files(self):
        p = proteomic_xml.mzIdent_parser()
        objs =[
                data_sequest_pep(),
                data_sequest_pep_dist(),
                data_sequest_pro(),
                data_sequest_pro_dist(),
                data_discoverer_pept(),
                data_discoverer_prot(),
                data_mascot(),
                data_pride(),
                #data_mzIdent()
        ]
        for obj in objs:
            for file in obj.get_file():
                print file
                self.assertRaises(proteomic_xml.wrongFile, p.parse, file)

class DiscovererProts_Case(unittest.TestCase):

    def test_xml_prots(self):
        p = proteomic_xml.discoverer_prot_parser()
        examples = data_discoverer_prot()
        for file in examples.get_file():
            p.parse(file)
        
        for (acc, prot_occs, seq, pept_occs,) in examples.data:
            self.assertEqual(prot_occs, p.proteins[acc],
                msg=form2 % (prot_occs, p.proteins[acc],acc))
            
            self.assertEqual(pept_occs, p.peptides[acc][seq],
                msg= form % (pept_occs, p.peptides[acc][seq],acc, seq))

    def test_wrong_files(self):
        p = proteomic_xml.discoverer_prot_parser()
        objs = [
                data_sequest_pep(),
                data_sequest_pep_dist(),
                data_sequest_pro(),
                data_sequest_pro_dist(),
                data_discoverer_pept(),
                #data_discoverer_prot(),
                data_mascot(),
                data_pride(),
                data_mzIdent()
        ]
        for obj in objs:
            for file in obj.get_file():
                print file
                self.assertRaises(proteomic_xml.wrongFile, p.parse, file)
                
class DiscovererPept_Case(unittest.TestCase):

    def test_xml_pepts(self):
        p = proteomic_xml.discoverer_pept_parser()
        examples = data_discoverer_pept()
        for file in examples.get_file():
            p.parse(file)
        
        for (acc, prot_occs, seq, pept_occs,) in examples.data:
            self.assertEqual(prot_occs, p.proteins[acc],
                msg=form2 % (prot_occs, p.proteins[acc],acc))
            
            self.assertEqual(pept_occs, p.peptides[acc][seq],
                msg= form % (pept_occs, p.peptides[acc][seq],acc, seq))

    def test_wrong_files(self):
        p = proteomic_xml.discoverer_pept_parser()
        objs = [
                data_sequest_pep(),
                data_sequest_pep_dist(),
                data_sequest_pro(),
                data_sequest_pro_dist(),
                #data_discoverer_pept(),
                data_discoverer_prot(),
                data_mascot(),
                data_pride(),
                data_mzIdent()
        ]
        for obj in objs:
            for file in obj.get_file():
                print file
                self.assertRaises(proteomic_xml.wrongFile, p.parse, file)

if __name__ == '__main__':
    #unittest.main()
    nose.main()
