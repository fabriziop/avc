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


from qt import * 			# Qt interface
from qtui import *			# ui files realizer
import sys				# system support

from avc.avcqt3 import *		# AVC for Qt3

UI_FILE = 'qt3_spinbox.ui'		# qt ui descriptor


class Example(QApplication,AVC):
  "A spin box whose value is replicated into a text label"

  def __init__(self):

    # create GUI
    QApplication.__init__(self,sys.argv)
    self.root = QWidgetFactory.create(UI_FILE)
    self.setMainWidget(self.root)
    self.root.show()
    
    # the variable holding the spinbox value
    self.spin_value = 0


#### MAIN

example = Example()			# instantiate the application
example.avc_init()			# connect widgets with variables
example.exec_loop()			# run Qt event loop until quit

#### END
