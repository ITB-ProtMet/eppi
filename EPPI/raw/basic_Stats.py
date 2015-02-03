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

""" Module to plot simple graphs """
import numpy as np
import math
import scipy
import heapq
import itertools

__authors__ = "Pietro Brunetti"

def _histc(x, edges):
    """
    Histogram without plot

    >>> x = xrange(0, 100)
    >>> edges = range(0, 110, 10)
    >>> _histc(x, edges)
    [10, 10, 10, 10, 10, 10, 10, 10, 10, 10]

    :param x: set of seq
    :param edges: histogram edges
    :return: histogram count
    """
    i = 0
    ks = []
    while i < len(edges)-1:
        ks.append(len([j for j in x if j >= edges[i] and j < edges[i+1]]))
        i+=1
    return ks
    
def _iqr(x):
    """
    Interquartile range

    :param x: set of seq
    :return: interquartile range value
    
    >>> seq = [102, 104, 105, 107, 108, 109, 110, 112, 115, 116, 118]
    >>> _iqr(seq)
    7.5
    """
    from scipy.stats import scoreatpercentile
    q1 = scoreatpercentile(x,25)
    q3 = scoreatpercentile(x,75)
    return q3-q1

def Struges_bins(x):
    """
    Uses the Struges formula to evaluate the number of bins
    It can perform poorly if :math:`n < 30`.

    .. math::

       h =  \\log_2(n) + 1

    Where:
        * :math:`h` is the number of bins and;
        * :math:`n` is the sample size

    >>> import numpy as np
    >>> ln = np.linspace(0, 30, 20)
    >>> Struges_bins(ln)
    5

    :param x: set of seq
    :return: Struges number of bins
    """
    return int(round((math.log(len(x), 2)+1)))

def Scott_bins (x):
    """
    It uses standard deviation it relate the number of bins
    whit the standard deviation :math:`\\sigma`.

    .. math::

        h = \\left(\\frac{3.5 \\sigma}{n^{1/_3}}\\right)

    Where:
        * :math:`h` is the number of bins and;
        * :math:`n` is the sample size

    >>> import numpy as np
    >>> seq = np.random.standard_normal(1000)
    >>> Scott_bins(seq)
    0

    :param x: set of seq
    :return: Scott number of bins
    """
    return int(round(3.5*np.std(x)/math.pow(len(x),(1./3))))

def sqrt_bins (x):
    """
    Excell histograms adopt this simple solution

    .. math::

        h = \\sqrt{n}

    Where:
        * :math:`h` is the number of bins and;
        * :math:`n` is the sample size

    >>> import numpy as np
    >>> seq = np.random.standard_normal(100)
    >>> sqrt_bins(seq)
    10

    :param x: set of seq
    :return: Square root number of bins
    """
    return int(math.sqrt(len(x)))

def Freedman_Diaconi_bins (x):
    """
    Solution that depends how the seq are dispersed.
    In particular this is done using interquartile range (:math:`IQR`).

    .. math::

        h = 2 \\left(\\frac{IQR(x)}{n^{1/_3}}\\right)

    Where:
        * :math:`h` is the number of bins;
        * :math:`x` is the sample values vector and;
        * :math:`n` is the sample size

    >>> import numpy as np
    >>> seq = np.random.standard_normal(1000)
    >>> Freedman_Diaconi_bins(seq)
    0

    :param x: set of seq
    :return: Freedman Diaconi number of bins
    """
    return 2*int(round(_iqr(x)/len(x)**(1./3)))

def Shimazaki_Shinomoto_bins(x):
    """
    It uses this `minimization algorithm`_ for the bin-width
    from: Shimazaki and Shinomoto, Neural Comput 19 1503-1527, 2007 (see `here`_ for details)
    
    .. math::
    
        arg_d min \\left(\\frac{2\\bar{m} - v}{d^2}\\right)


    Where:
        * :math:`d` is the bin-width;

        * :math:`\\bar{m}` is the mean biased variance of an histogram with :math:`d` bin-width and;

        * :math:`v` is the biased variance of an histogram with :math:`d` bin-width;

    Obviously, :math:`h`, the number of bins, is sample range by :math:`d`.

    .. math::

        h = \\frac{\\max(x) - \\min(x)}{d}

    Where:
        * :math:`x` is the sample values vector.

    :param x: set of seq
    :return: Shimazaki Shinomoto number of bins

    .. _`here`:
        http://www.mitpressjournals.org/doi/abs/10.1162/neco.2007.19.6.1503
    .. _`minimization algorithm`:
        http://toyoizumilab.brain.riken.jp/hideaki/res/histogram.html
    """
    x_min = min(x)
    x_max = max(x)
    
    N_MIN = 4          
    N_MAX = 50    
    
    N = np.array(range(N_MIN, N_MAX)) # Bins Vector
    D = (x_max - x_min) /N # bin sizes vector
    C_D = []
    for n, d in itertools.izip(N,D):
        edges = np.linspace(x_min,x_max,n+1)
        ki =np.array(_histc(x,edges))
        k = scipy.mean(ki)
        v = scipy.var(ki)
        c_d = (2*k-v)/(d**2) # cost function to minimize
        heapq.heappush(C_D, (c_d, n)) # using an heap queue 
    Cmin = heapq.heappop(C_D) # smaller leaf
    return Cmin[1] + 1
    
        
