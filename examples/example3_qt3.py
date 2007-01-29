#!/usr/bin/python
# .+
#
# .identifier :	$Id:$
# .context    : Application View Controller
# .title      : A table of all supported widget/control type conbinations (Qt3)
# .kind	      : python source
# .author     : Fabrizio Pollastri
# .site	      : Revello - Italy
# .creation   :	25-Nov-2006
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


UI_FILE = 'example3_qt3.ui'
INCREMENTER_PERIOD = 333		# ms


class Example(QApplication,AVC):
  "A table of all supported widget/control type combinations"

  def __init__(self,sys_argv):

    # create GUI
    QApplication.__init__(self,sys_argv)
    self.root = QWidgetFactory.create(UI_FILE)
    self.setMainWidget(self.root)
    self.root.show()
    
    # the control variables
    self.boolean1 = False
    self.boolean2 = False
    self.radio = 0
    self.integer = 0
    self.float = 0.0
    self.string = ''
    self.textview = ''
    
    # start variables incrementer
    self.increment = self.incrementer()
    self.timer = qt.QTimer(self)
    self.connect(self.timer,qt.SIGNAL("timeout()"),self.timer_function)
    self.timer.start(INCREMENTER_PERIOD)


  def timer_function(self):
    self.increment.next()


  def incrementer(self):
    """
    Booleans are toggled, radio button index is rotated from first to last,
    integer is incremented by 1, float by 0.5, string is appended a char
    untill maxlen when string is cleared, text view/edit is appended a line
    of text untill maxlen when it is cleared.
    Return True to keep timer alive.
    """
    while True:

      self.boolean1 = not self.boolean1
      yield True

      self.boolean2 = not self.boolean2
      yield True

      if self.radio == 2:
        self.radio = 0
      else:
        self.radio += 1
      yield True

      self.integer += 1
      yield True

      self.float += 0.5
      yield True

      if len(self.string) >= 10:
        self.string = 'A'
      else:
        self.string += 'A'
      yield True

      if len(self.textview) >= 200:
        self.textview = ''
      else:
        self.textview += 'line of text, line of text, line of text\n'
      yield True


#### MAIN

example = Example(sys.argv)		# instantiate the application
example.avc_init()			# connect widgets with variables
example.exec_loop()			# run Qt event loop until quit

#### END
