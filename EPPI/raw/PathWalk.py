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


""" This script is used to estimate the numer of
    xls MS files, number of proteins 
    and number of peptide"""
    
__authors__ = "Pietro Brunetti"

def all_files(root, patterns='*', single_level=False):
    """
    yield  the file containg b a directory three
    """
    
    import os,  fnmatch
    # Expand patterns from semicolon-separated 
    # string to list
    patterns = patterns.split(';')
    for path, subdirs, files in os.walk(root):
        files.sort()
        for name in files:
            for pattern in patterns:
                if fnmatch.fnmatch(name, pattern):
                    yield os.path.join(path, name)
                    break
        if single_level: 
            break

def count_pepts_N_prots(xlsfiles):
    """
    Count number of proteins and peptides
    inside a list of xls files
    """
    import xlrd
    #import string

    countProt = 0		# Number of proteins 
    countPept = 0		# Number of peptides 
  
    for xlsfile in xlsfiles:
        #print xlsfile   
        book = xlrd.open_workbook(xlsfile)
        sheet = book.sheet_by_index(0)
    
        PeptHits_col = 0
        cols_len = sheet.ncols
        col_idx = 0
        while(col_idx < cols_len):
            if sheet.cell_value(rowx = 0, colx = col_idx) == "Peptide (Hits)":
                PeptHits_col = col_idx
                break
        col_idx += 1
        col_idx = 0
        while(col_idx < cols_len):
            if sheet.cell_value(rowx = 1, colx = col_idx) == "Peptide (Hits)":
                PeptHits_col = col_idx
                break
        col_idx += 1

        rows_len = sheet.nrows
        row_idx = 0
        while(row_idx < rows_len):
            ctrl = sheet.cell_value(rowx=row_idx, colx=0)
            # A protein row starts with a number in the first cell
            #if(type(ctrl) == type(1.0) and ctrl != ''):
            if isinstance(ctrl, float):
                countProt += 1
                countPept += int(sheet.cell_value(rowx=row_idx, 
                                                  colx=PeptHits_col).split('(')[0])
            row_idx += 1  
  
    return (countProt, countPept)

if __name__ == "__main__":
    import shutil, sys, os
    try:
        me, ext, directory, dest =\
            sys.argv[0], sys.argv[1], sys.argv[2], sys.argv[3]
    
    except:
        me = sys.argv[0]
        sys.exit('Exit: use: {0} "extension", "root directory files",  "destination directory" ...\n'.format(me))
    main = os.path.split(directory)[1]
    #print dest, main
    new_dest = os.path.join(dest, main)
    if not os.path.exists(new_dest):
        os.makedirs(new_dest)
    os.chdir(new_dest)
    resume = open('{0}.txt'.format(main), 'w')
    files = list(all_files(directory, '{0}.{1}'.format('*[0-9][0-9]_[A-Z]', ext)))
    l = len(files)
    resume.write("Number of files: {0}\n".format(l))
    r = count_pepts_N_prots(files)
    #print r
    resume.write("Number of proteins: {0}\n".format(r[0]))
    resume.write("Number of peptides: {0}\n".format(r[1]))
    for path in files:
        shutil.copy2(path, new_dest)
        resume.write('{0}\n'.format(path))