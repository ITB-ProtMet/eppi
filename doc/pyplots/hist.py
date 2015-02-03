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

import os, sys
sys.path.insert(0, os.path.abspath('../../EPPI/raw/'))
from basic_Stats import *
import numpy as np
import matplotlib.pyplot as plt

mu, beta = 0, 0.1 # location and scale
d = np.random.gumbel(mu, beta, 1000)

fig = plt.figure(1)
plt.subplots_adjust(hspace=0.5, wspace=0.5)
b = Shimazaki_Shinomoto_bins(d)
ax1 = fig.add_subplot(111)
hist(ax1, x=d, trs=0.3, bins=b)
plt.show()