import os
import shutil
import subprocess
import sys

def clean():
    deleteDirectory('build')
    deleteDirectory('dist')
    deleteDirectory('deb_dist')
    deleteDirectory('EPPI.egg-info')    

def deleteDirectory(path):
    try:
        if os.path.isdir(path):
	    shutil.rmtree(path)
        elif os.path.isfile(path):
             os.unlink(path)
    except OSError as ose:
    # Ignore 'no such file o directory' errors
	if ose.errno != 2:
	    print ose

arg = sys.argv[1] if len(sys.argv) >= 2 else None

if arg == 'dist':
     if len(sys.argv) == 3:
         pyinst_path = sys.argv[2]
     else:
         pyinst_path = raw_input("Path to pyinstaller: ")
     clean()
     subprocess.call(['python', os.path.join(pyinst_path, 'pyinstaller.py'), 'EPPI.spec'])

elif arg == 'deb':
    print "Ensure you have the python-stdeb package installed!"
    subprocess.call(['python', 'setup.py', '--command-packages=stdeb.command', 'bdist_deb'])

elif arg == 'rpm':
    subprocess.call(['python', 'setup.py', 'bdist_rpm', '--post-install=rpm/postinstall', '--pre-unistall=rpm/preuninstall'])

elif arg == 'source':
    subprocess.call(['python', 'setup.py', 'sdist'])

elif arg == 'run':
    subprocess.call(['python', os.path.join('EPPI', "EPPI.py")])

elif arg == 'test':
    subprocess.call(['nosetests', '--with-doc'])

elif arg == 'clean':
    clean()
 
