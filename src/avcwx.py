# .+
# .context    : Application View Controller
# .title      : AVC wx bindings
# .kind	      : python source
# .author     : Fabrizio Pollastri
# .site	      : Torino - Italy
# .creation   :	23-Nov-2007
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

import wx			# wx tool kit bindings

from avc.avccore import *	# AVC core


#### AVC WX INTERFACE

class AVC(AVCCore):
  "AVC wx binding"

  _binding = 'wxWidgets'


  #### GENERAL ABSTRACTION METHODS

  def _top_level_widgets(self):
    "Return the list of all top level widgets"
    return [self.GetTopWindow()]

  def avc_init(self,*args,**kwargs):
    "Init and start all AVC activities"
    # get all top level widgets and store them
    self._toplevel_widgets = self._top_level_widgets()
    # do common init
    AVCCore.avc_init(self,*args,**kwargs)
    # if a timer is defined, start a timer calling back 'function' every
    # 'period' seconds. Return timer.
    try:
      if self._timer_function:
        self._timer = wx.Timer(self._toplevel_widgets[0],wx.NewId())
        self._toplevel_widgets[0].Bind(wx.EVT_TIMER,self.timer_wrap,self._timer)
        self._timer.Start(int(self._timer_period * 1000.0),oneShot=False)
    except:
      pass

  def _widget_children(self,widget):
    "Return the list of all children of the widget"
    # Widgets that are not a subclass of gtk.Container have no children.
    if isinstance(widget,wx.Window):
      return widget.GetChildren()
    else:
      return []

  def _widget_name(self,widget):
    "Return the widget name"
    return widget.GetName()

  def _null_writer(self,widget,value):
    "The widget null writer"
    pass

  def avc_timer(self,function,period):
    """
    Store timer parameters. Timer is started at avc_init time because "Timer"
    need an instance of root window or widget.
    """
    self._timer_function = function
    self._timer_period = period

  def timer_wrap(self,event):
    "Make room for the unused event argument passed by timerCall"
    self._timer_function()
    return True

  def avc_timer_delete(self,timer):
    "Stop timer"
    timer.Stop()


  #### WIDGETS ABSTRACTION LAYER (widget toolkit side)

  class _Button(AVCCore._Button):
    "wx Button widget abstractor"

    def _init(self):

      # create button press status variable
      self.widget.value = False

      # connect relevant signals
      self.widget.Bind(wx.EVT_LEFT_DOWN,
        lambda event: wx.CallAfter(
        lambda: self.coget.__set__(self,True,self.widget))
        or event.Skip())
      self.widget.Bind(wx.EVT_LEFT_UP,
        lambda event: wx.CallAfter(
        lambda: self.coget.__set__(self,False,self.widget))
        or event.Skip())


    def get_value(self):
      "Get button status"
      return self.widget.value

    def set_value(self,value):
      "Set button status"
      self.widget.value = value


  class _ComboBox(AVCCore._ComboBox):
    "wx ComboBox widget abstractor"

    def _init(self):

      # connect relevant signals
      if self.widget.__class__ == wx.ComboBox:
        event_type = wx.EVT_COMBOBOX
      else:
        event_type = wx.EVT_CHOICE
      self.widget.Bind(event_type,self._value_changed)


    def get_value(self):
      "Get index of selected item"
      return self.widget.GetSelection()

    def set_value(self,value):
      "Set selected item by its index value"
      self.widget.SetSelection(value)


  class _Entry(AVCCore._Entry):
    "wx Entry widget abstractor"

    def _init(self):

      # create entry text value variable
      self.widget.value =  self.widget.GetValue()

      # connect relevant signals
      self.widget.Bind(wx.EVT_TEXT,self._value_changed)


    def _get_value(self):
      "Get text from Entry"
      text = self.widget.GetValue()
      # when TextCtrl text is set by program, the event EVT_TEXT is
      # triggered twice: first time with an empty string, second time with
      # the correct value. Substitute first (wrong) value with the old one.
      if text:
        return text
      else:
        return self.widget.value
    
    def set_value(self,value):
      "Set text into Entry"
      self.widget.SetValue(str(value))
      self.widget.value = str(value)
 

  class _Label(AVCCore._Label):
    "wx Label widget abstractor"

    def _get_value(self):
      "Get value from Label"
      return self.widget.GetLabel()

    def _set_value(self,value):
      "Set text into Label"
      self.widget.SetLabel(value)


  class _RadioButton(AVCCore._RadioButton):
    "wx RadioButton widget abstractor"

    def _init(self):

      # connect relevant signals
      if self.widget.__class__ == wx.RadioBox:
        event_type = wx.EVT_RADIOBOX
      else:
        event_type = wx.EVT_RADIOBUTTON
      self.widget.Bind(event_type,self._value_changed)


    def get_value(self):
      "Get index of activated button"
      return self.widget.GetSelection()

    def set_value(self,value):
      "Set activate button indexed by value"
      self.widget.SetSelection(value)


  class _Slider(AVCCore._Slider):
    "wx Slider widget abstractor"

    def _init(self):

      # connect relevant signals
      self.widget.Bind(wx.EVT_LEFT_UP,
        lambda event: wx.CallAfter(self._value_changed) or event.Skip())
 

    def _get_value(self):
      "Get Slider value"
      return self.widget.GetValue()

    def set_value(self,value):
      "Set Slider value"
      self.widget.SetValue(value)


  class _SpinButton(AVCCore._SpinButton):
    "wx SpinButton widget abstractor"

    def _init(self):

      # connect relevant signals to handlers
      wx.EVT_SPINCTRL(self.widget,self.widget.GetId(),self._value_changed)


    def _get_value(self):
      "Get spinbutton value"
      return self.widget.GetValue()

    def set_value(self,value):
      "Set spinbutton value"
      self.widget.SetValue(value)


  class _StatusBar(AVCCore._StatusBar):
    "wx StatusBar widget abstractor"

    def set_value(self,value):
      "Set StatusBar value (only field 1)"
      self.widget.SetStatusText(value)


  class _TextView(AVCCore._TextView):
    "wx TextView widget abstractor"

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
    "wx ToggleButton widget abstractor"

    def _init(self):

      # connect relevant signals
      if self.widget.__class__ == wx.CheckBox:
        event_type = wx.EVT_CHECKBOX
      else:
        event_type = wx.EVT_TOGGLEBUTTON
      self.widget.Bind(event_type,self._value_changed)


    def get_value(self):
      "Get button status"
      return bool(self.widget.GetValue())

    def set_value(self,value):
      "Set button status"
      self.widget.SetValue(value)


  ## mapping between the real widget and the wal widget

  _WIDGETS_MAP = { \
  wx.BitmapButton:	_Button, \
  wx.Button:		_Button, \
  wx.CheckBox:		_ToggleButton, \
  wx.ComboBox:		_ComboBox,\
  wx.Choice:		_ComboBox,\
  wx.RadioBox:		_RadioButton, \
  wx.Slider:		_Slider, \
  wx.SpinCtrl:		_SpinButton, \
  wx.StaticText:	_Label, \
  wx.StatusBar:		_StatusBar,
  wx.TextCtrl:		_Entry,
  wx.ToggleButton:	_ToggleButton}
 
#### END
