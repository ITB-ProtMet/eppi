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

""" Module to execute simple statistical plot
on MS/MS frequencies seq
"""

__authors__ = "Pietro Brunetti"

import matplotlib.pyplot as plt
from matplotlib.collections import CircleCollection

import basic_Stats as basic

analysis_plot_fig = 2
scatter_plot_fig = 3

class preStats_Error(Exception):
    """
    preStats exception base class
    """
    pass

class NoData(preStats_Error):
    """
    raises if there aren't seq to plot
    """
    pass

def analysis_plot(stat_parser, analysis_name="", thrPrt=0.3, thrPep=0.5,
                  hist_bins=[10, 10], cdf_bins=[50, 50]):
    """
    plots two histograms for protein and peptide frequencies and
    two plots of cumulative distribution function.
    In the histograms best peptides are marked in red, the other in blue.

    :param stat_parser: the parser that store the seq
    :param analysis_name: the analysis name
    :param thrPrt: the protein frequency threshold
    :param thrPep: the peptide frequency threshold
    :param hist_bins: bin numbers for histograms
    :param cdf_bins: bin numbers for cdf plots
    :return: the figure of the analysis plot - after it can be plotted on the screen
        or saved in a picture file

    :raises NoData: If there are not proteins or peptides frequencies values
    .. plot:: pyplots/analysis.py
        :include-source:
    """

    prots, pepts = stat_parser.parser2arrays()

    fig = plt.figure(num=analysis_plot_fig)
    
    #DPI = fig.get_dpi()
#    print "DPI:", DPI
    #DefaultSize = fig.get_size_inches()
#    print "Default size in Inches", DefaultSize
#    print "Which should result in a %i x %i Image"%(DPI*DefaultSize[0], DPI*DefaultSize[1])

    fig.suptitle(analysis_name, fontsize=14, fontweight='bold')
    fig.subplots_adjust(hspace=0.5, wspace=0.5)

    if len(prots):
        ax1 = fig.add_subplot(221)
        basic.cdf(ax1, prots,
                  bins=cdf_bins[0],
                  Title="Proteins cumulative distribution",
                  Xlab="Frequency of proteins",
                  Ylab="Fraction of proteins")

        ax2 = fig.add_subplot(222)
        basic.hist(ax2, prots, trs=thrPrt,
                  bins= hist_bins[0],
                  Title="Proteins distribution",
                  Xlab="Frequency of proteins",
                  Ylab="Number of proteins")
    else:
        raise NoData, "There aren't proteins!!!"
    
    if len(pepts):
        ax3 = fig.add_subplot(223)   
        basic.cdf(ax3, pepts,
                  Title="Peptides cumulative distribution",
                  Xlab="Frequency of peptides",
                  Ylab="Fraction of peptides")

        ax4 = fig.add_subplot(224)
        basic.hist(ax4, pepts, trs=thrPep,
                  Title="Peptides distribution",
                  Xlab="Frequency of peptides",
                  Ylab="Number of peptides" )
    else:
        raise NoData, "There aren't peptides!!!"
    #fig.savefig(filename, papertype='a4',
    #                    orientation='landscape')
    #plt.close()
    return fig

def freq_Scatter(parser, thrPrt=0.3, thrPep=0.5,
                 analysis_name = "",
                 Xlab = "", Ylab = "" ):
    """
    plots an advanced scatter-plot for peptides and protein frequencies.

    :param parser: the parser that store the seq
    :param analysis_name: the analysis name
    :param thrPrt: the protein frequency threshold
    :param thrPep: the peptide frequency threshold
    :param Xlab: the label for X axe
    :param Ylab: the label for Y axe
    :return: the figure of the analysis plot - after it can be plotted on the screen
        or saved in a picture file

    :raises NoData: If there are not proteins or peptides frequencies values
    .. plot:: pyplots/scatter.py
        :include-source:
    """
    # calculating the plotting seq
    x, y, z = parser.frequencyMatrix()

    if x and y and z:

        # definitions for the axes
        left, width = 0.1, 0.65
        bottom, height = 0.1, 0.65
        bottom_b = left_b = left+width+0.01

        rect_scatter = [left, bottom, width, height]
        rect_box_x = [left, bottom_b, width, 0.2]
        rect_box_y = [left_b, bottom, 0.2, height]
        rect_leg = [left_b, bottom_b, 0.2, 0.2]

        # start with a rectangular Figure
        fig = plt.figure(scatter_plot_fig, figsize=(8,8))

        axScatter = plt.axes(rect_scatter)
        axBoxx = plt.axes(rect_box_x, xticks=[], yticks=[])
        axBoxy = plt.axes(rect_box_y, xticks=[], yticks=[])
        axLeg = plt.axes(rect_leg, xticks=[], yticks=[])

        # no labels
        import matplotlib.ticker
        nullfmt   = matplotlib.ticker.NullFormatter()
        axBoxx.xaxis.set_major_formatter(nullfmt)
        axBoxx.yaxis.set_major_formatter(nullfmt)
        axBoxy.xaxis.set_major_formatter(nullfmt)
        axBoxy.yaxis.set_major_formatter(nullfmt)
        axLeg.xaxis.set_major_formatter(nullfmt)
        axLeg.yaxis.set_major_formatter(nullfmt)

        # scatter plot
        axScatter.scatter(x, y, s=z, alpha=0.75)
        axScatter.set_xlabel(Xlab)
        axScatter.set_ylabel(Ylab)

        axScatter.axhline(linewidth=2, color='r',linestyle='-.', y=thrPep)
        axScatter.axvline(linewidth=2, color='r',linestyle='-.', x=thrPrt)

        axScatter.set_xlim( (-0.1, 1.1) )
        axScatter.set_ylim( (-0.1, 1.1) )

        # x boxplot
        axBoxx.boxplot(x,vert = 0)
        axBoxx.set_xlim( axScatter.get_xlim() )
        # title upside axBox
        axBoxx.set_title(analysis_name, x=0.6)

        # y box plot
        axBoxy.boxplot(y)
        axBoxy.set_ylim( axScatter.get_ylim() )

        # Legend
        c_c = CircleCollection(sizes=(1, 10, 100),
                           offsets=[(0.1, 0.5), (0.5, 0.5), (0.9, 0.5)],
                           transOffset=axLeg.transData,
                           alpha=0.75)
        axLeg.add_collection(c_c)
        plt.text(0.1, 0.3, "1", ha="center", size=8)
        plt.text(0.5, 0.3, "10", ha="center", size=8)
        plt.text(0.9, 0.3, "100", ha="center", size=8)
        fig.canvas.draw()


        return fig
    else:
        raise NoData, "There aren't about frequencies!!!"



    
if __name__ == "__main__":
    pass