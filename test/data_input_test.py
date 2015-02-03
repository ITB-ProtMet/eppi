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


__authors__ = "Pietro Brunetti"

import unittest
from EPPI.raw import data_input
import os

class Reference_Case(unittest.TestCase):
    """
    accessions from reference
    """
    gb_cases = ["gi|15803091|",
                "gi|295982060|pdb|2WUA|B Chain B, Structure Of The Peroxisomal 3-Ketoacyl-Coa Thiolase From Sunflo",
             """gi|50513461|pdb|1S6D|A Chain A, Structure In Solution Of A Methionine-Rich 2s Albumin Protein From Sunflower Seed
PYGRGRTESGCYQQMEEAEMLNHCGMYLMKNLGERSQVSPRMREEDHKQLCCMQLKNLDEKCMCPAIMMM
LNEPMWIRMRDQVMSMAHNLPIECNLMSQPCQM""",
             """gi|15834432|ref|NP_313205.1| 30S ribosomal protein S18 [Escherichia coli O157:H7 str. Sakai] gi|16132024|ref|NP_418623.1| 30S ribosomal subunit protein S18 [Escherichia coli str. K-12 substr. MG1655] gi|16763210|ref|NP_458827.1| 30S ribosomal protein S18 [Salmonella enterica subsp. enterica serovar Typhi str. CT18] gi|24115555|ref|NP_710065.1| 30S ribosomal protein S18 [Shigella flexneri 2a str. 301] gi|26251099|ref|NP_757139.1| 30S ribosomal protein S18 [Escherichia coli CFT073] gi|29144689|ref|NP_808031.1| 30S ribosomal protein S18 [Salmonella enterica subsp. enterica serovar Typhi str. Ty2] gi|30065573|ref|NP_839744.1| 30S ribosomal protein S18 [Shigella flexneri 2a str. 2457T] gi|37528390|ref|NP_931735.1| 30S ribosomal protein S18 [Photorhabdus luminescens subsp. laumondii TTO1] gi|56416184|ref|YP_153259.1| 30S ribosomal protein S18 [Salmonella enterica subsp. enterica serovar Paratyphi A str. ATCC 9150] gi|62182837|ref|YP_219254.1| 30S ribosomal protein S18 [Salmonella enterica subsp. enterica serovar Choleraesuis str. SC-B67] gi|74314683|ref|YP_313102.1| 30S ribosomal protein S18 [Shigella sonnei Ss046] gi|82546556|ref|YP_410503.1| 30S ribosomal protein S18 [Shigella boydii Sb227] gi|82779400|ref|YP_405749.1| 30S ribosomal protein S18 [Shigella dysenteriae Sd197] gi|89110922|ref|AP_004702.1| 30S ribosomal subunit protein S18 [Escherichia coli str. K-12 substr. W3110] gi|91213751|ref|YP_543737.1| 30S ribosomal protein S18 [Escherichia coli UTI89] gi|110644559|ref|YP_672289.1| 30S ribosomal protein S18 [Escherichia coli 536] gi|110808116|ref|YP_691636.1| 30S ribosomal protein S18 [Shigella flexneri 5 str. 8401] gi|146310038|ref|YP_001175112.1| 30S ribosomal protein S18 [Enterobacter sp. 638] gi|152973068|ref|YP_001338214.1| 30S ribosomal protein S18 [Klebsiella pneumoniae subsp. pneumoniae MGH 78578] gi|156932423|ref|YP_001436339.1| 30S ribosomal protein S18 [Cronobacter sakazakii ATCC BAA-894] gi|157147826|ref|YP_001455145.1| 30S ribosomal protein S18 [Citrobacter koseri ATCC BAA-895] gi|157158640|ref|YP_001465702.1| 30S ribosomal protein S18 [Escherichia coli E24377A] gi|157163667|ref|YP_001460985.1| 30S ribosomal protein S18 [Escherichia coli HS] gi|161505105|ref|YP_001572217.1| 30S ribosomal protein S18 [Salmonella enterica subsp. arizonae serovar 62:z4,z23:-- str. RSK2980] gi|161617665|ref|YP_001591630.1| 30S ribosomal protein S18 [Salmonella enterica subsp. enterica serovar Paratyphi B str. SPB7] gi|168263253|ref|ZP_02685226.1| ribosomal protein S18 [Salmonella enterica subsp. enterica serovar Hadar str. RI_05P066] gi|168464722|ref|ZP_02698625.1| ribosomal protein S18 [Salmonella enterica subsp. enterica serovar Newport str. SL317] gi|168751446|ref|ZP_02776468.1| ribosomal protein S18 [Escherichia coli O157:H7 str. EC4113] gi|168754774|ref|ZP_02779781.1| ribosomal protein S18 [Escherichia coli O157:H7 str. EC4401] gi|168760445|ref|ZP_02785452.1| ribosomal protein S18 [Escherichia coli O157:H7 str. EC4501] gi|168766482|ref|ZP_02791489.1| ribosomal protein S18 [Escherichia coli O157:H7 str. EC4486] gi|168774085|ref|ZP_02799092.1| ribosomal protein S18 [Escherichia coli O157:H7 str. EC4196] gi|168780635|ref|ZP_02805642.1| ribosomal protein S18 [Escherichia coli O157:H7 str. EC4076] gi|168784840|ref|ZP_02809847.1| ribosomal protein S18 [Escherichia coli O157:H7 str. EC869] gi|168801858|ref|ZP_02826865.1| ribosomal protein S18 [Escherichia coli O157:H7 str. EC508] gi|170021788|ref|YP_001726742.1| 30S ribosomal protein S18 [Escherichia coli ATCC 8739] gi|170083647|ref|YP_001732967.1| 30S ribosomal protein S18 [Escherichia coli str. K-12 substr. DH10B] gi|170680020|ref|YP_001746596.1| ribosomal protein S18 [Escherichia coli SMS-3-5] gi|170766627|ref|ZP_02901080.1| ribosomal protein S18 [Escherichia albertii TW07627] gi|183600324|ref|ZP_02961817.1| hypothetical protein PROSTU_03885 [Providencia stuartii ATCC 25827] gi|187732798|ref|YP_001882891.1| 30S ribosomal protein S18 [Shigella boydii CDC 3083-94] gi|188495594|ref|ZP_03002864.1| ribosomal protein S18 [Escherichia coli 53638] gi|188535071|ref|YP_001908868.1| 30S ribosomal protein S18 [Erwinia tasmaniensis Et1/99] gi|191165620|ref|ZP_03027460.1| ribosomal protein S18 [Escherichia coli B7A] gi|191170703|ref|ZP_03032255.1| ribosomal protein S18 [Escherichia coli F11] gi|193065998|ref|ZP_03047056.1| ribosomal protein S18 [Escherichia coli E22] gi|193070855|ref|ZP_03051787.1| ribosomal protein S18 [Escherichia coli E110019] gi|194426593|ref|ZP_03059147.1| ribosomal protein S18 [Escherichia coli B171] gi|194434584|ref|ZP_03066841.1| ribosomal protein S18 [Shigella dysenteriae 1012] gi|194439537|ref|ZP_03071611.1| ribosomal protein S18 [Escherichia coli 101-1] gi|194446807|ref|YP_002043646.1| 30S ribosomal protein S18 [Salmonella enterica subsp. enterica serovar Newport str. SL254] gi|194449942|ref|YP_002048435.1| 30S ribosomal protein S18 [Salmonella enterica subsp. enterica serovar Heidelberg str. SL476] gi|194472416|ref|ZP_03078400.1| ribosomal protein S18 [Salmonella enterica subsp. enterica serovar Kentucky str. CVM29188] gi|194734283|ref|YP_002117333.1| 30S ribosomal protein S18 [Salmonella enterica subsp. enterica serovar Schwarzengrund str. CVM19633] gi|195935992|ref|ZP_03081374.1| 30S ribosomal protein S18 [Escherichia coli O157:H7 str. EC4024] gi|197249759|ref|YP_002149307.1| 30S ribosomal protein S18 [Salmonella enterica subsp. enterica serovar Agona str. SL483] gi|197261817|ref|ZP_03161891.1| ribosomal protein S18 [Salmonella enterica subsp. enterica serovar Saintpaul str. SARA23] gi|197287188|ref|YP_002153060.1| 30S ribosomal protein S18 [Proteus mirabilis HI4320] gi|197365107|ref|YP_002144744.1| 30S ribosomal protein S18 [Salmonella enterica subsp. enterica serovar Paratyphi A str. AKU_12601] gi|198242690|ref|YP_002218274.1| 30S ribosomal protein S18 [Salmonella enterica subsp. enterica serovar Dublin str. CT_02021853] gi|200387853|ref|ZP_03214465.1| ribosomal protein S18 [Salmonella enterica subsp. enterica serovar Virchow str. SL491] gi|204927186|ref|ZP_03218388.1| ribosomal protein S18 [Salmonella enterica subsp. enterica serovar Javiana str. GA_MM04042433] gi|205355148|ref|YP_002228949.1| 30S ribosomal protein S18 [Salmonella enterica subsp. enterica serovar Gallinarum str. 287/91] gi|206579628|ref|YP_002240847.1| ribosomal protein S18 [Klebsiella pneumoniae 342] gi|207859538|ref|YP_002246189.1| 30S ribosomal protein S18 [Salmonella enterica subsp. enterica serovar Enteritidis str. P125109] gi|208809011|ref|ZP_03251348.1| ribosomal protein S18 [Escherichia coli O157:H7 str. EC4206] gi|208814274|ref|ZP_03255603.1| ribosomal protein S18 [Escherichia coli O157:H7 str. EC4045] gi|208819004|ref|ZP_03259324.1| ribosomal protein S18 [Escherichia coli O157:H7 str. EC4042] gi|209400527|ref|YP_002273743.1| ribosomal protein S18 [Escherichia coli O157:H7 str. EC4115] gi|209921692|ref|YP_002295776.1| 30S ribosomal protein S18 [Escherichia coli SE11] gi|212709964|ref|ZP_03318092.1| hypothetical protein PROVALCAL_01015 [Providencia alcalifaciens DSM 30120] gi|213028576|ref|ZP_03343023.1| 30S ribosomal protein S18 [Salmonella enterica subsp. enterica serovar Typhi str. 404ty] gi|213161635|ref|ZP_03347345.1| 30S ribosomal protein S18 [Salmonella enterica subsp. enterica serovar Typhi str. E00-7866] gi|213419166|ref|ZP_03352232.1| 30S ribosomal protein S18 [Salmonella enterica subsp. enterica serovar Typhi str. E01-6750] gi|213428641|ref|ZP_03361391.1| 30S ribosomal protein S18 [Salmonella enterica subsp. enterica serovar Typhi str. E02-1180] gi|213582064|ref|ZP_03363890.1| 30S ribosomal protein S18 [Salmonella enterica subsp. enterica serovar Typhi str. E98-0664] gi|213609732|ref|ZP_03369558.1| 30S ribosomal protein S18 [Salmonella enterica subsp. enterica serovar Typhi str. E98-2068] gi|213649001|ref|ZP_03379054.1| 30S ribosomal protein S18 [Salmonella enterica subsp. enterica serovar Typhi str. J185] gi|213864943|ref|ZP_03387062.1| 30S ribosomal protein S18 [Salmonella enterica subsp. enterica serovar Typhi str. M223] gi|215489546|ref|YP_002331977.1| 30S ribosomal protein S18 [Escherichia coli O127:H6 str. E2348/69] gi|217326502|ref|ZP_03442586.1| ribosomal protein S18 [Escherichia coli O157:H7 str. TW14588] gi|218551472|ref|YP_002385264.1| 30S ribosomal protein S18 [Escherichia fergusonii ATCC 35469] gi|218556754|ref|YP_002389668.1| 30S ribosomal protein S18 [Escherichia coli IAI1] gi|218561361|ref|YP_002394274.1| 30S ribosomal protein S18 [Escherichia coli S88] gi|218692585|ref|YP_002400797.1| 30S ribosomal protein S18 [Escherichia coli ED1a] gi|218697953|ref|YP_002405620.1| 30S ribosomal protein S18 [Escherichia coli 55989] gi|218702898|ref|YP_002410527.1| 30S ribosomal protein S18 [Escherichia coli IAI39] gi|218707813|ref|YP_002415332.1| 30S ribosomal protein S18 [Escherichia coli UMN026] gi|224586232|ref|YP_002640031.1| 30S ribosomal protein S18 [Salmonella enterica subsp. enterica serovar Paratyphi C strain RKS4594] gi|226326632|ref|ZP_03802150.1| hypothetical protein PROPEN_00482 [Proteus penneri ATCC 35198] gi|227357118|ref|ZP_03841487.1| 30S ribosomal protein S18 [Proteus mirabilis ATCC 29906] gi|227886754|ref|ZP_04004559.1| 30S ribosomal protein S18 [Escherichia coli 83972] gi|237703870|ref|ZP_04534351.1| 30S ribosomal subunit protein S18 [Escherichia sp. 3_2_53FAA] gi|237729131|ref|ZP_04559612.1| 30S ribosomal protein S18 [Citrobacter sp. 30_2] gi|238755922|ref|ZP_04617250.1| 30S ribosomal protein S18 [Yersinia ruckeri ATCC 29473] gi|238892682|ref|YP_002917416.1| 30S ribosomal protein S18 [Klebsiella pneumoniae NTUH-K2044] gi|238903309|ref|YP_002929105.1| 30S ribosomal subunit protein S18 [Escherichia coli BW2952] gi|238910550|ref|ZP_04654387.1| 30S ribosomal protein S18 [Salmonella enterica subsp. enterica serovar Tennessee str. CDC07-0191] gi|238918385|ref|YP_002931899.1| 30S ribosomal protein S18 [Edwardsiella ictaluri 93-146] gi|242238248|ref|YP_002986429.1| ribosomal protein S18 [Dickeya dadantii Ech703] gi|251788413|ref|YP_003003134.1| ribosomal protein S18 [Dickeya zeae Ech1591] gi|253775173|ref|YP_003038004.1| 30S ribosomal protein S18 [Escherichia coli BL21-Gold(DE3)pLysS AG] gi|253991543|ref|YP_003042899.1| 30S ribosomal protein S18 [Photorhabdus asymbiotica] gi|254037222|ref|ZP_04871299.1| ribosomal protein S18 [Escherichia sp. 1_1_43] gi|254164131|ref|YP_003047239.1| 30S ribosomal protein S18 [Escherichia coli B str. REL606] gi|254796221|ref|YP_003081058.1| 30S ribosomal subunit protein S18 [Escherichia coli O157:H7 str. TW14359] gi|256019847|ref|ZP_05433712.1| 30S ribosomal protein S18 [Shigella sp. D9] gi|256025137|ref|ZP_05439002.1| 30S ribosomal protein S18 [Escherichia sp. 4_1_40B] gi|259907191|ref|YP_002647547.1| 30S ribosomal protein S18 [Erwinia pyrifoliae Ep1/96] gi|260599460|ref|YP_003212031.1| 30S ribosomal protein s18 [Cronobacter turicensis z3032] gi|260847031|ref|YP_003224809.1| 30S ribosomal subunit protein S18 [Escherichia coli O103:H2 str. 12009] gi|260858354|ref|YP_003232245.1| 30S ribosomal subunit protein S18 [Escherichia coli O26:H11 str. 11368] gi|260870890|ref|YP_003237292.1| 30S ribosomal subunit protein S18 [Escherichia coli O111:H- str. 11128] gi|261225322|ref|ZP_05939603.1| 30S ribosomal subunit protein S18 [Escherichia coli O157:H7 str. FRIK2000] gi|261255426|ref|ZP_05947959.1| 30S ribosomal subunit protein S18 [Escherichia coli O157:H7 str. FRIK966] gi|261345205|ref|ZP_05972849.1| ribosomal protein S18 [Providencia rustigianii DSM 4541] gi|262045370|ref|ZP_06018394.1| 50S ribosomal protein L21 [Klebsiella pneumoniae subsp. rhinoscleromatis ATCC 13884] gi|268592870|ref|ZP_06127091.1| ribosomal protein S18 [Providencia rettgeri DSM 1131] gi|269137725|ref|YP_003294425.1| 30S ribosomal protein S18 [Edwardsiella tarda EIB202] gi|271501889|ref|YP_003334915.1| ribosomal protein S18 [Dickeya dadantii Ech586] gi|283786876|ref|YP_003366741.1| 30S ribosomal subunit protein S18 [Citrobacter rodentium ICC168] gi|283834822|ref|ZP_06354563.1| ribosomal protein S18 [Citrobacter youngae ATCC 29220] gi|288937503|ref|YP_003441562.1| ribosomal protein S18 [Klebsiella variicola At-22] gi|289811466|ref|ZP_06542095.1| 30S ribosomal protein S18 [Salmonella enterica subsp. enterica serovar Typhi str. AG3] gi|289829953|ref|ZP_06547404.1| 30S ribosomal protein S18 [Salmonella enterica subsp. enterica serovar Typhi str. E98-3139] gi|290512241|ref|ZP_06551608.1| 30S ribosomal protein S18 [Klebsiella sp. 1_1_55] gi|291285614|ref|YP_003502432.1| 30S ribosomal protein S18 [Escherichia coli O55:H7 str. CB9615] gi|291619075|ref|YP_003521817.1| RpsR [Pantoea ananatis LMG 20103] gi|292489606|ref|YP_003532496.1| 30S ribosomal protein S18 [Erwinia amylovora CFBP1430] gi|292898173|ref|YP_003537542.1| 30s ribosomal protein S18 [Erwinia amylovora ATCC 49946] gi|293393197|ref|ZP_06637512.1| 50S ribosomal protein L21 [Serratia odorifera DSM 4582] gi|293402827|ref|ZP_06646924.1| 30S ribosomal protein S18 [Escherichia coli FVEC1412] gi|293407927|ref|ZP_06651767.1| 30S ribosomal protein S18 [Escherichia coli B354] gi|293417705|ref|ZP_06660327.1| 30S ribosomal protein S18 [Escherichia coli B185] gi|293476510|ref|ZP_06664918.1| 30S ribosomal protein S18 [Escherichia coli B088] gi|294634472|ref|ZP_06713007.1| ribosomal protein S18 [Edwardsiella tarda ATCC 23685] gi|296100965|ref|YP_003611111.1| ribosomal protein S18 [Enterobacter cloacae subsp. cloacae ATCC 13047] gi|298378356|ref|ZP_06988240.1| 30S ribosomal protein S18 [Escherichia coli FVEC1302] gi|300816496|ref|ZP_07096717.1| ribosomal protein S18 [Escherichia coli MS 107-1] gi|300821296|ref|ZP_07101444.1| ribosomal protein S18 [Escherichia coli MS 119-7] gi|300899740|ref|ZP_07117965.1| ribosomal protein S18 [Escherichia coli MS 198-1] gi|300906032|ref|ZP_07123756.1| ribosomal protein S18 [Escherichia coli MS 84-1] gi|300918336|ref|ZP_07134937.1| ribosomal protein S18 [Escherichia coli MS 115-1] gi|300922390|ref|ZP_07138510.1| ribosomal protein S18 [Escherichia coli MS 182-1] gi|300928018|ref|ZP_07143571.1| ribosomal protein S18 [Escherichia coli MS 187-1] gi|300940689|ref|ZP_07155250.1| ribosomal protein S18 [Escherichia coli MS 21-1] gi|300949169|ref|ZP_07163211.1| ribosomal protein S18 [Escherichia coli MS 116-1] gi|300955265|ref|ZP_07167658.1| ribosomal protein S18 [Escherichia coli MS 175-1] gi|300987233|ref|ZP_07178062.1| ribosomal protein S18 [Escherichia coli MS 45-1] gi|300988551|ref|ZP_07178747.1| ribosomal protein S18 [Escherichia coli MS 200-1] gi|301024523|ref|ZP_07188198.1| ribosomal protein S18 [Escherichia coli MS 69-1] gi|301028025|ref|ZP_07191309.1| ribosomal protein S18 [Escherichia coli MS 196-1] gi|301045965|ref|ZP_07193148.1| ribosomal protein S18 [Escherichia coli MS 185-1] gi|301302619|ref|ZP_07208749.1| ribosomal protein S18 [Escherichia coli MS 124-1] gi|301325967|ref|ZP_07219388.1| ribosomal protein S18 [Escherichia coli MS 78-1] gi|301646650|ref|ZP_07246516.1| ribosomal protein S18 [Escherichia coli MS 146-1] gi|306815583|ref|ZP_07449732.1| 30S ribosomal protein S18 [Escherichia coli NC101] gi|307132412|ref|YP_003884428.1| 30S ribosomal subunit protein S18 [Dickeya dadantii 3937] gi|307140899|ref|ZP_07500255.1| 30S ribosomal protein S18 [Escherichia coli H736] gi|307146944|ref|ZP_07505376.1| 30S ribosomal protein S18 [Escherichia coli M605] gi|307224348|ref|ZP_07510772.1| 30S ribosomal protein S18 [Escherichia coli M718] gi|307228908|ref|ZP_07515319.1| 30S ribosomal protein S18 [Escherichia coli TA206] gi|307233766|ref|ZP_07520177.1| 30S ribosomal protein S18 [Escherichia coli TA143] gi|307238727|ref|ZP_07525138.1| 30S ribosomal protein S18 [Escherichia coli TA271] gi|307285856|ref|ZP_07565989.1| ribosomal protein S18 [Escherichia coli KO11] gi|307314849|ref|ZP_07594441.1| ribosomal protein S18 [Escherichia coli W] gi|307340045|ref|ZP_07616157.1| 30S ribosomal protein S18 [Escherichia coli H591] gi|307347096|ref|ZP_07616701.1| 30S ribosomal protein S18 [Escherichia coli TA280] gi|307558371|ref|ZP_07622138.1| 30S ribosomal protein S18 [Escherichia coli H299] gi|309787731|ref|ZP_07682342.1| ribosomal protein S18 [Shigella dysenteriae 1617] gi|309797014|ref|ZP_07691414.1| ribosomal protein S18 [Escherichia coli MS 145-7] gi|312965875|ref|ZP_07780101.1| ribosomal protein S18 [Escherichia coli 2362-75] gi|312973990|ref|ZP_07788161.1| ribosomal protein S18 [Escherichia coli 1827-70] gi|317049740|ref|YP_004117388.1| 30S ribosomal protein S18 [Pantoea sp. At-9b] gi|67472372|sp|P0A7T7.2|RS18_ECOLI RecName: Full=30S ribosomal protein S18 gi|67472373|sp|P0A7T8.2|RS18_ECOL6 RecName: Full=30S ribosomal protein S18 gi|67472374|sp|P0A7T9.2|RS18_ECO57 RecName: Full=30S ribosomal protein S18 gi|67472375|sp|P0A7U0.2|RS18_PHOLL RecName: Full=30S ribosomal protein S18 gi|67472376|sp|P0A7U1.2|RS18_SALTI RecName: Full=30S ribosomal protein S18 gi|67472377|sp|P0A7U2.2|RS18_SHIFL RecName: Full=30S ribosomal protein S18 gi|75505387|sp|Q57GI9.1|RS18_SALCH RecName: Full=30S ribosomal protein S18 gi|81677980|sp|Q5PJ56.1|RS18_SALPA RecName: Full=30S ribosomal protein S18 gi|123047658|sp|Q0SX84.1|RS18_SHIF8 RecName: Full=30S ribosomal protein S18 gi|123084302|sp|Q1R358.1|RS18_ECOUT RecName: Full=30S ribosomal protein S18 gi|123343273|sp|Q0T9J1.1|RS18_ECOL5 RecName: Full=30S ribosomal protein S18 gi|123728279|sp|Q31TD3.1|RS18_SHIBS RecName: Full=30S ribosomal protein S18 gi|123728458|sp|Q328J7.1|RS18_SHIDS RecName: Full=30S ribosomal protein S18 gi|123759489|sp|Q3YUE5.1|RS18_SHISS RecName: Full=30S ribosomal protein S18 gi|166220942|sp|A8AMJ6.1|RS18_CITK8 RecName: Full=30S ribosomal protein S18 gi|166220951|sp|A7MM78.1|RS18_ENTS8 RecName: Full=30S ribosomal protein S18 gi|166220955|sp|A6THB3.1|RS18_KLEP7 RecName: Full=30S ribosomal protein S18 gi|167011188|sp|A7ZV73.1|RS18_ECO24 RecName: Full=30S ribosomal protein S18 gi|167011189|sp|A8A7U8.1|RS18_ECOHS RecName: Full=30S ribosomal protein S18 gi|167011190|sp|A4W5T1.1|RS18_ENT38 RecName: Full=30S ribosomal protein S18 gi|189029651|sp|A9N520.1|RS18_SALPB RecName: Full=30S ribosomal protein S18 gi|189029677|sp|B1IT04.1|RS18_ECOLC RecName: Full=30S ribosomal protein S18 gi|189029686|sp|A9MFK9.1|RS18_SALAR RecName: Full=30S ribosomal protein S18 gi|226735113|sp|B7MLK7.1|RS18_ECO45 RecName: Full=30S ribosomal protein S18 gi|226735114|sp|B7NTQ7.1|RS18_ECO7I RecName: Full=30S ribosomal protein S18 gi|226735115|sp|B7M9G4.1|RS18_ECO8A RecName: Full=30S ribosomal protein S18 gi|226735116|sp|B7NGD6.1|RS18_ECOLU RecName: Full=30S ribosomal protein S18 gi|226735117|sp|B1LQM1.1|RS18_ECOSM RecName: Full=30S ribosomal protein S18 gi|226735119|sp|B7LLY4.1|RS18_ESCF3 RecName: Full=30S ribosomal protein S18 gi|229559983|sp|B6I2A8.1|RS18_ECOSE RecName: Full=30S ribosomal protein S18 gi|229559984|sp|B2VCV9.1|RS18_ERWT9 RecName: Full=30S ribosomal protein S18 gi|229559986|sp|B5Z2K7.1|RS18_ECO5E RecName: Full=30S ribosomal protein S18 gi|229559987|sp|B1XDV2.1|RS18_ECODH RecName: Full=30S ribosomal protein S18 gi|229560040|sp|B5Y306.1|RS18_KLEP3 RecName: Full=30S ribosomal protein S18 gi|229560053|sp|B4F277.1|RS18_PROMH RecName: Full=30S ribosomal protein S18 gi|229560058|sp|B5F3B9.1|RS18_SALA4 RecName: Full=30S ribosomal protein S18 gi|229560059|sp|B5FSA3.1|RS18_SALDC RecName: Full=30S ribosomal protein S18 gi|229560060|sp|B5R0S0.1|RS18_SALEP RecName: Full=30S ribosomal protein S18 gi|229560061|sp|B5R9F0.1|RS18_SALG2 RecName: Full=30S ribosomal protein S18 gi|229560062|sp|B4TFD7.1|RS18_SALHS RecName: Full=30S ribosomal protein S18 gi|229560063|sp|B4T3F3.1|RS18_SALNS RecName: Full=30S ribosomal protein S18 gi|229560064|sp|B5BKL1.1|RS18_SALPK RecName: Full=30S ribosomal protein S18 gi|229560065|sp|B4TT35.1|RS18_SALSV RecName: Full=30S ribosomal protein S18 gi|229560074|sp|B2TY75.1|RS18_SHIB3 RecName: Full=30S ribosomal protein S18 gi|254765429|sp|B7UQL1.1|RS18_ECO27 RecName: Full=30S ribosomal protein S18 gi|254765430|sp|B7LCR3.1|RS18_ECO55 RecName: Full=30S ribosomal protein S18 gi|254765431|sp|B7MST2.1|RS18_ECO81 RecName: Full=30S ribosomal protein S18 gi|254812953|sp|C0Q6G0.1|RS18_SALPC RecName: Full=30S ribosomal protein S18 gi|259494808|sp|C4ZR79.1|RS18_ECOBW RecName: Full=30S ribosomal protein S18 gi|259494809|sp|C5BF78.1|RS18_EDWI9 RecName: Full=30S ribosomal protein S18 gi|25294828|pir||AI1052 30s ribosomal chain protein S18 [imported] - Salmonella enterica subsp. enterica serovar Typhi (strain CT18) gi|116666565|pdb|1VS5|R Chain R, Crystal Structure Of The Bacterial Ribosome From Escherichia Coli In Complex With The Antibiotic Kasugamyin At 3.5a Resolution. This File Contains The 30s Subunit Of One 70s Ribosome. The Entire Crystal Structure Contains Two 70s Ribosomes And Is Described In Remark 400. gi|116666617|pdb|1VS7|R Chain R, Crystal Structure Of The Bacterial Ribosome From Escherichia Coli In Complex With The Antibiotic Kasugamyin At 3.5a Resolution. This File Contains The 30s Subunit Of One 70s Ribosome. The Entire Crystal Structure Contains Two 70s Ribosomes And Is Described In Remark 400. gi|257097339|pdb|3I1M|R Chain R, Crystal Structure Of The E. Coli 70s Ribosome In An Intermediate State Of Ratcheting gi|257097391|pdb|3I1O|R Chain R, Crystal Structure Of The E. Coli 70s Ribosome In An Intermediate State Of Ratcheting gi|257097443|pdb|3I1Q|R Chain R, Crystal Structure Of The E. Coli 70s Ribosome In An Intermediate State Of Ratcheting gi|257097497|pdb|3I1S|R Chain R, Crystal Structure Of The E. Coli 70s Ribosome In An Intermediate State Of Ratcheting gi|257097551|pdb|3I1Z|R Chain R, Crystal Structure Of The E. Coli 70s Ribosome In An Intermediate State Of Ratcheting gi|257097606|pdb|3I21|R Chain R, Crystal Structure Of The E. Coli 70s Ribosome In An Intermediate State Of Ratcheting gi|290560324|pdb|3KC4|R Chain R, Ribosome-Secy Complex. This Entry 3kc4 Contains 30s Ribosomal Subnit. The 50s Ribosomal Subunit Can Be Found In Pdb Entry 3kcr gi|308198704|pdb|3OR9|R Chain R, Crystal Structure Of The E. Coli Ribosome Bound To Cem-101. This File Contains The 30s Subunit Of The First 70s Ribosome. gi|308198725|pdb|3ORA|R Chain R, Crystal Structure Of The E. Coli Ribosome Bound To Cem-101. This File Contains The 30s Subunit Of The Second 70s Ribosome. gi|26111531|gb|AAN83713.1|AE016771_224 30S ribosomal protein S18 [Escherichia coli CFT073] gi|42847|emb|CAA27654.1| unnamed protein product [Escherichia coli] gi|537043|gb|AAA97098.1| 30S ribosomal subunit protein S18 [Escherichia coli str. K-12 substr. MG1655] gi|1790646|gb|AAC77159.1| 30S ribosomal subunit protein S18 [Escherichia coli str. K-12 substr. MG1655] gi|13364655|dbj|BAB38601.1| 30S ribosomal subunit protein S18 [Escherichia coli O157:H7 str. Sakai] gi|16505518|emb|CAD06870.1| 30s ribosomal subunit protein S18 [Salmonella enterica subsp. enterica serovar Typhi] gi|24054886|gb|AAN45772.1| 30S ribosomal subunit protein S18 [Shigella flexneri 2a str. 301] gi|29140328|gb|AAO71891.1| 30s ribosomal subunit protein S18 [Salmonella enterica subsp. enterica serovar Typhi str. Ty2] gi|30043837|gb|AAP19556.1| 30S ribosomal subunit protein S18 [Shigella flexneri 2a str. 2457T] gi|36787828|emb|CAE16943.1| 30S ribosomal protein S18 [Photorhabdus luminescens subsp. laumondii TTO1] gi|56130441|gb|AAV79947.1| 30s ribosomal subunit protein S18 [Salmonella enterica subsp. enterica serovar Paratyphi A str. ATCC 9150] gi|62130470|gb|AAX68173.1| 30S ribosomal protein S18 [Salmonella enterica subsp. enterica serovar Choleraesuis str. SC-B67] gi|73858160|gb|AAZ90867.1| 30S ribosomal subunit protein S18 [Shigella sonnei Ss046] gi|81243548|gb|ABB64258.1| 30S ribosomal subunit protein S18 [Shigella dysenteriae Sd197] gi|81247967|gb|ABB68675.1| 30S ribosomal subunit protein S18 [Shigella boydii Sb227] gi|85676953|dbj|BAE78203.1| 30S ribosomal subunit protein S18 [Escherichia coli str. K12 substr. W3110] gi|91075325|gb|ABE10206.1| 30S ribosomal subunit protein S18 [Escherichia coli UTI89] gi|110346151|gb|ABG72388.1| 30S ribosomal protein S18 [Escherichia coli 536] gi|110617664|gb|ABF06331.1| 30S ribosomal subunit protein S18 [Shigella flexneri 5 str. 8401] gi|145316914|gb|ABP59061.1| SSU ribosomal protein S18P [Enterobacter sp. 638] gi|150957917|gb|ABR79947.1| 30S ribosomal protein S18 [Klebsiella pneumoniae subsp. pneumoniae MGH 78578] gi|156530677|gb|ABU75503.1| hypothetical protein ESA_00202 [Cronobacter sakazakii ATCC BAA-894] gi|157069347|gb|ABV08602.1| ribosomal protein S18 [Escherichia coli HS] gi|157080670|gb|ABV20378.1| ribosomal protein S18 [Escherichia coli E24377A] gi|157085031|gb|ABV14709.1| hypothetical protein CKO_03630 [Citrobacter koseri ATCC BAA-895] gi|160866452|gb|ABX23075.1| hypothetical protein SARI_03239 [Salmonella enterica subsp. arizonae serovar 62:z4,z23:--] gi|161367029|gb|ABX70797.1| hypothetical protein SPAB_05528 [Salmonella enterica subsp. enterica serovar Paratyphi B str. SPB7] gi|169756716|gb|ACA79415.1| ribosomal protein S18 [Escherichia coli ATCC 8739] gi|169891482|gb|ACB05189.1| 30S ribosomal subunit protein S18 [Escherichia coli str. K-12 substr. DH10B] gi|170124065|gb|EDS92996.1| ribosomal protein S18 [Escherichia albertii TW07627] gi|170517738|gb|ACB15916.1| ribosomal protein S18 [Escherichia coli SMS-3-5] gi|187429790|gb|ACD09064.1| ribosomal protein S18 [Shigella boydii CDC 3083-94] gi|187770314|gb|EDU34158.1| ribosomal protein S18 [Escherichia coli O157:H7 str. EC4196] gi|188014502|gb|EDU52624.1| ribosomal protein S18 [Escherichia coli O157:H7 str. EC4113] gi|188020113|gb|EDU58153.1| hypothetical protein PROSTU_03885 [Providencia stuartii ATCC 25827] gi|188030113|emb|CAO97999.1| 30S ribosomal protein S18 [Erwinia tasmaniensis Et1/99] gi|188490793|gb|EDU65896.1| ribosomal protein S18 [Escherichia coli 53638] gi|189001716|gb|EDU70702.1| ribosomal protein S18 [Escherichia coli O157:H7 str. EC4076] gi|189357840|gb|EDU76259.1| ribosomal protein S18 [Escherichia coli O157:H7 str. EC4401] gi|189364286|gb|EDU82705.1| ribosomal protein S18 [Escherichia coli O157:H7 str. EC4486] gi|189368871|gb|EDU87287.1| ribosomal protein S18 [Escherichia coli O157:H7 str. EC4501] gi|189374715|gb|EDU93131.1| ribosomal protein S18 [Escherichia coli O157:H7 str. EC869] gi|189376068|gb|EDU94484.1| ribosomal protein S18 [Escherichia coli O157:H7 str. EC508] gi|190904315|gb|EDV64024.1| ribosomal protein S18 [Escherichia coli B7A] gi|190908927|gb|EDV68514.1| ribosomal protein S18 [Escherichia coli F11] gi|192926321|gb|EDV80957.1| ribosomal protein S18 [Escherichia coli E22] gi|192955801|gb|EDV86272.1| ribosomal protein S18 [Escherichia coli E110019] gi|194405470|gb|ACF65692.1| ribosomal protein S18 [Salmonella enterica subsp. enterica serovar Newport str. SL254] gi|194408246|gb|ACF68465.1| ribosomal protein S18 [Salmonella enterica subsp. enterica serovar Heidelberg str. SL476] gi|194415332|gb|EDX31600.1| ribosomal protein S18 [Escherichia coli B171] gi|194417169|gb|EDX33281.1| ribosomal protein S18 [Shigella dysenteriae 1012] gi|194421536|gb|EDX37549.1| ribosomal protein S18 [Escherichia coli 101-1] gi|194458780|gb|EDX47619.1| ribosomal protein S18 [Salmonella enterica subsp. enterica serovar Kentucky str. CVM29188] gi|194684675|emb|CAR46619.1| 30S ribosomal protein S18 [Proteus mirabilis HI4320] gi|194709785|gb|ACF89006.1| ribosomal protein S18 [Salmonella enterica subsp. enterica serovar Schwarzengrund str. CVM19633] gi|195632565|gb|EDX51019.1| ribosomal protein S18 [Salmonella enterica subsp. enterica serovar Newport str. SL317] gi|197096584|emb|CAR62196.1| 30s ribosomal subunit protein S18 [Salmonella enterica subsp. enterica serovar Paratyphi A str. AKU_12601] gi|197213462|gb|ACH50859.1| ribosomal protein S18 [Salmonella enterica subsp. enterica serovar Agona str. SL483] gi|197240072|gb|EDY22692.1| ribosomal protein S18 [Salmonella enterica subsp. enterica serovar Saintpaul str. SARA23] gi|197937206|gb|ACH74539.1| ribosomal protein S18 [Salmonella enterica subsp. enterica serovar Dublin str. CT_02021853] gi|199604951|gb|EDZ03496.1| ribosomal protein S18 [Salmonella enterica subsp. enterica serovar Virchow str. SL491] gi|204323851|gb|EDZ09046.1| ribosomal protein S18 [Salmonella enterica subsp. enterica serovar Javiana str. GA_MM04042433] gi|205274929|emb|CAR39998.1| 30s ribosomal subunit protein S18 [Salmonella enterica subsp. enterica serovar Gallinarum str. 287/91] gi|205347928|gb|EDZ34559.1| ribosomal protein S18 [Salmonella enterica subsp. enterica serovar Hadar str. RI_05P066] gi|206568686|gb|ACI10462.1| ribosomal protein S18 [Klebsiella pneumoniae 342] gi|206711341|emb|CAR35719.1| 30s ribosomal subunit protein S18 [Salmonella enterica subsp. enterica serovar Enteritidis str. P125109] gi|208728812|gb|EDZ78413.1| ribosomal protein S18 [Escherichia coli O157:H7 str. EC4206] gi|208735551|gb|EDZ84238.1| ribosomal protein S18 [Escherichia coli O157:H7 str. EC4045] gi|208739127|gb|EDZ86809.1| ribosomal protein S18 [Escherichia coli O157:H7 str. EC4042] gi|209161927|gb|ACI39360.1| ribosomal protein S18 [Escherichia coli O157:H7 str. EC4115] gi|209749988|gb|ACI73301.1| 30S ribosomal subunit protein S18 [Escherichia coli] gi|209749990|gb|ACI73302.1| 30S ribosomal subunit protein S18 [Escherichia coli] gi|209749992|gb|ACI73303.1| 30S ribosomal subunit protein S18 [Escherichia coli] gi|209749994|gb|ACI73304.1| 30S ribosomal subunit protein S18 [Escherichia coli] gi|209749996|gb|ACI73305.1| 30S ribosomal subunit protein S18 [Escherichia coli] gi|209914951|dbj|BAG80025.1| 30S ribosomal protein S18 [Escherichia coli SE11] gi|211638421|emb|CAR67043.1| 30s ribosomal subunit protein s18 [Photorhabdus asymbiotica subsp. asymbiotica ATCC 43949] gi|212687373|gb|EEB46901.1| hypothetical protein PROVALCAL_01015 [Providencia alcalifaciens DSM 30120] gi|215267618|emb|CAS12073.1| 30S ribosomal subunit protein S18 [Escherichia coli O127:H6 str. E2348/69] gi|217322723|gb|EEC31147.1| ribosomal protein S18 [Escherichia coli O157:H7 str. TW14588] gi|218354685|emb|CAV01702.1| 30S ribosomal subunit protein S18 [Escherichia coli 55989] gi|218359014|emb|CAQ91674.1| 30S ribosomal subunit protein S18 [Escherichia fergusonii ATCC 35469] gi|218363523|emb|CAR01177.1| 30S ribosomal subunit protein S18 [Escherichia coli IAI1] gi|218368130|emb|CAR05937.1| 30S ribosomal subunit protein S18 [Escherichia coli S88] gi|218372884|emb|CAR20764.1| 30S ribosomal subunit protein S18 [Escherichia coli IAI39] gi|218430149|emb|CAR11007.1| 30S ribosomal subunit protein S18 [Escherichia coli ED1a] gi|218434910|emb|CAR15848.1| 30S ribosomal subunit protein S18 [Escherichia coli UMN026] gi|222035972|emb|CAP78717.1| 30S ribosomal protein S18 [Escherichia coli LF82] gi|224470760|gb|ACN48590.1| 30S ribosomal protein S18 [Salmonella enterica subsp. enterica serovar Paratyphi C strain RKS4594] gi|224962813|emb|CAX54271.1| 30S ribosomal protein S18 [Erwinia pyrifoliae Ep1/96] gi|225204853|gb|EEG87207.1| hypothetical protein PROPEN_00482 [Proteus penneri ATCC 35198] gi|226840328|gb|EEH72330.1| ribosomal protein S18 [Escherichia sp. 1_1_43] gi|226901782|gb|EEH88041.1| 30S ribosomal subunit protein S18 [Escherichia sp. 3_2_53FAA] gi|226908860|gb|EEH94778.1| 30S ribosomal protein S18 [Citrobacter sp. 30_2] gi|227162650|gb|EEI47617.1| 30S ribosomal protein S18 [Proteus mirabilis ATCC 29906] gi|227836327|gb|EEJ46793.1| 30S ribosomal protein S18 [Escherichia coli 83972] gi|238544998|dbj|BAH61349.1| 30S ribosomal protein S18 [Klebsiella pneumoniae NTUH-K2044] gi|238705881|gb|EEP98270.1| 30S ribosomal protein S18 [Yersinia ruckeri ATCC 29473] gi|238859792|gb|ACR61790.1| 30S ribosomal subunit protein S18 [Escherichia coli BW2952] gi|238867953|gb|ACR67664.1| ribosomal protein S18, putative [Edwardsiella ictaluri 93-146] gi|242130305|gb|ACS84607.1| ribosomal protein S18 [Dickeya dadantii Ech703] gi|242379723|emb|CAQ34548.1| 30S ribosomal subunit protein S18, subunit of 30S ribosomal subunit and ribosome [Escherichia coli BL21(DE3)] gi|247537034|gb|ACT05655.1| ribosomal protein S18 [Dickeya zeae Ech1591] gi|253326217|gb|ACT30819.1| ribosomal protein S18 [Escherichia coli 'BL21-Gold(DE3)pLysS AG'] gi|253782993|emb|CAQ86158.1| 30s ribosomal subunit protein s18 [Photorhabdus asymbiotica] gi|253976032|gb|ACT41703.1| 30S ribosomal protein S18 [Escherichia coli B str. REL606] gi|253980188|gb|ACT45858.1| 30S ribosomal protein S18 [Escherichia coli BL21(DE3)] gi|254595621|gb|ACT74982.1| 30S ribosomal subunit protein S18 [Escherichia coli O157:H7 str. TW14359] gi|257757003|dbj|BAI28505.1| 30S ribosomal subunit protein S18 [Escherichia coli O26:H11 str. 11368] gi|257762178|dbj|BAI33675.1| 30S ribosomal subunit protein S18 [Escherichia coli O103:H2 str. 12009] gi|257767246|dbj|BAI38741.1| 30S ribosomal subunit protein S18 [Escherichia coli O111:H- str. 11128] gi|259037288|gb|EEW38535.1| 50S ribosomal protein L21 [Klebsiella pneumoniae subsp. rhinoscleromatis ATCC 13884] gi|260218637|emb|CBA33945.1| 30S ribosomal protein S18 [Cronobacter turicensis z3032] gi|260450971|gb|ACX41393.1| ribosomal protein S18 [Escherichia coli DH1] gi|261249483|emb|CBG27348.1| 30s ribosomal subunit protein S18 [Salmonella enterica subsp. enterica serovar Typhimurium str. D23580] gi|267983385|gb|ACY83214.1| 30S ribosomal protein S18 [Edwardsiella tarda EIB202] gi|267996727|gb|ACY91612.1| 30S ribosomal protein S18 [Salmonella enterica subsp. enterica serovar Typhimurium str. 14028S] gi|270345444|gb|ACZ78209.1| ribosomal protein S18 [Dickeya dadantii Ech586] gi|281181298|dbj|BAI57628.1| 30S ribosomal protein S18 [Escherichia coli SE15] gi|281603664|gb|ADA76648.1| 30S ribosomal protein S18 [Shigella flexneri 2002017] gi|282566898|gb|EFB72433.1| ribosomal protein S18 [Providencia rustigianii DSM 4541] gi|282950330|emb|CBG89977.1| 30S ribosomal subunit protein S18 [Citrobacter rodentium ICC168] gi|283477000|emb|CAY72892.1| 30S ribosomal protein S18 [Erwinia pyrifoliae DSM 12163] gi|284006637|emb|CBA71898.1| 30S ribosomal protein S18 [Arsenophonus nasoniae] gi|284924382|emb|CBG37504.1| 30S ribosomal subunit protein S18 [Escherichia coli 042] gi|288892212|gb|ADC60530.1| ribosomal protein S18 [Klebsiella variicola At-22] gi|289775236|gb|EFD83237.1| 30S ribosomal protein S18 [Klebsiella sp. 1_1_55] gi|290765487|gb|ADD59448.1| 30S ribosomal protein S18 [Escherichia coli O55:H7 str. CB9615] gi|291069070|gb|EFE07179.1| ribosomal protein S18 [Citrobacter youngae ATCC 29220] gi|291091986|gb|EFE24547.1| ribosomal protein S18 [Edwardsiella tarda ATCC 23685] gi|291154105|gb|ADD78689.1| RpsR [Pantoea ananatis LMG 20103] gi|291198021|emb|CBJ45124.1| 30s ribosomal subunit protein S18 [Erwinia amylovora ATCC 49946] gi|291311659|gb|EFE52112.1| ribosomal protein S18 [Providencia rettgeri DSM 1131] gi|291320963|gb|EFE60405.1| 30S ribosomal protein S18 [Escherichia coli B088] gi|291424343|gb|EFE97557.1| 50S ribosomal protein L21 [Serratia odorifera DSM 4582] gi|291429742|gb|EFF02756.1| 30S ribosomal protein S18 [Escherichia coli FVEC1412] gi|291430423|gb|EFF03421.1| 30S ribosomal protein S18 [Escherichia coli B185] gi|291472178|gb|EFF14660.1| 30S ribosomal protein S18 [Escherichia coli B354] gi|291555043|emb|CBA23114.1| 30S ribosomal protein S18 [Erwinia amylovora CFBP1430] gi|294492280|gb|ADE91036.1| ribosomal protein S18 [Escherichia coli IHE3034] gi|295055424|gb|ADF60162.1| ribosomal protein S18 [Enterobacter cloacae subsp. cloacae ATCC 13047] gi|295098349|emb|CBK87439.1| ribosomal protein S18 [Enterobacter cloacae subsp. cloacae NCTC 9394] gi|298280690|gb|EFI22191.1| 30S ribosomal protein S18 [Escherichia coli FVEC1302] gi|299878935|gb|EFI87146.1| ribosomal protein S18 [Escherichia coli MS 196-1] gi|300302008|gb|EFJ58393.1| ribosomal protein S18 [Escherichia coli MS 185-1] gi|300305897|gb|EFJ60417.1| ribosomal protein S18 [Escherichia coli MS 200-1] gi|300317842|gb|EFJ67626.1| ribosomal protein S18 [Escherichia coli MS 175-1] gi|300356712|gb|EFJ72582.1| ribosomal protein S18 [Escherichia coli MS 198-1] gi|300396522|gb|EFJ80060.1| ribosomal protein S18 [Escherichia coli MS 69-1] gi|300402199|gb|EFJ85737.1| ribosomal protein S18 [Escherichia coli MS 84-1] gi|300407710|gb|EFJ91248.1| ribosomal protein S18 [Escherichia coli MS 45-1] gi|300414468|gb|EFJ97778.1| ribosomal protein S18 [Escherichia coli MS 115-1] gi|300421209|gb|EFK04520.1| ribosomal protein S18 [Escherichia coli MS 182-1] gi|300451417|gb|EFK15037.1| ribosomal protein S18 [Escherichia coli MS 116-1] gi|300454577|gb|EFK18070.1| ribosomal protein S18 [Escherichia coli MS 21-1] gi|300463969|gb|EFK27462.1| ribosomal protein S18 [Escherichia coli MS 187-1] gi|300526185|gb|EFK47254.1| ribosomal protein S18 [Escherichia coli MS 119-7] gi|300530726|gb|EFK51788.1| ribosomal protein S18 [Escherichia coli MS 107-1] gi|300842144|gb|EFK69904.1| ribosomal protein S18 [Escherichia coli MS 124-1] gi|300847320|gb|EFK75080.1| ribosomal protein S18 [Escherichia coli MS 78-1] gi|301075197|gb|EFK90003.1| ribosomal protein S18 [Escherichia coli MS 146-1] gi|301160880|emb|CBW20412.1| 30s ribosomal subunit protein S18 [Salmonella enterica subsp. enterica serovar Typhimurium str. SL1344] gi|304557782|gb|ADM40446.1| SSU ribosomal protein S18p [Edwardsiella tarda FL6-60] gi|305851245|gb|EFM51700.1| 30S ribosomal protein S18 [Escherichia coli NC101] gi|306529941|gb|ADM99871.1| 30S ribosomal subunit protein S18 [Dickeya dadantii 3937] gi|306873097|gb|EFN04379.1| ribosomal protein S18 [Escherichia coli KO11] gi|306905652|gb|EFN36181.1| ribosomal protein S18 [Escherichia coli W] gi|307556369|gb|ADN49144.1| 30S ribosomal protein S18 [Escherichia coli ABU 83972] gi|307629274|gb|ADN73578.1| 30S ribosomal protein S18 [Escherichia coli UM146] gi|308119427|gb|EFO56689.1| ribosomal protein S18 [Escherichia coli MS 145-7] gi|308924481|gb|EFP69977.1| ribosomal protein S18 [Shigella dysenteriae 1617] gi|309704706|emb|CBJ04057.1| 30S ribosomal subunit protein S18 [Escherichia coli ETEC H10407] gi|310331524|gb|EFP98780.1| ribosomal protein S18 [Escherichia coli 1827-70] gi|310765318|gb|ADP10268.1| 30S ribosomal protein S18 [Erwinia sp. Ejp617] gi|312173783|emb|CBX82037.1| 30S ribosomal protein S18 [Erwinia amylovora ATCC BAA-2158] gi|312289118|gb|EFR17012.1| ribosomal protein S18 [Escherichia coli 2362-75] gi|312915490|dbj|BAJ39464.1| 30S ribosomal protein S18 [Salmonella enterica subsp. enterica serovar Typhimurium str. T000240] gi|312948852|gb|ADR29679.1| 30S ribosomal subunit protein S18 [Escherichia coli O83:H1 str. NRG 857C] gi|313646322|gb|EFS10784.1| ribosomal protein S18 [Shigella flexneri 2a str. 2457T] gi|315063516|gb|ADT77843.1| 30S ribosomal subunit protein S18 [Escherichia coli W] gi|315138756|dbj|BAJ45915.1| ribosomal protein S18 [Escherichia coli DH1] gi|315255547|gb|EFU35515.1| ribosomal protein S18 [Escherichia coli MS 85-1] gi|315288483|gb|EFU47881.1| ribosomal protein S18 [Escherichia coli MS 110-3] gi|315293516|gb|EFU52868.1| ribosomal protein S18 [Escherichia coli MS 153-1] gi|315299082|gb|EFU58336.1| ribosomal protein S18 [Escherichia coli MS 16-3] gi|315617610|gb|EFU98216.1| ribosomal protein S18 [Escherichia coli 3431] gi|316918528|gb|EFV39866.1| ribosomal protein S18 [Enterobacteriaceae bacterium 9_2_54FAA] gi|316951357|gb|ADU70832.1| ribosomal protein S18 [Pantoea sp. At-9b]
MARYFRRRKFCRFTAEGVQEIDYKDIATLKNYITESGKIVPSRITGTRAKYQRQLARAIKRARYLSLLPYTDRHQ
>gi|15802782|ref|NP_288809.1| ribonucleotide-diphosphate reductase subunit beta [Escherichia coli O157:H7 EDL933] gi|15832372|ref|NP_311145.1| ribonucleotide-diphosphate reductase subunit beta [Escherichia coli O157:H7 str. Sakai] gi|16130170|ref|NP_416738.1| ribonucleoside-diphosphate reductase 1, beta subunit, ferritin-like protein [Escherichia coli str. K-12 substr. MG1655] gi|82544520|ref|YP_408467.1| ribonucleotide-diphosphate reductase subunit beta [Shigella boydii Sb227] gi|82777644|ref|YP_403993.1| ribonucleotide-diphosphate reductase subunit beta [Shigella dysenteriae Sd197] gi|89109052|ref|AP_002832.1| ribonucleoside diphosphate reductase 1, beta subunit, ferritin-like [Escherichia coli str. K-12 substr. W3110] gi|157161718|ref|YP_001459036.1| ribonucleotide-diphosphate reductase subunit beta [Escherichia coli HS] gi|170081853|ref|YP_001731173.1| ribonucleoside diphosphate reductase 1, beta subunit, ferritin-like protein [Escherichia coli str. K-12 substr. DH10B] gi|187731010|ref|YP_001881065.1| ribonucleotide-diphosphate reductase subunit beta [Shigella boydii CDC 3083-94] gi|188495860|ref|ZP_03003130.1| ribonucleoside-diphosphate reductase, beta subunit [Escherichia coli 53638] gi|195935609|ref|ZP_03080991.1| ribonucleotide-diphosphate reductase subunit beta [Escherichia coli O157:H7 str. EC4024] gi|218548311|ref|YP_002382102.1| ribonucleotide-diphosphate reductase subunit beta [Escherichia fergusonii ATCC 35469] gi|218705765|ref|YP_002413284.1| ribonucleotide-diphosphate reductase subunit beta [Escherichia coli UMN026] gi|238901409|ref|YP_002927205.1| ribonucleoside diphosphate reductase 1, beta subunit, ferritin-like protein [Escherichia coli BW2952] gi|254794126|ref|YP_003078963.1| ribonucleoside diphosphate reductase 1, beta subunit, ferritin-like protein [Escherichia coli O157:H7 str. TW14359] gi|256022083|ref|ZP_05435948.1| ribonucleotide-diphosphate reductase subunit beta [Escherichia sp. 4_1_40B] gi|261223312|ref|ZP_05937593.1| ribonucleotide-diphosphate reductase subunit beta [Escherichia coli O157:H7 str. FRIK2000] gi|261259138|ref|ZP_05951671.1| ribonucleotide-diphosphate reductase subunit beta [Escherichia coli O157:H7 str. FRIK966] gi|293405702|ref|ZP_06649694.1| nrdB [Escherichia coli FVEC1412] gi|293410599|ref|ZP_06654175.1| ribonucleoside-diphosphate reductase [Escherichia coli B354] gi|298381383|ref|ZP_06990982.1| nrdB [Escherichia coli FVEC1302] gi|309785072|ref|ZP_07679705.1| ribonucleoside-diphosphate reductase 1, subunit beta [Shigella dysenteriae 1617] gi|312973510|ref|ZP_07787682.1| ribonucleoside-diphosphate reductase 1 subunit beta [Escherichia coli 1827-70] gi|57014104|sp|P69924.2|RIR2_ECOLI RecName: Full=Ribonucleoside-diphosphate reductase 1 subunit beta; AltName: Full=Protein B2; AltName: Full=Protein R2; AltName: Full=Ribonucleotide reductase 1 gi|57014105|sp|P69925.2|RIR2_ECO57 RecName: Full=Ribonucleoside-diphosphate reductase 1 subunit beta; AltName: Full=Protein B2; AltName: Full=Protein R2; AltName: Full=Ribonucleotide reductase 1 gi|12516573|gb|AAG57364.1|AE005456_1 ribonucleoside diphosphage reductase 1, beta subunit, B2 [Escherichia coli O157:H7 str. EDL933] gi|146967|gb|AAA24224.1| ribonucleoside diphosphate reductase B2 subunit precursor [Escherichia coli] gi|1788567|gb|AAC75295.1| ribonucleoside-diphosphate reductase 1, beta subunit, ferritin-like protein [Escherichia coli str. K-12 substr. MG1655] gi|1799582|dbj|BAA16054.1| ribonucleoside diphosphate reductase 1, beta subunit, ferritin-like [Escherichia coli str. K12 substr. W3110] gi|13362587|dbj|BAB36541.1| ribonucleoside-diphosphate reductase 1 beta subunit [Escherichia coli O157:H7 str. Sakai] gi|81241792|gb|ABB62502.1| ribonucleoside-diphosphate reductase 1, beta subunit, B2 [Shigella dysenteriae Sd197] gi|81245931|gb|ABB66639.1| ribonucleoside-diphosphate reductase 1, beta subunit, B2 [Shigella boydii Sb227] gi|157067398|gb|ABV06653.1| ribonucleoside-diphosphate reductase, beta subunit [Escherichia coli HS] gi|169889688|gb|ACB03395.1| ribonucleoside diphosphate reductase 1, beta subunit, ferritin-like protein [Escherichia coli str. K-12 substr. DH10B] gi|187428002|gb|ACD07276.1| ribonucleoside-diphosphate reductase, beta subunit [Shigella boydii CDC 3083-94] gi|188491059|gb|EDU66162.1| ribonucleoside-diphosphate reductase, beta subunit [Escherichia coli 53638] gi|218355852|emb|CAQ88465.1| ribonucleoside diphosphate reductase 1, beta subunit, ferritin-like [Escherichia fergusonii ATCC 35469] gi|218432862|emb|CAR13756.1| ribonucleoside diphosphate reductase 1, beta subunit, ferritin-like [Escherichia coli UMN026] gi|238863475|gb|ACR65473.1| ribonucleoside diphosphate reductase 1, beta subunit, ferritin-like protein [Escherichia coli BW2952] gi|254593526|gb|ACT72887.1| ribonucleoside diphosphate reductase 1, beta subunit, ferritin-like protein [Escherichia coli O157:H7 str. TW14359] gi|284922226|emb|CBG35308.1| ribonucleoside-diphosphate reductase 1 beta chain [Escherichia coli 042] gi|291427910|gb|EFF00937.1| nrdB [Escherichia coli FVEC1412] gi|291471067|gb|EFF13551.1| ribonucleoside-diphosphate reductase [Escherichia coli B354] gi|298278825|gb|EFI20339.1| nrdB [Escherichia coli FVEC1302] gi|308927442|gb|EFP72916.1| ribonucleoside-diphosphate reductase 1, subunit beta [Shigella dysenteriae 1617] gi|309702545|emb|CBJ01872.1| ribonucleoside-diphosphate reductase 1 beta chain [Escherichia coli ETEC H10407] gi|310332105|gb|EFP99340.1| ribonucleoside-diphosphate reductase 1 subunit beta [Escherichia coli 1827-70] gi|315615496|gb|EFU96128.1| ribonucleoside-diphosphate reductase 1 subunit beta [Escherichia coli 3431]
MAYTTFSQTKNDQLKEPMFFGQPVNVARYDQQKYDIFEKLIEKQLSFFWRPEEVDVSRDRIDYQALPEHEKHIFISNLKY
QTLLDSIQGRSPNVALLPLISIPELETWVETWAFSETIHSRSYTHIIRNIVNDPSVVFDDIVTNEQIQKRAEGISSYYDE
LIEMTSYWHLLGEGTHTVNGKTVTVSLRELKKKLYLCLMSVNALEAIRFYVSFACSFAFAERELMEGNAKIIRLIARDEA
LHLTGTQHMLNLLRSGADDPEMAEIAEECKQECYDLFVQAAQQEKDWADYLFRDGSMIGLNKDILCQYVEYITNIRMQAV
                    """]

    swiss_cases = ["""sp|P20699|ACEA_HELAN Isocitrate lyase (Fragment) OS=Helianthus annuus PE=3 SV=1
TRGMLAYVEKIQREERKHGVDTLAHQKWSGANYYDRVLRTVQGGMTSTAAMGKGVTEE"""]

    gis = ["15803091", "295982060", "50513461", "15834432"]

    def tearDown(self):
        rm_files = [
            "EPPI\\output.csv",
            "EPPI\\output_no_sc.csv",
            "EPPI\\output_sc.csv",
            "output.csv",
            "output_no_sc.csv",
            "output_sc.csv",]

        for f in rm_files:
            if os.path.exists(f):
                os.remove(f)

    def test_right_cases(self):
        """
        reference right cases
        """
        for prot in self.gb_cases:
            self.assertRegexpMatches(prot, data_input.parser.acc2id)

    #def gi_test(self):
    #    """
    #    Is the results right?
    #    """
    #    for i, prot in enumerate(self.gb_cases):
    #        self.assertEqual(self.gis[i], data_input.parser.fasta2accs.find(prot))
            
