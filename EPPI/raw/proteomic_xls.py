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

""" It calculates the number of occurrences of proteins 
and peptides inside xls MS derived files

Input: .xls file deriving from BIOWORK(TM) software analysis
"""

__authors__ = "Pietro Brunetti"

from xlrd import open_workbook, XL_CELL_BLANK, XL_CELL_EMPTY, XL_CELL_NUMBER
from data_input import parser, sequest_parser
import data_input

class xls_Error(Exception):
    """
    Base class for proteomic xls exception parser
    """
    pass

class wrongFile(xls_Error):
    """
    occurres when users confuse different xml format
    """
    pass

class EmptyCell(xls_Error):
    """
    occurres when a cell is unexpectedly empty
    """
    pass

class Same_Accession(xls_Error):
    """
    raises when two proteins have
    the same Accession number
    """
    pass

class Without_Field(xls_Error):
    """
    Raises when there's basic column in the file
    """
    pass
     
#ToDo: Make DRY! 

wrong_tmpl = "{0} must be a {1} xls file"
same_acc_tmpl = "{0}: {1} redundant {2}"
wrng_pep_tmpl = "{0}: {1} reading: '{2}'"

class xls_parser(parser):
    """
    Base class for each xls parser
    """

    #to-do: make this one a class method
    #@class_method
    def what_kind_of_file(self, sheet):
        """
        recognizes Kind of xls file

        :param sheet: excel sheet cointaing proteomic seq
        :type sheet: xlrd sheet
        :return: the kind of xls file. The chooses are:
            - onlypep
            - protpep
            - discoverer
            - wrongXLS
        :rtype: str
        """
        if sheet.ncols == 0:
            return 'wrongXLS'
        # Cannot exist a file that is at the same time onlypept and protpept
        if (sheet.cell_value(rowx=0, colx=1) == u'Reference') and\
            (sheet.cell_value(rowx=1, colx=1) == u'Scan(s), File') and\
            (sheet.cell_value(rowx=0, colx=0) == u'Scan(s)'):
            return 'wrongXLS'
        elif(sheet.cell_value(rowx=0, colx=1) == u'Reference') and\
            (sheet.cell_value(rowx=1, colx=1) == u'Scan(s), File'):
            return "protpep"
        elif(sheet.cell_value(rowx=0, colx=0) == u'Accession') and\
            (sheet.cell_value(rowx=0, colx=1) == u'Description'):
            return "discoverer"
        elif(sheet.cell_value(rowx=0, colx=0) == u'Scan(s)') and\
          (sheet.cell_value(rowx=0, colx=1) == u'Reference'):
            return "onlypep"
        else:
            return 'wrongXLS'
        
    
    def find_fields(self, sheet, xls_type, filename):
        """
        Searches and stores Accession column and peptide sequence column numbers

        :param sheet: excel sheet cointaing proteomic seq
        :type sheet: xlrd sheet
        :param xls_type: type of xls file. . The chooses are:
            - onlypep
            - protpep
        :type xls_type: str
        :param filename: the path of excel file
        :type filename: str
        :return: the two column numbers
        :rtype: (int, int)
        :raises Without_Field: if there aren't inside the file the Accession or the peptide columns
        """
        acc_n = -1
        pep_n = -1
        header0 = sheet.row_values(rowx=0)
        if u'Accession' in header0:
            acc_n = header0.index(u'Accession')
        if acc_n == -1:
            raise Without_Field,\
            "{0} without a Accession column".format(filename)
        if xls_type == "protpep":
            header1 = sheet.row_values(rowx=1)
            if  u'Peptide' in header1:
                pep_n = header1.index(u'Peptide')
        elif xls_type == "onlypep":
            if  u'Peptide' in header0:
                pep_n = header0.index(u'Peptide')
        elif xls_type == "discoverer":
            header1 = sheet.row_values(rowx=2)
            if u'Sequence' in header1:
                pep_n = header1.index(u'Sequence')
        if pep_n == -1:
            raise Without_Field, \
            "{0} {1} without a Peptide column".format(xls_type, filename)
        return acc_n, pep_n
 
class sequest_protpept_parser(xls_parser, sequest_parser):
    """
    parser for protein peptide sequest excel file
    """
    def parse(self, fileName):
        """
        Parse protein and peptide sequest xls file
        if spectral_count_mode is True count peptided repeats
        :param fileName: the path of the excel file
        :type fileName: str
        :raises wrongFile: If the file passed is wrong or corrupted
        :raises EmptyCell: If it reads an unexpected empty cell
        :raises Same_Accession: If there are almost two identical proteins
        """
        self._sources_store(fileName)
        # Opening .xls file
        book = open_workbook(fileName)
        sheet = book.sheet_by_index(0)
        xls_type = self.what_kind_of_file(sheet)
        if not xls_type == "protpep":
            raise wrongFile, wrong_tmpl.format(fileName, "protpep")
        rows_len = sheet.nrows
        # After two rows, seq start
        row_idx = 2
        acc_n, pep_n = self.find_fields(sheet, xls_type, fileName)
        prot_uniques = []
        _unique = []
        # Searching and scoring proteins and peptides
        #print rows_len
        while row_idx < rows_len:
            ctrl = sheet.cell(rowx=row_idx, colx=0)
            # A protein row starts with a numeber in the first cell
            if ctrl.ctype == XL_CELL_NUMBER :
                acc = sheet.cell(rowx=row_idx, colx=acc_n)
                # I don't remember if ctype is XL_CELL_EMPTY or XL_CELL_BLANK
                if acc.ctype in [XL_CELL_BLANK,XL_CELL_EMPTY]:
                    raise EmptyCell, wrng_pep_tmpl.format(fileName,
                      row_idx, acc_n)
                if acc.value in prot_uniques:
                    raise Same_Accession, \
                    same_acc_tmpl.format(fileName, row_idx, acc)
                else: prot_uniques.append(acc.value)
                if acc.ctype == XL_CELL_NUMBER:
                    acc_v = str(int(acc.value))
                    # if it is the first time that we see this protein for this file
                    self._in_case_prot(acc_v, prot_uniques)
                    
            #A peptide row starts with a empty cell
            elif ctrl.ctype == XL_CELL_EMPTY:
                pep = sheet.cell(rowx=row_idx, colx=pep_n)
                if pep.ctype in [XL_CELL_BLANK, XL_CELL_EMPTY]:
                    #pass
                    raise EmptyCell, wrng_pep_tmpl.format(fileName, row_idx, pep_n)
                seq_pep = self._to_peptide(pep.value)
                self._peptides_store(acc_v, seq_pep, _unique)
            row_idx+=1
        return self.proteins, self.peptides

