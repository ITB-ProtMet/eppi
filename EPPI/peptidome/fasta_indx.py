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
By this module it's possible to read a fasta file
to search proteins and/or peptides.

It's contains a class called **Saf**, accounts for
Simple api for fasta.

Initializing an instance passing a fasta
it's possible make an interrogation
about the contain.

The searching method are:

- *get_reference* : to obtain the reference by gi account
- *get_sequence* : to obtain the sequence of the protein by gi account
- *search_peptide* : to search proteins with given peptide
- *search_composition* : to search proteins by peptides\
with the same molecular weight


"""

__author__ = 'Pietro Brunetti'

import re
import os
from operator import itemgetter

import commons.peptidases as peptidases
from commons.aa import wrongFormat
from commons.Param import mw_map, mi_mw, wrongSequence

try:
    from agw import pyprogress as PP
except ImportError: # if it's not there locally, try the wxPython lib.
    import wx.lib.agw.pyprogress as PP
import wx


# TODO: I need a file with only these re, I use they also in data_input
gi_part = r"(?<=\A>gi\|)\d+(?=\|)"
sp_part = r"(?<=\A>sp\|)[0-9A-Z]+(?=\|)"
tr_part = r"(?<=\A>tr\|)[0-9A-Z]+(?=\|)"
ipi_part = r'(?<=\A>IPI:)IPI\d+\.\d(?=\|)'
uniRef100_part  = r'(?<=\A>UniRef100_)\w+'
groups = '|'.join([gi_part, sp_part, tr_part, ipi_part, uniRef100_part])
accInsideId = re.compile(groups)

class FastaIndxError(Exception):
    """ base class for fasta_indx PARSER class """
    pass

class WrongFile(FastaIndxError):
    """ Error occurred when the fasta file is wrong """
    pass

class WrongReference(FastaIndxError):
    """ From a reference we don't find the accession """
    pass

class WrongPeptide(FastaIndxError):
    """ From a wrong searched peptide"""
    pass

def gi_from_ref(ref):
    """
    from a reference return the gi number
    Given a SeqRecord, return the accession number as a string.

    >>> gi_from_ref(">gi|312598360|gb|ADQ90110.1| v-myc myelocyt")
    '312598360'
    >>> gi_from_ref(">gi|116878022|gb|ABK31871.1| cytochrome oxidase subunit 1 [Strix varia]")
    '116878022'
    >>> gi_from_ref(">sp|Q95BY0|MATK_CANSA Maturase K OS=Cannabis sativa GN=matK PE=3 SV=1")
    'Q95BY0'
    >>> gi_from_ref(">tr|Q8GTB6|Q8GTB6_CANSA Tetrahydrocannabinolic acid synthase OS=Cannabis sativa PE=2 SV=1")
    'Q8GTB6'
    >>> gi_from_ref(">IPI:IPI00000001.2|SWISS-PROT:O95793-1|TREMBL:A8K622;Q59F99|ENSEMBL:ENSP00000360922;")
    'IPI00000001.2'
    >>> gi_from_ref(">UniRef100_A0A009DIN6 Uncharacterized protein n=1 Tax=Escherichia coli MP1 RepID=A0A009DIN6_ECOLX")
    'A0A009DIN6'
    """
    parts = accInsideId.findall(ref)
    if parts:
        return parts[0]
    else:
        raise WrongReference, "{0} is not in the correct format".format(ref)

def _iterslice(sequence, running_window_lenght):
    """
    from a string iterates the return of substrings
    these are contiguous substrings that overlap each other
    for running_window_lenght chars

    >>> example = "Uncertainty and expectation are the joys of life."
    >>> s_s_list = [s_s for s_s in _iterslice(example, 4)]
    >>> print " ".join(s_s_list[:3])
    Unce ncer cert

    :param sequence: text to slice
    :type sequence: str
    :param running_window_lenght: length of the substrings
    :type running_window_lenght: int
    """
    i = 0
    while i < len(sequence)-running_window_lenght+1:
        yield sequence[i:i+running_window_lenght]
        i += 1

