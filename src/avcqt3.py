# .+
# .context    : Application View Controller
# .title      : AVC Qt3 bindings
# .kind	      : python source
# .author     : Fabrizio Pollastri
# .site	      : Revello - Italy
# .creation   :	7-Nov-2006
# .copyright  :	(c) 2006-2008 Fabrizio Pollastri
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
# along with AVC.  If not, see <http://www.gnu.org/licenses/>.
#
# .-

 
#### IMPORT REQUIRED MODULES

import qt			# Qt tool kit bindings


#### GENERAL ABSTRACTION METHODS

def toplevel_widgets():
  "Return the list of all top level widgets"
  return qt.QApplication.topLevelWidgets()

def init(*args,**kwargs):
  "Do init specific for this widget toolkit"
  pass

def widget_children(widget):
  "Return the list of all children of the widget"
  return widget.children() or []

def widget_name(widget):
  "Return the widget name"
  return widget.name()

def timer(function,period):
  "Start a Qt timer calling back 'function' every 'period' seconds."
  timer = qt.QTimer()
  qt.QObject.connect(timer,qt.SIGNAL("timeout()"),function)
  timer.start(int(period * 1000.0))
  return timer


#### WIDGETS ABSTRACTION LAYER (widget toolkit side)

class Widget:
  "Qt3 Widget Abstraction Layer abstract class"

  def connect_delete(self,widget,delete_method):
    "Connect widget delete method to destroy event"
    qt.QObject.connect(widget,qt.SIGNAL("destroyed()"),delete_method)
		       

class Button(Widget):
  "Qt3 Button widget abstractor"

  def __init__(self):
    # connect relevant signals
    qt.QObject.connect(
      self.widget,qt.SIGNAL("pressed()"),self.value_changed)
    qt.QObject.connect(
      self.widget,qt.SIGNAL("released()"),self.value_changed)

  def read(self):
    "Get button status"
    return self.widget.isDown()

  def write(self,value):
    "Set button status"
    self.widget.setDown(value)


class ComboBox(Widget):
  "Qt3 ComboBox widget abstractor"

  def __init__(self):
    # connect relevant signals to handlers
    qt.QObject.connect(
      self.widget,qt.SIGNAL("activated(int)"),self.value_changed)

  def read(self):
    "Get index of selected item"
    return self.widget.currentItem()

  def write(self,value):
    "Set selected item by its index value"
    self.widget.setCurrentItem(value)


class Entry(Widget):
  "Qt3 Entry widget abstractor"

  def __init__(self):
    # connect relevant signals to handlers
    qt.QObject.connect(
      self.widget,qt.SIGNAL("returnPressed()"),self.value_changed)

  def read(self):
    "Get text from Entry"
    return self.widget.text()
    
  def write(self,value):
    "Set text into Entry"
    self.widget.setText(str(value))
 

class Label(Widget):
  "Qt3 Label widget abstractor"

  def __init__(self):
    pass

  def read(self):
    "Get text into Label"
    return str(self.widget.text())

  def write(self,value):
    "Set text into Label"
    self.widget.setText(value)


class RadioButton(Widget):
  "Qt3 RadioButton widget abstractor"

  def __init__(self):
    # connect relevant signals
    qt.QObject.connect(
      self.widget,qt.SIGNAL("clicked()"),self.value_changed)

  def read(self):
    "Get index of activated button"
    return self.widget.group().selectedId()

  def write(self,value):
    "Set activate button indexed by value"
    self.widget.group().setButton(value)

 
class Slider(Widget):
  "Qt3 Slider widget abstractor"

  def __init__(self):
    # connect relevant signals to handlers
    qt.QObject.connect(
      self.widget,qt.SIGNAL("valueChanged(int)"),self.value_changed)
 
  def read(self):
    "Get Slider value"
    return self.widget.value()

  def write(self,value):
    "Set Slider value"
    self.widget.setValue(value)


class SpinButton(Widget):
  "Qt3 SpinButton widget abstractor"

  def __init__(self):
    # connect relevant signals to handlers
    qt.QObject.connect(
      self.widget,qt.SIGNAL("valueChanged(int)"),self.value_changed)
 
  def read(self):
    "Get spinbutton value"
    return self.widget.value()

  def write(self,value):
    "Set spinbutton value"
    self.widget.setValue(value)


class StatusBar(Widget):
  "Qt3 no status bar support"
  pass


class TextView(Widget):
  "Qt3 TextView/Edit widget abstractor"

  def __init__(self):
    # connect relevant signals
    qt.QObject.connect(
      self.widget,qt.SIGNAL("returnPressed()"),self.value_changed)

  def read(self):
    "Get text from TextView"
    return str(self.widget.text())
    
  def write(self,value):
    "Set text into TextView"
    self.widget.setText(str(value))
 

class ToggleButton(Widget):
  "Qt3 ToggleButton widget abstractor"

  def __init__(self):
    # connect relevant signals
    qt.QObject.connect(
      self.widget,qt.SIGNAL("clicked()"),self.value_changed)

  def read(self):
    "Get button status"
    return self.widget.isChecked()

  def write(self,value):
    "Set button status"
    self.widget.setChecked(value)


## mapping between real widget and the wal widget

WIDGETS_MAP = { \
  qt.QPushButton:	'Button', \
  qt.QCheckBox:		'ToggleButton', \
  qt.QComboBox:		'ComboBox', \
  qt.QLineEdit:		'Entry', \
  qt.QLabel:		'Label', \
  qt.QRadioButton:	'RadioButton', \
  qt.QSlider:		'Slider', \
  qt.QSpinBox:		'SpinButton', \
  qt.QTextEdit:		'TextView'}

#### END
