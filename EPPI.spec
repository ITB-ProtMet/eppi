# -*- mode: python -*-
import sys

block_cipher = None


a = Analysis(['EPPI/EPPI.py', 'EPPI/ChangeTargetPeptides.py', 'EPPI/DialogCommons.py', 'EPPI/EPPI_data.py', 'EPPI/flatnotebook.py', 'EPPI/html_generator.py', 'EPPI/Join.py', 'EPPI/ManageVars.py', 'EPPI/pages.py', 'EPPI/project.py', 'EPPI/ReportProtein.py', 'EPPI/ReportSequence.py', 'EPPI/Resume.py', 'EPPI/Search.py', 'EPPI/SelPepts.py', 'EPPI/Targets.py', 'EPPI/by_targets.py', 'EPPI/peptidome/fasta_indx.py', 'EPPI/peptidome/commons/aa.py', 'EPPI/peptidome/commons/aaData.py', 'EPPI/peptidome/commons/peptidases.py', 'EPPI/peptidome/commons/reporting.py', 'EPPI/raw/basic_Stats.py', 'EPPI/raw/data_input.py', 'EPPI/raw/PathWalk.py', 'EPPI/raw/preStats.py', 'EPPI/raw/proteomic_xls.py', 'EPPI/raw/proteomic_xml.py'],
             pathex=['/usr/local/lib/python2.7/site-packages', '/home/piotr/Workspace/eppi2'],
             hiddenimports=[],
             hookspath=None,
             runtime_hooks=None,
             cipher=block_cipher)
pyz = PYZ(a.pure,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          name=os.path.join('dist', 'EPPI' + ('.exe' if sys.platform == 'win32' else '')),
          debug=False,
          strip=None,
          console=False , icon='EPPI/faceglasses.ico')

# Build a .app if on OS X
if sys.platform == 'darwin':
   app = BUNDLE(exe,
                name='EPPI.app',
                icon=None)
