# .+
# .context    : Application View Controller
# .title      : AVC wx bindings
# .kind	      : python source
# .author     : Fabrizio Pollastri
# .site	      : Torino - Italy
# .creation   :	23-Nov-2007
# .copyright  :	(c) 2007-2008 Fabrizio Pollastri
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

import wx			# wx tool kit bindings


#### GENERAL ABSTRACTION METHODS

def toplevel_widgets():
  "Return the list of all top level widgets"
  return [wx.GetApp().GetTopWindow()]

def init(*args,**kwargs):
  "Do init specific to this widget toolkit"
  pass

def widget_children(widget):
  "Return the list of all children of the widget"
  # Widgets that are not a subclass of gtk.Container have no children.
  if isinstance(widget,wx.Window):
    return widget.GetChildren()
  else:
    return []

def widget_name(widget):
  "Return the widget name"
  return widget.GetName()

def timer(function,period):
  "Create and start a timer calling 'function' every 'period' time"
  first_toplevel = toplevel_widgets()[0]
  timer = wx.Timer(first_toplevel,wx.NewId())
  first_toplevel.Bind(wx.EVT_TIMER,lambda event: function(),timer)
  timer.Start(int(period * 1000.0),oneShot=False)
  return timer


#### WIDGETS ABSTRACTION LAYER (widget toolkit side)

class Widget:
  "wx Widget Abstraction Layer abstract class"

  def connect_delete(self,widget,delete_method):
    "Connect widget delete method to wondow destroy event"
    widget.Bind(wx.EVT_WINDOW_DESTROY,delete_method)


class Button(Widget):
  "wx Button widget abstractor"

  def __init__(self):
    # create button press status variable
    self.widget.value = False
    # connect relevant signals
    self.widget.Bind(wx.EVT_LEFT_DOWN,
      lambda event: wx.CallAfter(
      lambda: self.connection.coget.__set__(
        '',True,self.widget,self.connection))
      or event.Skip())
    self.widget.Bind(wx.EVT_LEFT_UP,
      lambda event: wx.CallAfter(
      lambda: self.connection.coget.__set__(
        '',False,self.widget,self.connection))
      or event.Skip())

  def read(self):
    "Get button status"
    return self.widget.value

  def write(self,value):
    "Set button status"
    self.widget.value = value


class ComboBox(Widget):
  "wx ComboBox widget abstractor"

  def __init__(self):
    # connect relevant signals
    if self.widget.__class__ == wx.ComboBox:
      event_type = wx.EVT_COMBOBOX
    else:
      event_type = wx.EVT_CHOICE
    self.widget.Bind(event_type,self.value_changed)

  def read(self):
    "Get index of selected item"
    return self.widget.GetSelection()

  def write(self,value):
    "Set selected item by its index value"
    self.widget.SetSelection(value)


class Entry(Widget):
  "wx Entry widget abstractor"

  def __init__(self):
    # create entry text value variable
    self.widget.value =  self.widget.GetValue()
    # connect relevant signals
    self.widget.Bind(wx.EVT_TEXT,self.value_changed)

  def read(self):
    "Get text from Entry"
    text = self.widget.GetValue()
    # when TextCtrl text is set by program, the event EVT_TEXT is
    # triggered twice: first time with an empty string, second time with
    # the correct value. Substitute first (wrong) value with the old one.
    if text:
      return text
    else:
      return self.widget.value
    
  def write(self,value):
    "Set text into Entry"
    self.widget.SetValue(str(value))
    self.widget.value = str(value)
 

class Label(Widget):
  "wx Label widget abstractor"

  def __init__(self):
    pass

  def read(self):
    "Get value from Label"
    return self.widget.GetLabel()

  def write(self,value):
    "Set text into Label"
    self.widget.SetLabel(value)


class RadioButton(Widget):
  "wx RadioButton widget abstractor"

  def __init__(self):
    # connect relevant signals
    if self.widget.__class__ == wx.RadioBox:
      event_type = wx.EVT_RADIOBOX
    else:
      event_type = wx.EVT_RADIOBUTTON
    self.widget.Bind(event_type,self.value_changed)

  def read(self):
    "Get index of activated button"
    return self.widget.GetSelection()

  def write(self,value):
    "Set activate button indexed by value"
    self.widget.SetSelection(value)


class Slider(Widget):
  "wx Slider widget abstractor"

  def __init__(self):
    # connect relevant signals
    self.widget.Bind(wx.EVT_LEFT_UP,
      lambda event: wx.CallAfter(self.value_changed) or event.Skip())
 
  def read(self):
    "Get Slider value"
    return self.widget.GetValue()

  def write(self,value):
    "Set Slider value"
    self.widget.SetValue(value)


class SpinButton(Widget):
  "wx SpinButton widget abstractor"

  def __init__(self):
    # connect relevant signals to handlers
    wx.EVT_SPINCTRL(self.widget,self.widget.GetId(),self.value_changed)


  def read(self):
    "Get spinbutton value"
    return self.widget.GetValue()

  def write(self,value):
    "Set spinbutton value"
    self.widget.SetValue(value)


class StatusBar(Widget):
  "wx StatusBar widget abstractor"

  def __init__(self):
    pass

  def write(self,value):
    "Set StatusBar value (only field 1)"
    self.widget.SetStatusText(value)


class TextView(Widget):
  "wx TextView widget abstractor"

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
  "wx ToggleButton widget abstractor"

  def __init__(self):
    # connect relevant signals
    if self.widget.__class__ == wx.CheckBox:
      event_type = wx.EVT_CHECKBOX
    else:
      event_type = wx.EVT_TOGGLEBUTTON
    self.widget.Bind(event_type,self.value_changed)

  def read(self):
    "Get button status"
    return bool(self.widget.GetValue())

  def write(self,value):
    "Set button status"
    self.widget.SetValue(value)


## mapping between the real widget and the wal widget

WIDGETS_MAP = { \
  wx.BitmapButton:	'Button', \
  wx.Button:		'Button', \
  wx.CheckBox:		'ToggleButton', \
  wx.ComboBox:		'ComboBox',\
  wx.Choice:		'ComboBox',\
  wx.RadioBox:		'RadioButton', \
  wx.Slider:		'Slider', \
  wx.SpinCtrl:		'SpinButton', \
  wx.StaticText:	'Label', \
  wx.StatusBar:		'StatusBar',
  wx.TextCtrl:		'Entry',
  wx.ToggleButton:	'ToggleButton'}
 
#### END
