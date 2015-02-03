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

shape, scale = 2., 2. # mean and dispersion
d = np.random.gamma(shape, scale, 1000)
fig = plt.figure(1)
#plt.subplots_adjust(hspace=0.5, wspace=0.5)
ax1 = fig.add_subplot(111)

cdf(ax1, d, bins=100)

plt.show()