class sequest_onlypept_parser(xls_parser, sequest_parser):
    """
    only peptide sequest excel file
    """
    def parse(self, fileName):
        """
        Parse peptide sequest xls file
        if spectral_count_mode is True count peptides repeats

        :param fileName: the path of the excel file
        :type fileName: str
        :raises wrongFile: If the file passed is wrong or corrupted
        :raises EmptyCell: If it reads an unexpected empty cell
        :raises Same_Accession: If there are almost two identical proteins
        """
        self._sources_store(fileName)
        # Opening .xls file
        book = open_workbook(fileName)
        sheet = book.sheet_by_index(0)
        xls_type = self.what_kind_of_file(sheet)
        if not xls_type == "onlypep":
            raise wrongFile, wrong_tmpl.format(fileName, "onlypep")
        rows_len = sheet.nrows
        row_idx = 1
        acc_n, pep_n = self.find_fields(sheet, xls_type, fileName)
        _unique = []
        _prot_unique = []
        # Searching and storing protein and peptide
        while row_idx < rows_len:
            ctrl = sheet.cell(rowx=row_idx, colx=0)
            if ctrl.ctype == XL_CELL_BLANK:
                break
            acc = sheet.cell(rowx=row_idx, colx=acc_n)
            if acc.ctype in [XL_CELL_BLANK, XL_CELL_EMPTY]:
                raise EmptyCell, wrng_pep_tmpl.format(fileName, row_idx, acc_n)
            if acc.ctype == XL_CELL_NUMBER:
                acc_v = str(int(acc.value))
                self._in_case_prot(acc_v, _prot_unique)
                
                pep = sheet.cell(rowx=row_idx, colx=pep_n)
                if pep.ctype in [XL_CELL_BLANK, XL_CELL_EMPTY]:
                    raise EmptyCell, wrng_pep_tmpl.format(fileName,
                    row_idx, pep_n)
                try:
                    seq_pep = self._to_peptide(pep.value)
                except data_input.bad_format_peptide:
                    raise data_input.bad_format_peptide, wrng_pep_tmpl.format(fileName, 
                    row_idx, pep_n)
                self._peptides_store(acc_v, seq_pep, _unique)
            row_idx+=1
        return self.proteins, self.peptides

class discoverer_parser(xls_parser, parser):
    """
    parser for protein peptide discoverer excel file
    """
    def parse(self, fileName):
        """
        Parse protein and peptide discoverer xls file
        if spectral_count_mode is True count peptides repeats
        :param fileName: the path of the excel file
        :type fileName: str
        :raises wrongFile: If the file passed is wrong or corrupted
        :raises Same_Accession: If there are almost two identical proteins
        """
        self._sources_store(fileName)
        # Opening .xls file
        book = open_workbook(fileName)
        sheet = book.sheet_by_index(0)
        xls_type = self.what_kind_of_file(sheet)
        if not xls_type == "discoverer":
            raise wrongFile,  wrong_tmpl.format(fileName, "discoverer")
        rows_len = sheet.nrows
        # Reading from first row
        row_idx = 0
        acc_n, pep_n = self.find_fields(sheet, xls_type, fileName)
        prot_uniques = []
        _unique = []
        # Searching and scoring proteins and peptides
        while row_idx < rows_len:
            acc = sheet.cell(rowx=row_idx, colx=acc_n)
            pep = sheet.cell(rowx=row_idx, colx=pep_n)
            # A protein row starts with a number in the first cell
            if acc.value == u'Accession':
                pass
            elif acc.ctype in [XL_CELL_BLANK, XL_CELL_EMPTY]:
                #work with peptide
                pep = sheet.cell(rowx=row_idx, colx=pep_n)
                if pep.value == u'Sequence':
                    pass
                else:
                    self._peptides_store(acc_v, pep.value, _unique)
            else:
                if acc.ctype == XL_CELL_NUMBER:
                    acc_v = str(int(acc.value))
                else: 
                    acc_v = acc.value
                
                if acc_v in prot_uniques:    
                    raise Same_Accession, \
                    same_acc_tmpl.format(fileName, row_idx, acc)
                else:
                    self._in_case_prot(acc_v, prot_uniques)
                        
            row_idx+=1