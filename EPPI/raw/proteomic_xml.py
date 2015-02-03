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
"""
proteomic_xml.py

all you need to read different xml file format
"""
from xml.dom import minidom
from xml.parsers.expat import ExpatError
import gzip
import data_input
import os
import tempfile
import re

class xml_Error(Exception):
    """
    base class for proteomic xml parser classes
    """
    pass

class wrongFile(xml_Error):
    """ Error occurred when users confuse different xml format """
    pass

class bad_id(xml_Error):
    """ Error occurred when protein identification is not standard"""
    pass

gi_part = r"(?<=^gi\|)\d+"
sp_part = r"(?<=^sp\|)[0-9A-Z]+"
tr_part = r"(?<=^tr\|)[0-9A-Z]+"
ipi_part = r'(?<=^IPI:)IPI\d+\.\d'
groups = r'|'.join([gi_part, sp_part, tr_part, ipi_part])
acc2id = re.compile(groups)

class _xml_parser(data_input.parser):
    """
    Base class for all xml_parser
    """
    #TODO: Some parts of parser are identical...
    # try to put them here
    def __init__(self, compressed=False):
        """
        parser initialization

        :cvar compressed: If the reading file is compressed (.gz) or not
        :type compressed: bool
        """
        data_input.parser.__init__(self)
        self.compressed = compressed


    def _start_parse(self, fileName, ctrl_tag):
        """
        start parsing a pride file

        :param fileName: the file path
        :type fileName: str
        :param ctrl_tag: check the file
        :type ctrl_tag: str
        :raises wrongFile: If you pass a wrong pride file
        :cvar Err_msg: error message if it's wrong ns
        :cvar Err_msg_2: error message if there is not a xml file
        """

        Err_msg = "ExpatError: {0} must be a regular {1} xml file"
        Err_msg_2 = "{0} must be a {1} xml file"

        try:
            if self.compressed:
                underlying_file = open(fileName, 'rb')
                uncompressing_wrapper = gzip.GzipFile(fileobj=underlying_file,
                                                      mode='rt')
                xmldoc = minidom.parse(uncompressing_wrapper)
                uncompressing_wrapper.close()
                underlying_file.close()
            else:
                xmldoc = minidom.parse(fileName)
        except ExpatError:
            raise wrongFile, Err_msg.format(fileName, type(self))
        if not xmldoc.getElementsByTagName(ctrl_tag):
            raise wrongFile, Err_msg_2.format(fileName, type(self))

        self._sources_store(fileName)
        return xmldoc

class pride_parser(_xml_parser):
    """
    Parser for pride old xml files.
    It's possible to open compressed seq
    """
    def __init__(self, compressed = False):
        """
        Initialize a pride parser
        """
        _xml_parser.__init__(self, compressed)


    def parse (self, fileName):
        """
        parsing a pride file

        :param fileName: the file path
        :type fileName: str
        :raises wrongFile: If you pass a wrong pride file
        """

        xmldoc = self._start_parse(fileName, "ExperimentCollection")

        _unique_prot = []
        _unique = []
        i_list = xmldoc.getElementsByTagName('GelFreeIdentification')
        i_list.extend(xmldoc.getElementsByTagName('TwoDimensionalIdentification'))
        for i in i_list:
            acc_list = i.childNodes
            for acc in acc_list:
                if acc.nodeName == 'Accession':
                    acc_key = acc.firstChild.nodeValue

                    self._in_case_prot(acc_key, _unique_prot)


                elif acc.nodeName == 'PeptideItem':
                    for s in acc.getElementsByTagName('Sequence'):
                        seq_key=s.firstChild.nodeValue
                        self._peptides_store(acc_key, seq_key, _unique)

class mzIdent_parser(_xml_parser):
    """
    Parser that reads the mzIdent file
    (v 1.1.0)
    """
    def __init__(self):
        _xml_parser.__init__(self, compressed=False)

    def parse(self, fileName):
        """
        parsing a mzIdent file (v 1.1.0)

        :param fileName: the file path
        :type fileName: str
        :raises wrongFile: If you pass a wrong pride file
        """

        xmldoc = self._start_parse(fileName, "MzIdentML")

        _unique_prot = []
        _unique = []
        evidences = xmldoc.getElementsByTagName('PeptideEvidence')
        proteins = xmldoc.getElementsByTagName('DBSequence')
        peptides = xmldoc.getElementsByTagName('Peptide')
        for evidence in evidences:
            prot_id = evidence.attributes[u'dBSequence_ref'].value
            pept_id = evidence.attributes[u'peptide_ref'].value
            for protein in proteins:
                if protein.attributes[u'id'].value == prot_id:
                    id_num = protein.attributes[u'accession'].value

                    accs= acc2id.findall(id_num)
                    if accs:
                        acc_key = accs[0]
                    else:
                        acc_key = id_num
                    #raise bad_id, "No standard id {0}".format(id_num)

                    self._in_case_prot(acc_key, _unique_prot)
            for peptide in peptides:
                if peptide.attributes[u'id'].value == pept_id:
                    for s in peptide.getElementsByTagName('PeptideSequence'):
                        seq_key = s.firstChild.nodeValue
                        self._peptides_store(acc_key, seq_key, _unique)

