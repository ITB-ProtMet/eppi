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

""" Module for protein report dialog"""

__authors__ = "Pietro Brunetti"

import os
import wx
import wx.html as html

import html_generator
import DialogCommons

class Dialog(wx.Dialog):
    """Protein report dialog"""
    def __init__(self, parent, ref):
        wx.Dialog.__init__(self, parent, -1, 'Protein', size=(440, 400), 
                           style=wx.DEFAULT_FRAME_STYLE)

        page = html.HtmlWindow(self)
        page.SetPage(self._getText(ref))

        if "gtk2" in wx.PlatformInfo:
            page.SetStandardFonts()

        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(page, 1, wx.EXPAND|wx.ALL, 5)

        self.SetSizer(sizer)
        self.Layout()
        

    def _getText(self, ref):
        """
        Only a Facade function to interact with html_generator
        """

        fileDB = self.GetParent().fileDB
        try:
            html = html_generator.Protein(fileDB=fileDB, reference=ref)
        except KeyError:
            txt = "There is any database or fasta file"
            DialogCommons.MsgDlg(self, txt, 'Error!', wx.OK)
        else:
            txt = '{0}{1}.html'.format(ref, fileDB.get_project_name())
            to_open= os.path.join(fileDB.get_project_dir(), txt)
            out = open(to_open, 'w')
            out.write(html)
            out.close()
            return html  




