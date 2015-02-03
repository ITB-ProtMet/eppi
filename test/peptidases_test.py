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

__author__ = 'Pietro Brunetti'

try:
    import unittest2 as unittest
except ImportError:
    import unittest
    
from EPPI.peptidome.commons import peptidases
from EPPI.peptidome.commons import Param
#import os

class Test_no_enzyme(unittest.TestCase):
     
    seq = "RKMASLLKVDQEVKLKPVDSFRERITSEAEDLVANFFPKKLLELDSFLKE"
    
    asp_results = [
    "RKMAS",
    "RKMASL",
    "RKMASLL",
    "RKMASLLK",
    "RKMASLLKV",
    "RKMASLLKVD",
    "RKMASLLKVDQ",
    "RKMASLLKVDQE",
    "RKMASLLKVDQEV",
    "RKMASLLKVDQEVK",
    "RKMASLLKVDQEVKL",
    "RKMASLLKVDQEVKLK",
    "RKMASLLKVDQEVKLKP",
    "RKMASLLKVDQEVKLKPV",
    "RKMASLLKVDQEVKLKPVD",
    "RKMASLLKVDQEVKLKPVDS",
    "RKMASLLKVDQEVKLKPVDSF",
    "RKMASLLKVDQEVKLKPVDSFR",
    "RKMASLLKVDQEVKLKPVDSFRE",
    "RKMASLLKVDQEVKLKPVDSFRER",
    "RKMASLLKVDQEVKLKPVDSFRERI",
    "RKMASLLKVDQEVKLKPVDSFRERIT",
    "RKMASLLKVDQEVKLKPVDSFRERITS",
    "RKMASLLKVDQEVKLKPVDSFRERITSE",
    "RKMASLLKVDQEVKLKPVDSFRERITSEA",
    "RKMASLLKVDQEVKLKPVDSFRERITSEAE",
    "RKMASLLKVDQEVKLKPVDSFRERITSEAED",
    "RKMASLLKVDQEVKLKPVDSFRERITSEAEDL",
    "RKMASLLKVDQEVKLKPVDSFRERITSEAEDLV",
    "RKMASLLKVDQEVKLKPVDSFRERITSEAEDLVA",
    "RKMASLLKVDQEVKLKPVDSFRERITSEAEDLVAN",
    "RKMASLLKVDQEVKLKPVDSFRERITSEAEDLVANF",
    "RKMASLLKVDQEVKLKPVDSFRERITSEAEDLVANFF",
    "RKMASLLKVDQEVKLKPVDSFRERITSEAEDLVANFFP",
    "RKMASLLKVDQEVKLKPVDSFRERITSEAEDLVANFFPK",
    "RKMASLLKVDQEVKLKPVDSFRERITSEAEDLVANFFPKK",
    "RKMASLLKVDQEVKLKPVDSFRERITSEAEDLVANFFPKKL",
    "RKMASLLKVDQEVKLKPVDSFRERITSEAEDLVANFFPKKLL",
    "RKMASLLKVDQEVKLKPVDSFRERITSEAEDLVANFFPKKLLE",
    "RKMASLLKVDQEVKLKPVDSFRERITSEAEDLVANFFPKKLLEL",
    "RKMASLLKVDQEVKLKPVDSFRERITSEAEDLVANFFPKKLLELD",
    "RKMASLLKVDQEVKLKPVDSFRERITSEAEDLVANFFPKKLLELDS",
    "RKMASLLKVDQEVKLKPVDSFRERITSEAEDLVANFFPKKLLELDSF",
    "RKMASLLKVDQEVKLKPVDSFRERITSEAEDLVANFFPKKLLELDSFL",
    "RKMASLLKVDQEVKLKPVDSFRERITSEAEDLVANFFPKKLLELDSFLK",
    "RKMASLLKVDQEVKLKPVDSFRERITSEAEDLVANFFPKKLLELDSFLKE",
    "KMASL",
    "KMASLL",
    "KMASLLK",
    "KMASLLKV",
    "KMASLLKVD",
    "KMASLLKVDQ",
    "KMASLLKVDQE",
    "KMASLLKVDQEV",
    "KMASLLKVDQEVK",
    "KMASLLKVDQEVKL",
    "KMASLLKVDQEVKLK",
    "KMASLLKVDQEVKLKP",
    "KMASLLKVDQEVKLKPV",
    "KMASLLKVDQEVKLKPVD",
    "KMASLLKVDQEVKLKPVDS",
    "KMASLLKVDQEVKLKPVDSF",
    "KMASLLKVDQEVKLKPVDSFR",
    "KMASLLKVDQEVKLKPVDSFRE",
    "KMASLLKVDQEVKLKPVDSFRER",
    "KMASLLKVDQEVKLKPVDSFRERI",
    "KMASLLKVDQEVKLKPVDSFRERIT",
    "KMASLLKVDQEVKLKPVDSFRERITS",
    "KMASLLKVDQEVKLKPVDSFRERITSE",
    "KMASLLKVDQEVKLKPVDSFRERITSEA",
    "KMASLLKVDQEVKLKPVDSFRERITSEAE",
    "KMASLLKVDQEVKLKPVDSFRERITSEAED",
    "KMASLLKVDQEVKLKPVDSFRERITSEAEDL",
    "KMASLLKVDQEVKLKPVDSFRERITSEAEDLV",
    "KMASLLKVDQEVKLKPVDSFRERITSEAEDLVA",
    "KMASLLKVDQEVKLKPVDSFRERITSEAEDLVAN",
    "KMASLLKVDQEVKLKPVDSFRERITSEAEDLVANF",
    "KMASLLKVDQEVKLKPVDSFRERITSEAEDLVANFF",
    "KMASLLKVDQEVKLKPVDSFRERITSEAEDLVANFFP",
    "KMASLLKVDQEVKLKPVDSFRERITSEAEDLVANFFPK",
    "KMASLLKVDQEVKLKPVDSFRERITSEAEDLVANFFPKK",
    "KMASLLKVDQEVKLKPVDSFRERITSEAEDLVANFFPKKL",
    "KMASLLKVDQEVKLKPVDSFRERITSEAEDLVANFFPKKLL",
    "KMASLLKVDQEVKLKPVDSFRERITSEAEDLVANFFPKKLLE",
    "KMASLLKVDQEVKLKPVDSFRERITSEAEDLVANFFPKKLLEL",
    "KMASLLKVDQEVKLKPVDSFRERITSEAEDLVANFFPKKLLELD",
    "KMASLLKVDQEVKLKPVDSFRERITSEAEDLVANFFPKKLLELDS",
    "KMASLLKVDQEVKLKPVDSFRERITSEAEDLVANFFPKKLLELDSF",
    "KMASLLKVDQEVKLKPVDSFRERITSEAEDLVANFFPKKLLELDSFL",
    "KMASLLKVDQEVKLKPVDSFRERITSEAEDLVANFFPKKLLELDSFLK",
    "KMASLLKVDQEVKLKPVDSFRERITSEAEDLVANFFPKKLLELDSFLKE"
    ]
    
    seq_no_std = "RKMXASLLKVDQEVKLKXPVDSFRERITSEAOEDLVANFFPKKLLELDSFLKE"
    #                ^             ^
    
    asp_results_no_std = [
#    "RKMAS",
#    "RKMASL",
#    "RKMASLL",
#    "RKMASLLK",
#    "RKMASLLKV",
#    "RKMASLLKVD",
#    "RKMASLLKVDQ",
#    "RKMASLLKVDQE",
#    "RKMASLLKVDQEV",
#    "RKMASLLKVDQEVK",
#    "RKMASLLKVDQEVKL",
#    "RKMASLLKVDQEVKLK",
#    "KMASL",
#    "KMASLL",
#    "KMASLLK",
#    "KMASLLKV",
#    "KMASLLKVD",
#    "KMASLLKVDQ",
#    "KMASLLKVDQE",
#    "KMASLLKVDQEV",
#    "KMASLLKVDQEVK",
#    "KMASLLKVDQEVKL",
#    "KMASLLKVDQEVKLK",
#    "MASLL",
#    "MASLLK",
#    "MASLLKV",
#    "MASLLKVD",
#    "MASLLKVDQ",
#    "MASLLKVDQE",
#    "MASLLKVDQEV",
#    "MASLLKVDQEVK",
#    "MASLLKVDQEVKL",
#    "MASLLKVDQEVKLK",
    "ASLLK",
    "ASLLKV",
    "ASLLKVD",
    "ASLLKVDQ",
    "ASLLKVDQE",
    "ASLLKVDQEV",
    "ASLLKVDQEVK",
    "ASLLKVDQEVKL",
    "ASLLKVDQEVKLK",
    "SLLKV",
    "SLLKVD",
    "SLLKVDQ",
    "SLLKVDQE",
    "SLLKVDQEV",
    "SLLKVDQEVK",
    "SLLKVDQEVKL",
    "SLLKVDQEVKLK",
    "LLKVD",
    "LLKVDQ",
    "LLKVDQE",
    "LLKVDQEV",
    "LLKVDQEVK",
    "LLKVDQEVKL",
    "LLKVDQEVKLK",
    "LKVDQ",
    "LKVDQE",
    "LKVDQEV",
    "LKVDQEVK",
    "LKVDQEVKL",
    "LKVDQEVKLK",
    "KVDQE",
    "KVDQEV",
    "KVDQEVK",
    "KVDQEVKL",
    "KVDQEVKLK",
    "VDQEV",
    "VDQEVK",
    "VDQEVKL",
    "VDQEVKLK",
    "DQEVK",
    "DQEVKL",
    "DQEVKLK",
    "QEVKL",
    "QEVKLK",
    "EVKLK",
    "PVDSF",
    "PVDSFR",
    "PVDSFRE",
    "PVDSFRER",
    "PVDSFRERI",
    "PVDSFRERIT",
    "PVDSFRERITS",
    "PVDSFRERITSE",
    "PVDSFRERITSEA",
    "VDSFR",
    "VDSFRE",
    "VDSFRER",
    "VDSFRERI",
    "VDSFRERIT",
    "VDSFRERITS",
    "VDSFRERITSE",
    "VDSFRERITSEA",
    "DSFRE",
    "DSFRER",
    "DSFRERI",
    "DSFRERIT",
    "DSFRERITS",
    "DSFRERITSE",
    "DSFRERITSEA",
    "SFRER",
    "SFRERI",
    "SFRERIT",
    "SFRERITS",
    "SFRERITSE",
    "SFRERITSEA",
    "FRERI",
    "FRERIT",
    "FRERITS",
    "FRERITSE",
    "FRERITSEA",
    "RERIT",
    "RERITS",
    "RERITSE",
    "RERITSEA",
    "ERITS",
    "ERITSE",
    "ERITSEA",
    "RITSE",
    "RITSEA",
    "ITSEA",
    "EDLVA",
    "EDLVAN",
    "EDLVANF",
    "EDLVANFF",
    "EDLVANFFP",
    "EDLVANFFPK",
    "EDLVANFFPKK",
    "EDLVANFFPKKL",
    "EDLVANFFPKKLL",
    "EDLVANFFPKKLLE",
    "EDLVANFFPKKLLEL",
    "EDLVANFFPKKLLELD",
    "EDLVANFFPKKLLELDS",
    "EDLVANFFPKKLLELDSF",
    "EDLVANFFPKKLLELDSFL",
    "EDLVANFFPKKLLELDSFLK",
    "EDLVANFFPKKLLELDSFLKE",
    "DLVAN",
    "DLVANF",
    "DLVANFF",
    "DLVANFFP",
    "DLVANFFPK",
    "DLVANFFPKK",
    "DLVANFFPKKL",
    "DLVANFFPKKLL",
    "DLVANFFPKKLLE",
    "DLVANFFPKKLLEL",
    "DLVANFFPKKLLELD",
    "DLVANFFPKKLLELDS",
    "DLVANFFPKKLLELDSF",
    "DLVANFFPKKLLELDSFL",
    "DLVANFFPKKLLELDSFLK",
    "DLVANFFPKKLLELDSFLKE",
    "LVANF",
    "LVANFF",
    "LVANFFP",
    "LVANFFPK",
    "LVANFFPKK",
    "LVANFFPKKL",
    "LVANFFPKKLL",
    "LVANFFPKKLLE",
    "LVANFFPKKLLEL",
    "LVANFFPKKLLELD",
    "LVANFFPKKLLELDS",
    "LVANFFPKKLLELDSF",
    "LVANFFPKKLLELDSFL",
    "LVANFFPKKLLELDSFLK",
    "LVANFFPKKLLELDSFLKE",
    "VANFF",
    "VANFFP",
    "VANFFPK",
    "VANFFPKK",
    "VANFFPKKL",
    "VANFFPKKLL",
    "VANFFPKKLLE",
    "VANFFPKKLLEL",
    "VANFFPKKLLELD",
    "VANFFPKKLLELDS",
    "VANFFPKKLLELDSF",
    "VANFFPKKLLELDSFL",
    "VANFFPKKLLELDSFLK",
    "VANFFPKKLLELDSFLKE",
    "ANFFP",
    "ANFFPK",
    "ANFFPKK",
    "ANFFPKKL",
    "ANFFPKKLL",
    "ANFFPKKLLE",
    "ANFFPKKLLEL",
    "ANFFPKKLLELD",
    "ANFFPKKLLELDS",
    "ANFFPKKLLELDSF",
    "ANFFPKKLLELDSFL",
    "ANFFPKKLLELDSFLK",
    "ANFFPKKLLELDSFLKE",
    "NFFPK",
    "NFFPKK",
    "NFFPKKL",
    "NFFPKKLL",
    "NFFPKKLLE",
    "NFFPKKLLEL",
    "NFFPKKLLELD",
    "NFFPKKLLELDS",
    "NFFPKKLLELDSF",
    "NFFPKKLLELDSFL",
    "NFFPKKLLELDSFLK",
    "NFFPKKLLELDSFLKE",
    "FFPKK",
    "FFPKKL",
    "FFPKKLL",
    "FFPKKLLE",
    "FFPKKLLEL",
    "FFPKKLLELD",
    "FFPKKLLELDS",
    "FFPKKLLELDSF",
    "FFPKKLLELDSFL",
    "FFPKKLLELDSFLK",
    "FFPKKLLELDSFLKE",
    "FPKKL",
    "FPKKLL",
    "FPKKLLE",
    "FPKKLLEL",
    "FPKKLLELD",
    "FPKKLLELDS",
    "FPKKLLELDSF",
    "FPKKLLELDSFL",
    "FPKKLLELDSFLK",
    "FPKKLLELDSFLKE",
    "PKKLL",
    "PKKLLE",
    "PKKLLEL",
    "PKKLLELD",
    "PKKLLELDS",
    "PKKLLELDSF",
    "PKKLLELDSFL",
    "PKKLLELDSFLK",
    "PKKLLELDSFLKE",
    "KKLLE",
    "KKLLEL",
    "KKLLELD",
    "KKLLELDS",
    "KKLLELDSF",
    "KKLLELDSFL",
    "KKLLELDSFLK",
    "KKLLELDSFLKE",
    "KLLEL",
    "KLLELD",
    "KLLELDS",
    "KLLELDSF",
    "KLLELDSFL",
    "KLLELDSFLK",
    "KLLELDSFLKE",
    "LLELD",
    "LLELDS",
    "LLELDSF",
    "LLELDSFL",
    "LLELDSFLK",
    "LLELDSFLKE",
    "LELDS",
    "LELDSF",
    "LELDSFL",
    "LELDSFLK",
    "LELDSFLKE",
    "ELDSF",
    "ELDSFL",
    "ELDSFLK",
    "ELDSFLKE",
    "LDSFL",
    "LDSFLK",
    "LDSFLKE",
    "DSFLK",
    "DSFLKE",
    "SFLKE"      
    ]
    
    seq_less_mw = "HVGGGGGGPKKLLWWWWWWYYYYYYPKKL"
    
    asp_results_less_mw = [
    "HVGGG",
    "HVGGGG",
    "HVGGGGG",
    "HVGGGGGG",
    "HVGGGGGGP",
    "HVGGGGGGPK",
    "HVGGGGGGPKK",
    "HVGGGGGGPKKL",
    "HVGGGGGGPKKLL",
    "HVGGGGGGPKKLLW",
    "HVGGGGGGPKKLLWW",
    "HVGGGGGGPKKLLWWW",
    "HVGGGGGGPKKLLWWWW",
    "HVGGGGGGPKKLLWWWWW",
    "HVGGGGGGPKKLLWWWWWW",
    "HVGGGGGGPKKLLWWWWWWY",
    "HVGGGGGGPKKLLWWWWWWYY",
    "HVGGGGGGPKKLLWWWWWWYYY",
    "HVGGGGGGPKKLLWWWWWWYYYY",
    "HVGGGGGGPKKLLWWWWWWYYYYY",
    "HVGGGGGGPKKLLWWWWWWYYYYYY",
    "HVGGGGGGPKKLLWWWWWWYYYYYYP",
    "HVGGGGGGPKKLLWWWWWWYYYYYYPK",
    "HVGGGGGGPKKLLWWWWWWYYYYYYPKK",
    "HVGGGGGGPKKLLWWWWWWYYYYYYPKKL",
   # "VGGGG",
    "VGGGGG",
    "VGGGGGG",
    "VGGGGGGP",
    "VGGGGGGPK",
    "VGGGGGGPKK",
    "VGGGGGGPKKL",
    "VGGGGGGPKKLL",
    "VGGGGGGPKKLLW",
    "VGGGGGGPKKLLWW",
    "VGGGGGGPKKLLWWW",
    "VGGGGGGPKKLLWWWW",
    "VGGGGGGPKKLLWWWWW",
    "VGGGGGGPKKLLWWWWWW",
    "VGGGGGGPKKLLWWWWWWY",
    "VGGGGGGPKKLLWWWWWWYY",
    "VGGGGGGPKKLLWWWWWWYYY",
    "VGGGGGGPKKLLWWWWWWYYYY",
    "VGGGGGGPKKLLWWWWWWYYYYY",
    "VGGGGGGPKKLLWWWWWWYYYYYY",
    "VGGGGGGPKKLLWWWWWWYYYYYYP",
    "VGGGGGGPKKLLWWWWWWYYYYYYPK",
    "VGGGGGGPKKLLWWWWWWYYYYYYPKK",
    "VGGGGGGPKKLLWWWWWWYYYYYYPKKL",
#    "GGGGG",
#    "GGGGGG",
    "GGGGGGP",
    "GGGGGGPK",
    "GGGGGGPKK",
    "GGGGGGPKKL",
    "GGGGGGPKKLL",
    "GGGGGGPKKLLW",
    "GGGGGGPKKLLWW",
    "GGGGGGPKKLLWWW",
    "GGGGGGPKKLLWWWW",
    "GGGGGGPKKLLWWWWW",
    "GGGGGGPKKLLWWWWWW",
    "GGGGGGPKKLLWWWWWWY",
    "GGGGGGPKKLLWWWWWWYY",
    "GGGGGGPKKLLWWWWWWYYY",
    "GGGGGGPKKLLWWWWWWYYYY",
    "GGGGGGPKKLLWWWWWWYYYYY",
    "GGGGGGPKKLLWWWWWWYYYYYY",
    "GGGGGGPKKLLWWWWWWYYYYYYP",
    "GGGGGGPKKLLWWWWWWYYYYYYPK",
    "GGGGGGPKKLLWWWWWWYYYYYYPKK",
    "GGGGGGPKKLLWWWWWWYYYYYYPKKL",
#    "GGGGG",
    "GGGGGP",
    "GGGGGPK",
    "GGGGGPKK",
    "GGGGGPKKL",
    "GGGGGPKKLL",
    "GGGGGPKKLLW",
    "GGGGGPKKLLWW",
    "GGGGGPKKLLWWW",
    "GGGGGPKKLLWWWW",
    "GGGGGPKKLLWWWWW",
    "GGGGGPKKLLWWWWWW",
    "GGGGGPKKLLWWWWWWY",
    "GGGGGPKKLLWWWWWWYY",
    "GGGGGPKKLLWWWWWWYYY",
    "GGGGGPKKLLWWWWWWYYYY",
    "GGGGGPKKLLWWWWWWYYYYY",
    "GGGGGPKKLLWWWWWWYYYYYY",
    "GGGGGPKKLLWWWWWWYYYYYYP",
    "GGGGGPKKLLWWWWWWYYYYYYPK",
    "GGGGGPKKLLWWWWWWYYYYYYPKK",
    "GGGGGPKKLLWWWWWWYYYYYYPKKL",
#    "GGGGP",
    "GGGGPK",
    "GGGGPKK",
    "GGGGPKKL",
    "GGGGPKKLL",
    "GGGGPKKLLW",
    "GGGGPKKLLWW",
    "GGGGPKKLLWWW",
    "GGGGPKKLLWWWW",
    "GGGGPKKLLWWWWW",
    "GGGGPKKLLWWWWWW",
    "GGGGPKKLLWWWWWWY",
    "GGGGPKKLLWWWWWWYY",
    "GGGGPKKLLWWWWWWYYY",
    "GGGGPKKLLWWWWWWYYYY",
    "GGGGPKKLLWWWWWWYYYYY",
    "GGGGPKKLLWWWWWWYYYYYY",
    "GGGGPKKLLWWWWWWYYYYYYP",
    "GGGGPKKLLWWWWWWYYYYYYPK",
    "GGGGPKKLLWWWWWWYYYYYYPKK",
    "GGGGPKKLLWWWWWWYYYYYYPKKL",
    "GGGPK",
    "GGGPKK",
    "GGGPKKL",
    "GGGPKKLL",
    "GGGPKKLLW",
    "GGGPKKLLWW",
    "GGGPKKLLWWW",
    "GGGPKKLLWWWW",
    "GGGPKKLLWWWWW",
    "GGGPKKLLWWWWWW",
    "GGGPKKLLWWWWWWY",
    "GGGPKKLLWWWWWWYY",
    "GGGPKKLLWWWWWWYYY",
    "GGGPKKLLWWWWWWYYYY",
    "GGGPKKLLWWWWWWYYYYY",
    "GGGPKKLLWWWWWWYYYYYY",
    "GGGPKKLLWWWWWWYYYYYYP",
    "GGGPKKLLWWWWWWYYYYYYPK",
    "GGGPKKLLWWWWWWYYYYYYPKK",
    "GGGPKKLLWWWWWWYYYYYYPKKL",
    "GGPKK",
    "GGPKKL",
    "GGPKKLL",
    "GGPKKLLW",
    "GGPKKLLWW",
    "GGPKKLLWWW",
    "GGPKKLLWWWW",
    "GGPKKLLWWWWW",
    "GGPKKLLWWWWWW",
    "GGPKKLLWWWWWWY",
    "GGPKKLLWWWWWWYY",
    "GGPKKLLWWWWWWYYY",
    "GGPKKLLWWWWWWYYYY",
    "GGPKKLLWWWWWWYYYYY",
    "GGPKKLLWWWWWWYYYYYY",
    "GGPKKLLWWWWWWYYYYYYP",
    "GGPKKLLWWWWWWYYYYYYPK",
    "GGPKKLLWWWWWWYYYYYYPKK",
    "GGPKKLLWWWWWWYYYYYYPKKL",
    "GPKKL",
    "GPKKLL",
    "GPKKLLW",
    "GPKKLLWW",
    "GPKKLLWWW",
    "GPKKLLWWWW",
    "GPKKLLWWWWW",
    "GPKKLLWWWWWW",
    "GPKKLLWWWWWWY",
    "GPKKLLWWWWWWYY",
    "GPKKLLWWWWWWYYY",
    "GPKKLLWWWWWWYYYY",
    "GPKKLLWWWWWWYYYYY",
    "GPKKLLWWWWWWYYYYYY",
    "GPKKLLWWWWWWYYYYYYP",
    "GPKKLLWWWWWWYYYYYYPK",
    "GPKKLLWWWWWWYYYYYYPKK",
    "GPKKLLWWWWWWYYYYYYPKKL",
    ]  
    
    seq_more_mw = "WWWWWWWWWWYWWWWWWWWWWYWWWWWWWWWWYWWWWWWWWWWYWWWWWWWWWWYWWWWWWWWWWYWWWWWWWWWWYWWWWWWWWWWY"
    
    asp_results_more_mw = [
    "WWWWW",
    "WWWWWW",
    "WWWWWWW",
    "WWWWWWWW",
    "WWWWWWWWW",
    "WWWWWWWWWW",
    "WWWWWWWWWWY",
    "WWWWWWWWWWYW",
    "WWWWWWWWWWYWW",
    "WWWWWWWWWWYWWW",
    "WWWWWWWWWWYWWWW",
    "WWWWWWWWWWYWWWWW",
    "WWWWWWWWWWYWWWWWW",
    "WWWWWWWWWWYWWWWWWW",
    "WWWWWWWWWWYWWWWWWWW",
    "WWWWWWWWWWYWWWWWWWWW",
    "WWWWWWWWWWYWWWWWWWWWW",
    "WWWWWWWWWWYWWWWWWWWWWY",
    "WWWWWWWWWWYWWWWWWWWWWYW",
    "WWWWWWWWWWYWWWWWWWWWWYWW",
    "WWWWWWWWWWYWWWWWWWWWWYWWW",
    "WWWWWWWWWWYWWWWWWWWWWYWWWW",
    "WWWWWWWWWWYWWWWWWWWWWYWWWWW",
    "WWWWWWWWWWYWWWWWWWWWWYWWWWWW",
    "WWWWWWWWWWYWWWWWWWWWWYWWWWWWW",
    "WWWWWWWWWWYWWWWWWWWWWYWWWWWWWW",
    "WWWWWWWWWWYWWWWWWWWWWYWWWWWWWWW",
    "WWWWWWWWWWYWWWWWWWWWWYWWWWWWWWWW",
    #"WWWWWWWWWWYWWWWWWWWWWYWWWWWWWWWWY",
    #"WWWWWWWWWWYWWWWWWWWWWYWWWWWWWWWWYW",
    "WWWWW",
    "WWWWWW",
    "WWWWWWW",
    "WWWWWWWW",
    "WWWWWWWWW",
    "WWWWWWWWWY",
    "WWWWWWWWWYW",
    "WWWWWWWWWYWW",
    "WWWWWWWWWYWWW",
    "WWWWWWWWWYWWWW",
    "WWWWWWWWWYWWWWW",
    "WWWWWWWWWYWWWWWW",
    "WWWWWWWWWYWWWWWWW",
    "WWWWWWWWWYWWWWWWWW",
    "WWWWWWWWWYWWWWWWWWW",
    "WWWWWWWWWYWWWWWWWWWW",
    "WWWWWWWWWYWWWWWWWWWWY",
    "WWWWWWWWWYWWWWWWWWWWYW",
    "WWWWWWWWWYWWWWWWWWWWYWW",
    "WWWWWWWWWYWWWWWWWWWWYWWW",
    "WWWWWWWWWYWWWWWWWWWWYWWWW",
    "WWWWWWWWWYWWWWWWWWWWYWWWWW"
    ]
    
    def test_equal_pro(self):
        it = peptidases.no_enz_digestion_c(self.seq)
        for seq in self.asp_results:
            n = it.next()[0]
            self.assertEqual(seq, n)
            
    def test_no_std_pro(self):
        it = peptidases.no_enz_digestion_c(self.seq_no_std)
        for seq in self.asp_results_no_std:
            print seq
            n = it.next()[0]
            self.assertEqual(seq, n)
            
            
    def test_less_pro(self):
        it = peptidases.no_enz_digestion_c(self.seq_less_mw)
        txt = "\ntheo: %s (%d)\ncalc: %s (%d)\n"
        for seq in self.asp_results_less_mw:
            val = it.next()
            self.assertEqual(seq, val[0] , 
                             msg = txt%(seq, Param.mi_mw(seq), val[0], val[1]))
            
    def test_more_pro(self):
        it = peptidases.no_enz_digestion_c(self.seq_more_mw)
        for seq in self.asp_results_more_mw:
            self.assertEqual(seq, it.next()[0])
            

            
