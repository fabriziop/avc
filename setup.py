#!/usr/bin/python
# .+
#
# .context    : Application View Controller
# .title      : AVC distutils setup
# .kind	      : python source
# .author     : Fabrizio Pollastri <pollastri@iriti.cnr.it>
# .site	      : Torino - Italy
# .creation   :	11-Nov-2006
# .copyright  :	(c) 2006-2009 Fabrizio Pollastri
# .license    : GNU General Public License (see below)
#
# This file is part of "AVC, Application View Controller".
#
# AVC is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# AVC is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
# .-

from distutils.core import setup
from shutil import copytree, rmtree
import os, os.path
import sys

# parameters
classifiers = """\
Development Status :: 4 - Beta
Intended Audience :: Developers
License :: OSI Approved :: GNU General Public License (GPL)
Programming Language :: Python
Topic :: System :: Hardware
Topic :: Software Development :: Libraries :: Python Modules
Operating System :: POSIX :: Linux
"""

# when command is 'install', we need to differentiate among python or jython
# install, selecting only files required respectively by python or jython.
# When command is 'sdist' there is no difference all files all copied into src.
if sys.argv[1] == 'install':
  # if command is 'install', create a temporary installation dir
  PACKAGE_DIR = {'avc':'src.setup'}
  copytree('src','src.setup')
  # remove files not required respectively by python or jython
  if 'python' in os.path.split(sys.executable)[1]:
    os.remove('src.setup/avcswing.py')
  else:
    map(os.remove,['src.setup/avcgtk.py','src.setup/avcqt3.py',
      'src.setup/avcqt4.py','src.setup/avctk.py','src.setup/avcwx.py'])
else:
  # for all other commands use original src dir
  PACKAGE_DIR = {'avc':'src'}

# workaround older python versions
if sys.version_info < (2, 3):
  _setup = setup
  def setup(**kwargs):
    if kwargs.has_key("classifiers"):
      del kwargs["classifiers"]
    _setup(**kwargs)

# do setup
setup (
  name = 'avc',
  version = '0.8.0',
  author = 'Fabrizio Pollastri',
  author_email = 'f.pollastri@inrim.it',
  maintainer = 'Fabrizio Pollastri',
  maintainer_email = 'f.pollastri@inrim.it',
  url = 'http://avc.inrim.it',
  download_url = 'http://avc.inrim.it/dist/avc-0.8.0.tar.gz',
  license = 'http://www.gnu.org/licenses/gpl.txt',
  platforms = ['Linux'],
  description = """
  AVC, the Application View Controller is a multiplatform, fully transparent,
  automatic and live connector between the values displayed and entered by GUI
  widgets and the variables of an application using the GUI.""",
  classifiers = filter(None, classifiers.split("\n")),
  long_description =  "see html/index.html or http://avc.inrim.it/",
  package_dir = PACKAGE_DIR,
  packages = ['avc'])

# cleanup
if os.access('MANIFEST',os.F_OK):
  os.remove('MANIFEST')
if os.access('src.setup',os.F_OK):
  rmtree('src.setup')

#### END
