
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

'''
Created on Oct 18, 2012

@author: Pietro Brunetti
'''

__authors__ = "Pietro Brunetti"

import unittest
from EPPI import by_targets
from EPPI.peptidome.commons import peptidases
from EPPI.peptidome import fasta_indx

import os
from os import curdir
import os.path as path
from os.path import abspath


import shutil
import csv



class by_targets_Test(unittest.TestCase):

    def tearDown(self):
        """
        Removing stuffs in filesystem  after tests
        """
        rm_files = [
           "peptidome\\mw_card.csv",
           "peptidome\\mw_search.csv",
           "peptidome\\mw_result.csv",
           "peptidome\\seq_card.csv",
           "peptidome\\seq_search.csv",
           "peptidome\\seq_result.csv",
           "mw_card.csv",
           "mw_search.csv",
           "mw_result.csv",
           "seq_card.csv",
           "seq_search.csv",
           "seq_result.csv"]

        for f in rm_files:
            if os.path.exists(f):
                os.remove(f)


    s1 = set([1,2,3,4,5])
    s2 = set([3,4,5,6,7,8,9])
    s3 = set([4,5,6])
    s4 = set(['foo'])
    s5 = set(['foo'])
    s6 = set(['foo'])
    
    asp_map_by_tar = [
        ([s1, s2, s3],
         [set([3, 4, 5]), set([4, 5]), set([4, 5, 6]), set([4, 5])]),
        ([s1, s2], 
         [set([3, 4, 5])]),
        ([s1, s3], 
         [set([4, 5])]),
        ([s2, s3], 
         [set([4, 5, 6])]),
        ([s1], 
         []),
        ([s2], 
         []),
        ([s3], 
         []),
        ([s4, s5, s6], 
         [set(['foo']),set(['foo']),set(['foo']),set(['foo'])])
    ]

    def test__intersect(self):
        for inp, asp in self.asp_map_by_tar:
            res = by_targets._intersect(inp)
            self.assertItemsEqual(res, asp, msg = res)


    asp_min_but_not_z = [([0, 0, 0, 5, 2, 100, 5, 2],     2),
                         ([0, 0, 0, 5, 2, 100, 5, 2, -1], 2),
                         ([0, 0, 0, 0, 0, 0, 0, 0.1],   0.1),
                         ([0, 0, 0, 0, 0, 0],             0),]

    def test__min_but_not_zero(self):
        for inp, asp in self.asp_min_but_not_z:
            self.assertEqual(by_targets._min_but_not_zero(inp), asp)

    asp_card = [([1, [1]], [1, 0, 0, 0, 0, 0, 0, 1]),
                ([2, [1, 4, 1]], [1, 4, 0, 1, 0, 0, 0, 1]),
                ([3, [1, 4, 1, 1, 1, 1, 1]],[1, 4, 1, 1, 1, 1, 1, 1])]

    def test__cardinals(self):
        for inp, asp in self.asp_card:
            self.assertItemsEqual(by_targets._cardinals(*inp), asp)

    asp_NA = [(1, ['NA', 'NA']),
              (2, ['NA']),
              (3, []),
              (4, []),
              (0, []),]

    def test__NA_insert(self):
        for inp, asp in self.asp_NA:
            self.assertEqual(by_targets._NA_insert(inp), asp)

    asp_part = [(('QWERTY', ['FOO'], [100200]),
                 ['QWERTY', 'FOO', 'NA', 'NA', 100200, 'NA','NA']),
                (('abcdef', ['pept1', 'pept2'], [100, 200]),
                 ['abcdef', 'pept1', 'pept2', 'NA', 100, 200, 'NA']),
                (('bar', ['foo', 'baaz', 'qux'], [100, 200, 0.3]),
                 ['bar', 'foo', 'baaz', 'qux', 100, 200, 0.3]),]

    def test__input_part(self):
        for inp, asp in self.asp_part:
            self.assertItemsEqual(by_targets._input_part(*inp), asp)

    asp_intersect = (
                     # 1
                     (("Accession1",
                       ["sequence1"], 
                       [100],
                       [1],
                       #["Accession1"]
                       ),
                       ["Accession1", "sequence1", 
                        'NA', 'NA', 100, 'NA', 'NA', 
                        1, 0, 0, 0, 0, 0, 0, 1, 
                        #"Accession1"
                        ]),
                     # 2
                        (("Accession1", 
                          ["sequence1", "sequence2"], 
                          [100, 200], 
                          [1, 4, 1], 
                          #["Accession2"]
                          ),
                          ["Accession1", "sequence1", "sequence2", 
                           'NA', 100, 200, 'NA', 
                           1, 4, 0, 1, 0, 0, 0, 1, 
                           #"Accession2"
                           ]),
                           
                         (("Accession1", 
                           ["sequence1", "sequence2", "sequence3"], 
                           [100, 200, 400], 
                           [1, 4, 1, 1, 1, 1, 1], 
                           #["Accession3"]
                           ),
                          ["Accession1", "sequence1", "sequence2", "sequence3",
                            100, 200, 400, 1, 4, 1, 1, 1, 1, 1, 1, 
                            #"Accession3"
                            ])
                     )

    def test__intersect_row(self):
        for inp, asp in self.asp_intersect:
            self.assertItemsEqual(by_targets._intersect_row(*inp), 
                                  asp, msg=by_targets._intersect_row(*inp))

    base_path = path.join(abspath(curdir), "example_files")
    fasta = "Ecoli_K12_IV.fasta"

    indx = fasta_indx.Saf(path.join(base_path, fasta))

    targets = {
        "16128048":[
            "DQSDIYNYDSSLLQSDYSGLFR",
            "VGPVPIFYSPYLQLPVGDK",
            "IASANQVTTGVTSR"
        ],
        "16131089":[
            "ITTDNAQINLVTQDVTSEDLVTLYGTTFNSSGLK",
            "LIAQHVEYYSDQAVSWFTQPVLTTFDKDK"
        ],
        "16131090":[
            "DFVVLTGNAYLQQVDSNIKGDK"
        ],
        "16131091":[
            "DAGNIIIDDDDISLLPLHAR",
            "FILLDEPFAGVDPISVIDIK"
        ],
        # "16127998":[
        #     "DQSDIYNYDSSLLQSDYSGLFR", #This peptide probably does not exist
        #     "VGPVPIFYSPYLQLPVGDK",
        #     "IASANQVTTGVTSR"
        # ],
    }

    csv_mw_folder = "search_by_mw_csv"
    mw_files = ["mw_card.csv",
                "mw_search.csv",
                "mw_result.csv"]


    def assert_csv(self, first, second, msg=None):
        self.assertTrue(isinstance(first, str),
                'First argument is not a string')
        self.assertTrue(isinstance(second, str),
                'Second argument is not a string')
        first_file = open(first, 'rb')
        second_file = open(second, 'rb')

        first_list =[d for d in csv.reader(first_file)]
        second_list =[d for d in csv.reader(second_file)]

        self.assertItemsEqual(first_list, second_list)

        first_file.close()
        second_file.close()



    def assert_card_csv(self, first, second, msg=None):
         self.assertTrue(isinstance(first, str),
                'First argument is not a string')
         self.assertTrue(isinstance(second, str),
                'Second argument is not a string')
         first_file = open(first, 'rb')
         second_file = open(second, 'rb')

         first_dicts_list =[d for d in csv.DictReader(first_file)]
         second_dicts_list =[d for d in csv.DictReader(second_file)]

         #for d in first_dicts_list: d[None] = d[None][0].split(';')
         #for d in second_dicts_list: d[None] = d[None][0].split(';')

         first_dicts_dicts = {d["Target"]:d \
                              for d in first_dicts_list}
         second_dicts_dicts = {d["Target"]:d \
                               for d in second_dicts_list}


         for k in first_dicts_dicts.keys():
             for k_k in first_dicts_dicts[k].keys():
                    if hasattr(first_dicts_dicts[k][k_k], "__iter__") \
                    and type(first_dicts_dicts[k][k_k]) != str:
                        self.assertItemsEqual(
                                        first_dicts_dicts[k][k_k],
                                        second_dicts_dicts[k][k_k],
                                        "target {0}, field {1}".format(k, k_k))
                    else:
                        self.assertEqual(first_dicts_dicts[k][k_k],
                                         second_dicts_dicts[k][k_k],
                                         "target {0}, field {1}".format(k, k_k))

         first_file.close()
         second_file.close()

    def test_find_mw(self):
        files = by_targets.find(targets=self.targets,
                                proteome=self.indx,
                                other_data={
                                    "enzyme":peptidases.no_enz},
                                kind="Mass")

        for each in files:
            dest = "mw_{0}".format(each)
            shutil.move(each, dest)


        self.assert_card_csv("mw_card.csv", path.join(self.base_path,
                                                         self.csv_mw_folder,
                                                         "mw_card.csv"))

        self.assert_csv("mw_search.csv", path.join(self.base_path,
                                                         self.csv_mw_folder,
                                                         "mw_search.csv"))

        self.assert_csv("mw_result.csv", path.join(self.base_path,
                                                         self.csv_mw_folder,
                                                         "mw_result.csv"))

    csv_seq_folder = "search_by_seq_csv"


    def test_find_seq(self):
        files = by_targets.find(targets=self.targets,
                                proteome=self.indx,
                                kind = 'Sequence',
                                other_data={})

        for each in files:
            dest = "seq_{0}".format(each)
            shutil.move(each, dest)


        self.assert_card_csv("seq_card.csv", path.join(self.base_path,
                                                         self.csv_seq_folder,
                                                         "seq_card.csv"))

        self.assert_csv("seq_search.csv", path.join(self.base_path,
                                                         self.csv_seq_folder,
                                                         "seq_search.csv"))

        self.assert_csv("seq_result.csv", path.join(self.base_path,
                                                         self.csv_seq_folder,
                                                         "seq_result.csv"))



if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
