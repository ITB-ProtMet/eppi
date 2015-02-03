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

""" Defining search dialogs """

__authors__ = "Pietro Brunetti"

import wx
import re

import DialogCommons

class Dialog(wx.Dialog):
    """ Search Dialog class"""
    def __init__( self, text,
            parent, ID, title, size=wx.DefaultSize, pos=wx.DefaultPosition,
            style=wx.DEFAULT_DIALOG_STYLE,
            useMetal=False):
        """Initialize a search dialog"""
        sizer = DialogCommons.createMainSizer(self, parent, ID, title, pos,
                                              size, style)
        self._createMask(sizer, text)

        DialogCommons.createBtnSizer(self, sizer,
                           "The OK button to start the Search")
        self.SetSizer(sizer)
        sizer.Fit(self)

    def _createMask(self, sizer, text):
        """ Create search mask """

        megabox = wx.FlexGridSizer(1, 2, 3, 3)
        megabox.AddGrowableCol(1)

        l_prot = wx.StaticText(self, -1, text)
        megabox.Add(l_prot, 0, wx.ALIGN_CENTER_VERTICAL)

        self.t_prot = wx.TextCtrl(self, -1)
        megabox.Add(self.t_prot, 0, wx.EXPAND)

        sizer.Add(megabox, 1, wx.EXPAND|wx.ALL, 5)

    def GetValue(self):
        return self.t_prot.GetValue()


