# -*- mode: python -*-
import sys

a = Analysis(['EPPI/EPPI.py'],
             pathex=['/home/piotr/Workspace/eppi2'],
             hiddenimports=[],
             hookspath=None)

pyz = PYZ(a.pure)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          name=os.path.join('dist', 'EPPI' + ('.exe' if sys.platform == 'win32' else '')),
          debug=False,
          strip=None,
          console=False,
          icon='EPPI/faceglasses.ico')

# Build a .app if on OS X
if sys.platform == 'darwin':
   app = BUNDLE(exe,
                name='EPPI.app',
                icon=None)
