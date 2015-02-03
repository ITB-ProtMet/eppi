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
This is the main file of EPPI application.
EPPI is *Experimental Proteotypic Peptides Investigator*

THIS SOFTWARE WORK ON XP ONLY USING float(wx.__version__) <= 2.8


The scheme of EPPI derive from an `IBM wx example`_

.. _`IBM wx example`:
        http://wiki.wxpython.org/WxProject
:var WILDCARD: the wildcard of EPPI project files

"""

__authors__ = "Pietro Brunetti"

import sys
import os
import wx
import shutil
import csv
import heapq
import re

import EPPI_data
import DialogCommons
import pages
import flatnotebook

import Resume
import Search
import ManageVars

import Join
import SelPepts
import Targets
import by_targets
import peptidome.commons.peptidases as peptidases
import ChangeTargetPeptides

import raw.preStats as preStats
import raw.data_input as data_input

import ReportProtein
import ReportSequence

import project

# TODO: Use these exceptions!
class EppiError(Exception):
    pass
class DirtyProject(EppiError):
    pass

WILDCARD = 'File Project (*.prj)|*.prj'

class main_window(wx.Frame):
    """
    wxProject Main Frame Windows

    :ivar parent: parent window (there aren't)
    :ivar id: identification number of the window
            (used -1, that mean for an automatic selection)
    :ivar title: main windows title
    :type title: str
    :ivar fileDB: is an object database repository builded by project.
        It store:
            - **files**: a EPPI project file_tree object
                (see project module for more informations).
    |   It may also store:
            - **parser**, with two dictionaries:
                - **proteins**:	a dictionary of proteins found.
                    schema {*Accession*:*Occurence*}
                - **peptides**:	a dictionary of peptides found. schema
                    {*Accession*:{*Sequence*:*Occurence*}}
            - **selected**, with two dictionaries:
                - **proteins**:	a dictionary of proteins found
                    that exceed protein IF threshold.
                    schema {*Accession*:*Occurence*}
                - **peptides**:	a dictionary of peptides found
                    that exceed peptides IF threshold. schema
                    {*Accession*:{*Sequence*:*Occurence*}}
            - **targets**:	list of targets proteins stored by *Accession*
    """

    def __init__(self, parent, id, title):
        """
        Create the wxProject MainFrame.
        """

        wx.Frame.__init__(self, parent, id,
                          title=title, size=(500, 600),
                          pos=wx.DefaultPosition)

        self.SetIcon(EPPI_data.getlogoIcon())
        self._create_menu_bar()
        self._create_status_bar()
        self._create_split()

        # Some global state variables.
        self.project_dirty = False
        self.root = None
        self.close = True
        self.dlg_style = wx.CAPTION #| wx.CLOSE_BOX | wx.THICK_FRAME

        self.Bind(wx.EVT_CLOSE, self.onProjectExit)
        self.Show(True)

    def _create_menu_bar(self):
        """
        Create the menu bar
        """

        mb = wx.MenuBar()
        self._create_project_menu(mb)
        self._create_actions_menu(mb)
        self._create_analysis_menu(mb)
        self._create_about_menu(mb)
        self.SetMenuBar(mb)

    def _create_project_menu(self, mb):
        """
        Make the 'Project' menu
        :param mb: menu bar
        """

        menu = wx.Menu()
        # Append a new menu
        item = menu.Append(wx.ID_OPEN, '&Open', 'Open project')
        # Create and assign a menu event
        self.Bind(wx.EVT_MENU, self.onProjectOpen, item)

        item = menu.Append(wx.ID_NEW, '&New', 'New project')
        self.Bind(wx.EVT_MENU, self.onProjectNew, item)

        item = menu.Append(wx.ID_SAVE, '&Save', 'Save the project')
        self.Bind(wx.EVT_MENU, self.onProjectSave, item)

        item = menu.Append(wx.ID_EXIT, 'E&xit', 'Exit program')
        #TODO: it does not work
        self.Bind(wx.EVT_MENU, self.onProjectExit, item)

        # Add the project menu to the menu bar
        mb.Append(menu, '&Project')

    def _create_item(self, msg1, menu, funct, msg2="", enable=False):
        """
        Create items to append to menus
        """
        if msg2 == "":
            msg2 = msg1
        item = menu.Append(-1, msg1, msg2)
        item.Enable(enable)
        self.Bind(wx.EVT_MENU, funct, item)
        return item

    def _create_actions_menu(self, mb):
        """
        Make the 'Actions' menu
        :param mb: menu bar
        """

        menu = wx.Menu()

        self.mv_item = self._create_item(
            "Insert Database",
            menu,
            self.OnManageVars
        )

        self.jn_item = self._create_item(
            'Join',
            menu,
            self.onJoin,
            'Join xls analysis files'
        )

        self.sl_item = self._create_item(
            'Select',
            menu,
            self.OnSelect,
            'Select proteotypic peptides'
        )

        self.it_item = self._create_item(
            'Insert Targets',
            menu,
            self.OnTarget,
            'Interface to insert target proteins'
        )

        self.ctp_item = self._create_item(
            'Change Target Peptides',
            menu,
            self.OnChangeTargetPeptides
        )

        self.fp_item = self._create_item(
            'Comparison by Mass',
            menu,
            self.OnQuery_MW,
            'Interface to mass finger printing'
        )

        self.fps_item = self._create_item(
            'Comparison by Sequence',
            menu,
            self.OnQuery_Seq,
            'Interface to sequence finger printing'
        )

        # Add the file menu to the menu bar
        mb.Append(menu, '&Actions')

    def _create_analysis_menu(self, mb):
        """
        Make the 'Analysis' menu
        :param mb: menu bar
        """

        menu = wx.Menu()

        self.resume_item = self._create_item(
            '&Resume',
            menu,
            self.OnProjectResume,
            'Information on project'
        )

        self.search_item = self._create_item(
            'Find &Proteins',
            menu,
            self.OnSearchProtein,
            'Search a protein inside current analysis'
        )

        self.s_seq_item = self._create_item(
            'Find a &Sequence',
            menu,
            self.OnSearchSequence,
            'Search a sequence inside current analysis'
        )

        # Add the file menu to the menu bar
        mb.Append(menu, "&Report")

    def _create_about_menu(self, mb):
        """
        Make the 'About' menu
        :param mb: menu bar
        """

        menu = wx.Menu()
        item = menu.Append(wx.ID_ABOUT, "&About",
                           "Information about this program")
        self.Bind(wx.EVT_MENU, self.OnAbout, item)
        # Add the file menu to the menu bar
        mb.Append(menu, '&Help')

    def _create_status_bar(self):
        """
        Create the Status Bar
        """

        self.CreateStatusBar()
        self.SetStatusText("...")

    def _create_split(self):
        """
        Create the splitter window
        """

        splitter = wx.SplitterWindow(self, style=wx.SP_3D)
        splitter.SetMinimumPaneSize(1)
        self._create_tree(splitter)
        self._create_notebook(splitter)
        # Install the tree and the editor.
        splitter.SplitVertically(self.tree, self.nb)
        splitter.SetSashPosition(180, True)

    def _create_tree(self, splitter):
        """
        Create the tree on the left
        :param splitter: splitter window
        """

        self.tree = wx.TreeCtrl(splitter, style=wx.TR_DEFAULT_STYLE)
        self.tree.Bind(wx.EVT_TREE_ITEM_ACTIVATED, self.onTreeItemActivated)


    def _get_item_by_label(self, search_text):
        """
        Search a label with given text and return its id.
        :param search_text: label to search in the tree
        :return: Id of the label
        """

        item, cookie = self.tree.GetFirstChild(self.root)

        while item.IsOk():
            text = self.tree.GetItemText(item)
            if text == search_text:
                return item
            item, cookie = self.tree.GetNextChild(self.root, cookie)
        return wx.TreeItemId()


    def _create_notebook(self, splitter):
        """
        Create the notebook on the right
        :param splitter: splitter window
        """

        self._openPages = []
        self.nb = flatnotebook.panel(splitter)


    def _create_dlg(self, init_dlg, kargs):
        """
        Help to manage each dialog
        :param init_dlg: dialog to initialize
        :param kargs: arguments for the dialog
        """

        dlg = init_dlg(**kargs)
        dlg.CenterOnScreen()
        return dlg

    # Some nice little handlers.
    def _allow_action(self):
        """
        Allow actions items in logic order
        """
        if self.fileDB:
            self.mv_item.Enable(True)
        if 'files' in self.fileDB.keys():
            self.jn_item.Enable(True)
            self.resume_item.Enable(True)
        if 'proteome' in self.fileDB.keys():
            self.search_item.Enable(True)
            self.s_seq_item.Enable(True)
        if 'p_proteins' in self.fileDB.keys():
            self.sl_item.Enable(True)
        if 's_proteins' in self.fileDB.keys():
            self.it_item.Enable(True)
        if 'targets' in self.fileDB.keys():
            self.ctp_item.Enable(True)
            self.fp_item.Enable(True)
            self.fps_item.Enable(True)

    def add_file(self, new_file):
        """
        Add a file in current project
        in two step:
        1) adding inside fileDB
        2) adding base name in the tree

        :param new_file: the file to add at the project
        """

        new_file = os.path.split(new_file)[1]
        if not new_file in self.fileDB["files"]:
            try:
                self.fileDB.append_file(new_file)
            except IOError:
                txt = 'There was an error adding a file to the project file.'
                DialogCommons.MsgDlg(self, txt, 'Error!', wx.OK)
            else:
                self.tree.AppendItem(self.root, os.path.basename(new_file))
                self.tree.Expand(self.root)
                self.project_dirty = True

    def add_files(self, files):
        """
        Add a file in current project
        in two step:
        1) adding inside fileDB
        2) adding base name in the tree

        and also
        3) if the file is open on notepad reload it

        :param files: a list of file to add at the project
        """

        files = [os.path.split(each)[1] for each in files]
        new_files = [each_file for each_file in files \
                     if not each_file in self.fileDB["files"]]
        try:
            self.fileDB.extend_files(new_files)
        except IOError:
            txt = 'There was an error extending with files the project.'
            DialogCommons.MsgDlg(self, txt, 'Error!', wx.OK)
        else:
            for each_file in new_files:
                self.tree.AppendItem(self.root,
                                     os.path.basename(each_file))
                self.tree.Expand(self.root)
            self.project_dirty = True

    def _project_open(self, project_file, flag):
        """
        Open and process a wxProject file.

        Here we initialize self.fileDB
        """
        # TODO: Validator?
        try:
            self.fileDB = project.EPPI_dbopen(project_file, flag)
            # open only here
        except IOError:
            DialogCommons.MsgDlg(self,
                             'There was an error opening the project file.',
                             'Error!', wx.OK)
        else:
            self.tree.DeleteAllItems()
            self.SetTitle(self.fileDB.get_project_name())
            # create the file elements in the tree control.
            self.root = self.tree.AddRoot(self.fileDB.get_project_name())
            self.activeitem = self.root
            if flag == 'c':
                files = [os.path.basename(each_file) \
                         for each_file in self.fileDB["files"]]
                for each_file in files:
                    self.tree.AppendItem(self.root,
                                     each_file.replace('\n', ''))
                self.tree.Expand(self.root)
            self.project_dirty = False
            self._allow_action()

    def _project_save(self, flag='s'):
        """
        Save a msProject file.
        If there are files not saved inside self.fileDB["files"]
        it saves they.

        :param flag: permits to chose between
            * 's' for save -> sync and
            * 'c' for close -> close
        """

        count = self.tree.GetChildrenCount(self.root)
        for i in range(count):
            if i == 0:
                child, cookie = self.tree.GetFirstChild(self.root)
            else:
                child, cookie = self.tree.GetNextChild(self.root, cookie)

                if not self.tree.GetItemText(child) in self.fileDB["files"]:
                    self.fileDB.append_file(self.tree.GetItemText(child))

        if flag == 's':
            self.fileDB.sync() # only here project sync
        elif flag == 'c':
            self.fileDB.close() # only here the project close
        self.project_dirty = False

    def _check_project_dirty(self):
        """
        Was the current project changed?
        If so, save it before.
        """

        open_it = True
        if self.project_dirty:
            # save the current project file first.
            result=DialogCommons.MsgDlg(self,
                    'The project has been changed. Save?')
            if result == wx.ID_YES:
                self._project_save('s')
            else:
                open_it = False
        return open_it

    # Event handlers from here on out.
    def onProjectOpen(self, event):
        """
        Open a msProject file.

        :param event: the event to open a project
        """

        open_it = self._check_project_dirty()
        if open_it:
            dlg = wx.FileDialog(
                parent=self,
                message='choose a project to open',
                wildcard=WILDCARD,
                style=wx.FD_OPEN,
                defaultDir=os.path.expanduser("~")
            )
            if dlg.ShowModal() == wx.ID_OK:
                self._project_open(dlg.GetPath(), 'c')
                self.resume_item.Enable(True)



                if 'proteome' in self.fileDB.keys():
                    f = self.fileDB["proteome"]
                    if not os.path.isfile(f['fasta_path']):
                        msg = "Warning:\n%s\nThere is not more in the path."
                        wx.MessageBox(
                            message=msg%(self.fileDB["proteome"]),
                            style=wx.ICON_INFORMATION
                        )
            dlg.Destroy()

    def onProjectNew(self, event):
        """
        Create a new msProject.

        :param event: the event to create a new project
        """
        open_it = self._check_project_dirty()
        if open_it:
            dlg = wx.FileDialog(
                parent=self,
                message="Create a new project.",
                #inside a directory with the same name',
                defaultFile='NewProject.prj',
                defaultDir=os.path.expanduser("~"),
                wildcard=WILDCARD,
                style=wx.FD_SAVE
            )
            if dlg.ShowModal() == wx.ID_OK:
                self._project_open(dlg.GetPath(), 'n')
            dlg.Destroy()
            self._project_save('s')

    def _save_current_file(self):
        """
        Check and save current file.
        """

        go_ahead = True
        if self.root and self.activeitem != self.root:
            pass
            # put some code instead to save the single file
        return go_ahead

    def onProjectExit(self, event):
        """
        Exit from Project.

        :param event: The event to quit the project
        :type event: wx.event
        """

        # I don't remember 'cause there is
        # this strange nested decision tree
        # if self.close is False it will change to True
        # except if self._save_current_file() is False
        # okay, it's better to write as follow
        if not self.close and self._save_current_file():
            self.close = True

        # Now, It passed the previous block
        # after if self.close is close but also
        # project_dirty. It creates a message
        # dialog to let choose if save or not the changes
        # on the project
        if self.project_dirty and self.close:
            result = DialogCommons.MsgDlg(
                self,
                'The project has been changed. Save?'
            )
            if result == wx.ID_YES:
                self._project_save('c')
                self.fileDB = None
                self.tree.DeleteAllItems()
            if result == wx.ID_CANCEL:
                self.close = False

            if self.close:
                if self.root:
                    self.Destroy()

        # if project is not change and
        # it skips the exit
        elif self.close:
            event.Skip() # How does it works?

    def onProjectSave(self, event):
        """
        Save the project

        :param event: The event to quit the program
        :type event: wx.event
        """
        self._project_save('s')

    def _single_item(self, func, act_file, status = True):
        """
        add the pages to the notebook
        with the label to show on the tab

        :param func: three possibility pages.Txt; pages.Image and pages.CSV
        :param act_file: The file to open in the notebook
        :param status: File open in foreground
        """
        self.Freeze()
        path = os.path.join(
            self.fileDB.get_project_dir(),
            act_file
        )
        page = func(self.nb.book, path)
        self.nb.book.AddPage(page, act_file, status)
        self.Thaw()

    def _item_activation(self, item, act_file):

        self.activeitem = item
        if item != self.root:
            if not act_file in self._openPages:
                ext = os.path.splitext(act_file)[1]
                # load the current selected file
                self.tree.SetItemBold(item, True)
                # create the page windows as children of the notebook
                self._openPages.append(act_file)
                if ext in ['.txt','.log']:
                    self._single_item(pages.Txt, act_file)

                elif ext == '.png':
                    self._single_item(pages.Image, act_file)

                elif ext == '.csv':
                    self._single_item(pages.CSV, act_file)
                    #self.SetSizeWH(1000, 1000)
            else:
                # TODO: REFRESH PAGE
                val = self._openPages.index(act_file)
                self.nb.book.SetSelection(int(val))

    def onTreeItemActivated(self, event, item=None):
        """Tree item was activated: try to open this file."""

        go_ahead = self._save_current_file()
        if go_ahead and event:
            item = event.GetItem()
            act_file = self.tree.GetItemText(item)
            self._item_activation(item, act_file)

    def _it_is_all_fine(self, label, end_msg="I done the deed"):

        self._allow_action()
        self.project_dirty = True

        # Now it writes in project only the label,
        # not the entire path
        self.add_file(label)

        item = self._get_item_by_label(label)
        self._item_activation(item, label)

        self.SetStatusText(end_msg)

    def OnManageVars(self, event):
        """Show Managing Variables dialog"""

        dlg = self._create_dlg(ManageVars.Dialog, {
            'parent': self,
            'ID': -1,
            'title': "Insert Database",
            'size': (450, 800),
            'style': self.dlg_style
        })
        ret = dlg.ShowModal()

        if ret == wx.ID_OK:
            val = dlg.GetValue()

            self.fileDB.update(val)

            self._allow_action()
            self.project_dirty = True

        dlg.Destroy()

    def onJoin(self, event):
        """Show Join dialog"""

        dlg = self._create_dlg(Join.Dialog, {
            'parent': self,
            'ID': -1,
            'title': "Join",
            'size': (450, 800),
            'style': self.dlg_style
        })

        if dlg.ShowModal() == wx.ID_OK:
            # retrieve values from dialog
            p = dlg.GetValue()
            self.fileDB.set_parser(p)

            # write file
            dir_name = self.fileDB.get_project_dir()
            out = os.path.join(dir_name, 'all_peptides.csv')
            p.peptide_csv(out)

            # open file on notetab,
            # set project as dirty and
            # set allowed actions
            self._it_is_all_fine('all_peptides.csv')
        dlg.Destroy()

    def OnSelect(self, event):
        """Show Select dialog"""

        self.SetStatusText("Start Selection...\n")

        dlg = self._create_dlg(SelPepts.Dialog, {
            'parent': self,
            'ID': -1,
            'title': "Select",
            'size': (450, 800),
            'style': self.dlg_style
        })

        if dlg.ShowModal() == wx.ID_OK:
            val = dlg.GetValue()
            p = self.fileDB.get_parser()

            frm = "SelPepts protThr: {0}, peptThr {1}"
            txt = frm.format(
                round(val["protThr"], 3),
                round(val["peptThr"], 3)
            )
            self.SetStatusText(txt)

            selected= data_input.selected(
                p,
                protThr=val["protThr"],
                peptThr=val["peptThr"]
            )
            project_name = self.fileDB.get_project_name()
            project_dir = self.fileDB.get_project_dir()
            out = os.path.join(project_dir, 'best_peptides.csv')
            selected.peptide_csv(out)

            self.fileDB.set_selected(selected)

            adding = [out]
            #-------------------------------------------------
            if val["haveHisto"]:
                plot_file = os.path.join(project_dir, 'pie_hist.png')

                if os.path.exists(plot_file):
                    os.unlink(plot_file)

                fig = preStats.analysis_plot(
                    p,
                    thrPrt=val["protThr"],
                    thrPep=val["peptThr"],
                    analysis_name=project_name
                )

                fig.savefig(plot_file, papertype='a4', orientation='landscape')
                adding.append(plot_file)
            #-------------------------------------------------
            if val["haveScatter"]:
                name = "{0} scatter".format(project_name)
                plot_file = os.path.join(project_dir,'scatter.png')

                if os.path.exists(plot_file):
                    os.unlink(plot_file)

                fig = preStats.freq_Scatter(
                    parser=p,
                    thrPrt=val["protThr"],
                    thrPep=val["peptThr"],
                    analysis_name = name,
                    Xlab = "Frequency of proteins",
                    Ylab = "Frequency of peptides"
                )

                fig.savefig(plot_file, papertype='a4', orientation='landscape')
                adding.append(plot_file)
            #-------------------------------------------------
            self.add_files(adding)
            self._it_is_all_fine('best_peptides.csv')
        dlg.Destroy()

    def _map_targets_by_occ(self, targets,
                            sel_pepts,
                            number_of_match=3):
        """
        Mapping peptides by occurrences

        :param targets: list of accessions that account for target proteins
        :param number_of_match: How many peptides for each targets it can use
        :return: a map from each targets to the most frequent peptides
        """
        withOcc = {}
        for prot in targets:
            withOcc[prot] = []
            if prot in sel_pepts.keys():
                l = [(v, k) for k, v in sel_pepts[prot].iteritems()]
                withOcc[prot] = [each[1] for each in heapq.nlargest(
                    number_of_match,
                    l
                )]
        return withOcc

    def OnTarget(self, event):
        """Show Targets dialog"""
        dlg = self._create_dlg(Targets.Dialog, {
            'parent': self,
            'ID': -1,
            'title': "Insert Targets",
            'size': (450, 800),
            'style': self.dlg_style
        })

        if dlg.ShowModal() == wx.ID_OK:
            val = dlg.GetValue()
            kof = val["kind_of_file"]
            targets = val["targets"]

            if kof == 0:
                self.fileDB["targets"] = self._map_targets_by_occ(
                    targets,
                    self.fileDB["p_peptides"]
                )
            elif kof == 1:
                self.fileDB["targets"] = self._map_targets_by_occ(
                    targets,
                    self.fileDB["s_peptides"]
                )

            # elaboarate files
            selected = self.fileDB.get_selected()
            parser = self.fileDB.get_parser()

            project_dir = self.fileDB.get_project_dir()

            targets = [s for s in targets if s in parser.peptides.keys()]
            targets = set(targets)

            adding = []

            namePep = os.path.join(
                project_dir,
                'peptides_in_targets.csv'
            )

            handle = open(namePep, 'wb')
            de_outPep_csv = csv.writer(handle)

            de_outPep_csv.writerow([
                "Protein",
                "Peptide",
                "#Protein",
                "#Peptide",
                "Best"
            ])
            for accession in targets:
                for sequence in parser.peptides[accession]:
                    if accession in selected.peptides.keys():
                        if sequence in selected.peptides[accession].keys():
                            row = [
                                accession,
                                sequence,
                                parser.proteins[accession],
                                parser.peptides[accession][sequence],
                                "True"
                            ]

                        else:
                            row = [
                                accession,
                                sequence,
                                parser.proteins[accession],
                                parser.peptides[accession][sequence],
                                "False"
                            ]
                    else:
                        row = [
                            accession,
                            sequence,
                            parser.proteins[accession],
                            parser.peptides[accession][sequence],
                            "False"
                        ]

                    de_outPep_csv.writerow(row)

            handle.close()
            adding.append(namePep)

            namePrt = os.path.join(
                project_dir,
                "target_proteins_list.csv"
            )
            handle = open(namePrt, 'wb')
            de_outPrt_csv = csv.writer(handle)

            de_outPrt_csv.writerow([
                "Protein",
                "#All Peptides",
                "#Best Peptides"
            ])

            for accession in targets:
                if accession in selected.peptides.keys():
                    de_outPrt_csv.writerow([
                        accession,
                        len(parser.peptides[accession]),
                        len(selected.peptides[accession])
                    ])
                else:
                    de_outPrt_csv.writerow([
                        accession,
                        len(parser.peptides[accession]),
                        0
                    ])

            handle.close()
            adding.append(namePrt)
            self.add_files(adding)
            self._it_is_all_fine('peptides_in_targets.csv')

        dlg.Destroy()

    def OnChangeTargetPeptides(self, event):
        """Show ChangeTargetPeptides dialog"""

        dlg = self._create_dlg(ChangeTargetPeptides.Dialog, {
            'parent': self,
            'ID': -1,
            'title': "Change Target Peptides",
            'size': (450, 800),
            'style': self.dlg_style
        })

        if dlg.ShowModal() == wx.ID_OK:
            protein, peptides = dlg.GetValue()
            self.fileDB["targets"][protein] = peptides
            self._it_is_all_fine('peptides_in_targets.csv')
        dlg.Destroy()

    def OnQuery_MW(self, event):
        """ Find Tagets """

        dir_name = self.fileDB.get_project_dir()
        enz_code = self.fileDB["enzyme"]

        data = {
            "targets": self.fileDB["targets"],
            "proteome": self.fileDB["proteome"],
            "kind": "Mass",
            "other_data": {
                "delta": self.fileDB["delta"],
                "enzyme": peptidases.int2enz[enz_code],
                "miscut": self.fileDB["miscut"],
            },
            "window": self
        }

        outputs = by_targets.find(**data)

        prefix = 'mw_'
        for each in outputs:
            dest = os.path.join(dir_name, "{0}{1}".format(prefix, each))
            shutil.move(each, dest)
            self.add_file(dest)

        self._it_is_all_fine('mw_search.csv')

    def OnQuery_Seq(self, event):
        """ Find Tagets """

        dir_name = self.fileDB.get_project_dir()
        data = {
            "targets": self.fileDB["targets"],
            "proteome": self.fileDB["proteome"],
            "kind": "Sequence",
            "other_data": {},
            "window": self
        }
        outputs = by_targets.find(**data)

        prefix = 'seq_'
        for each in outputs:
            dest = os.path.join(dir_name, "{0}{1}".format(prefix, each))
            shutil.move(each, dest)
            self.add_file(dest)
        self._it_is_all_fine('seq_search.csv')

    def OnProjectResume(self, event):
        """Show the resume"""

        dlg = Resume.Dialog(self)
        dlg.ShowModal()
        dlg.Destroy()

    def OnSearchProtein(self, event):
        """Show informations about a target protein"""
        dlg = self._create_dlg(Search.Dialog, {
            'parent': self,
            'text': 'Find Proteins',
            'ID': -1,
            'title': "Find Proteins",
            'size': (450, 800),
            'style': wx.CAPTION | wx.SYSTEM_MENU | wx.THICK_FRAME
        })

        if dlg.ShowModal() == wx.ID_OK:
            r = re.compile(r'\b[0-9]+\b')
            reflist = dlg.GetValue()
            for ref in r.finditer(reflist):
                dlg2 = ReportProtein.Dialog(self, ref.group())
                dlg2.ShowModal()
                dlg2.Destroy()
        dlg.Destroy()

    def OnSearchSequence(self, event):
        """Show informations about a target peptide"""
        dlg = self._create_dlg(Search.Dialog, {
            'parent': self,
            'text': 'Find a Sequence',
            'ID': -1,
            'title': "Find a Sequence",
            'size': (450, 800),
            'style': wx.CAPTION | wx.SYSTEM_MENU | wx.THICK_FRAME
        })

        if dlg.ShowModal() == wx.ID_OK:
            r = re.compile(r'[A-Z]{6,}')
            seq = dlg.GetValue()
            m = r.match(seq)
            if m:
                dlg2 = ReportSequence.Dialog(self, m.group())
                dlg2.ShowModal()
                dlg2.Destroy()
        # TODO: put an exit if the regex find doesn't find anything
        dlg.Destroy()

    def OnAbout(self, event):
        """show About box"""
        from wx.lib.wordwrap import wordwrap
        info = wx.AboutDialogInfo()
        info.Name = "EPPI"
        info.Version = "1.0.0"
        info.Copyright = "(C) 2015 ITB-CNR Proteomic & Metabolomic Group"
        eppi_acro = "Experimental Proteotypic Peptides Investigator"

        info.Description = wordwrap(
            eppi_acro,
            350,
            wx.ClientDC(self)
        )

        info.Developers = [
            "Pietro Brunetti - Programmer",
            "\nPierluigi Mauri - Supervisor",
            "\n\n Special thanks to Dario Di Silvestre, Simone Daminelli And Danila Vella"
        ]

        info.Artists = ["Icon - from Tango project - public Domain"]
        info.License = wordwrap(EPPI_data.licenseText, 500, wx.ClientDC(self))
        wx.AboutBox(info)


class App(wx.App):
    """wxProject Application."""
    def OnInit(self):
        """Create the wxProject Application."""
        frame = main_window(parent=None, id=-1,
                            title="{0}{1}".format('EPPI - ', project_file))
        frame.Show()
        return True

if __name__ == '__main__':

    global project_file
    project_file = 'Experimental Proteotypic Peptide Investigator'
    if len(sys.argv) > 1:
        project_file = sys.argv[1]

    app = App(False)
    app.MainLoop()