class Test_join_atoms(unittest.TestCase):
     
    sample_atom_join = [
                        (["GAGAMSSRKK", "PSRRTRVLVG"], 
                         ["GAGAMSSRKK", "GAGAMSSRKKPSRRTRVLVG",]),
                        (["PSRRTRVLVG", "GAALAVLGAG"], 
                         ["PSRRTRVLVG","PSRRTRVLVGGAALAVLGAG",]),
                        (["GAALAVLGAG", "VVGTVAANAA"],
                         ["GAALAVLGAG", "GAALAVLGAGVVGTVAANAA",]),
                        (["VVGTVAANAA", "DTTEATPAAA"],
                         ["VVGTVAANAA", "VVGTVAANAADTTEATPAAA",]),
                        (["DTTEATPAAA", "PVAARGGELT"],
                         ["DTTEATPAAA", "DTTEATPAAAPVAARGGELT",]),
                        (["PVAARGGELT", "QSTHLTLEAA"],
                         ["PVAARGGELT", "PVAARGGELTQSTHLTLEAA"]),
                        (["QSTHLTLEAA", "TKAARAAVEA"],
                         ["QSTHLTLEAA", "QSTHLTLEAATKAARAAVEA"]),
                        (["TKAARAAVEA", "AEKDGRHVSV"],
                         ["TKAARAAVEA", "TKAARAAVEAAEKDGRHVSV"]),
                        (["AEKDGRHVSV", "AVVDRNGNTL"],
                         ["AEKDGRHVSV", "AEKDGRHVSVAVVDRNGNTL"]),
                        (["AVVDRNGNTL", "VTLRGDGAGP"], 
                         ["AVVDRNGNTL", "AVVDRNGNTLVTLRGDGAGP"]),
                        (["VTLRGDGAGP", "QSYESAERKA"],
                         ["VTLRGDGAGP", "VTLRGDGAGPQSYESAERKA"]),
                        (["QSYESAERKA", "FTAVSWNAPT"],
                         ["QSYESAERKA", "QSYESAERKAFTAVSWNAPT"]),
                        (["FTAVSWNAPT", "SELAKRLAQA"], 
                         ["FTAVSWNAPT", "FTAVSWNAPTSELAKRLAQA"]),
                        (["SELAKRLAQA", "PTLKDIPGTL"], 
                         ["SELAKRLAQA","SELAKRLAQAPTLKDIPGTL"]),
                        (["PTLKDIPGTL","FLAGGTPVTA"],
                         ["PTLKDIPGTL","PTLKDIPGTLFLAGGTPVTA"]),
                        (["FLAGGTPVTA", "KGAPVAGIGV"],
                         ["FLAGGTPVTA", "FLAGGTPVTAKGAPVAGIGV"]),
                        (["KGAPVAGIGV", "AGAPSGDLDE"],
                         ["KGAPVAGIGV", "KGAPVAGIGVAGAPSGDLDE"]),
                        (["AGAPSGDLDE", "QYARAGAAVL"],
                         ["AGAPSGDLDE","AGAPSGDLDEQYARAGAAVL"]),
                        (["QYARAGAAVL","GH"],
                         ["QYARAGAAVL","QYARAGAAVLGH"]),
                        (["ER", "ITSEAEDLVANFFPK"],
                         ["ERITSEAEDLVANFFPK"]),
                        (["SDEEQTSTTTDTPATPAR", "VSTTLGN"],
                         ["SDEEQTSTTTDTPATPAR", "SDEEQTSTTTDTPATPARVSTTLGN"])
                    ]
    light_atoms = (["GG", "GGGG", "GGGGG"],
                   ["GGGGGGGGGGG"])
    
    short_atoms = (['CAT' 'A', 'AC', 'SSH'],
                   [
                    'CATAAC', 
                    'CATAACSSH'
                    ])
                
    def test_join_atoms(self):
        for data, asp in self.sample_atom_join:
            it = peptidases._join_atoms(data, 5, 50, 40000000, 600000000)
            res = [r[0] for r in it]
            self.assertItemsEqual(asp, res, msg = (data, asp, res))
        
    def test_join_less(self):        
        it = peptidases._join_atoms(self.light_atoms[0],
                                 5, 50, 40000000, 600000000)
        for seq in self.light_atoms[1]:
            r = it.next()
            self.assertEqual(seq, r[0])
        it = peptidases._join_atoms(self.short_atoms[0],
                                 5, 50, 40000000, 600000000)
        for seq in self.short_atoms[1]:
            r = it.next()
            self.assertEqual(seq, r[0])
            
