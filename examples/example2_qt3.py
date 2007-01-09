#!/usr/bin/python
# .+
#
# .identifier :	$Id:$
# .context    : Application View Controller
# .title      : A counter with count speed control (Qt3)
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


UI_FILE = 'example2_qt3.ui'
LOW_SPEED = 500				#--
HIGH_SPEED = 100			#- low and high speed period (ms)


class Example(QApplication,AVC):
  """
  A counter displayed in a Label widget whose count speed can be
  accelerated by checking a check box.
  """

  def __init__(self,sys_argv):

    # create GUI
    QApplication.__init__(self,sys_argv)
    self.root = QWidgetFactory.create(UI_FILE)
    self.setMainWidget(self.root)
    self.root.show()
    
    # the counter variable and its speed status
    self.counter = 0
    self.high_speed = False

    # start counter incrementer at low speed
    self.timer = qt.QTimer(self)
    self.connect(self.timer,qt.SIGNAL("timeout()"),self.incrementer)
    self.timer.start(LOW_SPEED)


  def incrementer(self):
    """
    Counter incrementer: increment period = LOW_SPEED, if high speed
    is False, increment period = HIGH_SPEED otherwise.
    """
    self.counter += 1
    if self.high_speed:
      period = HIGH_SPEED
    else:
      period = LOW_SPEED
    self.timer.stop()
    self.timer.start(period) 


#### MAIN

example = Example(sys.argv)		# instantiate the application
example.avc_init()			# connect widgets with variables
example.exec_loop()			# run Qt event loop until quit

#### END
