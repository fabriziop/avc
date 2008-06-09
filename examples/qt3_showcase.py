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

from avc import *			# AVC

UI_FILE = 'qt3_showcase.ui'		# qt ui descriptor
INCREMENTER_PERIOD = 333		# ms


class Example(QApplication,AVC):
  """
  A table of all supported widget/control type combinations
  """

  def __init__(self):

    # create GUI
    QApplication.__init__(self,sys.argv)
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
    self.timer = QTimer(self)
    self.connect(self.timer,SIGNAL("timeout()"),self.timer_function)
    self.timer.start(INCREMENTER_PERIOD)


  def timer_function(self):
    self.increment.next()


  def incrementer(self):
    """
    Booleans are toggled, radio button index is rotated from first to last,
    integer is incremented by 1, float by 0.5, string is appended a char
    until maxlen when string is cleared, text view/edit is appended a line
    of text until maxlen when it is cleared.
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

example = Example()			# instantiate the application
example.avc_init()			# connect widgets with variables
example.exec_loop()			# run Qt event loop until quit

#### END
