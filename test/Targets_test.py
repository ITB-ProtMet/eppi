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

__author__ = 'piotr'

import unittest
import re
from EPPI import Targets

class MyTestCase(unittest.TestCase):

    def test_usedRE(self):

        chases = [
            ("HS70A_BOVIN", ["HS70A_BOVIN"]), # gene name trembl swiss prot
            ("IPI5657885.1", ["IPI5657885.1"]), # IPI code
            ("756786896 868778089 769786", ["756786896", "868778089", "769786"]), # three gi numbers
            ("""8976878098
            6678698090
            78070""" , ["8976878098","6678698090","78070"]), # three gi numbers
            ("Rnd1psu|NC_LIV_001850", ["Rnd1psu|NC_LIV_001850"]) #55merge example for OMSA
        ]

        patt = re.compile(Targets.code_patt)

        for chase in chases:
            self.assertRegexpMatches(chase[0], patt)
            self.assertListEqual([each.group() for each in patt.finditer(chase[0])], chase[1])



if __name__ == '__main__':
    unittest.main()
