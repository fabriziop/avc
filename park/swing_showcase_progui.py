#!/usr/bin/env jython
# .+
# .context    : Application View Controller
# .title      : A table of all supported widget/control type (Swing),
#		GUI programmatically generated
# .kind	      : python source
# .author     : Fabrizio Pollastri
# .site	      : Torino - Italy
# .creation   :	19-Mar-2009
# .copyright  : (c) 2009 Fabrizio Pollastri.
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

from javax import swing			# swing toolkit bindings
from java import awt			# awt toolkit bindings
import pawt				# special grid bag support

from avc import *			# AVC for Swing

INCREMENTER_PERIOD = 333		# ms


class Example(AVC):
  """
  A table of all supported widget/control type combinations
  """

  def __init__(self):

    ## create GUI

    # root window with grid bag layout
    root = swing.JFrame('AVC Swing showcase example',size=(600,400),
      defaultCloseOperation = swing.JFrame.EXIT_ON_CLOSE)
    bag = pawt.GridBag(root.getContentPane(),fill='CENTER',weightx=1)

    # row 0: titles 
    bag.add(swing.JLabel('Control Type',swing.SwingConstants.CENTER))
    bag.add(swing.JLabel('Widgets',swing.SwingConstants.CENTER),gridwidth=3)
    bag.add(swing.JLabel('Control Value',swing.SwingConstants.CENTER))
    bag.addRow(swing.JSeparator(),gridwidth=5)

    # row 1: button/boolean
    bag.add(swing.JLabel('Boolean',swing.SwingConstants.CENTER),gridheight=2)
    bag.add(swing.JButton('button',name='boolean1__button'),gridwidth=3)
    bag.add(swing.JLabel('boolean1',swing.SwingConstants.CENTER,
      name='boolean1__label',))
    bag.addRow(swing.JSeparator(),gridwidth=5)

    # row 2: toggle button checkbox/boolean
    bag.add(swing.JToggleButton('toggle button',name='boolean2__togglebutton'))
    bag.add(swing.JCheckBox('check box',name='boolean2__checkbox'))
    bag.add(swing.JLabel('boolean2',swing.SwingConstants.CENTER,
      name='boolean2__label',),gridx=4)
    bag.addRow(swing.JSeparator(),gridwidth=5)

    # row 3: radio butoon combo box/index
    bag.add(swing.JLabel('Index \n(integer)',swing.SwingConstants.CENTER))
    radio_button1 = swing.JRadioButton('choice 0',name='radio__radiobutton1')
    radio_button2 = swing.JRadioButton('choice 1',name='radio__radiobutton2')
    radio_button3 = swing.JRadioButton('choice 2',name='radio__radiobutton3')
    radio_group = swing.ButtonGroup()
    radio_group.add(radio_button1)
    radio_group.add(radio_button2)
    radio_group.add(radio_button3)
    radio_box = swing.Box(swing.BoxLayout.Y_AXIS)
    radio_box.add(radio_button1)
    radio_box.add(radio_button2)
    radio_box.add(radio_button3)
    bag.add(radio_box)
    bag.add(swing.JComboBox(['choiche 0','choiche 1','choiche 2'],
      name='radio__combobox'))
    bag.add(swing.JLabel('index',swing.SwingConstants.CENTER,
      name='radio__label',),gridx=4)
    bag.addRow(swing.JSeparator(),gridwidth=5)

    # row 3: spinner entry slider/integer
    bag.add(swing.JLabel('Integer',swing.SwingConstants.CENTER))
    bag.add(swing.JSpinner(name='integer__spinner'),fill='BOTH')
    bag.add(swing.JTextField(name='integer__textfield'),fill='BOTH')
    bag.add(swing.JSlider(name='integer__slider'))
    bag.add(swing.JLabel('integer',swing.SwingConstants.CENTER,
      name='integer__label',),gridx=4)
    bag.addRow(swing.JSeparator(),gridwidth=5)

    # row 4: entry/float
    bag.add(swing.JLabel('Float',swing.SwingConstants.CENTER))
    bag.add(swing.JTextField(name='float__textfield'),fill='BOTH',gridx=2)
    bag.add(swing.JLabel('float',swing.SwingConstants.CENTER,
      name='float__label',),gridx=4)
    bag.addRow(swing.JSeparator(),gridwidth=5)

    # row 5: pogress bar/float
    bag.add(swing.JLabel('Float',swing.SwingConstants.CENTER))
    bag.add(swing.JProgressBar(name='progressbar__progressbar'),fill='BOTH',
      gridwidth=3)
    bag.add(swing.JLabel('progressbar',swing.SwingConstants.CENTER,
      name='progressbar__label',),gridx=4)
    bag.addRow(swing.JSeparator(),gridwidth=5)

    # row 6: entry/string
    bag.add(swing.JLabel('String',swing.SwingConstants.CENTER))
    bag.add(swing.JTextField(name='string__textfield'),fill='BOTH',gridwidth=3)
    bag.add(swing.JLabel('string',swing.SwingConstants.CENTER,
      name='string__label',),fill='BOTH',gridx=4)
    bag.addRow(swing.JSeparator(),gridwidth=5)

    # row 7: text area/string
    bag.add(swing.JLabel('String',swing.SwingConstants.CENTER))
    bag.add(swing.JTextArea(name='textview__textarea1'),fill='BOTH',gridwidth=3)
    bag.add(swing.JLabel('String',swing.SwingConstants.CENTER,size=(400,1),
      name='textview2__label'),gridx=4)
    bag.addRow(swing.JSeparator(),gridwidth=5)

    root.show()

    # the control variables
    self.boolean1 = False
    self.boolean2 = False
    self.radio = 0
    self.integer = 0
    self.float = 0.0
    self.progressbar = -1.0
    self.string = ''
    self.textview = ''
    self.textview2 = ''
    self.status = ''

    # start variables incrementer
    increment = self.incrementer()
    self.timer = swing.Timer(INCREMENTER_PERIOD,None)
    self.timer.actionPerformed = lambda event: increment.next()
    self.timer.start()


  def incrementer(self):
    """
    Booleans are toggled, radio button index is rotated from first to last,
    integer is incremented by 1, float by 0.5, progress bar is alternatively
    shuttled or incremented from 0 to 100%, string is appended a char
    until maxlen when string is cleared, text view/edit is appended a line
    of text until maxlen when it is cleared. Status bar message is toggled.
    Return True to keep timer alive.
    """
    while True:

      self.boolean1 = not self.boolean1
      yield True

      self.boolean2 = not self.boolean2
      yield True

      if self.radio >= 2:
        self.radio = 0
      else:
        self.radio += 1
      yield True

      self.integer += 1
      yield True

      self.float += 0.5
      yield True

      if self.progressbar >= 0.9999:
        self.progressbar = -1.0
      else:
        self.progressbar += 0.1
      yield True

      if len(self.string) >= 10:
        self.string = ''
      else:
        self.string += 'A'
      yield True

      if len(self.textview) >= 200:
        self.textview = ''
        self.textview2 = ''
      else:
        self.textview += 'line of text, line of text, line of text\n'
        self.textview2 = '<html>'+self.textview.replace('\n','<br>')+'<html>'
        print self.textview2
      yield True

      if not self.status:
        self.status = 'status message'
      else:
        self.status = ''
      yield True

#### MAIN

example = Example()			# instantiate the application
example.avc_init()			# connect widgets with variables

#### END

