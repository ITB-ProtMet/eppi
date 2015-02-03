PY = C:\\Python27\\python.exe

UPX = C:\\Program Files\\upx308w

PYINS = C:\\Docume~1\\Proteo~1\\pyinst~1\\pyinstaller.py

ISCC = C:\\Program Files\\Inno Setup 5\\ISCC.exe

MAIN = EPPI\\EPPI.py

MODULES = EPPI\\ChangeTargetPeptides.py\
EPPI\\DialogCommons.py\
EPPI\\EPPI_data.py\
EPPI\\flatnotebook.py\
EPPI\\html_generator.py\
EPPI\\Join.py\
EPPI\\ManageVars.py\
EPPI\\pages.py\
EPPI\\project.py\
EPPI\\ReportProtein.py\
EPPI\\ReportSequence.py\
EPPI\\Resume.py\
EPPI\\Search.py\
EPPI\\SelPepts.py\
EPPI\\Targets.py\
EPPI\\by_targets.py\
EPPI\\peptidome\\fasta_indx.py\
EPPI\\peptidome\\commons\\aa.py\
EPPI\\peptidome\\commons\\aaData.py\
EPPI\\peptidome\\commons\\peptidases.py\
EPPI\\peptidome\\commons\\reporting.py\
EPPI\\raw\\basic_Stats.py\
EPPI\\raw\\data_input.py\
EPPI\\raw\\PathWalk.py\
EPPI\\raw\\preStats.py\
EPPI\\raw\\proteomic_xls.py\
EPPI\\raw\\proteomic_xml.py

EXE = dist\\EPPI.exe
ICO = EPPI\\faceglasses.ico

DIR = C:\\Python27\\Lib\\site-packages

SU = EPPI\\peptidome\\commons\\setup.py
PPYX = EPPI\\peptidome\\commons\\Param.pyx
PC = EPPI\\peptidome\\commons\\Param.c

setup.exe:  $(EXE) scb.iss
	$(ISCC) scb.iss

$(EXE): $(MAIN) $(MODULES) $(ICO)
	$(PY) $(PYINS) --icon=$(ICO) --paths=$(DIR) -w -F $(MAIN) $(MODULES)
# -d for debug option
	

$(PC): $(PPYX) $(SU)
	$(PY) $(SU) build_ext --inplace


.PHONY: clean
clean:
	rm -fr Build
	rm -fr dist
	rm -fr Output
	rm -f EPPI.spec
	rm -f *.log
	rm -f warnEPPI.txt
