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

""" Module for peptides report dialog"""

__authors__ = "Pietro Brunetti"

import os

import wx
import wx.html as html

import html_generator
import DialogCommons

class Dialog(wx.Dialog):
    """ Peptide report dialog"""
    def __init__(self, parent, seq):
        wx.Dialog.__init__(self, parent, -1, 'Sequence', size=(440, 400), 
                           style=wx.DEFAULT_FRAME_STYLE)
        page = html.HtmlWindow(self)
        if "gtk2" in wx.PlatformInfo:
            page.SetStandardFonts()
        page.SetPage(self._getText(seq))
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(page, 1, wx.EXPAND|wx.ALL, 5)
        self.SetSizer(sizer)
        self.Layout()
        
        
    def _getText(self, seq): 
        """
        Only a Facade function that interfaces with html_generator.Peptides
        """
        fileDB = self.GetParent().fileDB

        if not "proteome" in fileDB.keys():

            DialogCommons.MsgDlg(self,
                                "There is any database or fasta file",
                                'Error!', wx.OK)

        else:
            wx.Yield()
            html = html_generator.Peptide(sequence=seq, fileDB=fileDB)

            to_open = os.path.join(fileDB.get_project_dir(),
                                    '{0}{1}.html'.format(seq[0:3], 
                                                         fileDB.get_project_name()))
            out = open(to_open, 'w')
            out.write(html)
            out.close()
            return html

    