class Redundant_Protein_Case(unittest.TestCase):
    """
    It's not possible to find two time the same protein in the same dataset
    """
    class data:
        pass

    d = data()
    d.proteins = ['acc1', 'acc2', 'acc3', 'acc4', 'acc1']
    d.peptides = [('acc1',['SEQONE','SEQTWO', 'SEQTWO','SEQTHREE']),
                      ('acc2',['SEQONE','SEQTWO']),
                      ('acc3',['SEQFOUR','SEQFIVE','SEQEIGHT']),
                      ('acc4',['SEQFOUR','SEQFIVE','SEQFIVE',])]

    def test_protein_redundant(self):
        """
        check if raise with a protein stored two time in d
        """
        p = data_input.parser()
        self.assertRaises(data_input.redundant_proteins, p.parse, self.d)


class No_Right_Peptide_Case(unittest.TestCase):
    """
    With strange peptide
    """
    class data:
        def __init__(self, prots, pepts):
            self.proteins=prots
            self.peptides=pepts

    trying_data = [data(['acc1'], [('acc1',['SEQ1'])]),
                   data(['acc2'], [('acc2',['!SEQTWO'])]),
                   data(['acc3'], [('acc3', ['SEQ TWO'])])]

    peptides = ['SEQ1', '!SEQTWO', 'SEQ TWO']

    def test_wrongPeptide_re(self):
        """
        the partner test
        """
        for peptide in self.peptides:
            self.assertNotRegexpMatches(peptide, data_input.parser.peptide_format)

    def test_wrongPeptide(self):
        """
        wrong peptide sequence
        """
        p = data_input.parser()
        for d in self.trying_data:
            self.assertRaises(data_input.bad_format_peptide, p.parse, d)