def _compare_composition(peptide, sub_seq):
    """
    controls if two string have the same composition.

    This functions is designed to compare by weight two peptides
    (To happen this they be have the same composition)
    "note" that Isoleucine and Leucine are isomers

    >>> _compare_composition("YAYAYA", "AAAYYY")
    True
    >>> _compare_composition("YAYAYA", "AAAYY")
    False

    :param peptide: 1st string to compare
    :type peptide: str
    :param sub_seq: 2nd string to compare
    :type sub_seq: str
    :return: if the two string have the same composition
    :rtype: bool
    """
    peptide_list = [each1 for each1 in peptide.replace('I', 'L')]
    sub_seq_list = [each2 for each2 in sub_seq.replace('I', 'L')]
    while peptide_list:
        amminoacid = peptide_list.pop(0)
        if amminoacid in sub_seq_list:
            sub_seq_list.remove(amminoacid)
        else:
            return False
    if not sub_seq_list:
        return True
    else: return False

def _sequence(f_input):
    """
    returns the sequence of a protein if the
    file position is right.

    :param f_input: file or stream of protein sequences

    >>> from os import curdir
    >>> import os.path as path
    >>> from os.path import abspath
    >>> input_file = path.join(curdir, "example_files", "out_ex.txt")
    >>> fr = open(input_file, 'rU')
    >>> seq = _sequence(fr)
    >>> fr.close()
    >>> print seq[:70]
    GAGAMSSRKKPSRRTRVLVGGAALAVLGAGVVGTVAANAADTTEATPAAAPVAARGGELTQSTHLTLEAA
    >>> print seq[70:140]
    TKAARAAVEAAEKDGRHVSVAVVDRNGNTLVTLRGDGAGPQSYESAERKAFTAVSWNAPTSELAKRLAQA
    >>> print seq[140:]
    PTLKDIPGTLFLAGGTPVTAKGAPVAGIGVAGAPSGDLDEQYARAGAAVLGH

    :var f_input: file handle open in read mode
    :type f_input: file
    :return:  the sequence
    :rtype: str
    """
    seq = []
    for line in f_input:
        # end of file or starting a new sequence
        if line == '' or line[0] == '>':
            break
        o_line = line.strip(os.linesep)
        seq.append(o_line)

    return ''.join(seq)

def _progress_bar(caption, opening="Sorry, I need some time"):
    """progress bar initialization"""
    dlg = PP.PyProgress(
            None, -1, caption,
            opening,
            agwStyle=wx.PD_APP_MODAL|wx.PD_CAN_ABORT
    )
    dlg.SetGaugeProportion(10/100.0)
    dlg.SetGaugeSteps(100)
    dlg.SetGaugeBackground("#FFFFFF")
    dlg.SetFirstGradientColour("#336666")
    dlg.SetSecondGradientColour("#66CCFF")
    dlg.EnableClose(True)
    return dlg

def _move_prg(dlg, update_text):
    wx.MilliSleep(1)
    keep_doing = dlg.UpdatePulse(update_text)
    wx.Yield()
    return keep_doing


def _close_prg(dlg):
    """ closing progress bar """
    dlg.Destroy()

