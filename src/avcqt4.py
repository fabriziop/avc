# .+
# .context    : Application View Controller
# .title      : AVC Qt4 bindings
# .kind	      : python source
# .author     : Fabrizio Pollastri
# .site	      : Revello - Italy
# .creation   :	7-Nov-2006
# .copyright  :	(c) 2006 Fabrizio Pollastri
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


#### IMPORT REQUIRED MODULES

import PyQt4.Qt as qt		# Qt4 tool kit GUI bindings

from avccore import *		# AVC core


#### WIDGETS ABSTRACTION LAYER (widget toolkit side)

class _Button(WALButton):
  "Qt4 Button widget abstractor"

  def __init__(self,coget,button):

    WALButton.__init__(self,coget,button)
    
    # connect relevant signals
    self.coget.application.connect(
        self.widget,qt.SIGNAL("pressed()"),self._value_changed)
    self.coget.application.connect(
        self.widget,qt.SIGNAL("released()"),self._value_changed)


  def get_value(self):
    "Get button status"
    return self.widget.isDown()

  def set_value(self,value):
    "Set button status"
    self.widget.setDown(value)


class _ComboBox(WALComboBox):
  "Qt4 ComboBox widget abstractor"

  def __init__(self,coget,combobox):

    WALComboBox.__init__(self,coget,combobox) 

    # connect relevant signals to handlers
    self.coget.application.connect(
        self.widget,qt.SIGNAL("activated(int)"),self._value_changed)


  def get_value(self):
    "Get index of selected item"
    return self.widget.currentIndex()

  def set_value(self,value):
    "Set selected item by its index value"
    self.widget.setCurrentIndex(value)


class _Entry(WALEntry):
  "Qt4 Entry widget abstractor"

  def __init__(self,coget,entry):

    WALEntry.__init__(self,coget,entry)

    # connect relevant signals to handlers
    self.coget.application.connect(
        self.widget,qt.SIGNAL("returnPressed()"),self._value_changed)


  def get_value(self):
    "Get text from Entry"
    return str(self.widget.text())
    
  def set_value(self,value):
    "Set text into Entry"
    self.widget.setText(str(value))
 

class _Label(WALLabel):
  "Qt4 Label widget abstractor"

  def __init__(self,coget,label):

    WALLabel.__init__(self,coget,label)


  def get_value(self):
    "Get text into Label"
    return str(self.widget.text())

  def set_value(self,value):
    "Set text into Label"
    if type(value) == list:
      value = tuple(value)
    self.widget.setText(self.format % value)


class _RadioButton(WALRadioButton):
  "Qt4 RadioButton widget abstractor"

  def __init__(self,coget,radiobutton):

    WALRadioButton.__init__(self,coget,radiobutton) 

    # connect relevant signals
    self.coget.application.connect(
        self.widget,qt.SIGNAL("clicked()"),self._value_changed)

  def get_value(self):
    "Get index of activated button"
    return self.widget.group().checkedId()

  def set_value(self,value):
    "Set activate button indexed by value"
    self.widget.group().buttons()[value].setChecked(True)

  
class _Slider(WALSlider):
  "Qt4 Slider widget abstractor"

  def __init__(self,coget,slider):

    WALSlider.__init__(self,coget,slider) 

    # connect relevant signals to handlers
    self.coget.application.connect(
        self.widget,qt.SIGNAL("valueChanged(int)"),self._value_changed)
 

  def get_value(self):
    "Get Slider value"
    return self.widget.value()

  def set_value(self,value):
    "Set Slider value"
    self.widget.setValue(value)


class _SpinButton(WALSpinButton):
  "Qt4 SpinButton widget abstractor"

  def __init__(self,coget,spinbutton):

    WALSpinButton.__init__(self,coget,spinbutton) 

    # connect relevant signals to handlers

    # QSpinBox manages integers, while QDoubleSpinBox manages floats
    if self.widget.__class__ == qt.QSpinBox:
      SIGNAL_NAME = "valueChanged(int)"
    else:
      SIGNAL_NAME = "valueChanged(double)"

    self.coget.application.connect(
        self.widget,qt.SIGNAL(SIGNAL_NAME),self._value_changed)
 

  def get_value(self):
    "Get spinbutton value"
    return self.widget.value()

  def set_value(self,value):
    "Set spinbutton value"
    self.widget.setValue(value)


class _TextView(WALTextView):
  "Qt4 TextView/Edit widget abstractor"

  def __init__(self,coget,textview):

    WALTextView.__init__(self,coget,textview)

    # connect relevant signals
    self.coget.application.connect(
        self.widget,qt.SIGNAL("textChanged()"),self._value_changed)


  def get_value(self):
    "Get text from TextView"
    return str(self.widget.toPlainText())
    
  def set_value(self,value):
    "Set text into TextView"
    self.widget.setPlainText(str(value))


class _ToggleButton(WALToggleButton):
  "Qt4 ToggleButton widget abstractor"

  def __init__(self,coget,togglebutton):

    WALToggleButton.__init__(self,coget,togglebutton)

    # connect relevant signals
    self.coget.application.connect(
        self.widget,qt.SIGNAL("clicked()"),self._value_changed)


  def get_value(self):
    "Get button status"
    return self.widget.isChecked()

  def set_value(self,value):
    "Set button status"
    self.widget.setChecked(value)


#### AVC Qt4 interface

class AVC(AVCCore):
  "AVC Qt4 bindings"

  #### PARAMETERS

  # mapping between the real widget and the wal widget
  _WIDGETS_MAP = { \
  qt.QPushButton:	_Button, \
  qt.QCheckBox:		_ToggleButton, \
  qt.QComboBox:		_ComboBox, \
  qt.QLineEdit:		_Entry, \
  qt.QLabel:		_Label, \
  qt.QRadioButton:	_RadioButton, \
  qt.QSlider:		_Slider, \
  qt.QSpinBox:		_SpinButton, \
  qt.QDoubleSpinBox:	_SpinButton, \
  qt.QTextEdit:		_TextView}


  #### METHODS

  def _top_level_widgets(self):
    "Return the list of all top level widgets"
    return qt.QApplication.topLevelWidgets()

  def avc_init(self,view_period=0.1):
    "Init and start all AVC activities"
    # get all top level widgets and store them
    self._toplevel_widgets = self._top_level_widgets()
    # do common init
    AVCCore.avc_init(self,view_period)

  def _widget_children(self,widget):
    "Return the list of all children of the widget"
    return widget.children()

  def _widget_name(self,widget):
    "Return the widget name"
    return str(widget.objectName())

  def _null_writer(self,widget,value):
    "The widget null writer"
    pass

  def avc_timer(self,function,period):
    "Start a Qt timer calling back 'function' every 'period' seconds."
    self._timer_function = function
    self._timer = qt.QTimer(self)
    self.connect(self._timer,qt.SIGNAL("timeout()"),self._timer_wrap)
    self._timer.start(int(period * 1000.0))
    return

  def _timer_wrap(self):
    "Qt dont like calls to iterators, so wrap for this case."
    self._timer_function()


#### END