class NoRedundant_Right_Case(unittest.TestCase):
    """
    if parsing is right
    """
    fist_results_prot = (
        ('acc1',1),
        ('acc2',1),
        ('acc3',1),
        ('acc4',1)
    )

    second_results_prot = (
        ('acc1',2),
        ('acc2',2),
        ('acc3',2),
        ('acc4',1)
    )

    first_results_pept_no_sc = (
        ('acc1','SEQONE',1),
        ('acc1','SEQTWO',1),
        ('acc1','SEQTHREE',1),

        ('acc2','SEQONE',1),
        ('acc2','SEQTWO',1),

        ('acc3','SEQFOUR',1),
        ('acc3','SEQFIVE',1),
        ('acc3','SEQEIGHT',1),

        ('acc4','SEQFOUR',1),
        ('acc4','SEQFIVE',1)
    )

    second_results_pept_no_sc = (
        ('acc1','SEQONE',2),
        ('acc1','SEQTWO',2),
        ('acc1','SEQTHREE',1),

        ('acc2','SEQONE',2),
        ('acc2','SEQTWO',2),

        ('acc3','SEQFOUR',2),
        ('acc3','SEQFIVE',2),
        ('acc3','SEQEIGHT',2),

        ('acc4','SEQFOUR',1),
        ('acc4','SEQFIVE',1)
    )

    first_results_pept_sc = (
        ('acc1','SEQONE',1),
        ('acc1','SEQTWO',2),
        ('acc1','SEQTHREE',1),

        ('acc2','SEQONE',1),
        ('acc2','SEQTWO',1),

        ('acc3','SEQFOUR',1),
        ('acc3','SEQFIVE',1),
        ('acc3','SEQEIGHT',1),

        ('acc4','SEQFOUR',1),
        ('acc4','SEQFIVE',2)
    )

    second_results_pept_sc = (
        ('acc1','SEQONE',2),
        ('acc1','SEQTWO',4),
        ('acc1','SEQTHREE',1),

        ('acc2','SEQONE',2),
        ('acc2','SEQTWO',3),

        ('acc3','SEQFOUR',2),
        ('acc3','SEQFIVE',3),
        ('acc3','SEQEIGHT',3),

        ('acc4','SEQFOUR',1),
        ('acc4','SEQFIVE',2)
    )

    csv_results_red= (
        ["Protein", "#Protein",
                             "fProtein", "Peptide",
                             "#Peptide", "fPeptide"],
        ['acc1', '2', '1.0', 'SEQONE', '2', '1.0'],
        ['acc1', '2', '1.0', 'SEQTHREE', '1', '0.5'],
        ['acc1', '2', '1.0', 'SEQTWO', '4', '2.0'],

        ['acc2', '2', '1.0', 'SEQONE', '2', '1.0'],
        ['acc2', '2', '1.0', 'SEQTWO', '3', '1.5'],

        ['acc3', '2', '1.0', 'SEQEIGHT', '3', '1.5'],
        ['acc3', '2', '1.0', 'SEQFIVE', '3', '1.5'],
        ['acc3', '2', '1.0', 'SEQFOUR', '2', '1.0'],

        ['acc4', '1', '0.5', 'SEQFIVE', '2', '2.0'],
        ['acc4', '1', '0.5', 'SEQFOUR', '1', '1.0'],
    )

    csv_results_no_red= (
        
        ["Protein", "#Protein",
                             "fProtein", "Peptide",
                             "#Peptide", "fPeptide"],
        ['acc1', '2', '1.0', 'SEQONE', '2', '1.0'],
        ['acc1', '2', '1.0', 'SEQTHREE', '1', '0.5'],
        ['acc1', '2', '1.0', 'SEQTWO', '2', '1.0'],

        ['acc2', '2', '1.0', 'SEQONE', '2', '1.0'],
        ['acc2', '2', '1.0', 'SEQTWO', '2', '1.0'],

        ['acc3', '2', '1.0', 'SEQEIGHT', '2', '1.0'],
        ['acc3', '2', '1.0', 'SEQFIVE', '2', '1.0'],
        ['acc3', '2', '1.0', 'SEQFOUR', '2', '1.0'],

        ['acc4', '1', '0.5', 'SEQFIVE', '1', '1.0'],
        ['acc4', '1', '0.5', 'SEQFOUR', '1', '1.0'],
    )


    class data:
        pass

    data1 = data()
    data1.proteins = ['acc1', 'acc2', 'acc3', 'acc4']
    data1.peptides = [('acc1',['SEQONE','SEQTWO', 'SEQTWO','SEQTHREE']),
                      ('acc2',['SEQONE','SEQTWO']),
                      ('acc3',['SEQFOUR','SEQFIVE','SEQEIGHT']),
                      ('acc4',['SEQFOUR','SEQFIVE','SEQFIVE'])]

    data2 = data()

    data2.proteins = ['acc1', 'acc2','acc3']
    data2.peptides = [('acc1',['SEQONE','SEQTWO','SEQTWO']),
                      ('acc2',['SEQONE','SEQTWO','SEQTWO']),
                      ('acc3',['SEQFOUR','SEQFIVE','SEQEIGHT', 'SEQFIVE', 'SEQEIGHT'])]

    all_pepts = ['SEQONE','SEQTWO', 'SEQTHREE', 'SEQFOUR','SEQFIVE','SEQEIGHT']
    all_pepts.sort()

    def test_parse_no_sc(self):
        """
        with spectral_count false
        """
        p = data_input.parser()
        p.parse(self.data1)
        for acc, occ in self.fist_results_prot:
            self.assertEqual(p.proteins[acc], occ)
        for acc, seq, occ in self.first_results_pept_no_sc:
            self.assertEqual(p.peptides[acc][seq], occ, "%s %s" %(acc, seq))
        p.parse(self.data2)
        for acc, occ in self.second_results_prot:
            self.assertEqual(p.proteins[acc], occ)
        for acc, seq, occ in self.second_results_pept_no_sc:
            self.assertEqual(p.peptides[acc][seq], occ)

    def test_parse_sc(self):
        """
        with spectral_count true
        """
        p = data_input.parser(mode=True)
        p.parse(self.data1)
        for acc, occ in self.fist_results_prot:
            self.assertEqual(p.proteins[acc], occ)
        for acc, seq, occ in self.first_results_pept_sc:
            self.assertEqual(p.peptides[acc][seq], occ)
        p.parse(self.data2)
        for acc, occ in self.second_results_prot:
            self.assertEqual(p.proteins[acc], occ)
        for acc, seq, occ in self.second_results_pept_sc:
            self.assertEqual(p.peptides[acc][seq], occ)

    def test_get_pepts_no_sc(self):
        """
        get_peptides_list with spectral count false
        """
        p = data_input.parser()
        p.parse(self.data1)
        pepts_found = p.get_peptides_list()
        self.assertListEqual(pepts_found, self.all_pepts)
        p.parse(self.data2)
        self.assertListEqual(pepts_found, self.all_pepts)

    def test_get_pepts_sc(self):
        """
        get_peptides_list with spectral count true
        """
        p = data_input.parser(mode=True)
        p.parse(self.data1)
        pepts_found = p.get_peptides_list()
        self.assertListEqual(pepts_found, self.all_pepts)
        p.parse(self.data2)
        self.assertListEqual(pepts_found, self.all_pepts)

    def test_csv_no_sc(self):
        """
        Trying the function to write a peptide csv file
        spectral count mode False
        """
        p = data_input.parser()
        p.parse(self.data1)
        p.parse(self.data2)
        p.peptide_csv("output_no_sc.csv")
        import csv
        handle = csv.reader(open('output_no_sc.csv'))
        for i,row in enumerate(handle):
            self.assertListEqual(row, self.csv_results_no_red[i])

    def test_csv_sc(self):
        """
        Trying the function to write a peptide csv file
        spectral count mode True
        """
        p = data_input.parser(mode=True)
        p.parse(self.data1)
        p.parse(self.data2)
        p.peptide_csv("output_sc.csv")
        import csv
        handle = csv.reader(open('output_sc.csv'))
        for i,row in enumerate(handle):
            self.assertListEqual(row, self.csv_results_red[i])