class Test__seq_conditions(unittest.TestCase):

    less = ['A', #SHORTER
            'AC', 
            'ACD', 
            'ACDE', 
            'GGGGG', #LIGHTER 
            'AAAAA', 
#            'PPPPP', 
#            'SSSSS',
#            'VVVVV'
            ]
    
    def test_raise_less(self):
        for seq in self.less:
            
            self.assertRaises(peptidases.Less, 
                              peptidases._seq_conditions,
                              seq, 5, 50, 40000000, 600000000)
            
    more = [
            'GAGAMSSRKKPSRRTRVLVGGAALAVLGAGVVGTVAANAADTTEATPAAAG', #LONGER
            'PVAARGGELTQSTHLTLEAATKAARAAVEAAEKDGRHVSVAVVDRNGNTLG',
            'VTLRGDGAGPQSYESAERKAFTAVSWNAPTSELAKRLAQAPTLKDIPGTLG',
            "FLAGGTPVTAKGAPVAGIGVAGAPSGDLDEQYARAGAAVLGH"+"LKDIPGTLG"
            
            "WWWWWWWWWWYWWWWWWWWWWYWWWWWWWWWWY", #HEAVER
            "WWWWWWWWWWYWWWWWWWWWWYWWWWWWWWWWYW",
            "WWWWWWWWWWYWWWWWWWWWWYWWWWWWWWWWL",
            ]
    def test_raise_more(self):
        for seq in self.more:
            self.assertRaises(peptidases.More, 
                              peptidases._seq_conditions,
                              seq, 5, 50, 40000000, 600000000) 
    
    strange_Chars = ["GAGAMSSRKOKPSR",
                     "GAGAMSSRKXKPSR",
                     "GAGAMSSRK1KPSR",
                     "GAGAMSSRKgKPSR",
                     "GAGAMSSRK-KPSR"]
                
    def test_raise_param_error(self):
        for seq in self.strange_Chars:
            self.assertRaises(Param.wrongSequence,
                              peptidases._seq_conditions,
                              seq, 5, 50, 40000000, 600000000)
            