class Saf(dict):
    """
    Simple api for fasta

    Instances read and index fasta files.
    The instances are dictionaries that store
    the position inside the fasta file of the sequence
    and the reference using gi accession as key.

    >>> from os import curdir
    >>> import os.path as path
    >>> from os.path import abspath
    >>> fasta = path.join(abspath(curdir), "example_files", "Cypselurus_Hbps.fasta")
    >>> reader = Saf(fasta)
    >>> position = reader.indx['221046918'][0]
    >>> print position
    76
    >>> with open(fasta, 'rU') as f_input:
    ...    f_input.seek(0)
    ...    line1 = f_input.readline()
    >>> print line1.strip()
    >gi|221046918|pdb|3FPW|A Chain A, Crystal Structure Of Hbps With Bound Iron

    :cvar path: file fasta to read
    :type path: str
    :cvar proteome: indx of the fasta file - each accession accounts for a file location and a description
    :type proteome: dict
    :cvar window: if there is a gui
    :type window: boolean
    """
    def __init__(self, fasta_file=None, proteome=None, window=False):

        super(Saf, self).__init__(self)
        self.__dict__ = self
        self.fasta_path = ""
        self.indx = {}

        if fasta_file:
            if not os.path.exists(fasta_file):
                raise WrongFile, "File {0} does not exist".format(fasta_file)

            self.fasta_path = os.path.abspath(fasta_file)

            if not proteome:
                if window:
                    dlg = _progress_bar("Indexing proteome", opening="Sorry, I need some time")

                with open(self.fasta_path, 'rU') as f_input:
                    while True:
                        # to read the correct position we must use readline iteration.
                        # for line in f_input
                        # and
                        # for line in f_input.readlines()
                        # do not function
                        line = f_input.readline()
                        if line:
                            # each line that start with '>' contains a reference
                            if line[0] == '>':
                                # 1) store the bites position of the line
                                ref_ind = f_input.tell()
                                # 2) extract the gi_account number
                                gi_account = gi_from_ref(line)
                                # 3) use gi_account as key to refer to reference
                                # and position inside fasta
                                self.indx[gi_account] = (ref_ind, line)
                                if window:
                                    if not _move_prg(dlg, "Indexing %s"%(ref_ind,)):
                                        break
                            else: pass
                        else: break
                if window:
                    _close_prg(dlg)
            # TODO: check the format here
            else:
                self.indx = proteome

    @staticmethod
    def from_dict(dict_):
        """ (re)construct Saf from dictionary. """
        root = Saf(dict_["fasta_path"], dict_['indx'])
        print root["fasta_path"]
        return root

    def __repr__(self):
        """
        repr overloaded method.
        It's prints where is the fasta files.

        >>> from os import curdir
        >>> import os.path as path
        >>> from os.path import abspath
        >>> fasta = path.join(abspath(curdir), "example_files", "Cypselurus_Hbps.fasta")
        >>> reader = Saf(fasta)
        >>> print repr(reader)
        <Saf for Cypselurus_Hbps.fasta>
        """
        return r"<Saf for {0}>".format(os.path.split(self.fasta_path)[1])

    def __str__(self):
        """
        str overloaded method.
        It's prints where is the fasta files and the number of sequences stored

        >>> from os import curdir
        >>> import os.path as path
        >>> from os.path import abspath
        >>> fasta = path.join(abspath(curdir), "example_files","Cypselurus_Hbps.fasta")
        >>> reader = Saf(fasta)
        >>> print(str(reader))
        file: Cypselurus_Hbps.fasta
        number of sequences: 9
        """
        msg = "file: {0}\nnumber of sequences: {1}"
        return msg.format(os.path.split(self.fasta_path)[1], len(self.indx.keys()))

    def get_reference(self, acc):
        """
        returns the protein reference by
        accession number

        >>> from os import curdir
        >>> import os.path as path
        >>> from os.path import abspath
        >>> fasta = path.join(abspath(curdir), "example_files","Cypselurus_Hbps.fasta")
        >>> reader = Saf(fasta)
        >>> ref = reader.get_reference('221046916')
        >>> print ref
        >gi|221046916|pdb|3FPV|G Chain G, Crystal Structure Of Hbps

        :var acc: accession gi to search in Fasta
        :type acc: str
        :return: the reference corresponding to accession gi
        :rtype: str
        """
        #if type(acc) != type('string'):
        acc = str(acc)
        return self.indx[acc][1].rstrip(os.linesep)

    def get_sequence(self, acc):
        """
        searches the protein sequence by
        accession number

        >>> from os import curdir
        >>> import os.path as path
        >>> from os.path import abspath
        >>> fasta = path.join(abspath(curdir), "example_files", "Cypselurus_Hbps.fasta")
        >>> reader = Saf(fasta)
        >>> seq = reader.get_sequence('221046916')
        >>> print seq[:70]
        GAGAMSSRKKPSRRTRVLVGGAALAVLGAGVVGTVAANAADTTEATPAAAPVAARGGELTQSTHLTLEAA
        >>> print seq[70:140]
        TKAARAAVEAAEKDGRHVSVAVVDRNGNTLVTLRGDGAGPQSYESAERKAFTAVSWNAPTSELAKRLAQA
        >>> print seq[140:]
        PTLKDIPGTLFLAGGTPVTAKGAPVAGIGVAGAPSGDLDEQYARAGAAVLGH

        :var acc: accession gi to search in Fasta
        :type acc: str
        :return: the sequence corresponding to accession gi
        :rtype: str
        """
        with open(self.fasta_path, 'rU') as f_input:
            position = self.indx[acc][0]
            f_input.seek(position)
            return _sequence(f_input)

    def search_peptide(self, peptide):
        """
        searches the proteins that contains given peptide

        >>> from os import curdir
        >>> import os.path as path
        >>> from os.path import abspath
        >>> fasta = path.join(abspath(curdir), "example_files", "Cypselurus_Hbps.fasta")
        >>> reader = Saf(fasta)
        >>> prots = [prot for prot in reader.search_peptide('VLVGGAALA')]
        >>> '221046916' in [gi_from_ref(ref) for ref in prots]
        True

        :var peptide: peptide to find
        :type peptide: str
        """
