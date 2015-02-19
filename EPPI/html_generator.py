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
Write html pages for EPPI, using template library.
It's works clean!
"""

__authors__ = "Pietro Brunetti"

import peptidome.commons.Param as Param
import peptidome.commons.peptidases as peptidases
from peptidome import fasta_indx
from peptidome.commons import reporting

import textwrap
# used on template file version
# from jinja2 import Environment, PackageLoader
# env = Environment(loader=PackageLoader('EPPI', 'templates'))
# used in stand-alone version
from jinja2 import Template

def Summary(fileDB, t="EPPI project report"):
    """
    Writing a html file
    A summary of the project
    """
    # used on template file version
    # templ = env.get_template('resume.html')
    # used in stand-alone version
    templ = Template(summary)
    return str(templ.render(_get_data(fileDB, t)))

def Protein(reference, fileDB, title="EPPI protein report"):
    """
    Writing a html file
    to resume a protein
    """
    # used on template file version
    # templ = env.get_template('proteinReport.html')
    # used in stand-alone version
    templ = Template(proteinReport)
    return str(templ.render(_proteinQuery(reference, fileDB, title)))

def Peptide(sequence, fileDB,  title="EPPI peptide report"):
    """
    Writing a html file
    to resume a peptide
    """

    # used on template file version
    # templ = env.get_template('peptideReport.html')
    # return  str(templ.render(_peptideQuery(sequence, fileDB, title))

    # used in stand-alone version
    templ = Template(peptideReport)
    return str(templ.render(_peptideQuery(sequence, fileDB, title)))

def _get_data(fileDB, title):
    """
    Generate the search list
    """
    name = fileDB.get_project_name()
    data = []

    try:
        enz_code = fileDB["enzyme"]
    except KeyError:
        pass
    else:
        enzyme = peptidases.int2enz_name[enz_code]
        data.append(("enzyme: ", enzyme))

    try:
        data.append(("misscut: ",
                     fileDB["miscut"]))
    except KeyError:
        pass

    try:
        data.append(("Fasta file used: ",
                     fileDB['proteome']['fasta_path']))
    except KeyError:
        pass

    try:
        data.append(("Number of lists: ",
                     len(fileDB['p_sources'])))
    except KeyError:
        pass

    try:
        data.append(("Number of proteins: ",
                     len(fileDB['p_proteins'])))
    except KeyError:
        pass

    try:
        data.append(("Number of peptides: ",
                     len(fileDB.get_parser().get_peptides_list())))
    except KeyError:
        pass

    try:
        data.append(("Number of best proteins: ",
                     len(fileDB['s_proteins'])))
    except KeyError:
        pass

    try:
        data.append(("Protein frequency threshold: ",
                     fileDB["s_protThr"]))
    except KeyError:
        pass

    try:
        data.append(("Peptide frequency threshold: ",
                     fileDB["s_peptThr"]))
    except KeyError:
        pass

    try:
        data.append(("Delta mass: ",
                     "{0}Da".format(fileDB["delta"]*(10**-5))))
    except KeyError:
        pass

    try:
        data.append(("Number of best peptides: ",
                    len(fileDB.get_selected().get_peptides_list())))
    except KeyError:
        pass

    #_createOtherRows(fileDB, data)
    nameSpace = {'title': title, 'head': name, 'data': data}
    return nameSpace

def _proteinQuery(accession, fileDB, title):
    """
    Generate namespace
    """
    try:
        #fasta = fasta_indx.Saf(fileDB["fasta"])
        fasta = fasta_indx.Saf(proteome=fileDB["proteome"]["indx"])
        fasta.fasta_path = fileDB["proteome"]["fasta_path"]
    except fasta_indx.WrongFile:
        reporting.echo_error("{0} not found.".format(fileDB["proteome"]["fasta_path"]), True)
    except fasta_indx.WrongReference, e:
        reporting.echo_error("{0}".format(str(e)), True)
    try:
        seq = textwrap.fill(fasta.get_sequence(accession))
        des = fasta.get_reference(accession)
    except:
        seq, des = (None, None)

    try:
        prot_num = fileDB.get_parser().proteins[accession]
    except KeyError:
        prot_num = None

    try:
        pepts = fileDB.get_parser().peptides[accession]
    except KeyError:
        pepts = None

    nameSpace = {'title': title, 'sequence': seq, 'description': des,
                 'reference': accession, 'protein': prot_num,
                 'peptides': pepts}
    return nameSpace

def _data_format(results, fileDB):
    """
    Formatting results of a query
    """
    for p in results:
        accession = unicode(p[0])
        try:
            prot_num = fileDB.get_parser().proteins[accession]
        except KeyError:
            prot_num = 'NA'
        try:
            pepts = fileDB.get_parser().peptides[accession]
        except KeyError:
            pepts = None
        datum = (p[0], p[3], p[1],
                 p[2], prot_num, pepts)
        yield datum


def _peptideQuery(sequence,  fileDB, title):
    """ Writing a peptide report """

    mw_ori = Param.mi_mw(str(sequence))
    try:
        fst_i = fasta_indx.Saf(proteome=fileDB["proteome"]["indx"])
        fst_i.fasta_path = fileDB["proteome"]["fasta_path"]
    except fasta_indx.WrongFile:
        reporting.echo_error("{0} not found.".format(fileDB["proteome"]["fasta_path"]), True)
    except fasta_indx.WrongReference, e:
        reporting.echo_error("{0}".format(str(e)), True)

    #for sequence
    data_seq = _data_format(fst_i.search_by_sequence(str(sequence), window=True), fileDB)
 #for weight
    if "delta" in fileDB.keys():
        d = fileDB["delta"]
    else:
        d = 800
    if "enzyme" in fileDB.keys():
        enz_code = fileDB["enzyme"]
        e = peptidases.int2enz[enz_code]
    else:
        e = peptidases.tryp_simp_pro
    if "enzyme_exception" in fileDB.keys():
        e_exc = fileDB["enzyme_exception"]
    else:
        e_exc = None
    if "miscut" in fileDB.keys():
        mc = fileDB["miscut"]
    else:
        mc = 2

    data_mw = _data_format(fst_i.search_by_mw(mw_ori, e, e_exc, mc, d, window=True), fileDB)

    nameSpace = {'title': title, 'sequence': sequence,
                 'mw': mw_ori*10**(-5), 'delta': d*10**(-5),
                 'results_seq': data_seq, 'results_mw': data_mw}
    return nameSpace


summary = """
<HTML>
  <HEAD>
    <TITLE>{{title}}</TITLE>
  </HEAD>
  <BODY>
    <CENTER>
      <TABLE bgcolor=blue width="100%%" cellspacing="0" cellpadding="0" border="1">
        <TR>
          <TD align="center">
            <H1 style="font-family:verdana">{{head}}</H1>
          </TD>
        </TR>
     </TABLE>
    </CENTER>
    <TABLE border="0" cellspacing="10">
    {% for d in data %}
      <TR>
        <TD align="left"><B>{{ d[0] }}</B></TD> <TD align="right"> {{ d[1] }}</TD>
      </TR>
    {% endfor  %}
    </TABLE>
  </BODY>
