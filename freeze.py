#! python

# This script freezes Frescobaldi to a standalone application without
# needing to install any dependencies.
#
# Usage:
# C:\Python27\Python freeze.py
#
# How it works:
# It creates, using cx_Freeze, a frescobaldi executable inside the frozen/
# directory, along with all used (manually specified) Python modules.
# Then the whole frescobaldi_app directory is copied and the Python scripts
# byte-compiled.
# Finally, an installer is created using the Inno Setup console-mode compiler.

# the Inno Setup console-mode compiler
iscc = 'c:\\Program Files\\Inno Setup 5\\ISCC'

# where to build the frozen program folder
target_dir = 'frozen'

# import standard modules and cx_Freeze
import imp
import os
import py_compile
import shutil
import subprocess
import sys
from cx_Freeze import Executable, Freezer

# access meta-information such as version, etc.
from frescobaldi_app import info

# find pypm by adding the dir of pygame to sys.path
sys.path.append(imp.find_module('pygame')[1])

includes = [
    'sip',
    'PyQt4.QtCore',
    'PyQt4.QtGui',
    'PyQt4.QtWebKit',
    'PyQt4.QtNetwork',
    'PyQt4.QtSvg',
    'PyQt4.QtXml',
    'popplerqt4',
    'pypm',
    
    '__future__',
    'bisect',
    'contextlib',
    'difflib',
    'fractions',
    'glob',
    'json',
    'itertools',
    'functools',
    'optparse',
    'os',
    'platform',
    're',
    'sys',
    'shutil',
    'struct',
    'subprocess',
    'traceback',
    'types',
    'unicodedata',
    'weakref',
]

excludes = [
    'frescobaldi_app',  # we'll add this one manually
    
]

frescobaldi = Executable(
    'frescobaldi',
    icon = 'frescobaldi_app/icons/frescobaldi.ico',
    appendScriptToExe = True,
    base = 'Win32GUI', # no console
)

f = Freezer(
    [frescobaldi],
    includes = includes,
    excludes = excludes,
    targetDir = target_dir,
    copyDependentFiles = True,
    compress = False,
    # silent = True,
)

f.Freeze()

# copy PyQt4 imageformat plugins
path = imp.find_module('PyQt4')[1]
img_formats = os.path.join(path, 'plugins', 'imageformats')
img_formats_target = os.path.join(target_dir, 'imageformats')
shutil.rmtree(img_formats_target, ignore_errors = True)
shutil.copytree(img_formats, img_formats_target)

# copy the frescobaldi_app directory
f_app = os.path.join(target_dir, 'frescobaldi_app')
shutil.rmtree(f_app, ignore_errors=True)
shutil.copytree('frescobaldi_app', f_app, ignore=shutil.ignore_patterns('*~'))

# bytecompile frescobaldi_app
current_dir = os.getcwd()
os.chdir(target_dir)
for root, dirs, files in os.walk('frescobaldi_app'):
    for f in files:
        if f.endswith('.py'):
            f = os.path.join(root, f)
            sys.stdout.write('Byte-compiling %s\n' % f)
            py_compile.compile(f)
os.chdir(current_dir)

# make an Inno Setup installer
inno_script = b'''
[Setup]
AppName=Frescobaldi
AppVersion={version}
AppVerName=Frescobaldi {version}
AppPublisher={author}
AppPublisherURL={homepage}
AppComments={comments}

DefaultDirName={{pf}}\\Frescobaldi
DefaultGroupName=Frescobaldi
UninstallDisplayIcon={{app}}\\frescobaldi.exe
Compression=lzma2
SolidCompression=yes

SourceDir={target}\\
OutputDir=..\\dist\\
OutputBaseFilename="Frescobaldi Setup {version}"
SetupIconFile=frescobaldi_app\\icons\\frescobaldi.ico
LicenseFile=..\\COPYING
WizardImageFile=..\\frescobaldi-wininst.bmp
WizardImageStretch=no

[Files]
Source: "*.*"; DestDir: "{{app}}"; Flags: recursesubdirs;

[Icons]
Name: "{{group}}\Frescobaldi"; Filename: "{{app}}\\frescobaldi.exe";

[Tasks]
Name: assocly; Description: "{{cm:AssocFileExtension,Frescobaldi,.ly}}";

[Registry]
Root: HKCR; Subkey: "LilyPond\\shell\\frescobaldi";\
 ValueType: string; ValueName: ""; ValueData: "Edit with &Frescobaldi...";\
 Flags: uninsdeletekey
Root: HKCR; Subkey: "LilyPond\\shell\\frescobaldi\\command";\
 ValueType: string; ValueName: ""; ValueData: """{{app}}\\frescobaldi.exe"" ""%1"""
Tasks: assocly; Root: HKCR; Subkey: "LilyPond\\shell";\
 ValueType: string; ValueName: ""; ValueData: "frescobaldi";

'''.format(
    version=info.version,
    homepage=info.url,
    author=info.maintainer,
    comments=info.description,
    target=target_dir,
)

subprocess.Popen([iscc, '-'], stdin=subprocess.PIPE).communicate(inno_script)

