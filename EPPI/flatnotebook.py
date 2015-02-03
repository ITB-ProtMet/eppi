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

"""
To create flat notebook (with different tabs)
"""

__authors__ = "Pietro Brunetti"

import wx

import wx.lib.agw.flatnotebook as fnb

#----------------------------------------------------------------------
#MENU_EDIT_DELETE_PAGE = wx.NewId()

class panel(wx.Panel):
    """
    The notebook used to visualize project file
    """

    def __init__(self, parent):
        """Initialize the notebook"""
        wx.Panel.__init__(self, parent)

        self._LayoutItems()
        self.Bind(fnb.EVT_FLATNOTEBOOK_PAGE_CLOSING, self.OnPageClosing)


    def _LayoutItems(self):
        """ Layout """
        mainSizer = wx.BoxSizer(wx.VERTICAL)
        self.SetSizer(mainSizer)
        bookStyle = fnb.FNB_FANCY_TABS
        self.book = fnb.FlatNotebook(self, wx.ID_ANY, style=bookStyle)
        bookStyle &= ~(fnb.FNB_NODRAG)
        bookStyle |= fnb.FNB_ALLOW_FOREIGN_DND

        mainSizer.Add(self.book, 6, wx.EXPAND)
        mainSizer.Layout()
        self.SendSizeEvent()



    def OnPageClosing(self, event):
        ind = int(self.book.GetSelection())
        # searching the key in dictionary
        eppi = self.GetParent().GetParent()
        file_opened =  eppi._openPages.pop(ind)
        item = eppi._get_item_by_label(file_opened)
        if item:
            eppi.tree.SetItemBold(item, False)
        event.Skip()