#        if type(peptide) not in (str, unicode):
#            msg = "The searched peptide {0} is bad formed.  {1}"
#            raise WrongPeptide, msg.format(peptide, type(peptide))
        with open(self.fasta_path, 'rU') as f_input:
            key = re.compile(peptide, re.M)
            for acc in self.indx.keys():
                f_input.seek(self.indx[acc][0])
                if key.search(_sequence(f_input)):
                    yield self.indx[acc][1].rstrip(os.linesep)

    def search_composition(self, peptide):
        """
        searches the proteins that contains peptides with the same composition
        of the given peptide

        >>> from os import curdir
        >>> import os.path as path
        >>> from os.path import abspath
        >>> fasta = path.join(abspath(curdir), "example_files", "Cypselurus_Hbps.fasta")
        >>> reader = Saf(fasta)
        >>> prots = [prot for prot in reader.search_composition('VLVGGAALA')]
        >>> '221046916' in [gi_from_ref(ref) for ref in prots]
        True

        :var peptide: peptide to find
        :type peptide: str
        """
        len_sp = len(peptide)
        with open(self.fasta_path, 'rU') as f_input:
            for acc in self.indx.keys():
                f_input.seek(self.indx[acc][0])
                seq = _sequence(f_input)
                for sub_seq in _iterslice(seq, len_sp):
                    if _compare_composition(peptide, sub_seq):
                        yield self.indx[acc][1].rstrip(os.linesep)

    def search_by_mw(self, mw_target, enzyme, enzyme_exception=None, miscut=0, delta=800, window = None):
        """
        searches the proteins that contains peptides with the same weight
        of the given peptide
        It yields a list of tuples
        (protein accession, peptide sequence, peptide molecular weigth, protein reference)

        >>> from commons import peptidases
        >>> from os import curdir
        >>> import os.path as path
        >>> from os.path import abspath
        >>> fasta = path.join(abspath(curdir), "example_files","Cypselurus_Hbps.fasta")
        >>> reader = Saf(fasta)
        >>> accessions = [prot[0] for prot in reader.search_by_mw(77047757, peptidases.no_enz) ]
        >>> '221046916' in accessions
        True

        :var mw_target: mw of the peptide to find
        :type mw_target: int
        :var enzyme: The cutting pattern to generate the peptidome. By default it's cut on K and R see peptidases
        :type enzyme: regular expression
        :var enzyme_exception: exception in cutting rule
        :type enzyme_exception: regular expression
        :var miscut: how many cut sites could jump
        :type miscut: int
        :var delta: precision to find mw
        :type delta: int
        :return: yields tuples, each tuples cointain protein accession, peptide sequence, peptide molecula weigth and prtein reference
        :rtype: list
        """
        with open(self.fasta_path, 'rU') as f_input:
            min_len = int(mw_target/mw_map['W'])
            max_len = int(mw_target/mw_map['G'])
            min_mw = int(mw_target-delta)
            max_mw = int(mw_target+delta)

            if window:
                dlg = _progress_bar("Find targets by molecular weight")


            # write the chose of the type the enzyme
            # in project file
            if enzyme != peptidases.no_enz:
                for acc in self.indx.keys():
                    f_input.seek(self.indx[acc][0])
                    prot_seq = _sequence(f_input)

                    if window:
                        if not _move_prg(dlg, "Searching in %s" %(acc,)):
                            break
                    try:
                        temp = list(peptidases.real_digestion_pro(
                                        prot_seq,
                                        enzyme,
                                        enzyme_exception, miscut,
                                        min_len, max_len,
                                        min_mw, max_mw
                                    ))
                    except wrongFormat, e:
                        wx.MessageBox("Bad Sequnce %s"%(str(e),),
                                      "Bad Sequence Error!", wx.ICON_ERROR)

                    for seq, mw in temp:
                        ref = self.indx[acc][1].rstrip(os.linesep)
                        yield (acc, seq, round(mw*10**-5, 5), ref)

            else:
                for acc in self.indx.keys():

                    f_input.seek(self.indx[acc][0])
                    prot_seq = _sequence(f_input)

                    if window:
                        if not _move_prg(dlg, "Searching in %s" %(acc, )):
                            break
                    try:
                        temp = list(peptidases.no_enz_digestion_c(
                                prot_seq,
                                min_len, max_len,
                                min_mw, max_mw
                        ))
                    except wrongFormat, e:
                        wx.MessageBox("Bad Sequnce %s"%(str(e),),
                                          "Bad Sequence Error!", wx.ICON_ERROR)

                    for seq, mw in temp:
                        ref = self.indx[acc][1].rstrip(os.linesep)
                        yield (acc, seq, round(mw*10**-5, 5), ref)

            if window:
                _close_prg(dlg)


    def search_by_sequence(self, sequence, window = None):
        """
        searches the proteins that contains peptides with the same sequence
        of the given peptide
        It yields a list of tuples
        (protein accession, peptide sequence, peptide molecular weigth, protein reference)

        >>> from os import curdir
        >>> import os.path as path
        >>> from os.path import abspath
        >>> fasta = path.join(abspath(curdir), "example_files", "Cypselurus_Hbps.fasta")
        >>> reader = Saf(fasta)
        >>> '221046916' in [prot[0] for prot in reader.search_by_sequence('VLVGGAALA')]
        True

        :var sequence: sequence of the peptide to find
        :type sequence: string

        :return: yields tuples, each tuple contains protein accession, peptide sequence, peptide molecular weight and protein reference
        :rtype: list
        """

        try:
            mw = mi_mw(sequence)
        except wrongSequence:
            raise WrongPeptide
        else:
            with open(self.fasta_path, 'rU') as f_input:
                #print self.indx.keys()
                if window:
                    dlg = _progress_bar("Find targets by sequence")

                for acc in self.indx.keys():
                    if acc != "__name":
                        f_input.seek(self.indx[acc][0])
                        prot_seq = _sequence(f_input)
                        where =  prot_seq.find(sequence)
                        if where > -1:
                            ref = self.indx[acc][1].rstrip(os.linesep)
                            yield (acc, sequence, round(mw*10**-5, 5), ref)

                        if window:
                            if not _move_prg(dlg, "Searching in %s" % (acc, )):
                                break

                    if window:
                        # closing progress bar
                        _close_prg(dlg)

    def search_by_sequence_red(self, sequence):
        """
        searches the proteins that contains peptides with the same sequence
        of the given peptide
        It yields a list of accession, description, seq

        >>> from os import curdir
        >>> import os.path as path
        >>> from os.path import abspath
        >>> fasta = path.join(abspath(curdir), "example_files", "Cypselurus_Hbps.fasta")
        >>> reader = Saf(fasta)
        >>> '221046916' in [prot[0] for prot in reader.search_by_sequence('VLVGGAALA')]
        True

        :var sequence: sequence of the peptide to find
        :type sequence: string

        :return: yields tuples, each tuples cointain protein accession, peptide sequence, peptide molecula weigth and prtein reference
        :rtype: list
        """

        with open(self.fasta_path, 'rU') as f_input:
            for acc in self.indx.keys():
                if acc != "__name":
                    f_input.seek(self.indx[acc][0])
                    prot_seq = _sequence(f_input)
                    where =  prot_seq.find(sequence)
                    if where > -1:
                        ref = self.indx[acc][1].rstrip(os.linesep)
                        yield acc, prot_seq, ref


    def sort_by_seq_len(self, reverse=False):
        """
        yield acc, seq by inverse of sequence lenght

        :var peptide: peptide to find
        :type peptide: str
        """
        items = [(k,len(self.get_sequence(k))) for k in self.indx.keys()]
        #items = adict.items()
        items.sort(key = itemgetter(1), reverse=reverse)
        for each in items:
            yield each[0], self.get_sequence(each[0])

    def search_including(self):
        """
        Scans each sequence versus other sequences of the fasta
        to find including seq
        """
        for acc, sequence in self.sort_by_seq_len():
            yield (acc,
                [each for each in self.search_by_sequence_red(sequence)])

