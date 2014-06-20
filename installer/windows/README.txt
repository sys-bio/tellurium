This directory does not have, on github, hardly anything you need to get it to run.  You'll need to add and unzip the following files:

http://sourceforge.net/projects/pytellurium/files/dependencies/libRoadrunner-installer-dependencies.zip/download
http://sourceforge.net/projects/pytellurium/files/dependencies/spyder_dependencies.zip/download
http://sourceforge.net/projects/pytellurium/files/dependencies/super_installer_dependencies.zip/download

Then go into the super_installer_dependencies/ directory and unzip all of *those* files, too.

If you have to update any of the files therein, zip up the directories again and upload them back again.


The particular files in those zip files come from:

libRoadRunner-installer-dependencies/*
  * The NOTICE.txt file has the URLs for all of the files in this directory.

spyder_dependencies/PyQt4-4.10.4-gpl-Py2.7-Qt4.8.5-x32.exe
  * http://www.riverbankcomputing.com/software/pyqt/download
spyder_dependencies/PyQt4/
  * Created when using the Spyder 'setup.py' command.  Or maybe it used to be?  Can't seem to create it now.
spyder_dependencies/spyder-2.2.5-tellurium.win32.exe
  * Created by using the Spyder command (from the root directory): 'python.exe setup.py bdist_wininst' command.  Source currently at https://code.google.com/p/tellurium/

super_installer_dependencies/wheel/*.whl
  * Various files for local installations using pip.  Created by Mike using http://pip.readthedocs.org/en/latest/reference/pip_wheel.html
super_installer_dependencies/AntimonyPythonBindings-2.5.1-win32.exe
  * Find as part of the Antimony releases.  Created from antimony/win32/AntimonyPythonBindings.iss
super_installer_dependencies/ez_setup.py
  * Part of setuptools, below
super_installer_dependencies/get-pip.py
  * from https://raw.github.com/pypa/pip/master/contrib/get-pip.py
super_installer_dependencies/pip-1.5.4.zip
  * From https://pypi.python.org/pypi/pip#downloads
super_installer_dependencies/pylibroadrunner-1.2.0-beta4.zip
  * From 
super_installer_dependencies/sbml2matlab_1.2.0_win32.zip
  * From   
super_installer_dependencies/setuptools-3.3.zip
  * From https://pypi.python.org/packages/source/s/setuptools/setuptools-3.3.zip#md5=284fa92c5e32c113a4bc00bd20c4eef8
super_installer_dependencies/telplugins-1.0.15-Python-2.7-win32-minimal-setup.exe
  * Find as part of TePlugins release, maybe?  Created from telPlugins/installer/windows/tePlugins-python-2.7-win32-minimal-setup.iss
super_installer_dependencies/unzip.exe
  * Added by Mike directly.  No idea the source.
super_installer_dependencies/wheel
  * Added by Mike directly.  No idea the source.
super_installer_dependencies/zip.exe
  * Added by Mike directly.  No idea the source.

