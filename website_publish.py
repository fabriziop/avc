#!/usr/bin/python
# .+
#
# .context    : Application View Controller
# .title      : Publish AVC web site
# .kind	      : python source
# .author     : Fabrizio Pollastri <pollastri@inrim.it>
# .site	      : Torino - Italy
# .creation   :	5-Feb-2011
# .copyright  :	(c) 2011 Fabrizio Pollastri
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

# required modules
import os
import re

## parameters
SERVER = 'serzot'
# read version from file
ftext = open('src/avccore.py').read()
VERSION = re.search('__version__\s+=\s+\'(\d+\.\d+\.\d+)\'',ftext).group(1)
# computed parameters
SOURCE_ROOT = 'avc-' + VERSION

## publishweb site
print 'publishing web site ...',
os.system('rsh fabrizio@' + SERVER + ' rm -rf /var/www/avc/*')
os.system('scp '+SOURCE_ROOT+'_site.tbz fabrizio@'+SERVER+':/var/www/avc')
os.system('rsh fabrizio@' + SERVER + ' "cd /var/www/avc; ' + \
  'tar -jxvf ' + SOURCE_ROOT + '_site.tbz; ' + \
  'rm ' + SOURCE_ROOT + '_site.tbz"')
print 'Done'

#### END
