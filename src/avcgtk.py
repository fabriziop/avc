# .+
# .context    : Application View Controller
# .title      : AVC GTK bindings
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

import gtk			# gimp tool kit bindings
import gobject			# gimp tool kit bindings

from avc.avccore import *	# AVC core


#### AVC GTK INTERFACE

class AVC(AVCCore):
  "AVC GTK binding"

  _binding = 'GTK'


  #### GENERAL ABSTRACTION METHODS

  def _top_level_widgets(self):
    "Return the list of all top level widgets"
    return gtk.window_list_toplevels()

  def avc_init(self,*args,**kwargs):
    "Init and start all AVC activities"
    # get all top level widgets and store them
    self._toplevel_widgets = self._top_level_widgets()
    # do common init
    AVCCore.avc_init(self,*args,**kwargs)

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


  #### WIDGETS ABSTRACTION LAYER (widget toolkit side)

  class _Button(AVCCore._Button):
    "GTK Button real widget abstractor"

    def _init(self):

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


  class _ComboBox(AVCCore._ComboBox):
    "GTK ComboBox widget abstractor"

    def _init(self):

      # connect relevant signals
      self.widget.connect("changed",self._value_changed)


    def get_value(self):
      "Get index of selected item"
      return self.widget.get_active()

    def set_value(self,value):
      "Set selected item by its index value"
      self.widget.set_active(value)


  class _Entry(AVCCore._Entry):
    "GTK Entry widget abstractor"

    def _init(self):

      # connect relevant signals to handlers
      self.widget.connect("activate",self._value_changed)


    def _get_value(self):
      "Get text from Entry"
      return self.widget.get_text()
    
    def set_value(self,value):
      "Set text into Entry"
      self.widget.set_text(str(value))
 

  class _Label(AVCCore._Label):
    "GTK Label widget abstractor"

    def _get_value(self):
      "Get value from Label"
      return self.widget.get_label()

    def _set_value(self,value):
      "Set text into Label"
      self.widget.set_label(value)


  class _RadioButton(AVCCore._RadioButton):
    "GTK RadioButton widget abstractor"

    def _init(self):

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


  class _Slider(AVCCore._Slider):
    "GTK Slider widget abstractor"

    def _init(self):

      # connect relevant signals to handlers
      self.widget.connect("value_changed",self._value_changed)
 

    def _get_value(self):
      "Get Slider value"
      return self.widget.get_value()

    def set_value(self,value):
      "Set Slider value"
      self.widget.set_value(value)


  class _SpinButton(AVCCore._SpinButton):
    "GTK SpinButton widget abstractor"

    def _init(self):

      # connect relevant signals to handlers
      self.widget.connect("value_changed",self._value_changed)
 

    def _get_value(self):
      "Get spinbutton value"
      return self.widget.get_value()

    def set_value(self,value):
      "Set spinbutton value"
      self.widget.set_value(value)


  class _StatusBar(AVCCore._StatusBar):
    "GTK StatusBar widget abstractor"

    def set_value(self,value):
      "Set StatusBar value"
      self.widget.pop(1)
      self.widget.push(1,value)


  class _TextView(AVCCore._TextView):
    "GTK TextView widget abstractor"

    def _init(self):

      # connect relevant signals to handlers
      self.widget.get_buffer().connect("changed",self._value_changed)


    def get_value(self):
      "Get text from TextView"
      textbuf = self.widget.get_buffer()
      return textbuf.get_text(textbuf.get_start_iter(),textbuf.get_end_iter())
    
    def set_value(self,value):
      "Set text into TextView"
      self.widget.get_buffer().set_text(str(value))


  class _ToggleButton(AVCCore._ToggleButton):
    "GTK ToggleButton widget abstractor"

    def _init(self):

      # connect relevant signals
      self.widget.connect("clicked",self._value_changed)


    def get_value(self):
      "Get button status"
      return self.widget.get_active()

    def set_value(self,value):
      "Set button status"
      self.widget.set_active(value)


  ## mapping between the real widget and the wal widget

  _WIDGETS_MAP = { \
  gtk.Button:		_Button, \
  gtk.CheckButton:	_ToggleButton, \
  gtk.ComboBox:		_ComboBox,\
  gtk.Entry:		_Entry, \
  gtk.Label:		_Label, \
  gtk.RadioButton:	_RadioButton, \
  gtk.HScale:		_Slider, \
  gtk.SpinButton:	_SpinButton, \
  gtk.Statusbar:	_StatusBar, \
  gtk.TextView:		_TextView, \
  gtk.ToggleButton:	_ToggleButton, \
  gtk.VScale:		_Slider}
 
#### END