</HTML>"""

peptideReport = """
<HTML>
  <HEAD>
    <TITLE>{{ title }}</TITLE>
  </HEAD>
  <BODY>
    <CENTER>
      <TABLE bgcolor=blue width="100%%" cellspacing="0" cellpadding="0" border="1">
        <TR>
          <TD align="center"> 
            <H1 style="font-family:verdana">{{ sequence }} : {{ mw }} kDa</H1>
          </TD>
        </TR>
      </TABLE>
    </CENTER>
    <BR />
{% if results_seq  %}
    <H2>
      Peptides found by sequence matching
    </H2>
    {{ sequence }}
    <TABLE border="1">
      <TR>
        <TH>Accession</TH>
        <TH>Description</TH>
        <TH>Sequence</TH>
        <TH>Molecular Weight</TH>
        <TH>Occurrence</TH>
        <TH>Peptides Found</TH>
      </TR>
{% for p in results_seq %}
      <TR>
        <TD><STRONG> {{ p[0] }} </STRONG></TD>
        <TD><I> {{ p[1] }} </I></TD>
        <TD><PRE> {{ p[2] }} </PRE></TD>
        <TD><PRE> {{ p[3] }}KDa </PRE></TD>
        <TD> {{ p[4] }} </TD>
{% if p[5] %}
        <TD>
          <TABLE border="0">
{% for each in p[5].iteritems() %}
            <TR>
              <TD><PRE> {{ each[0] }} </PRE></TD>
              <TD><B> {{ each[1] }} </B></TD>
            </TR>
{% endfor %}
          </TABLE>
        </TD>
{% else %}
        <TD> No Found </TD>
{% endif %}
{% endfor %}
    </TABLE>
{% else %}
    <BIG>Peptide no found!</BIG>
{% endif %}
{% if results_mw %}
    <H2>
      Peptides found by Molecular Weigth matching
    </H2>
        {{ sequence }} : {{ mw }}kDa (d = {{ delta }}kDa)
     <TABLE border="1">
      <TR>
        <TH>Accession</TH>
        <TH>Description</TH>
        <TH>Sequence</TH>
        <TH>Molecular Weight</TH>
        <TH>Occurrence</TH>
        <TH>Peptides Found</TH>
      </TR>
{% for p in results_mw %}
       <TR>
        <TD><STRONG> {{ p[0] }} </STRONG></TD>
        <TD><I> {{ p[1] }} </I></TD>
        <TD><PRE> {{ p[2] }} </PRE></TD>
        <TD><PRE> {{ p[3] }}KDa </PRE></TD>
        <TD> {{ p[4] }} </TD>
{% if p[5] %}
        <TD>
          <TABLE border="0">
{% for each in p[5].iteritems() %}
            <TR>
              <TD><PRE> {{ each[0] }} </PRE></TD>
              <TD><B> {{ each[1] }} </B></TD>
            </TR>
{% endfor %}
          </TABLE>
        </TD>
{% else %}
        <TD> No Found </TD>
{% endif %}
{% endfor %}
    </TABLE>
{% else %}
    <BIG>Peptide no found!</BIG>
{% endif %}
  </BODY>
