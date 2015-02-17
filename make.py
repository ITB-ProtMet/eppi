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
#-------------------------------------------------
# I need to build the library if it isn't
# or if it is not recent
#-------------------------------------------------

build_exist = os.path.exists(r'./EPPI/peptidome/commons/build')
time_build = os.path.getmtime(r'./EPPI/peptidome/commons/build') 
time_param = os.path.getmtime(r'./EPPI/peptidome/commons/Param.pyx')

if not build_exist or time_build < time_param:
    os.chdir(r"./EPPI/peptidome/commons/")
    subprocess.call([
        'python', 
        'setup.py', 
        "build_ext",
        '--inplace'
    ]) 
    os.chdir(r'../../../')
   
if arg == 'dist':
    if len(sys.argv) == 3:
        pyinst_path = sys.argv[2]
    else:
        pyinst_path = raw_input("Path to pyinstaller: ")
    clean()
    subprocess.call([
        'python', 
        os.path.join(pyinst_path, 'pyinstaller.py'), 
        'EPPI.spec'
    ])

elif arg == 'deb':
    print "Ensure you have the python-stdeb package installed!"
    subprocess.call([
        'python', 
        'setup.py', 
        '--command-packages=stdeb.command', 
        'bdist_deb'
    ])

elif arg == 'rpm':
    subprocess.call([
        'python', 
        'setup.py', 
        'bdist_rpm', 
        '--post-install=rpm/postinstall', 
        '--pre-unistall=rpm/preuninstall'
    ])

elif arg == 'source':
    subprocess.call([
        'python', 'setup.py', 'sdist'
    ])

elif arg == 'run':
    subprocess.call([
        'python', os.path.join('EPPI', "EPPI.py")
    ])

elif arg == 'test':
    subprocess.call(['nosetests', '--with-doc'])

elif arg == 'clean':
    clean()

elif arg == 'inst':
    if os.platform != 'win32':
	print "This option is only avaible on ms windows os"
        sys.exit(0)        

    if not os.path.exists('./dist/EPPI.exe'):
        print "please, excecute before 'pymake.py dist'"
        sys.exit(0)
     
    if len(sys.argv) == 3:
        inno_path = sys.argv[2]
    else:
        inno_path = raw_input("path to Inno setup ISCC.exe: ")
        subprocess.call([inno_path, 'scb.iss']) 