class Peptides_Case(unittest.TestCase):
    """
    Evaluating peptide formats
    """
    right_peptides = ["-.AKJNUIEINLMIIR.C",
                     "R.FEBUFBWOUFBBBRUE.-",
                     "K.JWNEUIEWWWR.F",
                     "W.W.W"]

    wrong_peptides = ['Q.SEQ1.Q',
                      'Q.!SEQTWO.Q',
                      'Q.SEQ TWO.W',
                      ".NJEIWNRUW.W",
                      "R.JEINBWIURR.",
                      "?.ERWBIURO.#",
                      "AC.IJBNEIWURI.R",
                      "-.ENRUEIRUNUN.JHFG",
                      "ENWIURNIU.R",
                      "D.UIEBBFURBFIUU",
                      "a.jenruiwikewo.f",
                      "FRWENRUIIUIRRGN",
                      "W..W"]

    def test_right_pepts_re(self):
        """
        Evaluating the formats
        """
        for seq in self.right_peptides:
            self.assertRegexpMatches(seq, data_input.sequest_parser.sequest_format)

    def test_wrong_pepts_re(self):
        """
        Negative cases
        """
        for seq in self.wrong_peptides:
            self.assertNotRegexpMatches(seq, data_input.sequest_parser.sequest_format)

    def test_wrong_pepts(self):
        """
        Evaluating if raise bad_format_peptide
        """
        sp = data_input.sequest_parser()
        for seq in self.wrong_peptides:
            self.assertRaises(data_input.bad_format_peptide, sp._to_peptide, seq)


if __name__ == '__main__':
    unittest.main()
