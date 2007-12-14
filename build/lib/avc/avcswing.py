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

from avc.avccore import *	# AVC core


#### WIDGETS ABSTRACTION LAYER (widget toolkit side)

class _Button(WALButton):
  "GTK Button widget abstractor"

  def __init__(self,coget,button):

    WALButton.__init__(self,coget,button)
    
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


class _ComboBox(WALComboBox):
  "GTK ComboBox widget abstractor"

  def __init__(self,coget,combobox):

    WALComboBox.__init__(self,coget,combobox) 

    # connect relevant signals
    self.widget.connect("changed",self._value_changed)


  def get_value(self):
    "Get index of selected item"
    return self.widget.get_active()

  def set_value(self,value):
    "Set selected item by its index value"
    self.widget.set_active(value)


class _Entry(WALEntry):
  "GTK Entry widget abstractor"

  def __init__(self,coget,entry):

    WALEntry.__init__(self,coget,entry)

    # connect relevant signals to handlers
    self.widget.connect("activate",self._value_changed)


  def get_value(self):
    "Get text from Entry"
    return self.coget.control_type(self.widget.get_text())
    
  def set_value(self,value):
    "Set text into Entry"
    self.widget.set_text(str(value))
 

class _Label(WALLabel):
  "GTK Label widget abstractor"

  def __init__(self,coget,label):

    WALLabel.__init__(self,coget,label)


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


class _Slider(WALSlider):
  "GTK Slider widget abstractor"

  def __init__(self,coget,slider):

    WALSlider.__init__(self,coget,slider) 

    # connect relevant signals to handlers
    self.widget.connect("value_changed",self._value_changed)
 

  def get_value(self):
    "Get Slider value"
    return self.coget.control_type(self.widget.get_value())

  def set_value(self,value):
    "Set Slider value"
    self.widget.set_value(value)


class _SpinButton(WALSpinButton):
  "GTK SpinButton widget abstractor"

  def __init__(self,coget,spinbutton):

    WALSpinButton.__init__(self,coget,spinbutton) 

    # connect relevant signals to handlers
    self.widget.actionPerformed(self._value_changed)
 

  def get_value(self):
    "Get spinbutton value"
    return self.coget.control_type(self.widget.value)

  def set_value(self,value):
    "Set spinbutton value"
    self.widget.value = value


class _StatusBar(WALStatusBar):
  "GTK StatusBar widget abstractor"

  def __init__(self,coget,statusbar):

    WALStatusBar.__init__(self,coget,statusbar) 


  def set_value(self,value):
    "Set StatusBar value"
    self.widget.pop(1)
    self.widget.push(1,value)


class _TextView(WALTextView):
  "GTK TextView widget abstractor"

  def __init__(self,coget,textview):

    WALTextView.__init__(self,coget,textview)

    # connect relevant signals to handlers
    self.widget.get_buffer().connect("changed",self._value_changed)


  def get_value(self):
    "Get text from TextView"
    textbuf = self.widget.get_buffer()
    return textbuf.get_text(textbuf.get_start_iter(),textbuf.get_end_iter())
    
  def set_value(self,value):
    "Set text into TextView"
    self.widget.get_buffer().set_text(str(value))


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
  swing.JButton:	_Button, \
  swing.JCheckButton:	_ToggleButton, \
  swing.JComboBox:	_ComboBox,\
####  gtk.Entry:		_Entry, \
  swing.JLabel:		_Label, \
  swing.JRadioButton:	_RadioButton, \
  swing.JSlider:	_Slider, \
  swing.JSpinner:	_SpinButton, \
  gtk.Statusbar:	_StatusBar, \
  swing.JTextArea:	_TextView}
 

  #### METHODS

  def _top_level_widgets(self):
    "Return the list of all top level widgets"
    return awt.Frame.getFrames().tolist()

  def avc_init(self,view_period=0.1):
    "Init and start all AVC activities"
    # get all top level widgets and store them
    self._toplevel_widgets = self._top_level_widgets()
    # do common init
    AVCCore.avc_init(self,view_period)

  def _widget_children(self,widget):
    "Return the list of all children of the widget"
    # Widgets that are not a subclass of gtk.Container have no children.
    if isinstance(widget,awt.Container):
      return widget.components.tolist()
    else:
      return []

  def _widget_name(self,widget):
    "Return the widget name"
    return widget.getName()

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
