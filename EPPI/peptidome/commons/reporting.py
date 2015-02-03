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

'''
Created on Oct 24, 2012

@author: Pietro Brunetti
'''

import wx
#import DialogCommons

def echo_error(msg, window = False):
    if window:
        #DialogCommons.MsgDlg(window, msg, style=wx.ICON_HAND)
        dlg = wx.MessageDialog(None, msg, 'EPPI', style=wx.ICON_HAND)
        dlg.ShowModal()
        dlg.Destroy()
        #return result
    else:
        print msg