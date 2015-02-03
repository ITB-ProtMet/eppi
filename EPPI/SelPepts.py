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

""" Selecting peptides using IF treshold values"""

__authors__ = "Pietro Brunetti"

import os

import wx
import wx.lib.agw.floatspin as FS

import DialogCommons

class Dialog(wx.Dialog):
    """ Dialog to set the threshold for selection"""
    def __init__(
            self, parent, ID, title, size=wx.DefaultSize,
            pos=wx.DefaultPosition,
            style=wx.DEFAULT_DIALOG_STYLE):

        sizer = DialogCommons.createMainSizer(self, parent, ID,
                                              title, pos, size, style)
        self._createSelBox(sizer)
        self._createPlotBox(sizer)
        DialogCommons.createBtnSizer(self, sizer,
                           "The OK button to start the Selection")
        self.SetSizer(sizer)
        sizer.Fit(self)

    def _createSelBox(self, sizer):
        # setting default values
        """
        Create a box that allows user to choose
        the select parameters
        """
        self.protThr = 0.3
        self.peptThr = 0.5

        self._createSpinner(sizer, "Protein IF threshold ", self.protThr,
                            "Protein identification frequency threshold",
                            self.OnProtSpin)
        self._createSpinner(sizer, "Peptide IF threshold ", self.peptThr,
                            "Peptide identification frequency threshold",
                            self.OnPeptSpin)

    def _createSpinner(self, sizer, title, defaultValue, helptxt, fun):
        p_sizer = wx.BoxSizer(wx.HORIZONTAL)
        p_Stat = wx.StaticText(self, -1, title)
        p_Spin = FS.FloatSpin(self, -1, min_val=0, max_val=1,
                             increment=0.1, value=defaultValue)
#                             ,extrastyle=FS.FS_LEFT)
        p_Spin.SetDigits(1)
        p_Spin.SetHelpText(helptxt)
        p_Spin.Bind(  FS.EVT_FLOATSPIN, fun)

        p_sizer.Add(p_Stat, 1)
        p_sizer.Add(p_Spin, 1)
        sizer.Add(p_sizer, 0,
                  wx.GROW|wx.ALIGN_CENTER_VERTICAL|wx.RIGHT|wx.TOP, 5)


    def _createPlotBox(self, sizer):
        self.HaveHisto = None
        self._createCheck(sizer, " Histogramm",
                         "Plot Peptide/Protein frequencies Histogram",
                          self.OnHistos)
        self.HaveScatter = None
        self._createCheck(sizer, " Scatter Plot",
                         "Plot Peptide/Protein frequencies Scatter Plot",
                          self.OnScatter)

    def _createCheck(self, sizer, title, helptxt, funz):
        check   = wx.CheckBox( self, -1, title,  style = wx.ALIGN_RIGHT )
        check.SetHelpText(helptxt,)
        check.Bind(  wx.EVT_CHECKBOX, funz)
        sizer.Add(check, 0,
                  wx.GROW|wx.ALIGN_CENTER_VERTICAL|wx.RIGHT|wx.TOP, 5)

    def OnProtSpin(self, e):
        """ Setting the Protein threshold"""
        floatspin = e.GetEventObject()
        self.protThr = floatspin.GetValue()
        txt = "Protein IF threshold: {0}\n".format(self.protThr)
        self.GetParent().SetStatusText(txt)

    def OnPeptSpin(self, e):
        """ Setting the Peptide threshold"""
        floatspin = e.GetEventObject()
        self.peptThr = floatspin.GetValue()
        txt = "Peptide IF threshold: {0}\n".format(self.peptThr)
        self.GetParent().SetStatusText(txt)

    def OnHistos(self, e):
        """ Make a histogram? """
        self.HaveHisto = e.IsChecked()

    def OnScatter(self, e):
        """ Make a Scatter Plot?"""
        self.HaveScatter = e.IsChecked()

    def GetValue(self):
        return {"protThr": self.protThr,
                "peptThr": self.peptThr,
                "haveHisto": self.HaveHisto,
                "haveScatter": self.HaveScatter}
