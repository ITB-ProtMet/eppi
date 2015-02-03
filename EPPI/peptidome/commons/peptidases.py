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


""" Tools to digest peptides  """

__authors__ = "Pietro Brunetti"

import re

import aa
import Param_dummy
import Param
#import ParamData

mi_mw = Param_dummy.mi_mw
mi_mw_c = Param.mi_mw

no_enz = re.compile(r"[A-Z]")

tryp_simp_pro = re.compile(r"([A-Z]*?[KR])|((?<=[KR])[A-Z]*?$)")

# Refer to http://www.expasy.org/tools/peptidecutter/peptidecutter_enzymes.html#Tryps
_trypsin_rules_pro = [r"([A-Z]*?[KR](?!P))",
                      r"((?<=[KR])[A-NQ-Y][A-Z]*?$)"
                      r"(([A-Z]*?)WK(?=P))",
                      r"(([A-Z]*?)MR(?=P))"]
trypsin_pro = re.compile('|'.join(_trypsin_rules_pro))

proteinase_k_pro = re.compile( r"[A-Z]*?[AVLIGFYW]" )

_pepsin_simple_rules_pro = [r"[A-Z]*?[FYWL]",
                            r"[A-Z]*?(?=[FYWL])"]
pepsin_simple_pro = re.compile('|'.join(_pepsin_simple_rules_pro))

revDict = \
    {
        tryp_simp_pro: "trypsin",
        trypsin_pro: "tryp_simp",
        proteinase_k_pro: "proteinase_k",
        pepsin_simple_pro: "pepsin_simple",
    }

int2enz =\
    {
        0: no_enz,
        1: tryp_simp_pro,
        2: trypsin_pro,
        3: pepsin_simple_pro,
        4: proteinase_k_pro
    }

int2enz_name = \
    {
        0: "no enzyme",
        1: "trypsin simple rule",
        2: "trypsin complex rule",
        3: "pepsin",
        4: "proteinase"
    }

class PeptidaseError(Exception):
    """ base class for fasta_indx PARSER class """
    pass

class More(PeptidaseError):
    """ Error occurred when a sequence is
    longer or weighter than max limits"""
    pass

class Less(PeptidaseError):
    """ Error occurred when a peptide is
    shortless than minimum limits
    or less weight than mMW"""
    pass

class InvalidValue(PeptidaseError):
    """ Error occurred when insert in functions
    an invalid value, like misscut less than zero"""
    pass


def _seed_ctrl_c(seq, start, mlen, s_len):
    #mass = Param.mi_mw
    ns_find = aa.find_noStandards

    end = start+mlen if start+mlen < s_len else s_len
    frag = seq[start: end]

    while True:
        try:
            mw = mi_mw_c(frag)
        except Param.wrongSequence:
            #print "_seed exceptS"
            start += ns_find(frag)+1
            end = start+mlen if start+mlen < s_len else s_len
            frag = seq[start: end]
        else: break
    return (start, end, mw)

def no_enz_digestion_c(seq, mlen=5, Mlen = 50, mMW = 400*10**5, MMW=6000*10**5):
    """
    generate all possible peptides from a protein

    >>> seq1 = 'RKMASLLK'
    >>> print '|'.join([each[0] for each in no_enz_digestion_c(seq1)])
    RKMAS|RKMASL|RKMASLL|RKMASLLK|KMASL|KMASLL|KMASLLK|MASLL|MASLLK|ASLLK

    """
    no_nl = seq.replace('\n','')
    s_len = len(no_nl)

    start = 0

    while True:
        real_term = start+Mlen if start+Mlen < s_len else s_len
        start, end, mw = _seed_ctrl_c(no_nl, start, mlen, real_term)
        #print start, end, mw
        if s_len-start < mlen:
            break

        while True:
            #print no_nl[start:end]
            break_condition = (mw > MMW) or (end > real_term)
            #print (mw > MMW), (end > real_term)
            #print end, real_term
            if break_condition:
                break
            if mw >= mMW:# and not break_condition:
                yield(no_nl[start:end], mw)


            end += 1
            try:
                mw = mi_mw_c(no_nl[start:end])
            except Param.wrongSequence:
                 break
        start += 1




def _digestion_pro(seq, enzyme, enzyme_exception=None):

    #l_seq = seq.splitlines()
    #seq = ''.join(l_seq)
    no_nl = seq.replace('\n','')
    #enzyme = re.compile(enzyme_pattern)

    if not enzyme_exception:
        for each in enzyme.finditer(no_nl):
            yield each.group()
    else:
        exception = re.compile(enzyme_exception)
        for each in enzyme.finditer(no_nl):
            if not exception.match(each):
                yield each.group()

def _seq_conditions(seq, minlimit, maxlimit, mMW, MMW):

    l = len(seq)

    if l > maxlimit:
        raise More
    elif l < minlimit:
        raise Less
    else:
        mw = mi_mw_c(seq)
        if mw > MMW:
            raise More
        elif mw < mMW:
            raise Less
    return(seq, mw)


