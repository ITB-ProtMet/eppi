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

""" Managing variable values """

__authors__ = "Pietro Brunetti"

import os

import wx
import  wx.lib.filebrowsebutton as filebrowse
import wx.lib.agw.floatspin as FS

from peptidome import fasta_indx

import DialogCommons

wildcard_f  = "Fasta File (*.fasta)|*.fasta|Aminoacids Fasta File(*.faa)|*.faa"

class Dialog(wx.Dialog):
    """ Dialog for the variable managing"""
    def __init__(self, parent, ID, title, size=wx.DefaultSize,
                 pos=wx.DefaultPosition, style=wx.DEFAULT_DIALOG_STYLE):
        szr = DialogCommons.createMainSizer(self, parent, ID, title,
                                            pos, size, style)
        self._createMegabox(szr)
        DialogCommons.createBtnSizer(self, szr)
        self.SetSizer(szr)
        szr.Fit(self)


    def _createMegabox(self, sizer):
        self.megabox = wx.BoxSizer(wx.VERTICAL)
        self._createFastaButton()
        self._createEnzymeChoice()
        self._createMissCutSpinCtrl()
        self._createDeltaPrecisionBox()
        self._setInitialState(self.megabox, sizer)

    def _createFastaButton(self):
        fileDB = self.GetParent().fileDB
        if not fileDB.has_key("proteome"):
            self.fasta_path = os.path.expanduser("~")
        else:
            if not os.path.isfile(fileDB["proteome"]["fasta_path"]):
                self.fasta_path = os.path.expanduser("~")
            else:
                self.fasta_path = fileDB["proteome"]["fasta_path"]
        self.cF = filebrowse.FileBrowseButton(self,
                            labelText="Select a fasta file:",
                            fileMask=wildcard_f,
                            fileMode=wx.OPEN,
                            initialValue=self.fasta_path,
                            changeCallback = self._faCallback)

        self.megabox.Add(self.cF, 0,
                         wx.GROW|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)

    def _createEnzymeChoice(self):
        self.st2 = wx.StaticText(self, -1, "Enzyme", (45, 15))
        enzymeList = ["No enzyme",
                      "Trypsin (K or R)",
                      "Trypsin (complex rule)",
                      "Pepsin (A, V, L, I, G, F, Y or W)",
                      "Proteinase K (F, Y, W or L)"]
        self.chEnz = wx.Choice(self, -1, (100, 50), choices = enzymeList)
        self._setHorizontal([self.st2, self.chEnz], self.megabox)
        self.Bind(wx.EVT_CHOICE, self._enable_misscut, self.chEnz)

    def _enable_misscut(self, event):
        if self.chEnz.GetSelection() != 0:
            self.chMC.Enable(True)
        else:
            self.chMC.Enable(False)


    def _createMissCutSpinCtrl(self):
        self.st = wx.StaticText(self, -1, "Miss-cleavage value",
                                (45, 15))
        self.chMC = wx.SpinCtrl(self, -1, "", (30, 50))
        self.chMC.SetRange(0,5)
        self.chMC.SetValue(0)
        self._setHorizontal([self.st, self.chMC], self.megabox)
        self.chMC.Enable(False)

    def _createDeltaPrecisionBox(self):
        #self._createDigitsControl()
        self._createPrecisionControl()

    def _createDigitsControl(self):
        self.sc = wx.SpinCtrl(self, -1, "", (30, 50))
        self.sc.SetRange(1, 5)
        self.sc.SetValue(3)
        sd = wx.Button(self, -1, "Set Digits")
        self.Bind(wx.EVT_BUTTON, self.SetDigits, sd)
        self._setHorizontal([self.sc, sd], self.megabox)

    def _createPrecisionControl(self):
        label = wx.StaticText(self, -1, "Delta mass [Da]")
        self.floatspin = FS.FloatSpin(self, -1, min_val=0, max_val=1,
                                       increment=0.001, value=0.008)
                                       #, extrastyle=FS.FS_LEFT)
        self.floatspin.SetFormat("%f")
        self.floatspin.SetDigits(3)
        self.floatspin.SetIncrement(10**(-3))
        self._setHorizontal([label, self.floatspin], self.megabox)

    def _setHorizontal(self, ctrls, biggerBox):
        box = wx.BoxSizer(wx.HORIZONTAL)
        for each in ctrls:
            box.Add(each)
        biggerBox.Add(box, 0, wx.GROW|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)

    def _setInitialState(self, megabox, sizer):
        sizer.Add(megabox, 0, wx.GROW|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)

    def _faCallback(self, evt):
        self.fasta_path = evt.GetString()

    def SetDigits(self, evt):
        """
        Set digits of precision
        """
        self.floatspin.SetValue(0.0)
        power = self.sc.GetValue()
        self.floatspin.SetDigits(power)
        self.floatspin.SetIncrement (10**-(power))


    def GetValue(self):
        #TO-DO: check if self.fasta_path is a valid file
        self.values = {}
        # the path fasta file is in Saf.name <-
        # but project does not report the name
        # use for the moment
        # >>> saf_obj = fileDB["proteome"]
        # >>> saf_obj.name = fileDB["fasta"]
        self.values["proteome"] = fasta_indx.Saf(self.fasta_path, window=True)
        self.values["delta"] = self.floatspin.GetValue()*(10**5)

        self.values["enzyme"] = self.chEnz.GetSelection()

        self.values["enzyme_exception"] = None
        self.values["miscut"] = self.chMC.GetValue()
        return self.values

if __name__ == "__main__":
    app = wx.App()
    Dialog(None, -1, "Test")
    app.MainLoop()
