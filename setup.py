#!/usr/bin/python
# .+
#
# .identifier :	$Id:$
# .context    : Application View Controller
# .title      : AVC distutils setup
# .kind	      : python source
# .author     : Fabrizio Pollastri <pollastri@iriti.cnr.it>
# .site	      : Torino - Italy
# .creation   :	11-Nov-2006
# .copyright  :	(c) 2006 Fabrizio Pollastri
# .license    : GNU General Public License (see .copying below)
#
# .copying
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
# 
# .-

from distutils.core import setup
import os
import os.path
import re
import string
import sys

classifiers = """\
Development Status :: 3 - Alpha
Intended Audience :: Developers
License :: OSI Approved :: GNU General Public License (GPL)
Programming Language :: Python
Topic :: System :: Hardware
Topic :: Software Development :: Libraries :: Python Modules
Operating System :: POSIX :: Linux
"""

if sys.version_info < (2, 3):
  _setup = setup
  def setup(**kwargs):
    if kwargs.has_key("classifiers"):
      del kwargs["classifiers"]
    _setup(**kwargs)

setup (
  name = 'avc',
  version = '0.2.0',
  author = 'Fabrizio Pollastri',
  author_email = 'pollastri@iriti.cnr.it',
  maintainer = 'Fabrizio Pollastri',
  maintainer_email = 'pollastri@iriti.cnr.it',
  url = 'http://avc.iriti.cnr.it',
  license = 'http://www.gnu.org/licenses/gpl.txt',
  platforms = ['Linux'],
  description = """
  AVC, the Application View Controller, is a fully transparent and
  automatic connector between the values displayed and entered by GUI
  widgets and the variables of an application using the GUI.""",
  classifiers = filter(None, classifiers.split("\n")),
  long_description =  "see html/index.html or http://avc.iriti.cnr.it/",
  package_dir = {'avc':''},
  packages = ['avc'])

# cleanup
try:
  os.remove('MANIFEST')
except:
  pass

#### END
