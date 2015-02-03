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

__authors__ = "Pietro Brunetti"

from xlrd import open_workbook
from random import randint


path = r"/media/raid_2009/User_Temp/Pietro/NoVa_X_01_R_Ana_pep.xls"
def xls_extract(path):
    book = open_workbook(path)
    sheet = book.sheet_by_index(0)

    peptide = ""
    protein = ""
    for row_index in range(1, sheet.nrows):
        if (sheet.cell(row_index, 0).value):
            protein = sheet.cell(row_index, 0).value
        else:
            if sheet.cell(row_index, 2).value != "Sequence":
                if (protein, sheet.cell(row_index, 2).value) != (protein, peptide):
                    peptide = sheet.cell(row_index, 2).value
                    if randint(1,40) == 7:
                        #print form.format(protein, peptide)
                        yield (protein, 2, peptide, 2)

if __name__ == "__main__":
    path = r"/media/raid_2009/User_Temp/Pietro/NoVa_X_01_R_Ana_pep.xls"
    for i in xls_extract(path):
        print i