</HTML>
"""

proteinReport = """
<HTML>
  <HEAD>
    <TITLE>{{ title }}</TITLE>
  </HEAD>
  <BODY>
    <CENTER>
      <TABLE bgcolor=blue width="100%%" cellspacing="0" cellpadding="0" border="1">
         <TR>
{% if sequence and description %}
           <TD align="center"><H1 style="font-family:verdana">{{ reference }}</H1></TD>
           <TD align="center"><H2 style="font-family:times">{{ description  }}</H2></TD>
         </TR>
       </TABLE>
     </CENTER>
     <P>
       <B>Sequence:</B><BR />
       <PRE>{{ sequence }}</PRE><HR />
     </P>
{% else %}
           <TD align="center"><H1>{{ reference }}</H1></TD>
         </TR>
       </TABLE>
     </CENTER>
{% endif %}
{% if protein %}
      <P><B>Protein Occurence: </B>{{ protein }}</P><HR />
{% if peptides %}
      <B>Peptides found: </B><BR />
      <TABLE border="1">
        <TR>
          <TH><B>Sequence</B></TH>
          <TH><B>Occurence</B></TH>
        </TR>
{% for pept , occ in peptides.iteritems() %}
        <TR>
          <TH><PRE>{{ pept }}</PRE></TH>
          <TH>{{ occ }}</TH>
        </TR>
{% endfor %}
      </TABLE>
{% else %}
      <BIG>Peptide no found!</BIG>
{% endif %}
{% endif %}
  </BODY>
</HTML>    
"""