def get_all_sequences(fasta):
    """
    It's used to parse an entire fasta,
    from the begin to the end,
    yielding for each protein
    the pair of value reference and Sequence

    I hope that it's faster than Bio version

    >>> from os import curdir
    >>> import os.path as path
    >>> from os.path import abspath
    >>> fasta_ = path.join(abspath(curdir), "example_files", "Cypselurus_Hbps.fasta")
    >>> all_seq = {k:v for k,v in get_all_sequences(fasta_)}
    >>> print all_seq['221046915'][:10]
    GAGAMSSRKK
    >>> print all_seq['221046915'][70:80]
    TKAARAAVEA
    >>> print all_seq['221046915'][-10:]
    ARAGAAVLGH
    >>> print all_seq['221046918'][:10]
    GAGAMSSRKK
    >>> print all_seq['221046918'][70:80]
    TKAARAAVEA
    >>> print all_seq['221046918'][-10:]
    ARAGAAVLGH
    >>> print all_seq['221046910'][:10]
    GAGAMSSRKK
    >>> print all_seq['221046910'][70:80]
    TKAARAAVEA
    >>> print all_seq['221046910'][-10:]
    ARAGAAVLGH

    :var fasta: the path of the fasta file
    :type fasta: str
    :return: a generator for the couple accession, sequence
    """
    with open(fasta, 'rU') as f_input:
        seq = list()
        gi_account = ''
        for line in f_input:
            # each line that start with '>' contains a reference
            if line[0] == '>':
                if gi_account:
                    yield gi_account, ''.join(seq)
                seq = []
                gi_account = gi_from_ref(line)
            else:
                line = line.rstrip('\n')
                seq.append(line)
        yield gi_account, ''.join(seq)

def main(fasta, out_file="Esempio.fasta"):
    indx = Saf(fasta)
    with open(out_file, 'wb') as handle:
        for each in indx.search_including():

            if len(each[1]) == 1:
                # finding only its self.
                acc, seq, ref = each[1][0]
                handle.write(ref)
                print "indexing:\t", ref
                handle.write("\n".join([seq[i:i+70] for i in xrange(0,
                                 len(seq), 70)]))

if __name__ == "__main__":
    main("/home/piotr/Fastas/Homo_sapiens_X.fasta")
