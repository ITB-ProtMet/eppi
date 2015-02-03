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

""" Module for the project Resume Dialog """

__authors__ = "Pietro Brunetti"

import os

import wx
import wx.html as html

import html_generator


class Dialog(wx.Dialog):
    """ To visualize a main information about the project"""
    def __init__(self, parent):
        wx.Dialog.__init__(self, parent, -1, 'Analysis Summary', size=(480, 500), 
                           style=wx.DEFAULT_FRAME_STYLE)
        page = html.HtmlWindow(self)
        page.SetPage(self._getText())

        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(page, 1, wx.EXPAND|wx.ALL, 5)

        self.SetSizer(sizer)
        self.Layout()
        
    def _getText(self):
        """Used to write HTML project report"""

        fileDB = self.GetParent().fileDB

        html = html_generator.Summary(fileDB)

        to_open = os.path.join(fileDB.get_project_dir(),
                            '{0}.html'.format(fileDB.get_project_name()))
        with open(to_open, 'w') as out:
            out.write(html)

        return html