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

__authors__ = "Pietro Brunetti"

import os


import wx
from xlrd import open_workbook

import re

import DialogCommons

wildcard = "Microsoft Excel 97/2000/XP (*.xls)|*.xls"

code_patt = r'(?<=\b)[\w\.\|]+(?=\b)'

class Dialog(wx.Dialog):
    """ Insert target dialog"""
    def __init__(self, parent, ID, title, size=wx.DefaultSize,
                 pos=wx.DefaultPosition,
                 style=wx.DEFAULT_DIALOG_STYLE):

        sizer = DialogCommons.createMainSizer(self, parent, ID, title, pos,
                                              size, style)
        self._createSetBox(sizer)
        self._createMegaBox(sizer)
        DialogCommons.createBtnSizer(self, sizer,
                             "The OK button to start the Finger Printing")
        self.SetSizer(sizer)
        sizer.Fit(self)

        self.kindOfFile = 0

    def _createMegaBox(self, sizer):
        megabox = wx.BoxSizer(wx.VERTICAL)
        radio1 = wx.RadioButton( self, -1, " Target protein identifiers list",
                                 style = wx.RB_GROUP )
        radio2 = wx.RadioButton( self, -1 ,"Excel file contains target proteins")
        box1 = self._createGIinsertion()
        box2 = self._createXLSinsertion()
        self._setInitialState(megabox, radio1, radio2, box1, box2)
        sizer.Add(megabox, 0, wx.GROW|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)

    def _setInitialState(self, megabox, radio1, radio2, box1, box2):
        self.group_ctrls = []
        self.group_ctrls.append((radio1, self.ctrl1))
        self.group_ctrls.append((radio2 ,self.ctrl2))
        for subctrl in self.ctrl2:
                subctrl.Enable(False)
        megabox.Add(radio1, 0, wx.ALIGN_LEFT|wx.ALL|wx.TOP, 5)
        megabox.Add(box1, 0, wx.GROW|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)
        megabox.Add(radio2, 0, wx.ALIGN_LEFT|wx.ALL|wx.TOP, 5)
        megabox.Add(box2, 0, wx.GROW|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)
        for radio, ctrl in self.group_ctrls:
            self.Bind(wx.EVT_RADIOBUTTON, self.OnGroupSelect, radio )
        self.byHand = True
        radio1.SetValue(1)

    def _createGIinsertion(self):
        sb1  = wx.StaticBox(self, -1)
        box1  = wx.StaticBoxSizer(sb1, wx.VERTICAL)
        self.text = wx.TextCtrl(self, -1, "", size=(200, 100),
                        style=wx.TE_MULTILINE|wx.TE_PROCESS_ENTER)
        box1.Add(self.text, 0, wx.ALIGN_CENTRE|wx.ALL, 5)
        self.ctrl1 = [self.text, ]
        return box1

    def _createXLSinsertion(self):
        sb2  = wx.StaticBox(self, -1)
        box2  = wx.StaticBoxSizer(sb2, wx.VERTICAL)
        self.ctrl2 = []
        self._createChooseFile(box2)
        self._createChooseSheet(box2)
        self._createChooseColon(box2)
        return box2

    def _createChooseFile(self, box2):
        s21 = wx.BoxSizer(wx.HORIZONTAL)
        label21 = wx.StaticText(self, -1, "File")
        s21.Add(label21, 0, wx.ALIGN_CENTRE|wx.ALL, 5)
        choose = wx.Button(self, -1, "...", (50,50))
        self.Bind(wx.EVT_BUTTON, self.OnButton, choose)
        s21.Add(choose, 0, wx.ALIGN_CENTRE|wx.ALL, 5)
        box2.Add(s21, 0, wx.GROW|wx.ALIGN_CENTER_VERTICAL|wx.RIGHT|wx.TOP, 5)
        self.ctrl2.extend([choose, label21])

    def _createChooseSheet(self, box2):
        s22 = wx.BoxSizer(wx.HORIZONTAL)
        label22 = wx.StaticText(self, -1, "Sheet")
        s22.Add(label22, 0, wx.ALIGN_CENTRE|wx.ALL, 5)
        self.ch22 = wx.Choice(self, -1, (100, 50))
        self.ch22.Bind(wx.EVT_CHOICE, self.EvtChoiceSheet)
        s22.Add(self.ch22, 0, wx.ALIGN_CENTRE|wx.ALL, 5)
        box2.Add(s22, 0, wx.GROW|wx.ALIGN_CENTER_VERTICAL|wx.RIGHT|wx.TOP, 5)
        self.ctrl2.extend([self.ch22, label22])

    def _createChooseColon(self, box2):
        s23 = wx.BoxSizer(wx.HORIZONTAL)
        label23 = wx.StaticText(self, -1, "Column")
        s23.Add(label23, 0, wx.ALIGN_CENTRE|wx.ALL, 5)
        self.ch23 = wx.Choice(self, -1, (100, 50))
        self.ch23.Bind(wx.EVT_CHOICE, self.EvtChoiceColumn)
        s23.Add(self.ch23, 0, wx.ALIGN_CENTRE|wx.ALL, 5)
        box2.Add(s23, 0, wx.GROW|wx.ALIGN_CENTER_VERTICAL|wx.RIGHT|wx.TOP, 5)
        self.ctrl2.extend([self.ch23, label23])

    def _createSetBox(self, sizer):
        DBList = ['All Peptides', 'Best Peptides']
        rb = wx.RadioBox(
                self, -1, "Peptide Set", wx.DefaultPosition,
                wx.DefaultSize,
                DBList, 2, wx.RA_SPECIFY_COLS| wx.NO_BORDER)
        txt = "It's possible to use peptide from best or from all the set"
        rb.SetHelpText(txt)
        self.Bind(wx.EVT_RADIOBOX, self.EvtRadioBox, rb)

        sizer.Add(rb, 0, wx.GROW|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)

    def EvtRadioBox(self, event):
        """ Chose peptide dataset """
        self.kindOfFile = event.GetInt()
        if self.kindOfFile == 0:
            self.GetParent().SetStatusText("Matching agaist stat pept\n")
        elif self.kindOfFile == 1:
            self.GetParent().SetStatusText("Matching agaist  best pept\n")

    def OnGroupSelect( self, event ):
        """ Select between hand insert
            or insert a excell file"""
        radio_selected = event.GetEventObject()
        for radio, ctrl in self.group_ctrls:
            if radio is radio_selected:
                for subctrl in ctrl:
                    subctrl.Enable(True)
            else:
                for subctrl in ctrl:
                    subctrl.Enable(False)
        self.byHand = not(self.byHand)

    def GetValue(self):
        res = self.FingerList() if self.byHand else self.FingerSheet()
        return {"kind_of_file": self.kindOfFile, "targets":res}

    def FingerList(self):
        """
        Record hand inserting targets
        """
        text = self.text.GetValue()
        r = re.compile(code_patt)
        targets = []
        for each in r.finditer(text):
            targets.append(each.group())

        return targets

    def FingerSheet(self):
        """
        Record targets inserted with excell
        """
        targets = []
        for r in range(1, self.sheet.nrows):
            if self.sheet.cell_type(r, self.acc) == 2:
                num = int(self.sheet.cell_value(r, self.acc))
                targets.append(str(num))
            else:
                targets.append(self.sheet.cell_value(r,
                                        self.acc))
        return targets

    def OnButton(self, evt):
        """Choosing excell file"""
        self.ch22.Clear()
        dlg = wx.FileDialog(
            self, message="choose a file",
            defaultDir=os.path.expanduser("~"),
            wildcard=wildcard,
            style=wx.OPEN | wx.MULTIPLE | wx.CHANGE_DIR
            )
        global paths #why global?
        paths = []
        if dlg.ShowModal() == wx.ID_OK:
            paths = dlg.GetPaths()
            global wb #why global?
            wb = open_workbook(paths[0])
            for s in wb.sheets():
                self.ch22.Append(s.name)

        dlg.Destroy()

    def EvtChoiceSheet(self, evt):
        """Choosing Sheet in excell file"""
        self.ch23.Clear()
        sheet = evt.GetString()
#        global s
        self.sheet = wb.sheet_by_name(sheet)
        for c in range(self.sheet.ncols):
            self.colName = self.sheet.cell(0, c).value
            if self.colName:
                self.ch23.Append(self.colName)

    def EvtChoiceColumn(self, evt):
        """Choosing Column in sheet chosen before"""
        self.colName = evt.GetString()
        for c in range(self.sheet.ncols):
            if self.sheet.cell(0, c).value == self.colName:
                self.acc = c


if __name__ == "__main__":
    app = wx.App()
    Dialog(None, -1, "Test")
    app.MainLoop()
