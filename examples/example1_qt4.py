#!/usr/bin/python
# .+
#
# .identifier :	$Id:$
# .context    : Application View Controller
# .title      : A spin box replicated into a text label (Qt4)
# .kind	      : python source
# .author     : Fabrizio Pollastri
# .site	      : Revello - Italy
# .creation   :	7-Dec-2006
# .copyright  : (c) 2006 Fabrizio Pollastri.
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


from PyQt4.QtCore import *		# Qt core
from PyQt4.QtGui import *		# Qt GUI interface
from PyQt4.uic import *			# ui files realizer
import sys				# system support

from avc.avcqt4 import *		# AVC for Qt4


UI_FILE = 'example1_qt4.ui'


class Example(QApplication,AVC):
  "A spin box iwhose value is replicated into a text label"

  def __init__(self,sys_argv):

    # create GUI
    QApplication.__init__(self,sys_argv)
    self.root = loadUi(UI_FILE)
    self.root.show()
    
    # the variable holding the spin box value
    self.spin_value = 0
    

#### MAIN

example = Example(sys.argv)		# instantiate the application
example.avc_init()			# connect widgets with variables
example.exec_()				# run Qt event loop until quit

#### END
