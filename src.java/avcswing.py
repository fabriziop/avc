# .+
# .context    : Application View Controller
# .title      : AVC SWING bindings
# .kind	      : python source
# .author     : Fabrizio Pollastri
# .site	      : Revello - Italy
# .creation   :	18-Nov-2007
# .copyright  :	(c) 2007 Fabrizio Pollastri
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

from java import awt		# awt tool kit bindings
from javax import swing		# swing tool kit bindings


#### GENERAL ABSTRACTION METHODS

def toplevel_widgets():
  "Return the list of all top level widgets"
  return awt.Frame.getFrames().tolist()

def init(*args,**kwargs):
  "Do init specific for this widget toolkit"
  pass

def widget_children(widget):
  "Return the list of all children of the widget"
  # Widgets that are not a subclass of gtk.Container have no children.
  if isinstance(widget,awt.Container):
    return widget.components.tolist()
  else:
    return []

def widget_name(widget):
  "Return the widget name"
  widgetname = widget.getName()
  if not widgetname:
    widgetname = '<unnamed>'
  return widgetname

def timer(function,period):
  """
  Start a GTK timer calling back 'function' every 'period' seconds.
  Return timer id.
  """
  return gobject.timeout_add(int(period * 1000.0),self._timer_wrap,function)

def timer_wrap(function):
  "Call given function and return True to keep timer alive"
  function()
  return True

def avc_timer_delete(self,timer_id):
  "Stop timer with id = timer_id"
  gobject.source_remove(timer_id)


#### WIDGETS ABSTRACTION LAYER (widget toolkit side)

class Widget:
  "Widget Abstraction Layer abstract class"

  def __init__(self,allowed_types=None):
    # check for supported control type
    if allowed_types and not self.connection.control_type in allowed_types:
      raise error, "Control type '%s' not supported with '%s' widget" % \
        (self.connection.control_type.__name__,self.widget.__class__.__name__)

  def connect_delete(self,widget,delete_method):
    "Connect widget delete method to destroy event"
    widget.connect("destroy",delete_method)
 


class Button(Widget):
  "GTK Button widget abstractor"

  def __init__(self):
    # connect relevant signals
    self.widget.actionPerformed(self._value_changed)

  def get_value(self):
    "Get button status"
    return self.widget.selected

  def set_value(self,value):
    "Set button status"
    if value:
      self.widget.selected = 1
    else:
      self.widget.selected = 0 


class ComboBox(Widget):
  "GTK ComboBox widget abstractor"

  def __init__(self):
    # connect relevant signals
    self.widget.connect("changed",self._value_changed)

  def get_value(self):
    "Get index of selected item"
    return self.widget.get_active()

  def set_value(self,value):
    "Set selected item by its index value"
    self.widget.set_active(value)


class Entry(Widget):
  "GTK Entry widget abstractor"

  def __init__(self):
    # connect relevant signals to handlers
    self.widget.connect("activate",self._value_changed)

  def get_value(self):
    "Get text from Entry"
    return self.coget.control_type(self.widget.get_text())
    
  def set_value(self,value):
    "Set text into Entry"
    self.widget.set_text(str(value))
 

class Label(Widget):
  "GTK Label widget abstractor"

  def __init__(self):
    pass

  def get_value(self):
    "Get value from Label"
    # first try to coerce to control type
    try:
      return self.coget.control_type(self.widget.text)
    # if fail, return value as string, needed for initial get of format string.
    except:
      return self.widget.text

  def set_value(self,value):
    "Set text into Label"
    if type(value) == list:
      value = tuple(value)
    self.widget.text = self.format % value


class ProgressBar(Widget):
  "GTK ProgressBar widget abstractor"
  pass


class RadioButton(Widget):
  "GTK RadioButton widget abstractor"

  def __init__(self):
    # connect relevant signals
    self.widget.connect("clicked",self._value_changed)

  def get_value(self):
    "Get index of activated button"
    button = self.widget
    buttons = button.get_group()
    for index,rbutton in enumerate(buttons):
      if rbutton.get_active():
        break
    index = len(buttons) - index - 1
    return index

  def set_value(self,value):
    "Set activate button indexed by value"
    button = self.widget
    rbuttons = button.get_group()
    rbutton = rbuttons[len(rbuttons) - value - 1]
    rbutton.set_active(True)


class Slider(Widget):
  "GTK Slider widget abstractor"

  def __init__(self):
    # connect relevant signals to handlers
    self.widget.connect("value_changed",self._value_changed)
 
  def get_value(self):
    "Get Slider value"
    return self.coget.control_type(self.widget.get_value())

  def set_value(self,value):
    "Set Slider value"
    self.widget.set_value(value)


class SpinButton(Widget):
  "GTK SpinButton widget abstractor"

  def __init__(self,coget,spinbutton):
    # connect relevant signals to handlers
    self.widget.actionPerformed(self._value_changed)

  def get_value(self):
    "Get spinbutton value"
    return self.coget.control_type(self.widget.value)

  def set_value(self,value):
    "Set spinbutton value"
    self.widget.value = value


class StatusBar(Widget):
  "GTK StatusBar widget abstractor"

  def __init__(self):
    pass

  def set_value(self,value):
    "Set StatusBar value"
    self.widget.pop(1)
    self.widget.push(1,value)


class TextView(Widget):
  "GTK TextView widget abstractor"

  def __init__(self):
    # connect relevant signals to handlers
    self.widget.get_buffer().connect("changed",self._value_changed)

  def get_value(self):
    "Get text from TextView"
    textbuf = self.widget.get_buffer()
    return textbuf.get_text(textbuf.get_start_iter(),textbuf.get_end_iter())
    
  def set_value(self,value):
    "Set text into TextView"
    self.widget.get_buffer().set_text(str(value))


class ToggleButton(Widget):
  "GTK ToggleButton widget abstractor"

  def __init__(self):
    # connect relevant signals
    self.widget.connect("clicked",self._value_changed)

  def get_value(self):
    "Get button status"
    return self.widget.get_active()

  def set_value(self,value):
    "Set button status"
    self.widget.set_active(value)


class TreeView(Widget):
  "GTK TreeView widget abstractor"
  pass


## mapping between the real widget and the wal widget

WIDGETS_MAP = { \
  swing.JButton:	'Button', \
  swing.JCheckBox:	'ToggleButton', \
  swing.JComboBox:	'ComboBox',\
####  gtk.Entry:		'Entry', \
  swing.JLabel:		'Label', \
  swing.JRadioButton:	'RadioButton', \
  swing.JSlider:	'Slider', \
  swing.JSpinner:	'SpinButton', \
####  gtk.Statusbar:	'StatusBar', \
  swing.JTextArea:	'TextView'}
 
#### END