class mascot_parser(_xml_parser):
    """
    parser for mascot xml files
    """

    def __init__(self, compressed = False):
        """
        Initialize a parser
        """
        _xml_parser.__init__(self, compressed)

    def parse(self, fileName):
        """
        parsing a mascot xml file

        :param fileName: the file path
        :type fileName: str
        :raises wrongFile: If you pass a wrong mascot file
        :raises bad_id: If there is a no standard protein id
        """

        xmldoc = self._start_parse(fileName, "mascot_search_results")

        _unique_prot = []
        _unique = []

        for i in xmldoc.getElementsByTagName('protein'):
            id_num = i.attributes[u'accession'].value
            accs= acc2id.findall(id_num)

            if accs:
                acc_key = accs[0]
            else:
                acc_key = id_num

            self._in_case_prot(acc_key, _unique_prot)


            for pep in i.getElementsByTagName('peptide'):
                for s in pep.getElementsByTagName('pep_seq'):
                    seq_key=s.firstChild.nodeValue
                    self._peptides_store(acc_key, seq_key, _unique)


class sequest_pep_parser(_xml_parser, data_input.sequest_parser):
    """
    parser for sequest peptides xml files
    """

    def __init__(self, compressed = False):
        """
        Initialize a parser
        """
        _xml_parser.__init__(self, compressed)

    def _fix_sequest_pep(self, fileName):
        """
        If xml pep sequest files are wrong this fixes the error
        (There is a trouble inside sequest program, probably)

        :param fileName: the file path
        :type fileName: str
        """
        row1 = \
            '<sequestresults xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">\n'

        fd, path = tempfile.mkstemp(suffix=".xml", text=True)
        handler = open(fileName, mode='rb')
        handlew = open(path, mode='wb')

        for line in handler:
            if "<sequestresults" in line:
                handlew.write(row1)
                handlew.write('<origfilename></origfilename>\n')
            elif "</sequestresults>" in line:
                handlew.write("</sequestresults>")
            else:
                handlew.write(line)
        handler.close()
        handlew.close()
        return fd, path

    def parse(self, fileName):
        """
        parsing a sequest xml peptide file

        :param fileName: the file path
        :type fileName: str
        :raises wrongFile: If you pass a wrong sequest peptide xml file
        """
        fh, temp = self._fix_sequest_pep(fileName)

        xmldoc = self._start_parse(temp, "peptide_match")

        _unique_prot = []
        _unique = []

        for i in xmldoc.getElementsByTagName('peptide_match'):
            acc_list = i.childNodes
            for acc in acc_list:
                if acc.nodeName == 'reference':
                    node_value = acc.firstChild.nodeValue
                    acc_key = acc2id.findall(node_value)[0]

                    self._in_case_prot(acc_key, _unique_prot)

                elif acc.nodeName == 'peptide':
                    seq_key = self._to_peptide(acc.firstChild.nodeValue)
                    self._peptides_store(acc_key, seq_key, _unique)
        os.close(fh)
        os.unlink(temp)

class sequest_prot_parser(_xml_parser, data_input.sequest_parser):
    """
    parser for sequest protein xml files
    """
    def __init__(self, compressed = False):
        """
        Initialize a parser
        """
        _xml_parser.__init__(self, compressed)

    def parse(self, fileName):
        """
        parsing a sequest xml protein file

        :param fileName: the file path
        :type fileName: str
        :raises wrongFile: If you pass a wrong sequest protein xml file
        """

        xmldoc = self._start_parse(fileName, "bioworksinfo")
                                   #"peptide_match")

        _unique_prot = []
        _unique = []

        for i in xmldoc.getElementsByTagName('protein'):
            acc_list = i.childNodes
            for acc in acc_list:
                if acc.nodeName == 'reference':
                    node_value = acc.firstChild.nodeValue
                    acc_key = acc2id.findall(node_value)[0]

                    self._in_case_prot(acc_key, _unique_prot)

                elif acc.nodeName == 'peptide':
                    for s in acc.getElementsByTagName('sequence'):
                        seq_key = self._to_peptide(s.firstChild.nodeValue)
                        self._peptides_store(acc_key, seq_key, _unique)

class discoverer_prot_parser(_xml_parser):
    """
    parser for discoverer protein xml files
    """
    def __init__(self, compressed = False):
        """
        Initialize a parser
        """
        _xml_parser.__init__(self, compressed)

    def parse(self, fileName):
        """
        parsing a discoverer xml protein file

        :param fileName: the file path
        :type fileName: str
        :raises wrongFile: If you pass a wrong discoverer protein xml file
        """

        xmldoc = self._start_parse(fileName, "protein_summary")

        _unique_prot = []
        _unique = []

        for i in xmldoc.getElementsByTagName('protein_group'):
            for acc in i.getElementsByTagName('protein'):
                acc_key = acc.attributes[u'protein_name'].value

                self._in_case_prot(acc_key, _unique_prot)

                for s in i.getElementsByTagName('peptide'): #seqlist:
                    seq_key = s.attributes[u'peptide_sequence'].value

                    self._peptides_store(acc_key, seq_key, _unique)

class discoverer_pept_parser(_xml_parser):
    """
    parser for dscoverer peptides xml files
    """
    def __init__(self, compressed = False, alternative = True):
        """
        Initialize a parser
        """
        _xml_parser.__init__(self, compressed)
        self.alt = alternative

    def parse(self, fileName):
        """
        parsing a discoverer xml protein file

        :param fileName: the file path
        :type fileName: str
        :raises wrongFile: If you pass a wrong discoverer protein xml file
        """

        xmldoc = self._start_parse(fileName, "msms_pipeline_analysis")

        _unique_prot = []
        _unique = []

        for i in xmldoc.getElementsByTagName('search_hit'):

            acc_key = i.attributes[u'protein'].value

            self._in_case_prot(acc_key, _unique_prot)

            seq_key = i.attributes[u'peptide'].value
            self._peptides_store(acc_key, seq_key, _unique)

            # if there are alternatives
            if self.alt:
                for each in i.getElementsByTagName("alternative_protein"):
                    acc_key = each.attributes[u'protein'].value
                    self._in_case_prot(acc_key, _unique_prot)
                    self._peptides_store(acc_key, seq_key, _unique)

