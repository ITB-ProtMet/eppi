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

import numpy as np
import matplotlib.pyplot as plt
import os, sys
sys.path.insert(0, os.path.abspath('../../EPPI/raw/'))
from basic_Stats import *

d = np.random.random_sample((2,1000))
nBest_pept = 0
nBest_prot = 0
for i in range(1000):
    if d[0][i] > 0.3:
        nBest_prot+=1
        if d[1][i] > 0.8:
            nBest_pept+=1
nWorst_prot = 1000 - nBest_prot
fig = plt.figure(1)
ax1 = fig.add_subplot(111)
pie(ax1, nBest=nBest_prot, nOther=1000-nBest_prot, Title="prova 0.3")
plt.show()
  