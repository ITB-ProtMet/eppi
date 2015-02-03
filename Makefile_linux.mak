PYTHON = python

PYINS = /home/piotr/pyinstaller/pyinstaller.py

MAIN = EPPI/EPPI.py

MODULES = EPPI/ChangeTargetPeptides.py\
EPPI/DialogCommons.py\
EPPI/EPPI_data.py\
EPPI/flatnotebook.py\
EPPI/html_generator.py\
EPPI/Join.py\
EPPI/ManageVars.py\
EPPI/pages.py\
EPPI/project.py\
EPPI/ReportProtein.py\
EPPI/ReportSequence.py\
EPPI/Resume.py\
EPPI/Search.py\
EPPI/SelPepts.py\
EPPI/Targets.py\
EPPI/by_targets.py\
EPPI/peptidome/fasta_indx.py\
EPPI/peptidome/commons/aa.py\
EPPI/peptidome/commons/aaData.py\
EPPI/peptidome/commons/peptidases.py\
EPPI/peptidome/commons/reporting.py\
EPPI/raw/basic_Stats.py\
EPPI/raw/data_input.py\
EPPI/raw/PathWalk.py\
EPPI/raw/preStats.py\
EPPI/raw/proteomic_xls.py\
EPPI/raw/proteomic_xml.py

EXE = dist/EPPI
ICO = EPPI/faceglasses.ico

DIR = /usr/local/lib/python2.7/site-packages

SU = EPPI/peptidome/commons/setup.py
PPYX = EPPI/peptidome/commons/Param.pyx
PC = EPPI/peptidome/commons/Param.c

$(EXE): $(MAIN) $(MODULES) $(ICO)
	$(PYINS) --icon=$(ICO) --paths=$(DIR) -w -F $(MAIN) $(MODULES)
#-d for debug option

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
