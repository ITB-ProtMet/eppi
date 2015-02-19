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

""" Searching for query with more results """

__authors__ = "Pietro Brunetti"

import csv

from peptidome import fasta_indx

import peptidome.commons.Param as Param
import wx
from peptidome.commons import reporting

_csv_results_header = ["Target",
                       "Matched"]

_csv_search_header = ["Target",
                       "Sequence",
                       "Weight",
                       "#Match"]

_csv_card_header = ["Target",
                    'seq1','seq2', 'seq3',
                    'mw1', 'mw2', 'mw3',
                    's1',    's2',  's3',
                    's12',   's13', 's23',
                    's123',  'results']


class by_targets_error(Exception):
    pass

class wrong_intersection_list(by_targets_error):
    pass

def _intersect(MatchingProts):
    """
    intersections between matching proteins

    """
    intersecs = []
    for i,t1 in enumerate(MatchingProts):
        for j,t2 in enumerate(MatchingProts[i+1:]):
            # & is equal to .intersection()
            intersecs.append(t1&t2)
    if len(MatchingProts) == 3:
            intersecs.append(intersecs[0]&MatchingProts[2])
    return intersecs

def _min_but_not_zero(to_search_min):
    """
    find minimum not 0
    """
    greather_than_0 = [each for each in to_search_min if each > 0]
    lower_or_eq_0 = [each for each in to_search_min if each <= 0]
    if greather_than_0:
        m = min(greather_than_0)
    else:
        m = min(lower_or_eq_0)
    return m

def _cardinals(len_sp, card_list):
    """
    Function that return the row for cardinal csv
    """
    row = []
    if len_sp == 1:
        if len(card_list) != 1:
            raise wrong_intersection_list
        row.extend(card_list)
        row.extend([0,0,0,0,0,0])
    elif len_sp == 2:
        if len(card_list) != 3:
            raise wrong_intersection_list
        row.extend(card_list[:2])
        row.append(0)
        row.append(card_list[2])
        row.extend([0,0,0])
    elif len_sp == 3:
        if len(card_list) != 7:
            raise wrong_intersection_list
        row.extend(card_list)

    m = _min_but_not_zero(card_list)
    row.append(m)
    return row


def _NA_insert(len_sp):
    row = []
    if len_sp == 1:
        row.extend(['NA','NA'])
    elif len_sp == 2:
        row.append('NA')
    return row

def _input_part(acc, sample_pepts, masses):
    len_sp = len(sample_pepts)
    row = [acc]
    row.extend(sample_pepts)
    row.extend(_NA_insert(len_sp))
    row.extend(masses)
    row.extend(_NA_insert(len_sp))
    return row

def _intersect_row(acc, sample_pepts, masses, card_list):#, found_prots):
    """
    Function that return the row for intersect csv
    """
    row = _input_part(acc, sample_pepts, masses)
    cards = _cardinals(len(sample_pepts), card_list)
    row.extend(cards)
    return row


def find(targets, proteome, kind, other_data, window = None):
    """
    find inside the database how many target proteins are digested in peptides
    It can distinguish by sequence or mass

    :param targets: list of accessions that account for target proteins
    :param proteome: Saf where searching in
    :param kind: kind of search
    :param other_data: data for the iterator searching function
    :param window: if it is in a window version
    :return: the name of the file where the informations are resumed
    """

    #ToDo: I need a log file to write what wrong happens

    # open output files
    cardinal_csv = csv.writer(open("card.csv", 'wb'))
    cardinal_csv.writerow(_csv_card_header)

    result_csv = csv.writer(open('result.csv','wb'))
    result_csv.writerow(_csv_results_header)

    search_csv = csv.writer(open('search.csv','wb'))
    search_csv.writerow(_csv_search_header)

    if window != None:
        # progress bar initialization
        dlg = fasta_indx._progress_bar("Find targets by %s" %(kind))

    # two variables used only for progress bar
    count = 0

    indx = fasta_indx.Saf(proteome=proteome["indx"])
    indx.fasta_path = proteome["fasta_path"]
    for acc, sample_pepts in targets.iteritems():

        count+=1
        matching_prots = []
        masses = []

        for pept in sample_pepts:
            pept = str(pept)
            prot_found = []

            try:
                mw = Param.mi_mw(pept)
            except Param.wrongSequence, emsg:
                msg = "error wrong format in {0}".format(emsg)
                reporting.echo_error(msg, window)

            else:
                float_mw = "%.5f" % (mw*10**(-5),)

                masses.append(float_mw)

                # ToDo: Search a good design pattern here
                # Ugly part, but better the two too similar function
                if kind == "Sequence":
                    it = indx.search_by_sequence(pept)
                if kind == "Mass":
                    it = indx.search_by_mw(mw, **other_data)

                for single_match in it:
                    # Iterating progress bar
                    if window != None:
                        if not fasta_indx._move_prg(dlg, "Looking for %s in %s" %(acc, single_match[0])):
                            break

                    prot_found.append(single_match[0])

                matching_prots.append(set(prot_found))
                row_list = [acc, pept, float_mw, len(set(prot_found))]
                search_csv.writerow(row_list)

        # there are not matches
        if not any(len(mp) > 0 for mp in matching_prots):
            msg = "Protein {0} without valid peptides".format(acc)
            reporting.echo_error(msg, window)

        else:
            intersects = _intersect(matching_prots)
            matching_prots.extend(intersects)
            cards = [len(s) for s in matching_prots]

            len_sp = len(sample_pepts)

            # writing cardinal seq
            if len_sp >= 1:
                i_row = _intersect_row(
                    acc, sample_pepts,
                    masses, cards
                )

                i = cards.index(i_row[-1])
                # the last element of i_row is the cardinality of the result

                cardinal_csv.writerow(i_row)
                # Writing results
                res_row = [acc]

                # Danila prefers that all the accessions reside on the same cell
                res_row.append(';'.join(matching_prots[i]))

                result_csv.writerow(res_row)

    if window != None:
        # closing progress bar
        fasta_indx._close_prg(dlg)


    return ["card.csv", "result.csv", "search.csv"]

if __name__=='__main__':

    tar = {"105706":[
            "NLEWIAGGTWTPSALK",
            "VFAVVITDGR",
            "DVTVTAIGIGDMFHEK"
        ]}
    fasta = r'/home/piotr/Fastas/Homo_sapiens_X.fasta'

    app = wx.App(0)
    find(tar, fasta, "Sequence", {}, app)
    app.MainLoop()