class Test_digestion(unittest.TestCase):
    
    seq = "AAARKMASLLKVDQEVKLKPVDSFRERITSEAEDLVANFFPKKLLELDSFLKE"
    #         ^^     ^     ^ ^     ^ ^              ^^        ^

    seq_sc = "AAARKMASLLKVDQEVKLKPVDSFRERITOSEAEDLVANFFPKKLLELDSFLKE"
    #            ^^     ^     ^ ^     ^ ^  !            ^^        ^
    
    #>gi|16128624|ref|NP_415174.1| RlpB [Escherichia coli K12]
    seq_ecoli = """MRYLATLLLSLAVLITAGCGWHLRDTTQVPSTMKVMILDSGDPNGPLSRAVRNQLRLNGVELLDKETTRK
DVPSLRLGKVSIAKDTASVFRNGQTAEYQMIMTVNATVLIPGRDIYPISAKVFRSFFDNPQMALAKDNEQ
DMIVKEMYDRAAEQLIRKLPSIRAADIRSDEEQTSTTTDTPATPARVSTTLGN"""

    aspected = ["AAAR",
               "K",
               "MASLLK",
               "VDQEVK",
               "LK",
               "PVDSFR",
               "ER",
               "ITSEAEDLVANFFPK",
               "K",
               "LLELDSFLK",
               "E"]
    
    aspected_sc = ["AAAR",
                   "K",
                   "MASLLK",
                   "VDQEVK",
                   "LK",
                   "PVDSFR",
                   "ER",
                   "ITOSEAEDLVANFFPK",
                   "K",
                   "LLELDSFLK",
                   "E"]
    
    asp_ecoli = ["MR", 
                 "YLATLLLSLAVLITAGCGWHLR", 
                 "DTTQVPSTMK", 
                 "VMILDSGDPNGPLSR", 
                 "AVR", 
                 "NQLR", 
                 "LNGVELLDK", 
                 "ETTR", 
                 "K", 
                 "DVPSLR", 
                 "LGK", 
                 "VSIAK", 
                 "DTASVFR", 
                 "NGQTAEYQMIMTVNATVLIPGR", 
                 "DIYPISAK", 
                 "VFR", 
                 "SFFDNPQMALAK",  
                 "DNEQDMIVK", 
                 "EMYDR", 
                 "AAEQLIR", 
                 "K", 
                 "LPSIR", 
                 "AADIR", 
                 "SDEEQTSTTTDTPATPAR", 
                 "VSTTLGN"]
    
    def test_no_exceptions(self):
        results = peptidases._digestion_pro(self.seq, 
                                           peptidases.tryp_simp_pro)
        res = [each for each in results]
        self.assertItemsEqual(self.aspected, res)
    
    def test_no_exceptions_sc(self):
        results = peptidases._digestion_pro(self.seq_sc, 
                                           peptidases.tryp_simp_pro)
        res = [each for each in results]
        self.assertItemsEqual(self.aspected_sc, res)
        
    def test_no_exceptions_ecoli(self):
        results = peptidases._digestion_pro(self.seq_ecoli, 
                                           peptidases.tryp_simp_pro)
        res = [each for each in results]
        self.assertItemsEqual(self.asp_ecoli, res)
        
    real_aspected = [
               "MASLLK",
               "VDQEVK",
               "PVDSFR",
               "ITSEAEDLVANFFPK",
               "LLELDSFLK",
               ]
    
    real_aspected_1 = [
               "AAARK",
               "KMASLLK",
               "MASLLK",
               "MASLLKVDQEVK",
               "VDQEVK",
               "VDQEVKLK",
               "LKPVDSFR",
               "PVDSFR",
               "PVDSFRER",
               "ERITSEAEDLVANFFPK",
               "ITSEAEDLVANFFPK",
               "ITSEAEDLVANFFPKK",
               "KLLELDSFLK",
               "LLELDSFLK",
               "LLELDSFLKE"
               ]
    
    real_aspected_Ecoli = ["YLATLLLSLAVLITAGCGWHLR", 
                           "DTTQVPSTMK", 
                           "VMILDSGDPNGPLSR", 
                           "LNGVELLDK",  
                           "DVPSLR", 
                           "VSIAK", 
                           "DTASVFR", 
                           "NGQTAEYQMIMTVNATVLIPGR", 
                           "DIYPISAK", 
                           "SFFDNPQMALAK",  
                           "DNEQDMIVK", 
                           "EMYDR", 
                           "AAEQLIR", 
                           "LPSIR", 
                           "AADIR", 
                           "SDEEQTSTTTDTPATPAR", 
                           "VSTTLGN"]
    
    maxDiff = None
    
    real_asp_ecoli_1 = ["MRYLATLLLSLAVLITAGCGWHLR", 
                        "YLATLLLSLAVLITAGCGWHLR",
                        "YLATLLLSLAVLITAGCGWHLRDTTQVPSTMK", 
                        "DTTQVPSTMK",
                        "DTTQVPSTMKVMILDSGDPNGPLSR", 
                        "VMILDSGDPNGPLSR",
                        "VMILDSGDPNGPLSRAVR", 
                        "AVRNQLR", 
                        "NQLRLNGVELLDK", 
                        "LNGVELLDK", 
                        "LNGVELLDKETTR",
                        "ETTRK", 
                        "KDVPSLR", 
                        "DVPSLR",
                        "DVPSLRLGK", 
                        "LGKVSIAK", 
                        "VSIAK",
                        "VSIAKDTASVFR", 
                        "DTASVFR", 
                        "DTASVFRNGQTAEYQMIMTVNATVLIPGR", 
                        "NGQTAEYQMIMTVNATVLIPGR",
                        "NGQTAEYQMIMTVNATVLIPGRDIYPISAK",  
                        "DIYPISAK",
                        "DIYPISAKVFR", 
                        "VFRSFFDNPQMALAK", 
                        "SFFDNPQMALAK",
                        "SFFDNPQMALAKDNEQDMIVK",  
                        "DNEQDMIVK",
                        "DNEQDMIVKEMYDR",  
                        "EMYDR",
                        "EMYDRAAEQLIR", 
                        "AAEQLIR",
                        "AAEQLIRK", 
                        "KLPSIR", 
                        "LPSIR",
                        "LPSIRAADIR",  
                        "AADIR",
                        "AADIRSDEEQTSTTTDTPATPAR",  
                        "SDEEQTSTTTDTPATPAR",
                        "SDEEQTSTTTDTPATPARVSTTLGN", 
                        "VSTTLGN"]
    
    real_asp_ecoli_2 = ["MRYLATLLLSLAVLITAGCGWHLR",
                        "MRYLATLLLSLAVLITAGCGWHLRDTTQVPSTMK",
                        "YLATLLLSLAVLITAGCGWHLR",
                        "YLATLLLSLAVLITAGCGWHLRDTTQVPSTMK",
                        "YLATLLLSLAVLITAGCGWHLRDTTQVPSTMKVMILDSGDPNGPLSR", 
                        "DTTQVPSTMK",
                        "DTTQVPSTMKVMILDSGDPNGPLSR", 
                        "DTTQVPSTMKVMILDSGDPNGPLSRAVR",  
                        "VMILDSGDPNGPLSR",
                        "VMILDSGDPNGPLSRAVR", 
                        "VMILDSGDPNGPLSRAVRNQLR",  
                        "AVRNQLR",
                        "AVRNQLRLNGVELLDK",  
                        "NQLRLNGVELLDK",
                        "NQLRLNGVELLDKETTR",  
                        "LNGVELLDK",
                        "LNGVELLDKETTR",
                        "LNGVELLDKETTRK", 
                        "ETTRK",
                        "ETTRKDVPSLR",  
                        "KDVPSLR",
                        "KDVPSLRLGK",  
                        "DVPSLR",
                        "DVPSLRLGK", 
                        "DVPSLRLGKVSIAK",  
                        "LGKVSIAK",
                        "LGKVSIAKDTASVFR",  
                        "VSIAK",
                        "VSIAKDTASVFR", 
                        "VSIAKDTASVFRNGQTAEYQMIMTVNATVLIPGR",  
                        "DTASVFR",
                        "DTASVFRNGQTAEYQMIMTVNATVLIPGR", 
                        "DTASVFRNGQTAEYQMIMTVNATVLIPGRDIYPISAK",  
                        "NGQTAEYQMIMTVNATVLIPGR",
                        "NGQTAEYQMIMTVNATVLIPGRDIYPISAK", 
                        "NGQTAEYQMIMTVNATVLIPGRDIYPISAKVFR",  
                        "DIYPISAK", 
                        "DIYPISAKVFR", 
                        "DIYPISAKVFRSFFDNPQMALAK", 
                        "VFRSFFDNPQMALAK",
                        "VFRSFFDNPQMALAKDNEQDMIVK",  
                        "SFFDNPQMALAK",
                        "SFFDNPQMALAKDNEQDMIVK",  
                        "SFFDNPQMALAKDNEQDMIVKEMYDR",    
                        "DNEQDMIVK",
                        "DNEQDMIVKEMYDR", 
                        "DNEQDMIVKEMYDRAAEQLIR",  
                        "EMYDR",
                        "EMYDRAAEQLIR", 
                        "EMYDRAAEQLIRK",  
                        "AAEQLIR",
                        "AAEQLIRK", 
                        "AAEQLIRKLPSIR",  
                        "KLPSIR",
                        "KLPSIRAADIR",  
                        "LPSIR",
                        "LPSIRAADIR", 
                        "LPSIRAADIRSDEEQTSTTTDTPATPAR",  
                        "AADIR",
                        "AADIRSDEEQTSTTTDTPATPAR", 
                        "AADIRSDEEQTSTTTDTPATPARVSTTLGN",  
                        "SDEEQTSTTTDTPATPAR",
                        "SDEEQTSTTTDTPATPARVSTTLGN",  
                        "VSTTLGN"]
    
    def test_real(self):
        it = peptidases.real_digestion_pro(self.seq)
        res = [each[0] for each in it]
        self.assertItemsEqual(self.real_aspected, res)
        
    def test_real_ms1(self):
        it = peptidases.real_digestion_pro(self.seq, miscut=1)
        res = [each[0] for each in it]
        self.assertItemsEqual(self.real_aspected_1, res)
        
    def test_real_Ecoli(self):
        it = peptidases.real_digestion_pro(self.seq_ecoli)
        res = [each[0] for each in it]
        self.assertItemsEqual(self.real_aspected_Ecoli, res)
        
    def test_real_Ecoli_ms1(self):
        it = peptidases.real_digestion_pro(self.seq_ecoli, miscut=1)
        res = [each[0] for each in it]
        self.assertItemsEqual(self.real_asp_ecoli_1, res)
        
    def test_real_Ecoli_ms2(self):
        it = peptidases.real_digestion_pro(self.seq_ecoli, miscut=2)
        res = [each[0] for each in it]
        self.assertItemsEqual(self.real_asp_ecoli_2, res)
    
    real_aspected_sc = [
               #"AAAR",
               #"K",
               "MASLLK",
               "VDQEVK",
               #"LK",
               "PVDSFR",
               #"ER",
#               "ITOSEAEDLVANFFPK",
               #"K",
               "LLELDSFLK",
               #"E"
               ]
            
    real_aspected_1_sc = [
               "AAARK",
               "KMASLLK",
               "MASLLK",
               "MASLLKVDQEVK",
               "VDQEVK",
               "VDQEVKLK",
               "LKPVDSFR",
               "PVDSFR",
               "PVDSFRER",
#               "ERITSEAEDLVANFFPK",
#               "ITSEAEDLVANFFPK",
#               "ITSEAEDLVANFFPKK",
               "KLLELDSFLK",
               "LLELDSFLK",
               "LLELDSFLKE"
               ]
    raising_Less = [
        "AAAR",
        "K",
        "LK",
        "ER",
    ]
    def test__seq_conditions_raising_Less(self):
        for pept in self.raising_Less:
            self.assertRaises(peptidases.Less, peptidases._seq_conditions, pept,  5, 50,
                              400*10**5, 6000*10**5)
   
    raising_wrong_seq = [
        "ITOSEAEDLVANFFPK",
    ]
    
    def test__seq_conditions_raising_wrong_seq(self):
        for pept in self.raising_wrong_seq:
            self.assertRaises(Param.wrongSequence, peptidases._seq_conditions, pept,  5, 50,
                              400*10**5, 6000*10**5)
    def test_real_sc(self):
        it = peptidases.real_digestion_pro(self.seq_sc)
        res = [each[0] for each in it]
        print res
        self.assertItemsEqual(self.real_aspected_sc, res)
        
    def test_real_1(self):
        it = peptidases.real_digestion_pro(self.seq, miscut=1)
        res = [each[0] for each in it if each]
#        print '"'+'",\n"'.join(res)+'"'
        self.assertItemsEqual(self.real_aspected_1, res)
        
    def test_real_1_sc(self):
        it = peptidases.real_digestion_pro(self.seq_sc, miscut=1)
        res = [each[0] for each in it if each]
#        print '"'+'",\n"'.join(res)+'"'
        self.assertItemsEqual(self.real_aspected_1_sc, res)
        
    def test_real_sc_old(self):
        it = peptidases.real_digestion_pro(self.seq_sc)
        res = [each[0] for each in it]
        self.assertItemsEqual(self.real_aspected_sc, res)
        
        
if __name__ == '__main__':
    unittest.main()
