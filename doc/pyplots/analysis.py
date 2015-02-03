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

import matplotlib.pyplot as plt
import os, sys
sys.path.insert(0, os.path.abspath('../../EPPI/raw/'))
from preStats import analysis_plot
from proteomic_xls import sequest_onlypept_parser, EmptyCell

print os.path.abspath(os.curdir)

onlypept_dir = "../../example_files//xls_testfiles/five_right_onlypept/"
files =["A1.xls", "B1.xls", "B2.xls", "B3.xls", "B4.xls" ]
p = sequest_onlypept_parser()
for i, file in enumerate(files):
    try:
        p.parse(onlypept_dir + file)
    except EmptyCell:
        pass

analysis_plot(p)
plt.show()