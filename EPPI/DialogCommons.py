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
Everything to create Dialog used by EPPI
Note: It's done without using classes.

The original code is in example codes
demo/Dialog.py
"""

__authors__ = "Pietro Brunetti"

import wx

def createMainSizer(parent, granparent, ID, title, pos, size, style):
    """
    Function to create control dialogs.
    """
    pre = _precreate(granparent, ID, title, pos, size, style)
    return _postcreate(parent, pre)

def _precreate(granparent, ID, title, pos, size, style):
    """
    Instead of calling wx.Dialog.__init__ we precreate the dialog
    so we can set an extra style that must be set before
    creation, and then we create the GUI object using the Create
    method.
    """
    pre = wx.PreDialog()
    pre.SetExtraStyle(wx.DIALOG_EX_CONTEXTHELP)
    pre.Create(granparent, ID, title, pos, size, style)
    return pre

def _postcreate(parent, pre):
    """
    This next step is the most important, it turns this Python
    object into the real wrapper of the dialog (instead of pre)
    as far as the wxPython extension is concerned.
    """
    parent.PostCreate(pre)
    return wx.BoxSizer(wx.VERTICAL)

def createBtnSizer(parent, sizer, helpTxt=""):
    """ At the end of the control dialog we need to use
        some buttons... to use functionality or to close it"""

    _createLine(parent, sizer)

    btn_sizer = parent.CreateButtonSizer(wx.OK|wx.CANCEL)
    sizer.Add(btn_sizer, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALL, 5)

def _createLine(parent, sizer):
        line = wx.StaticLine(parent, -1, size=(20,-1), style=wx.LI_HORIZONTAL)
        mask_ = wx.GROW|wx.ALIGN_CENTER_VERTICAL|wx.RIGHT|wx.TOP
        sizer.Add(line, 0, mask_, 5)

def MsgDlg(window, string, caption='EPPI', style=wx.YES_NO):
    """
    Create a custom Message Dialog
    """
    dlg = wx.MessageDialog(window, string, caption, style)
    result = dlg.ShowModal()
    dlg.Destroy()
    return result

class Is_there_file(wx.PyValidator):
    """
    A validator to check if the file is ok.
    For the moment it check only the present in FS,
    but for the late I can also check inside it.
    """
    def Clone(self): return Is_there_fasta()
    def TransferToWindow(self): return True
    def TransferFromWindow(self): return True

    def Validate(self, ctl):
        win = self.GetWindow()
        val = win.GetValue()

        return os.path.isfile(val)


