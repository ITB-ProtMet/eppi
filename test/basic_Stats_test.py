
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


"""Unit test for basic_Stats.py"""

__authors__ = "Pietro Brunetti"

from EPPI.raw import basic_Stats as basic
import unittest

class Shimazaki_Shinomoto_bins_exactely(unittest.TestCase):
    trydata = [
        4.37, 3.87, 4.00, 4.03, 3.50, 4.08, 2.25, 4.70, 1.73, 4.93, 1.73, 4.62,
        3.43, 4.25, 1.68, 3.92, 3.68, 3.10, 4.03, 1.77, 4.08, 1.75, 3.20, 1.85,
        4.62, 1.97, 4.50, 3.92, 4.35, 2.33, 3.83, 1.88, 4.60, 1.80, 4.73, 1.77,
        4.57, 1.85, 3.52, 4.00, 3.70, 3.72, 4.25, 3.58, 3.80, 3.77, 3.75, 2.50,
        4.50, 4.10, 3.70, 3.80, 3.43, 4.00, 2.27, 4.40, 4.05, 4.25, 3.33, 2.00,
        4.33, 2.93, 4.58, 1.90, 3.58, 3.73, 3.73, 1.82, 4.63, 3.50, 4.00, 3.67,
        1.67, 4.60, 1.67, 4.00, 1.80, 4.42, 1.90, 4.63, 2.93, 3.50, 1.97, 4.28,
        1.83, 4.13, 1.83, 4.65, 4.20, 3.93, 4.33, 1.83, 4.53, 2.03, 4.18, 4.43,
        4.07, 4.13, 3.95, 4.10, 2.27, 4.58, 1.90, 4.50, 1.95, 4.83, 4.12]

    optimal_bin_size = .233

    def test_From_know_data_2_bin_size(self):
        """The bins size there is equal to 0.233"""
        num_bins = basic.Shimazaki_Shinomoto_bins(self.trydata)
        size = round((max(self.trydata)-min(self.trydata))/float(num_bins), 3)
        self.assertEqual(size, self.optimal_bin_size)
        
if __name__ == "__main__":
    unittest.main()
    pass