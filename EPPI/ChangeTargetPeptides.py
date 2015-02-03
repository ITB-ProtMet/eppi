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
Used to changes the peptides searched for each target.

This code is form ComboCtrl Demo of wx python demos.
"""


__authors__ = "Pietro Brunetti <pietro.brunetti@itb.cnr.it>"

import wx
import wx.combo

import DialogCommons


#To-Do Think how resize the list when there are few elements
class ListCtrlComboPopup(wx.ListCtrl, wx.combo.ComboPopup):

    def __init__(self):

        # Since we are using multiple inheritance, and don't know yet
        # which window is to be the parent, we'll do 2-phase create of
        # the ListCtrl instead, and call its Create method later in
        # our Create method.  (See Create below.)
        self.PostCreate(wx.PreListCtrl())

        # Also init the ComboPopup base class.
        wx.combo.ComboPopup.__init__(self)


    def AddItem(self, txt):
        self.InsertStringItem(self.GetItemCount(), txt)

    def OnMotion(self, evt):
        item, flags = self.HitTest(evt.GetPosition())
        if item >= 0:
            self.Select(item)
            self.curitem = item

    def OnLeftDown(self, evt):
        self.value = self.curitem
        self.Dismiss()


    # The following methods are those that are overridable from the
    # ComboPopup base class.  Most of them are not required, but all
    # are shown here for demonstration purposes.


    # This is called immediately after construction finishes.  You can
    # use self.GetCombo if needed to get to the ComboCtrl instance.
    def Init(self):
        self.value = -1
        self.curitem = -1


    # Create the popup child control.  Return true for success.
    def Create(self, parent):
        wx.ListCtrl.Create(self, parent,
                           style=wx.LC_LIST|wx.LC_SINGLE_SEL|wx.SIMPLE_BORDER)

        self.Bind(wx.EVT_MOTION, self.OnMotion)
        self.Bind(wx.EVT_LEFT_DOWN, self.OnLeftDown)
        return True


    # Return the widget that is to be used for the popup
    def GetControl(self):
        return self

    # Called just prior to displaying the popup, you can use it to
    # 'select' the current item.
    def SetStringValue(self, val):
        idx = self.FindItem(-1, val)
        if idx != wx.NOT_FOUND:
            self.Select(idx)

    # Return a string representation of the current item.
    def GetStringValue(self):
        if self.value >= 0:
            return self.GetItemText(self.value)
        return ""

    # Called immediately after the popup is shown
    def OnPopup(self):
        wx.combo.ComboPopup.OnPopup(self)

    # Called when popup is dismissed
    def OnDismiss(self):
        evt = wx.PyCommandEvent(wx.EVT_TEXT.typeId, self.GetId())
        evt.SetEventObject(self.GetParent())
        wx.PostEvent(self,evt)
        wx.combo.ComboPopup.OnDismiss(self)

    # This is called to custom paint in the combo control itself
    # (ie. not the popup).  Default implementation draws value as
    # string.
    def PaintComboControl(self, dc, rect):
        wx.combo.ComboPopup.PaintComboControl(self, dc, rect)

    # Receives key events from the parent ComboCtrl.  Events not
    # handled should be skipped, as usual.
    def OnComboKeyEvent(self, event):
        wx.combo.ComboPopup.OnComboKeyEvent(self, event)

    # Implement if you need to support special action when user
    # double-clicks on the parent wxComboCtrl.
    def OnComboDoubleClick(self):
        wx.combo.ComboPopup.OnComboDoubleClick(self)

    # Return final size of popup. Called on every popup, just prior to OnPopup.
    # minWidth = preferred minimum width for window
    # prefHeight = preferred height. Only applies if > 0,
    # maxHeight = max height for window, as limited by screen size
    #   and should only be rounded down, if necessary.
    def GetAdjustedSize(self, minWidth, prefHeight, maxHeight):
        return wx.combo.ComboPopup.GetAdjustedSize(self, minWidth,
                                                   prefHeight, maxHeight)

    # Return true if you want delay the call to Create until the popup
    # is shown for the first time. It is more efficient, but note that
    # it is often more convenient to have the control created
    # immediately.
    # Default returns false.
    def LazyCreate(self):
        return wx.combo.ComboPopup.LazyCreate(self)


class Dialog(wx.Dialog):
    """ Change peptide dialog"""
    def __init__(
            self, parent, ID, title, size=wx.DefaultSize,
            pos=wx.DefaultPosition,
            style=wx.DEFAULT_DIALOG_STYLE):

        sizer = DialogCommons.createMainSizer(self, parent, ID, title,
                                              pos, size, style)
        self._createPeptidesChangeBox(sizer)

        DialogCommons.createBtnSizer(self, sizer,
                             "The OK button to start the Finger Printing")
        self.SetSizer(sizer)
        sizer.Fit(self)


    def MakeLCCombo(self, style=wx.CB_READONLY):
        # Create a ComboCtrl
        cc = wx.combo.ComboCtrl(self, style=style, size=(250, -1)) # sizes of control control, not of the list
        # Create a Popup
        popup = ListCtrlComboPopup()
        # Associate them with each other.  This also triggers the
        # creation of the ListCtrl.
        cc.SetPopupControl(popup)
        # Add some items to the listctrl.
        return cc, popup

    def _createPeptidesChangeBox(self, sizer):
        #TODO: is there the same function applied 3 time?
        # Why I do not use a map?
        box  = wx.BoxSizer(wx.VERTICAL)
        box_prot = self._createChooseProtein()
        box_pept1 =  self._createChoosePeptide1()
        box_pept2 =  self._createChoosePeptide2()
        box_pept3 =  self._createChoosePeptide3()
        box.Add(box_prot, 0, wx.ALIGN_LEFT|wx.ALL|wx.TOP, 5)
        box.Add(box_pept1, 0, wx.ALIGN_LEFT|wx.ALL|wx.TOP, 5)
        box.Add(box_pept2, 0, wx.ALIGN_LEFT|wx.ALL|wx.TOP, 5)
        box.Add(box_pept3, 0, wx.ALIGN_LEFT|wx.ALL|wx.TOP, 5)
        sizer.Add(box, 0, wx.GROW|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)


    def _set_ch_list(self, items, ch):
        ch.DeleteAllItems()
        for item in items:
            ch.AddItem(item)

    def _flex_grid(self, st_text="Peptide"):
        fgs = wx.FlexGridSizer(1, 3, 10, 10)
        ch, popup = self.MakeLCCombo()

        fgs.Add(ch)
        fgs.Add((10,10))
        fgs.Add(wx.StaticText(self, -1, st_text))

        return fgs, ch, popup

    def _createChooseProtein(self):

        target_prot = self.GetParent().fileDB["targets"].keys()
        try:
            # sort by numerical order
            target_prot.sort(key=int)
        except:
            # if is not possible to cast to int - alphabetical order
            target_prot.sort()


        fgs, self.ch_prot, self.prot_popup = self._flex_grid("Target protein")

        self._set_ch_list(target_prot, self.prot_popup)

        self.peptides = {}
        self.prot_popup.Bind(wx.EVT_TEXT, self.OnChoiceProtein)
        return fgs

    def _createChoosePeptide1(self):

        fgs, self.ch_pept1, self.pept1_popup = self._flex_grid("Peptide 1")

        self.Bind(wx.EVT_TEXT, self.OnChoicePeptide1, self.ch_pept1)
        return fgs

    def _createChoosePeptide2(self):

        fgs, self.ch_pept2, self.pept2_popup = self._flex_grid("Peptide 2")

        self.Bind(wx.EVT_TEXT, self.OnChoicePeptide2, self.ch_pept2)
        return fgs

    def _createChoosePeptide3(self):

        fgs, self.ch_pept3, self.pept3_popup = self._flex_grid("Peptide 3")

        self.Bind(wx.EVT_TEXT, self.OnChoicePeptide3, self.ch_pept3)
        return fgs

    def _setPeptidesInitialValue(self):
        try:
            target_pepts = self.GetParent().fileDB["targets"][self.prot]
        # When user does not choice
        except KeyError:
            pass
        # otherwise
        else:
            from_dict = self.GetParent().fileDB["p_peptides"][self.prot].iteritems()
            pepts = {k:"{0}:{1}".format(k,v) for k,v in from_dict}
            chs = [self.ch_pept1, self.ch_pept2, self.ch_pept3]
            for i, each in enumerate(target_pepts):
                if each:
                    value = pepts[each]
                else:
                    value = ""
                self.peptides[i] = value
                chs[i].SetValue(value)

    def _postPept(self, popups):
        try:
            from_dict = self.GetParent().fileDB["p_peptides"][self.prot].iteritems()
        # When user does not choice
        except KeyError:
            pass
        # otherwise
        else:
            pepts = ["{0}:{1}".format(k,v) for k,v in from_dict]
            for rm_pept in self.peptides.values():
                if rm_pept:
                    pepts.remove(rm_pept)
            pepts.sort()
            pepts.append("")
            for p_u in popups:
                self._set_ch_list(pepts, p_u)

    def OnChoiceProtein(self, evt):
        self.prot = self.prot_popup.GetStringValue()
        self._setPeptidesInitialValue()
        popups = [self.pept1_popup, self.pept2_popup, self.pept3_popup]
        self._postPept(popups)

    def OnChoicePeptide1(self, evt):
        pept = self.pept1_popup.GetStringValue()
        self.peptides[0] = pept
        popups = [self.pept2_popup, self.pept3_popup]
        self._postPept(popups)

    def OnChoicePeptide2(self, evt):
        pept = self.pept2_popup.GetStringValue()
        self.peptides[1] = pept
        popups = [self.pept1_popup, self.pept3_popup]
        self._postPept(popups)

    def OnChoicePeptide3(self, evt):
        pept = self.pept3_popup.GetStringValue()
        self.peptides[2] = pept
        popups = [self.pept1_popup, self.pept2_popup]
        self._postPept(popups)

    def GetValue (self):
        return (self.prot,
            [pept.split(':')[0] for pept in self.peptides.values() if pept])
