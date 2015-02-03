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

""" Some classes to use for the notebook pages."""

__authors__ = "Pietro Brunetti"

import wx
import wx.lib.sheet as sheet
import csv
import DialogCommons
import ReportProtein
import ReportSequence

class _General(wx.Panel):
    """ Main classes, derived from Panel"""
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)
        self.sizer = wx.BoxSizer(wx.VERTICAL)
    def _fix_sizer(self, obj):
        self.sizer.Add(obj, 2, wx.ALIGN_CENTER|wx.ALL|wx.EXPAND, 5)
        self.SetSizer(self.sizer)
        self.sizer.Fit(self)

class Txt(_General):
    """ Used to open text file inside the project"""
    def __init__(self, parent, txtfile):
        _General.__init__(self, parent)
        self.editor = wx.TextCtrl(self, -1, style=wx.TE_MULTILINE)
        self._fix_sizer(self.editor)
        self.editor.LoadFile(txtfile)
        self.editor.SetInsertionPoint(0)

class Image(_General):
    """ Used to open image inside the project"""
    def __init__(self, parent, pngfile):
        _General.__init__(self, parent)
        png = wx.Image(pngfile, wx.BITMAP_TYPE_PNG).ConvertToBitmap()
        self.image = wx.StaticBitmap(self, -1, png,
                     (5, 5), (png.GetWidth(), png.GetHeight()))
        self._fix_sizer(self.image)

class CSV(_General):
    """ Used to open CSV inside the project"""
    def __init__(self, parent, csvfile):
        _General.__init__(self, parent)
        self.sheet = SheetCSV(self, csvfile)
        self._fix_sizer(self.sheet)

class SheetCSV(sheet.CSheet):
    """ Sheet used to visualize CSV file"""
    def __init__(self, parent, csvfile, cols=256, rows=80000):
        """ Initialize the sheet """
        sheet.CSheet.__init__(self, parent)
        self.SetRowLabelAlignment(wx.ALIGN_CENTRE, wx.ALIGN_CENTRE)

        self.cols = cols
        self.rows = rows
        self.load_CSV(csvfile)


    def load_CSV(self, csvfile):
        """ load csv file """
        handle = open(csvfile, 'rb')
        reader = csv.reader(handle)

        # calculate (counting) the number of rows and of columns
        ncols = -1
        for nrows, row in enumerate(reader):
            if ncols < len(row):
                ncols = len(row)
        #I'm using enumerate, and i need to add 1 to result
        nrows+=1

        # if they are less then rows and cols using these values
        # to initialize the spreadsheet
        # otherwise use rows and/or cols
        warm_msg = "Number of {0} is {1} bigger than {2}"
        if nrows >= self.rows:
            DialogCommons.MsgDlg(self,warm_msg.format('rows', nrows, rows))
        else:
            self.rows = nrows
        if ncols >= self.cols:
            DialogCommons.MsgDlg(self,warm_msg.format('columns', ncols, cols))
        else:
            self.cols = ncols
        # start again the input csv file
        handle.seek(0)

        self.SetNumberCols(self.cols)
        self.SetNumberRows(self.rows)
        self.SetLabelBackgroundColour('#DBD4D4')

        # note that the title row=0 is taken
        try:
            for n_row, row in enumerate(reader):
                if n_row >= self.rows: break
                for n_col, value in enumerate(row):
                    if n_col >= self.cols: break
                    self.SetCellValue(n_row, n_col, value)
        except csv.Error, e:
            txt = 'file {0}, line {1}: {2}'.format(csvfile, reader.line_num, e)
            DialogCommons.MsgDlg(self, text, 'Error!', wx.OK)
        if n_row > self.rows:
            txt = 'Number of CSV rows greater than sheet rows'
            DialogCommons.MsgDlg(self, txt, 'Warning!', wx.OK)
        if n_col > self.cols:
            txt = 'Number of CSV colums greater than sheet colums'
            DialogCommons.MsgDlg(self, txt, 'Warning!', wx.OK)
        handle.close()

    def OnRightClick(self, event) :
        """
        a CSheet method
        cell is right-clicked, get cell seq
        """
        r = event.GetRow()
        c = event.GetCol()
        self.popupmenu = wx.Menu()
        self.cellvalue = self.GetCellValue(r, c)
#        for text in "copy/blast/find protein/find sequence".split('/'):
        for text in "copy/find protein/find sequence".split('/'):
            item = self.popupmenu.Append(-1, text)
            if text in ["find protein","find sequence"] and\
                            'proteome' not in self.GetTopLevelParent().fileDB.keys():
                item.Enable(False)
            self.Bind(wx.EVT_MENU, self.OnPopupItemSelected, item)
        self.Bind(wx.EVT_CONTEXT_MENU, self.OnShowPopup)

        pos = event.GetPosition()
        self.PopupMenu(self.popupmenu, pos)

    def OnShowPopup(self, event):
        """ Method to show popup menu """
        pos = event.GetPosition()
        pos = self.ScreenToClient(pos)
        self.PopupMenu(self.popupmenu, pos)

    def OnPopupItemSelected(self, event):
        """ Method  on selecting item on popup menu """
        root = self.GetTopLevelParent()
        item = self.popupmenu.FindItemById(event.GetId())
        text = item.GetText()
        if text == 'copy':
            clipdata = wx.TextDataObject()
            clipdata.SetText(self.cellvalue)
            wx.TheClipboard.Open()
            wx.TheClipboard.SetData(clipdata)
            wx.TheClipboard.Close()
#        elif text == 'blast':
#            # TODO: Insert the blast find codes
#            pass
        elif text == 'find protein':
            dlg = ReportProtein.Dialog(root, self.cellvalue)
            dlg.ShowModal()
            dlg.Destroy()
        elif text == 'find sequence':
            dlg = ReportSequence.Dialog(root, self.cellvalue)
            dlg.ShowModal()
            dlg.Destroy()
