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

""" To make Join of MS/MS files"""

__authors__ = "Pietro Brunetti"

import os
import wx
import DialogCommons

import raw.proteomic_xls as MS_xls
import raw.proteomic_xml as MS_xml
import raw.PathWalk as PathWalk
import raw.data_input as data_input

class Dialog(wx.Dialog):
    """
    For Join Dialog
    Starting from many files is possible to aggragte the information.
    IT is simple descriptive statistic
    """
    def __init__(self, parent, ID, title,
                 size=wx.DefaultSize, pos=wx.DefaultPosition,
                 style=wx.DEFAULT_FRAME_STYLE):
        """Initialize Join Dialog"""

        self.kindOfFile = 0
        self.sources = os.path.expanduser("~")
        sizer =  DialogCommons.createMainSizer(self, parent, ID, title,
                                               pos, size, style)
        self._createDirBox(sizer)
        self._createFileChose(sizer)
        DialogCommons.createBtnSizer(self, sizer,
                           "The OK button to start the Join")
        self.SetSizer(sizer)
        sizer.Fit(self)


    def _createDirBox(self, sizer):
        box  = wx.BoxSizer(wx.HORIZONTAL)
        label   = wx.StaticText(self, -1, "Root directory ")
        box.Add(label, 0, wx.ALIGN_CENTRE|wx.ALL, 5)
        btn = wx.Button(self, -1, "Choose", wx.Point(50, 50)) #id 10??
        btn.SetHelpText("Choose the root directory cointaing excel files")
        self.Bind(wx.EVT_BUTTON, self.OnDir, btn)
        box.Add(btn, 0, wx.ALIGN_CENTRE|wx.ALL, 5)
        sizer.Add(box, 0, wx.GROW|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)

    def _createFileChose(self, sizer):
        self.extList = ['mzIdentML (v 1.1.0) - XML',
                        'Bioworks - Protein/Peptide - Excel',
                        'Bioworks - Peptide - Excel',
                        'Discoverer - Excel',
                        'Bioworks - Protein/Peptide - XML',
                        'Bioworks - Peptide - XML',
                        'Discoverer - Protein - XML',
                        'Discoverer - Peptide - XML',
                        'Mascott XML',
                        'PRIDE XML',
                        'PRIDE XML.gz']

        self.ch = wx.Choice(self, -1, (100, 50), choices = self.extList)
        self.ch.SetHelpText("To Choice Analysis File Extensions")
        self.Bind(wx.EVT_CHOICE, self.EvtChoice, self.ch)
        sizer.Add(self.ch, 0, wx.GROW|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)

    def OnDir(self, event):
        """ Choose the directory conteing files.
            It's possible to meke this with nested directories,
            In this case the choice is the root directory."""
        dlg = wx.DirDialog(self,
                           "Choose the directory containg files:",
                           style=wx.DD_DIR_MUST_EXIST|wx.DD_CHANGE_DIR,
                           defaultPath=os.path.expanduser("~"))
        if dlg.ShowModal() == wx.ID_OK:
            self.sources = dlg.GetPath()
            txt = "lists directory: {0}\n".format(self.sources)
            self.GetParent().SetStatusText(txt)
        dlg.Destroy()

    def EvtChoice(self, event):
        """ Writing choses on status bar"""
        self.kindOfFile = event.GetInt()
        form = "You have chosen {0} {1} \n"
        txt = form.format(self.extList[self.kindOfFile], self.kindOfFile)
        self.GetParent().SetStatusText(txt)

    def _join(self, parser, ext):
        """ Execute parsing of MS files"""
        files_pep = list(PathWalk.all_files(self.sources, ext))
        wrong = []
        for f in files_pep:
            wx.Yield()
            try:
                parser.parse(f)
            except (MS_xls.wrongFile, MS_xml.wrongFile, MS_xls.Without_Field):
                wrong.append(f)
            except MS_xls.EmptyCell:
                pass
            except data_input.bad_format_peptide, e:
                msg = 'There is a wrong format peptide:{0} in file {1}'
                txt = msg.format(unicode(e.args[0]),unicode(f))
                DialogCommons.MsgDlg(self, txt, style=wx.ICON_HAND)
            else:
                self.GetParent().SetStatusText(f)

        if wrong:
            uls = unicode('\n- '.join([os.path.split(f)[1] for f in wrong]))
            txt = "Wrong files:\n- {0}".format(uls)
            DialogCommons.MsgDlg(self, txt, style=wx.ICON_HAND)

        return parser

    def GetValue(self):
        #TODO: if the kind of file chosen is wrong
        # use a warming message dialog window.
        if self.kindOfFile == 0:
            ext = '*.mzid'
            self.p = MS_xml.mzIdent_parser()

        if self.kindOfFile == 1:
            ext = '*.xls'
            self.p = MS_xls.sequest_protpept_parser()

        elif self.kindOfFile == 2:
            ext = '*.xls'
            self.p = MS_xls.sequest_onlypept_parser()

        elif self.kindOfFile == 3:
            ext = '*.xls'
            self.p = MS_xls.discoverer_parser()

        elif self.kindOfFile == 4:
            ext = '*.xml'
            self.p =  MS_xml.sequest_prot_parser()

        elif self.kindOfFile == 5:
            ext = '*.xml'
            self.p =  MS_xml.sequest_pep_parser()
            
        elif self.kindOfFile == 6:
            ext = '*.xml'
            self.p =  MS_xml.discoverer_prot_parser()

        elif self.kindOfFile == 7:
            ext = '*.xml'
            self.p =  MS_xml.discoverer_pept_parser()

        elif self.kindOfFile == 8:
            ext = '*.xml'
            self.p =  MS_xml.mascot_parser()

        elif self.kindOfFile == 9:
            ext = '*.xml'
            self.p =  MS_xml.pride_parser()

        elif self.kindOfFile == 10:
            ext = '*.xml.gz'
            self.p = MS_xml.pride_parser(compressed=True)

        self._join(self.p, ext)
        return self.p
