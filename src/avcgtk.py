# .+
# .context    : Application View Controller
# .title      : AVC GTK+ bindings
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

import gtk			#--
import gobject			#- gimp tool kit bindings


#### GENERAL ABSTRACTION METHODS

def toplevel_widgets():
  "Return the list of all top level widgets"
  return gtk.window_list_toplevels()

def init(*args,**kwargs):
  "Do init specific for this widget toolkit"
  pass

def widget_children(widget):
  "Return the list of all children of the widget"
  # Widgets that are not a subclass of gtk.Container have no children.
  if isinstance(widget,gtk.Container):
    return widget.get_children()
  else:
    return []

def widget_name(widget):
  "Return the widget name"
  return widget.get_name()

def timer(function,period):
  """
  Start a GTK timer calling back 'function' every 'period' seconds.
  Return timer id.
  """
  return gobject.timeout_add(int(period * 1000.0),timer_wrap,function)

def timer_wrap(function):
  "Call given function and return True to keep timer alive"
  function()
  return True


#### WIDGETS ABSTRACTION LAYER (widget toolkit side)

class Widget:
  "GTK Widget Abstraction Layer abstract class"

  def connect_delete(self,widget,delete_method):
    "Connect widget delete method to destroy event"
    widget.connect("destroy",delete_method)
 

class Button(Widget):
  "GTK Button real widget abstractor"

  def __init__(self):
    # connect relevant signals
    self.widget.connect("pressed",self.value_changed)
    self.widget.connect("released",self.value_changed)

  def read(self):
    "Get button status"
    if self.widget.state == gtk.STATE_ACTIVE:
      return True
    return False

  def write(self,value):
    "Set button status"
    if value:
      self.widget.set_state(gtk.STATE_ACTIVE)
    else:
      self.widget.set_state(gtk.STATE_NORMAL)


class ComboBox(Widget):
  "GTK ComboBox widget abstractor"

  def __init__(self):
    # connect relevant signals
    self.widget.connect("changed",self.value_changed)

  def read(self):
    "Get index of selected item"
    return self.widget.get_active()

  def write(self,value):
    "Set selected item by its index value"
    self.widget.set_active(value)


class Entry(Widget):
  "GTK Entry widget abstractor"

  def __init__(self):
    # connect relevant signals to handlers
    self.widget.connect("activate",self.value_changed)

  def read(self):
    "Get text from Entry"
    return self.widget.get_text()
    
  def write(self,value):
    "Set text into Entry"
    self.widget.set_text(str(value))
 

class Label(Widget):
  "GTK Label widget abstractor"

  def __init__(self):
    pass

  def read(self):
    "Get value from Label"
    return self.widget.get_label()

  def write(self,value):
    "Set text into Label"
    self.widget.set_label(value)


class RadioButton(Widget):
  "GTK RadioButton widget abstractor"

  def __init__(self):
    # connect relevant signals
    self.widget.connect("clicked",self.value_changed)

  def read(self):
    "Get index of activated button"
    button = self.widget
    buttons = button.get_group()
    for index,rbutton in enumerate(buttons):
      if rbutton.get_active():
        break
    index = len(buttons) - index - 1
    return index

  def write(self,value):
    "Set activate button indexed by value"
    button = self.widget
    rbuttons = button.get_group()
    rbutton = rbuttons[len(rbuttons) - value - 1]
    rbutton.set_active(True)


class Slider(Widget):
  "GTK Slider widget abstractor"

  def __init__(self):
    # connect relevant signals to handlers
    self.widget.connect("value_changed",self.value_changed)

  def read(self):
    "Get Slider value"
    return self.widget.get_value()

  def write(self,value):
    "Set Slider value"
    self.widget.set_value(value)


class SpinButton(Widget):
  "GTK SpinButton widget abstractor"

  def __init__(self):
    # connect relevant signals to handlers
    self.widget.connect("value_changed",self.value_changed)

  def read(self):
    "Get spinbutton value"
    return self.widget.get_value()

  def write(self,value):
    "Set spinbutton value"
    self.widget.set_value(value)


class StatusBar(Widget):
  "GTK StatusBar widget abstractor"

  def __init__(self):
    pass

  def write(self,value):
    "Set StatusBar value"
    self.widget.pop(1)
    self.widget.push(1,value)


class TextView(Widget):
  "GTK TextView widget abstractor"

  def __init__(self):
    # connect relevant signals to handlers
    self.widget.get_buffer().connect("changed",self.value_changed)

  def read(self):
    "Get text from TextView"
    textbuf = self.widget.get_buffer()
    return textbuf.get_text(textbuf.get_start_iter(),textbuf.get_end_iter())
    
  def write(self,value):
    "Set text into TextView"
    self.widget.get_buffer().set_text(str(value))


class ToggleButton(Widget):
  "GTK ToggleButton widget abstractor"

  def __init__(self):
    # connect relevant signals
    self.widget.connect("clicked",self.value_changed)

  def read(self):
    "Get button status"
    return self.widget.get_active()

  def write(self,value):
    "Set button status"
    self.widget.set_active(value)


## mapping between the real widget and the wal widget

WIDGETS_MAP = { \
  gtk.Button:		'Button', \
  gtk.CheckButton:	'ToggleButton', \
  gtk.ComboBox:		'ComboBox',\
  gtk.Entry:		'Entry', \
  gtk.Label:		'Label', \
  gtk.RadioButton:	'RadioButton', \
  gtk.HScale:		'Slider', \
  gtk.SpinButton:	'SpinButton', \
  gtk.Statusbar:	'StatusBar', \
  gtk.TextView:		'TextView', \
  gtk.ToggleButton:	'ToggleButton', \
  gtk.VScale:		'Slider'}
 
#### END
