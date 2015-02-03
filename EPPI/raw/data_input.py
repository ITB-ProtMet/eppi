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
To initialize each input data parser
for mass spectrometry proteomics
"""

__authors__ = "Pietro Brunetti"

import re
#import os
import csv
import json
from collections import Counter
from codecs import encode

class data_input_Error(Exception):
    pass

class bad_format_peptide(data_input_Error):
    """
    Exception for malformed peptide sequence
    """
    pass

class redundant_proteins(data_input_Error):
    """
    Exception for redundant protein inside the file
    """
    pass

class protein_peptide_pair_over(data_input_Error):
    """
    When there are more than one pair accession-sequence pairs
    """
    pass

class DecodeError(data_input_Error):
    """
    When you would decode a wrong dict to a parser
    """
    pass

class parser(object):
    """
    Superclass used to derive all input seq parser

    :cvar peptide_format: if the peptides has the right format
    :cvar gi_part: recognize an gene-bank accession from an identifier
    :cvar sp_part: recognize an swiss_prot accession from an identifier
    :cvar ipi_part: recognize an international protein index accession from an identifier
    :cvar groups: union of gi_part, sp_part and ipi_part
    :cvar acc2id: recognizes accession from identifier

    :ivar spectral_count: defines if it must count all peptide occurrences in a specific file,
        or if it must count one time only a peptide that appear more times in a file.
    :ivar proteins: is a dictionary that for each accession accounts for occurrence inside seq
    :ivar peptides: is the seq storage for peptides. A peptides are specified by a dictionary,
        each key is a protein accession id and each value is an other dictionary,
        For this child dictionary each key is a peptide sequence and each value is the occurrence
    :ivar sources: a list of source analyzed objects
    """

    #TODO: move these stuff and make them global
    peptide_format = re.compile(r"\A[A-Z]+\Z")
    # TODO: I need a file with only these re, I use they also in data_input
    gi_part = r"(?<=^gi\|)\d+(?=\|)"
    sp_part = r"(?<=^sp\|)[0-9A-Z]+(?=\|)"
    tr_part = r"(?<=^tr\|)[0-9A-Z]+(?=\|)"
    ipi_part = r'(?<=^IPI:)IPI\d+\.\d(?=\|)'
    groups = '|'.join([gi_part, sp_part, tr_part, ipi_part])
    acc2id = re.compile(groups)

    def __init__(self, mode=False):
        """
        Initialize a parse object

        :param mode: spectral count mode, default False
        :type mode: bool
        """
        self.spectral_count = mode
        self.sources = []
        self.proteins = Counter()
        self.peptides = dict()

    def parse(self, data):
        """
        parse seq

        :param data: an object that it has two lists:
            - proteins [acc]
            - peptides [(acc, [seq])]

        :raises redundant_proteins: If there are redundant protein (more than one value for type)
        :raises bad_format_peptide: If the peptide format is not correct, with only UPPERCASE characters
        """
        
        r_msg = "{0} is repeated inside seq set"
        _prot_unique = []
        for acc in data.proteins:
            if acc in _prot_unique:
                raise redundant_proteins, r_msg.format(acc)
            
            self._in_case_prot(acc, _prot_unique)
            
        for acc, pepts in data.peptides:
            _unique = []
            for seq  in pepts:
                self._peptides_store(acc, seq, _unique )
        self._sources_store(data)

    def _sources_store(self, data):
        """
        To store object parsed

        :param data: seq analyzed
        """
        self.sources.append(encode(str(data), 'utf-8'))
        
    def _in_case_prot(self, acc_key, _unique_prot):
        
        if not acc_key in _unique_prot:
            self.proteins[acc_key]+=1
            _unique_prot.append(acc_key)
            if self.proteins[acc_key] == 1:
                self.peptides[acc_key] = Counter()

    def _peptides_store(self, acc, seq_pep, _unique):
        """
        This method is used to storage peptides seq

        It's possible don't count peptides as unique for seq set
        switch spectral_count on True!

        :param acc: protein accession
        :param seq_pep: peptide sequence
        :type seq_pep: str
        :param _unique: list of seen peptides
        :type _unique: list
        """
        bad_seq_msg = "{0} is not a standard peptide"
        if not self.peptide_format.match(seq_pep):
            raise bad_format_peptide, bad_seq_msg.format(seq_pep)
        
        if not self.spectral_count and (acc, seq_pep) in _unique:
            pass
        
        elif not self.spectral_count and not (acc, seq_pep) in _unique:
            _unique.append((acc, seq_pep))
            self.peptides[acc][seq_pep] += 1
        
        elif self.spectral_count:
            self.peptides[acc][seq_pep] += 1
            
            
            

    def get_peptides_list(self):
        """
        to get the peptides

        >>> p = parser()
        >>> class seq():
        ...     pass
        >>> data1 = seq()
        >>> data1.proteins = ['acc1','acc2']
        >>> data1.peptides = [('acc1',['SEQONE', 'SEQTWO','SEQTHREE']),
        ...                   ('acc2',['SEQONE', 'SEQTWO',])]
        >>> p.parse(data1)
        >>> p.get_peptides_list()
        ['SEQONE', 'SEQTHREE', 'SEQTWO']
        >>> data2 = seq()
        >>> data2.proteins = ['acc1','acc3']
        >>> data2.peptides = [('acc1',['SEQONE', 'SEQTWO']),
        ...                   ('acc3',['SEQFIVE', 'SEQSIX'])]
        >>> p.parse(data2)
        >>> p.get_peptides_list()
        ['SEQFIVE', 'SEQONE', 'SEQSIX', 'SEQTHREE', 'SEQTWO']

        
        :return: the list of singles peptides
        :rtype: list
        """
        total = []
#        for acc, pepts in self.peptides.iteritems():
#            total.extend(pepts.keys())
        for pepts in self.peptides.values():
            total.extend(pepts.keys())
        result = list(set(total))
        #n = len
        result.sort()
        return result

    def __str__(self):
        """
        casting to string value

        >>> p = parser()
        >>> class seq():
        ...     pass
        >>> data1 = seq()
        >>> data1.proteins = ['acc1','acc2']
        >>> data1.peptides = [('acc1',['SEQONE', 'SEQTWO','SEQTHREE']),
        ...                   ('acc2',['SEQONE', 'SEQTWO',])]
        >>> p.parse(data1)
        >>> print p # doctest: +NORMALIZE_WHITESPACE
        Spectral_count: False
        accession   freq_prot       sequence        freq_pept
        acc1        1       SEQONE  1
        acc1        1       SEQTHREE        1
        acc1        1       SEQTWO  1
        acc2        1       SEQONE  1
        acc2        1       SEQTWO  1
        <BLANKLINE>
        >>> data2 = seq()
        >>> data2.proteins = ['acc1','acc3']
        >>> data2.peptides = [('acc1',['SEQONE', 'SEQTWO']),
        ...                   ('acc3',['SEQFIVE', 'SEQSIX'])]
        >>> p.parse(data2)
        >>> print p # doctest: +NORMALIZE_WHITESPACE
        Spectral_count: False
        accession   freq_prot       sequence        freq_pept
        acc1        2       SEQONE  2
        acc1        2       SEQTHREE        1
        acc1        2       SEQTWO  2
        acc2        1       SEQONE  1
        acc2        1       SEQTWO  1
        acc3        1       SEQFIVE 1
        acc3        1       SEQSIX  1
        <BLANKLINE>

        :return: the frequencies table
        :rtype: str
        """
        res_list = ["Spectral_count: {0}".format(self.spectral_count),
                    "accession\tfreq_prot\tsequence\tfreq_pept"]
        accs = self.peptides.keys()
        accs.sort()
        for acc in accs:
            pepts = self.peptides[acc]
            seqs = pepts.keys()
            seqs.sort()
            for seq in seqs:
                res_list.append("{0}\t{1}\t{2}\t{3}".format(acc, 
                                    self.proteins[acc], seq, pepts[seq]))
        return '\n'.join(res_list)

    def peptide_csv(self, filename):
        """
        Writes csv file containing peptides and proteins frequencies
        
        >>> p = parser()
        >>> class seq():
        ...     pass
        >>> data1 = seq()
        >>> data1.proteins = ['acc1','acc2']
        >>> data1.peptides = [('acc1',['SEQONE', 'SEQTWO','SEQTHREE']),
        ...                   ('acc2',['SEQONE', 'SEQTWO',])]
        >>> p.parse(data1)
        >>> data2 = seq()
        >>> data2.proteins = ['acc1','acc3']
        >>> data2.peptides = [('acc1',['SEQONE', 'SEQTWO']),
        ...                   ('acc3',['SEQFIVE', 'SEQSIX'])]
        >>> p.parse(data2)
        >>> p.peptide_csv('output.csv')
        >>> import csv
        >>> handle = csv.reader(open('output.csv'))
        >>> for row in handle:
        ...     print ', '.join(row) 
        Protein, #Protein, fProtein, Peptide, #Peptide, fPeptide
        acc1, 2, 1.0, SEQONE, 2, 1.0
        acc1, 2, 1.0, SEQTHREE, 1, 0.5
        acc1, 2, 1.0, SEQTWO, 2, 1.0
        acc2, 1, 0.5, SEQONE, 1, 1.0
        acc2, 1, 0.5, SEQTWO, 1, 1.0
        acc3, 1, 0.5, SEQFIVE, 1, 1.0
        acc3, 1, 0.5, SEQSIX, 1, 1.0

        :param filename: output file
        :type outdir: file
        """
        handle_pep = csv.writer(open(filename, 'wb'))
        handle_pep.writerow(["Protein", "#Protein",
                             "fProtein", "Peptide",
                             "#Peptide", "fPeptide"])

        n = len(self.sources)
        accs = self.peptides.keys()
        accs.sort()
        for acc in accs:
            prt_occ = self.proteins[acc]
            rProt = 1.*prt_occ/n
            seqs = self.peptides[acc].keys()
            seqs.sort()
            for seq in seqs:
                pept_occ = self.peptides[acc][seq]
                rPept = 1.* pept_occ/prt_occ
                handle_pep.writerow([acc, prt_occ, rProt, seq, pept_occ, rPept])

    def parser2arrays(self):
        """
        converts to frequencies arrays

        >>> p = parser()
        >>> class seq():
        ...     pass
        >>> data1 = seq()
        >>> data1.proteins = ['acc1','acc2']
        >>> data1.peptides = [('acc1',['SEQONE', 'SEQTWO','SEQTHREE']),
        ...                   ('acc2',['SEQONE', 'SEQTWO',])]
        >>> p.parse(data1)
        >>> data2 = seq()
        >>> data2.proteins = ['acc1','acc3']
        >>> data2.peptides = [('acc1',['SEQONE', 'SEQTWO']),
        ...                   ('acc3',['SEQFIVE', 'SEQSIX'])]
        >>> p.parse(data2)
        >>> p.parser2arrays()
        ([1.0, 0.5, 0.5], [1.0, 1.0, 0.5, 1.0, 1.0, 1.0, 1.0])

        :return: two array for proteins and peptides frequencies
        """
        prots = []
        pepts = []
        n_files = len(self.sources)
        for k,v in self.proteins.iteritems():
            prots.append(v/float(n_files))
            for p in self.peptides[k].values():
                freq = p/float(v)
                pepts.append(freq)
        return prots, pepts

    def frequencyMatrix(self):
        """
        converts a parser to a matrix of frequency
        For each couple of frequencies (protein, peptide),
        it computes a many times this pair of values appears

        >>> p = parser()
        >>> class seq():
        ...     pass
        >>> data1 = seq()
        >>> data1.proteins = ['acc1','acc2']
        >>> data1.peptides = [('acc1',['SEQONE', 'SEQTWO','SEQTHREE']),
        ...                   ('acc2',['SEQONE', 'SEQTWO',])]
        >>> p.parse(data1)
        >>> data2 = seq()
        >>> data2.proteins = ['acc1','acc3']
        >>> data2.peptides = [('acc1',['SEQONE', 'SEQTWO']),
        ...                   ('acc3',['SEQFIVE', 'SEQSIX'])]
        >>> p.parse(data2)
        >>> p.frequencyMatrix()
        [[0.5, 1.0, 1.0], [1.0, 0.5, 1.0], [4, 1, 2]]

        :return: the matrix of frequencies
        """
        n_files = len(self.sources)
        xyz = {}
        # Using a dictionary to count the frequencies
        for acc, prot_occ in self.proteins.iteritems():
            f1 = prot_occ/float(n_files)
            for pept_occ in self.peptides[acc].values():
                f2 = pept_occ/float(prot_occ)
                if xyz.has_key((f1, f2)):
                    xyz[(f1, f2)]+=1
                else:
                    xyz[(f1, f2)]=1
        # Reverting the dictionary to a matrix
        x = []
        y = []
        z = []
        for k2,v2 in xyz.iteritems():
            x.append(k2[0])
            y.append(k2[1])
            z.append(v2)
        return [x, y, z]

class selected(parser):
    """
    Using to select best results for a parse object
    or a derivative

    >>> p = parser()
    >>> class seq():
    ...     pass
    >>> data1 = seq()
    >>> data1.proteins = ['acc1','acc2']
    >>> data1.peptides = [('acc1',['SEQONE', 'SEQTWO','SEQTHREE']),
    ...                   ('acc2',['SEQONE', 'SEQTWO',])]
    >>> p.parse(data1)
    >>> data2 = seq()
    >>> data2.proteins = ['acc1','acc3']
    >>> data2.peptides = [('acc1',['SEQONE', 'SEQTWO']),
    ...                   ('acc3',['SEQFIVE', 'SEQSIX'])]
    >>> p.parse(data2)
    >>> p_2 = selected(p, peptThr=1., protThr=1.)
    >>> p_2.get_peptides_list()
    ['SEQONE', 'SEQTWO']
    >>> print p_2 # doctest: +NORMALIZE_WHITESPACE
    Spectral_count: False
    accession   freq_prot       sequence        freq_pept
    acc1        2       SEQONE  2
    acc1        2       SEQTWO  2
    
    :ivar peptThr: threshold to select peptides by frequencies
    :type peptThr: float
    :ivar protThr: threshold to select proteins by frequencies
    :type protThr: float
    """
    def __init__(self, pars, peptThr=0.3, protThr=0.5):
        """
        Initialize a selected object

        :param pars: a parser object used to select its seq
        """
        parser.__init__(self)
        self.spectral_count=pars.spectral_count
        self.peptThr = peptThr
        self.protThr = protThr
        self._select(pars)

    def _select(self, pars):
        """
        selects protein and peptides by frequencies using the two 
        threshold values peptThr and protThr

        :param pars: a parser object used to select its seq

        :raises protein_peptide_pair_over: if there are more than one proteins-peptides pairs
        """
        selectedProt = { }
        selectedPept= { }
        nfiles = len(pars.sources)
        for accession, prot_occurence in pars.proteins.iteritems():
            rProt = 1.*prot_occurence/nfiles
            if rProt >= self.protThr:
                selectedProt[accession] = prot_occurence
                selectedPept[accession] = { }
                for sequence, pept_occurence in pars.peptides[accession].iteritems():
                    rPep = 1.*pept_occurence/prot_occurence
                    if rPep >= self.peptThr :
                        if not selectedPept.has_key(accession):
                            selectedPept[accession] = { }
                        if not selectedPept[accession].has_key(sequence):
                            selectedPept[accession][sequence] = pept_occurence
                        else:
                            raise protein_peptide_pair_over,"It's impossible that are more than one accession-sequence pairs"
        self.sources = pars.sources
        self.peptides = selectedPept
        self.proteins = selectedProt

class sequest_parser(parser):
    """
    Containing features typical of sequest files xls either xml
    It is the base class for each parser for sequest software output files

    :cvar sequest_format: recognizes the peptide between cutting edges
    """
    sequest_format = re.compile(r"(?<=\A[A-Z-]{1}\.)[A-Z]+(?=\.[A-Z-]{1}\Z)")

    def _to_peptide(self, sequence):
        """
        Extracts from a sequest peptide sequence the peptide

        >>> sp = sequest_parser()
        >>> print sp._to_peptide("K.VFDEFKPLVEEPQNLIK.R")
        VFDEFKPLVEEPQNLIK

        :param sequence: the sequest peptide sequence
        :type sequence: str
        :return: exactly peptide, without dots notation
        :rtype: str
        :raises bad_format_peptide: If the sequence is not in dots notation
        """
        trips = self.sequest_format.findall(sequence)
        if trips:
            return trips[0]
        else:
            raise bad_format_peptide, "{0}".format(sequence)

class Parser_encoder(json.JSONEncoder):
    """
            Encoder from data_input.parser to dict

            >>> import json
            >>> p = parser()
            >>> class seq():
            ...     def __str__(self):
            ...         return self.name
            >>> data1 = seq()
            >>> data1.name = "data1"
            >>> data1.proteins = ['acc1','acc2']
            >>> data1.peptides = [('acc1',['SEQTWO']),
            ...                   ('acc2',['SEQONE'])]
            >>> p.parse(data1)
            >>> print json.dumps(obj=p, cls=Parser_encoder, indent=4) # doctest: +NORMALIZE_WHITESPACE
            {
                "sources": [
                    "data1"
                ],
                "spectral_count": false,
                "proteins": {
                    "acc1": 1,
                    "acc2": 1
                },
                "peptides": {
                    "acc1": {
                        "SEQTWO": 1
                    },
                    "acc2": {
                        "SEQONE": 1
                    }
                }
            }
    """

    def default(self, obj):
        """
        :param obj: a data_input.parser object
        """
        if isinstance(obj, parser):
            result = obj.__dict__
            return result
        return json.JSONEncoder.default(self, obj)

def as_parser(dictio):
    """
    Decode a dictionary to a data_input.parser or raises an error

    >>> d = {'spectral_count': False,
    ...     'sources': ['d1', 'd2'],
    ...     'proteins': {'acc1': 3, 'acc2': 1},
    ...     'peptides': {'acc1': {'SEQTWO': 3}, 'acc2': {'SEQONE': 1}}}
    >>> print as_parser(d) # doctest: +NORMALIZE_WHITESPACE
    Spectral_count: False
    accession	freq_prot	sequence	freq_pept
    acc1	3	SEQTWO	3
    acc2	1	SEQONE	1
    <BLANKLINE>

    :param dictio: dictonary to decode
    :raises DecodeError: if the dictonary doesn't have the names of keys equal to data_input.parser object name
    """
    keys = dictio.keys()
    keys.sort()
    if  keys == ['peptides', 'proteins', 'sources', 'spectral_count']:
        result = parser()
        result.spectral_count = dictio["spectral_count"]
        result.proteins = dictio["proteins"]
        result.peptides = dictio["peptides"]
        result.sources = dictio["sources"]
        return result
    else:
        raise DecodeError, "the dictionary cannot be converted in a data_input.parser instance"

def as_selected(dictio):
    """
    Decode a dictionary to a selected data_input.parser or raises an error

    >>> d = {'spectral_count': False,
    ...     'sources': ['d1', 'd2'],
    ...     'proteins': {'acc1': 3, 'acc2': 1},
    ...     'peptides': {'acc1': {'SEQTWO': 3}, 'acc2': {'SEQONE': 1}},
    ...     'peptThr':.5, 'protThr':.5}
    >>> print as_selected(d) # doctest: +NORMALIZE_WHITESPACE
    Spectral_count: False
    accession   freq_prot       sequence        freq_pept
    acc1        3       SEQTWO  3
    acc2        1       SEQONE  1
    <BLANKLINE>

    :param dictio: dictonary to decode
    :raises DecodeError: if the dictonary doesn't have the names of keys equal to data_input.parser object name
    """
    keys = dictio.keys()
    keys.sort()
    if  keys == ['peptThr', 'peptides', 'protThr', 'proteins', 'sources', 'spectral_count']:
        pars = parser()
        result = selected(pars)
        result.spectral_count = dictio["spectral_count"]
        result.proteins = dictio["proteins"]
        result.peptides = dictio["peptides"]
        result.sources = dictio["sources"]
        result.peptThr = dictio["peptThr"]
        result.protThr = dictio["protThr"]
        return result
    else:
        raise DecodeError, "the dictionary cannot be converted in a selected instance"

if __name__ == "__main__":
    import doctest
    doctest.testmod()


