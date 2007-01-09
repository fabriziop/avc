#!/usr/bin/python
# .+
#
# .identifier :	$Id:$
# .context    : Application View Controller
# .title      : A spin box replicated into a text label (Qt3)
# .kind	      : python source
# .author     : Fabrizio Pollastri
# .site	      : Revello - Italy
# .creation   :	17-Nov-2006
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


from qt import * 			# Qt interface
from qtui import *			# ui files realizer
import sys				# system support

from avc.avcqt3 import *		# AVC for Qt3


UI_FILE = 'example1_qt3.ui'


class Example(QApplication,AVC):
  "A spin box whose value is replicated into a text label"

  def __init__(self,sys_argv):

    # create GUI
    QApplication.__init__(self,sys_argv)
    self.root = QWidgetFactory.create(UI_FILE)
    self.setMainWidget(self.root)
    self.root.show()
    
    # the variable holding the spinbox value
    self.spin_value = 0


#### MAIN

example = Example(sys.argv)		# instantiate the application
example.avc_init()			# connect widgets with variables
example.exec_loop()			# run Qt event loop until quit

#### END
