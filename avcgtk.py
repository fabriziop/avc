#!/usr/bin/python
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

import gtk			# gimp tool kit bindings
import gobject			# gimp tool kit bindings

from avc.avccore import *	# AVC core


#### WIDGETS ABSTRACTION LAYER (widget toolkit side)

class _Button(WALButton):
  "GTK Button widget abstractor"

  def __init__(self,coget,button):

    WALButton.__init__(self,coget,button)
    
    # connect relevant signals
    self.widget.connect("pressed",self._value_changed)
    self.widget.connect("released",self._value_changed)


  def get_value(self):
    "Get button status"
    if self.widget.state == gtk.STATE_ACTIVE:
      return True
    return False

  def set_value(self,value):
    "Set button status"
    if value:
      self.widget.set_state(gtk.STATE_ACTIVE)
    else:
      self.widget.set_state(gtk.STATE_NORMAL)


class _Entry(WALEntry):
  "GTK Entry widget abstractor"

  def __init__(self,coget,entry):

    WALEntry.__init__(self,coget,entry)

    # connect relevant signals to handlers
    self.widget.connect("activate",self._value_changed)


  def get_value(self):
    "Get text from Entry"
    return self.widget.get_text()
    
  def set_value(self,value):
    "Set text into Entry"
    self.widget.set_text(str(value))
  

class _Label(WALLabel):
  "GTK Label widget abstractor"

  def __init__(self,coget,label):

    WALLabel.__init__(self,coget,label)


  def get_value(self):
    "Get text into Label"
    return self.widget.get_label()

  def set_value(self,value):
    "Set text into Label"
    if type(value) == list:
      value = tuple(value)
    self.widget.set_label(self.format % value)


class _RadioButton(WALRadioButton):
  "GTK RadioButton widget abstractor"

  def __init__(self,coget,radiobutton):

    WALRadioButton.__init__(self,coget,radiobutton) 

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


class _SpinButton(WALSpinButton):
  "GTK SpinButton widget abstractor"

  def __init__(self,coget,spinbutton):

    WALSpinButton.__init__(self,coget,spinbutton) 

    # connect relevant signals to handlers
    self.widget.connect("value_changed",self._value_changed)
 

  def get_value(self):
    "Get spinbutton value"
    return self.widget.get_value()

  def set_value(self,value):
    "Set spinbutton value"
    self.widget.set_value(value)


class _ToggleButton(WALToggleButton):
  "GTK ToggleButton widget abstractor"

  def __init__(self,coget,togglebutton):

    WALToggleButton.__init__(self,coget,togglebutton)

    # connect relevant signals
    self.widget.connect("clicked",self._value_changed)


  def get_value(self):
    "Get button status"
    return self.widget.get_active()

  def set_value(self,value):
    "Set button status"
    self.widget.set_active(value)


#### AVC GTK interface

class AVC(AVCCore):
  "AVC GTK binding"

  #### PARAMETERS

  # mapping between the real widget and the wal widget
  _WIDGETS_MAP = { \
  gtk.Button: _Button, \
  gtk.CheckButton: _ToggleButton, \
  gtk.Entry: _Entry, \
  gtk.Label: _Label, \
  gtk.RadioButton: _RadioButton, \
  gtk.SpinButton: _SpinButton, \
  gtk.ToggleButton: _ToggleButton}
 

  #### METHODS

  def avc_init(self,view_period=0.1):

    AVCCore.avc_init(self,view_period)


  def _top_level_widgets(self):
    "Return the list of all top level widgets known to pygtk"
    return gtk.window_list_toplevels()

  def _widget_children(self,widget):
    "Return the list of all children of the widget"
    # Widgets that are not a subclass of gtk.Container have no children.
    if isinstance(widget,gtk.Container):
      return widget.get_children()
    else:
      return []

  def _widget_name(self,widget):
    "Return the widget name"
    return widget.get_name()

  def _null_writer(self,widget,value):
    "The widget null writer"
    pass

  def avc_timer(self,function,period):
    """
    Start a GTK timer calling back 'function' every 'period' seconds.
    Return timer id.
    """
    return gobject.timeout_add(int(period * 1000.0),self._timer_wrap,function)

  def _timer_wrap(self,function):
    "Call given function and return True to keep timer alive"
    function()
    return True

  def avc_timer_delete(self,timer_id):
    "Stop timer with id = timer_id"
    gobject.source_remove(timer_id)


#### END
