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
    
from EPPI.peptidome.commons import Param_dummy
from EPPI.peptidome.commons import Param
import os

class Test_functions(unittest.TestCase):
    functions = [
                 Param_dummy.mi_mw,
                 Param_dummy.mi_mw_np,
                 Param.mi_mw
                 ]
    
    good_chases =[("GGGGG", 30412568),
                  ("WWWWW", 94941493),
                  ("GGGGGV", 40319409),
                  ("VGGGGG", 40319409),
                  ("GGGGGP", 40117844),
                  ("PGGGGG", 40117844),
                  ("HSQVFSTAEDNQSAVTIHVLQGER", 265329699),
                  ]
    
    
    def test_mi_mw(self):
        for seq, mw in self.good_chases:
            for f in self.functions:
                self.assertEqual(f(seq), mw)

    wrong_seqs = [ "GGGxGG",
                   "XWWWWW",
                   "GGG@GGV",
                   "VGGGGG ",
                   "GG GGGP", 
                   "2PGGGGG"]

    def test_raise_wronseq(self):
        for seq in self.wrong_seqs:
            for f in self.functions[:2]:
                self.assertRaises(Param_dummy.wrongSequence, f, seq)
            self.assertRaises(Param.wrongSequence, self.functions[2], seq)
                
if __name__ == '__main__':
    unittest.main()