def _join_atoms(atoms, minlimit, maxlimit, mMW, MMW):
    i = 1
    while i <= len(atoms):
        frag = ("".join(atoms[:i]))
        try:
            res = _seq_conditions(frag, minlimit, maxlimit, mMW, MMW)
        except(More):
            break
        except(Param.wrongSequence):
            break
        except Less:
            pass

        else:
            yield res
        finally:
            i += 1

def real_digestion_pro(seq, enzyme_pattern=tryp_simp_pro,
                       enzyme_exception=None, miscut=0,
                       minlimit=5, maxlimit=50,
                       mMW=400*10**5, MMW=6000*10**5):
    """
    for digestion using enzyne and size limits.
    It's also present a miss-cleavage factor

    >>> seq1 = '''RKMASLLKVDQEVKLKPVDSFRERI
    ... TSEAEDLXVANFFPKKLLELDSFLKEPILNIHWKPDLTQID'''
    >>> frm1 = '^^     ^     ^ ^!    ^ ^               ^^        ^       !^!      '
    >>> print '|'.join([each[0] for each in real_digestion_pro(seq1)])
    MASLLK|VDQEVK|PVDSFR|LLELDSFLK|EPILNIHWK|PDLTQID

    """

    # This part is used to make degenarating peptides.
    digestion = _digestion_pro

    if miscut == 0:
        conditions = _seq_conditions
        for atom in digestion(seq, enzyme_pattern, enzyme_exception):
            try:
                yield(conditions(atom, minlimit, maxlimit, mMW, MMW))
            except (More, Param.wrongSequence, Less):
                pass

    elif miscut > 0:

        join_atoms = _join_atoms

        atoms = []
        i = 0
        it = digestion(seq, enzyme_pattern, enzyme_exception)

        # start - the seed
        while i <= miscut:
            atom = it.next()
            atoms.append(atom)
            i += 1

        # now ... rock and roll
        for atom in it:
            for each in join_atoms(atoms, minlimit, maxlimit, mMW, MMW):
                yield each
            atoms = atoms[1:]
            atoms.append(atom)

        # end cycle for the last atoms
        i = 0
        while i <= miscut:
            for each in join_atoms(atoms[i:], minlimit, maxlimit, mMW, MMW):
                yield each
            i += 1

    elif miscut < 0:
        raise InvalidValue, "Miscut must be equal or greater than zero"

if __name__ == "__main__":
    seq_ex =''.join([
              "MPQRHHQGHKRTPKQLALIIKRCLPMVLTGSGMLCTTANAEEYYFDPIMLETTKSGMQTTDLSRFSKKYA",
              "QLPGTYQVDIWLNKKKVSQKKITFTANAEQLLQPQFTVEQLRELGIKVDEIPALAEKDDDSVINSLEQII",
              "PGTAAEFDFNHQQLNLSIPQIALYRDARGYVSPSRWDDGIPTLFTNYSFTGSDNRYRQGNRSQRQYLNMQ",
              "NGANFGPWRLRNYSTWTRNDQTSSWNTISSYLQRDIKALKSQLLLGESATSGSIFSSYTFTGVQLASDDN",
              "MLPNSQRGFAPTVRGIANSSAIVTIRQNGYVIYQSNVSAGAFEINDLYPSSNSGDLEVTIEESDGTQRRF",
              "IQPYSSLPMMQRPGHLKYSATAGRYRADANSDSKEPEFAEATAIYGLNNTFTLYGGLLGSEDYYALGIGI",
              "GGTLGALGALSMDINRADTQFDNQHSFHGYQWRTQYIKDIPETNTNIAVSYYRYTNDGYFSFNEANTRNW",
              "DYNSRQKSEIQFNISQTIFDGVSLYASGSQQDYWGNNDKNRNISVGVSGQQWGVGYSLNYQYSRYTDQNN",
              "DRALSLNLSIPLERWLPRSRVSYQMTSQKDRPTQHEMRLDGSLLDDGRLSYSLEQSLDDDNNHNSSLNAS",
              "YRSPYGTFSAGYSYGNDSSQYNYGVTGGVVIHPHGVTLSQYLGNAFALIDANGASGVRIQNYPGIATDPF",
              "GYAVVPYLTTYQENRLSVDTTQLPDNVDLEQTTQFVVPNRGAMVAARFNANIGYRVLVTVSDRNGKPLPF",
              "GALASNDDTGQQSIVDEGGILYLSGISSKSQSWTVRWGNQADQQCQFAFSTPDSEPTTSVLQGTAQCH",])
    print list(no_enz_digestion_c(seq_ex,
                                  mlen=19, Mlen = 64,
                                  mMW = 365882591, MMW=365882591))