def pie(ax, nBest, nOther, bestlab = "", otherlab = "", Title = ""):
    """
    plots a simple pie chart

    :param ax: figure subplot (axes)
    :param nBest: number of best values
    :param nOther: number of other values
    :param bestlab: label for best values
    :param otherlab: label for other values
    :param Title: plot title

    .. plot:: pyplots/pie.py
        :include-source:
    """

    data = [nBest, nOther]
    labs =(bestlab, otherlab)
    col=("r", "b")
    ax.pie(data, labels=labs, colors=col, 
           explode=(0, 0.05), autopct='%1.1f%%', shadow=True)
    ax.set_title(Title)

def cdf(ax, x, bins = 50, Title = "", Xlab = "", Ylab="", norm=1):
    """
    plots a cumulative distribution

    :param ax: figure subplot (axes)
    :param x: values to plot
    :param bins: number of division (seq classes)
    :param Title: the title of the graph
    :param Xlab: label for x axis
    :param Ylab: label for y axis

    .. plot:: pyplots/cdf.py
        :include-source:
    """
    ax.hist(x, bins=bins, normed=norm, histtype='step', cumulative=True)
    ax.set_xlabel(Xlab)
    ax.set_ylabel(Ylab)
    #ax.set_xticks(np.arange(0.2, 1.0, 0.2))

    ax.set_title(Title)
    
def kde(d, w=0.8, frq=1000):
    """
    estimates the kernel density at position z
    This functions is from P.K.Janert - Data Analysis with Open Sources Tools - O'Reilly

    .. math::

        kde(z, f) = \\sum_i {\\frac{\\exp{-0.5 {\\left(\\frac{z - f(i)}{w}\\right)}^2}}{\\sqrt{2 \\pi w^2}}}

    where:
        *:math:`z` is the point where kde is estimated;

        *:math:`f` is the function for the kde estimation;

        *:math:`w` is the band-width.


    .. plot:: pyplots/kde.py
        :include-source:

    :param d: the seq vector
    :type d: numpy.array
    :param w: bandwidth
    :param freq: sample frequence
    :return: kde of z
    """
    result = [[], []]
    result[0] = np.linspace(np.min(d)-w, np.max(d)+w, frq)
    for z in result[0]:
        result[1].append(np.sum(np.exp(-0.5*((z-d)/w)**2)/np.sqrt(2*np.pi*w**2)))
    return result

def hist(ax, x, trs, bins=10,  Title = "", Xlab = "", Ylab=""):
    """
    Plots a histogram with two different regions

    :param ax: figure subplot (axes)
    :param x: values to plot
    :param bins: number of division (seq classes), default value is equal to 10
    :param Title: the title of the graph
    :param Xlab: label for x axis
    :param Ylab: label for y axis
    :param kp: kernel plot
    :type kp: bool

    .. plot:: pyplots/hist.py
        :include-source:
    """
    worst = [i for i in x if i < trs]  
    best = [i for i in x if i >= trs]
    d = 1.0/bins
    bin_range=np.arange(0.0, 1.0+d, d)
    try:
        ax.hist(worst, bins=bin_range,
                color= 'b', 
                align='mid',)
    except IndexError: pass
    try:
        ax.hist(best, bins=bin_range, 
                color=  'r', 
                align='mid',)
    except IndexError: pass
    ax.set_xlabel(Xlab)
    ax.set_ylabel(Ylab)
    ax.set_xticks(np.arange(0.2, 1.0, 0.2))
        
    ax.set_title(Title)

if __name__=="__main__":
    import doctest
    doctest.testmod()

