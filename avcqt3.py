#!/usr/bin/python2.4
# .+
# .identifier :	$Id:$
# .context    : Application View Controller
# .title      : AVC GTK bindings
# .kind	      : python source
# .author     : Fabrizio Pollastri
# .site	      : Revello - Italy
# .creation   :	7-Nov-2006
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


#### IMPORT REQUIRED MODULES

import qt			# Qt tool kit bindings

from avc.avccore import *	# AVC core


#### WIDGETS ABSTRACTION LAYER (widget toolkit side)

class _Button(WALButton):
  "Qt Button widget abstractor"

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


class _Entry(WALEntry):
  "Qt Entry widget abstractor"

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
  "Qt Label widget abstractor"

  def __init__(self,coget,label):

    WALLabel.__init__(self,coget,label)


  def get_value(self):
    "Get text into Label"
    return self.widget.text()

  def set_value(self,value):
    "Set text into Label"
    if type(value) == list:
      value = tuple(value)
    self.widget.setText(self.format % value)


class _RadioButton(WALRadioButton):
  "Qt RadioButton widget abstractor"

  def __init__(self,coget,radiobutton):

    WALRadioButton.__init__(self,coget,radiobutton) 

    # connect relevant signals
    self.coget.application.connect(
        self.widget,qt.SIGNAL("clicked()"),self._value_changed)

  def get_value(self):
    "Get index of activated button"
    return self.widget.group().selectedId()

  def set_value(self,value):
    "Set activate button indexed by value"
    self.widget.group().setButton(value)

 
class _SpinButton(WALSpinButton):
  "Qt SpinButton widget abstractor"

  def __init__(self,coget,spinbutton):

    WALSpinButton.__init__(self,coget,spinbutton) 

    # connect relevant signals to handlers
    self.coget.application.connect(
        self.widget,qt.SIGNAL("valueChanged(int)"),self._value_changed)
 

  def get_value(self):
    "Get spinbutton value"
    return self.widget.value()

  def set_value(self,value):
    "Set spinbutton value"
    self.widget.setValue(value)


class _ToggleButton(WALToggleButton):
  "Qt ToggleButton widget abstractor"

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


#### AVC Qt interface

class AVC(AVCCore):
  "AVC GTK bindings"

  #### PARAMETERS

  # mapping between the real widget and the wal widget
  _WIDGETS_MAP = { \
  qt.QPushButton: _Button, \
  qt.QCheckBox: _ToggleButton, \
  qt.QLineEdit: _Entry, \
  qt.QLabel: _Label, \
  qt.QRadioButton: _RadioButton, \
  qt.QSpinBox: _SpinButton}
 

  #### METHODS

  def avc_init(self,view_period=0.1):

    AVCCore.avc_init(self,view_period)
	 

  def _top_level_widgets(self):
    "Return the list of all top level widgets"
    return qt.QApplication.topLevelWidgets()

  def _widget_children(self,widget):
    "Return the list of all children of the widget"
    return widget.children() or []

  def _widget_name(self,widget):
    "Return the widget name"
    return widget.name()

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
