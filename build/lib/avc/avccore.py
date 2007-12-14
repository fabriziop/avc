# .+
# .context    : Application View Controller
# .title      : AVC core
# .kind	      : python source
# .author     : Fabrizio Pollastri
# .site	      : Revello - Italy
# .creation   :	3-Nov-2006
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

import copy


#### AVC core

class AVCCore(object):
  "Application View Controller Core"

  # separator between widget name part 1 and 2
  _WIDGET_NAME_SEP	= '__'


  def avc_init(self,view_period=0.1):
    "Init AVC core logic"

    # if a sampled (periodic) update of all controls views is required,
    # start a periodic call to view update function.
    self._view_period = view_period
    if self._view_period:
      self._coget_updates = {}
      self.avc_timer(self._view_update,view_period) 

    # bind widgets to controls
    bindings = self._bind()

    # create all cogets
    self._create_cogets(bindings)


  def _bind(self):
    """
    Bind widgets to application attributes (controls). Each widget whose
    part 1 of name is equal to an application attribute with the same name
    (the control name) is associated to the control name.
    Return a dictionary of bindings, keyed by control names. Each binding
    is a list of all the widgets associated to the control.
    """

    # bindings by control names
    bindings = {}
    
    # for each widget in GUI ... 
    for widget, widget_name in self._get_widget():

      # control name is the widget name part before WIDGET_NAME_SEP string,
      # if present, otherwise is the whole widget name.
      control_name = widget_name.split(self._WIDGET_NAME_SEP)[0]
      
      # if no application attribute with the same name: go to next widget. 
      if not hasattr(self,control_name):
        continue
	
      # exists an application attribute with the same name, append widget
      # to current control binding
      widgets = bindings.get(control_name,[])
      widgets.append(widget)
      bindings[control_name] = widgets

    return bindings

	
  def _create_cogets(self,bindings):
    """
    Create a coget for each existing pair of unique part 1 of widget names
    (assumed as coget name) and an application attribute with the same name.
    Sets a dictionary of cogets, keyed by coget names.
    """
    # for each widget check if it belongs to a coget, if yes associate it to
    # the coget with a specific widget driver.
    self._cogets = {}			# cogets by control names
    for control_name in bindings.keys():
      self._cogets[control_name] = \
          _Coget(control_name,self,bindings[control_name])


  def _get_widget(self):
    """
    Widget tree iterator. Get all top level windows and traverse their
    widgets trees in breath first mode returning for each widget its
    pointer and name.
    """
    widgets = self._toplevel_widgets
    while widgets:
      children = []
      # for each widget in this level ...
      for widget in widgets:
        # return pointer and name of widget
        yield (widget,self._widget_name(widget))
        children += self._widget_children(widget)
      # children of this level are widgets of next level
      widgets = children


  def _view_update(self):
    "Periodically update views for all scheduled cogets"

    for coget in self._coget_updates.keys():
      setter = self._coget_updates[coget]
      # set the new control value in all widgets binded to this control
      # excluding the setting widget, if setter is a widget.
      for wal_widget in coget.wal_widgets:
        if wal_widget.widget != setter:
          wal_widget.set_value(coget.control_value)

    # clear all update requests
    self._coget_updates = {}


class _Coget(object):
  "A control object as data descriptor"

  def __init__(self,control_name,application,widgets):
    "Create the coget control and bind it to one application attribute"

    # save arguments
    self.control_name = control_name
    self.application = application

    # save initial control value and type
    self.control_value_initial = getattr(application,control_name)
    self.control_type = self.control_value_initial.__class__

    # storage for control value
    self.control_value = None

    # set control as an application property with get and set functions
    # as defined below
    setattr(application.__class__,control_name,self)

    # map the list of binded widgets into a list of abstract widgets
    self.wal_widgets = []
    for widget in widgets:
      wal_widget = application._WIDGETS_MAP.get(widget.__class__,None)
      # silently discard unsupported widgets
      if wal_widget:
        self.wal_widgets.append(wal_widget(self,widget))
    
    # if exists an application method with the name control_name+'_changed',
    # store it, it will be called when a widget set a new control value.
    if hasattr(application,control_name + '_changed'):
      self.set_handler = getattr(application,control_name + '_changed')
    else:
      self.set_handler = None

    # init all connected widgets with the control initial value 
    self.__set__(self,self.control_value_initial)


  def __get__(self,instance,classinfo):
    "Get control value"

    return self.control_value


  def __set__(self,instance,value,setter=None):
    """
    Set a new control value into application control variable. If setter
    is a widget (setter != None), call the application set handler, if exists.
    Update control view in all widgets binded to the control, if setter is
    a widget, do not update it.
    """

    # if control old value equal to the new one, return immediately.
    if value == self.control_value:
      return

    # set new control value: if control is a mutable sequence (list) or
    # mapping (dict), a full copy inside the coget is needed to test if it
    # is really changed.
    if self.control_type in (list,dict):
      self.control_value = copy.deepcopy(value)
    else:
      self.control_value = value

    # if setter is a widget, call the application set handler for this
    # control, if exists.
    if setter and self.set_handler:
      self.set_handler(value)

    # if a sampled view update is required, schedule this coget for view update.
    if self.application._view_period != 0.0:
      self.application._coget_updates[self] = setter
      return
      
    # set the new control value in all widgets binded to this control
    # excluding the setting widget, if setter is a widget.
    for wal_widget in self.wal_widgets:
      if wal_widget.widget != setter:
        wal_widget.set_value(value)


  def __delete__(self,instance):
    "Cogets cannot be deleted"
    raise Error,"Trying to delete " + str(self) + ": Cogets cannot be deleted."


#### WIDGETS ABSTRACTION LAYER (coget side)

class WALWidget:
  "Widget Abstraction Layer abstract class"

  def __init__(self,coget,widget):
  
    # save references
    self.coget = coget
    self.widget = widget


  def set_value(self,value):
    raise Error,"Method \"set_value\" of abstract class _Widget is undefined"

  def get_value(self):
    raise Error,"Method \"get_value\" of abstract class _Widget is undefined"
 
  def _value_changed(self,*args):
    "widget value changed handler"
    # set new value into control variable
    self.coget.__set__(self,self.get_value(),self.widget)


class WALButton(WALWidget):
  "Button widget abstractor"

  def __init__(self,coget,button):

    WALWidget.__init__(self,coget,button)

    # check for supported control type
    if self.coget.control_type != bool:
      raise Error, \
        "Control type '%s' not supported with Button widget" % \
	self.coget.control_type


class WALComboBox(WALWidget):
  "ComboBox widget abstractor"

  def __init__(self,coget,combobox):

    WALWidget.__init__(self,coget,combobox)

    # check for supported control type
    if not self.coget.control_type is int:
      raise Error,"Control type '%s' not supported with ComboBox widget" % \
        self.coget.control_type


class WALEntry(WALWidget):
  "Entry widget abstractor"

  def __init__(self,coget,entry):

    WALWidget.__init__(self,coget,entry)

    # check for supported control type
    if not self.coget.control_type in (int,float,str):
      raise Error,"Control type '%s' not supported with Entry widget" % \
        self.coget.control_type
 

  def _value_changed(self,*args):
    "Entry activate signal (return pressed) handler"
    # read entry value and convert it if required by control type
    value = self.get_value()
    if self.coget.control_type == int:
      value = int(value)
    if self.coget.control_type == float:
      value = float(value)
    # set new value into control variable
    self.coget.__set__(self,value,self.widget)


class WALLabel(WALWidget):
  "Label widget abstractor"

  # control type to format string mapping
  FORMAT_MAP = {bool:'%s',int:'%d',float:'%.2f',str:'%s',list:''}


  def __init__(self,coget,label):

    WALWidget.__init__(self,coget,label)

    # check for supported control type
    if not self.FORMAT_MAP.has_key(coget.control_type):
      raise Error, \
        "Control type '%s' not supported with Label widget" % \
	self.coget.control_type

    # first try to use any default text into label as python formatting string 
    # for output writing
    self.format = self.get_value()
    try:
      if coget.control_type == list:
        junk = self.format % tuple(coget.control_value_initial)
      else:
        junk = self.format % (coget.control_value_initial)

    # if default text fails, set format according to control type
    except:
       self.format = self.FORMAT_MAP[coget.control_type]


class WALRadioButton(WALWidget):
  "RadioButton widget abstractor"

  def __init__(self,coget,radiobutton):

    WALWidget.__init__(self,coget,radiobutton)

    # check for supported control type
    if not self.coget.control_type is int:
      raise Error,"Control type '%s' not supported with RadioButton widget" % \
        self.coget.control_type


class WALSlider(WALWidget):
  "Slider widget abstractor"

  def __init__(self,coget,slider):

    WALWidget.__init__(self,coget,slider)

    # check for supported control type
    if not self.coget.control_type in (float,int):
      raise Error,"Control type '%s' not supported with Slider widget" % \
        self.coget.control_type
 

class WALSpinButton(WALWidget):
  "SpinButton widget abstractor"

  def __init__(self,coget,spinbutton):

    WALWidget.__init__(self,coget,spinbutton)

    # check for supported control type
    if not self.coget.control_type in (float,int):
      raise Error,"Control type '%s' not supported with SpinButton widget" % \
        self.coget.control_type
 

  def _value_changed(self,*args):
    "Spinbutton value_changed signal handler"
    # read button value
    value = self.get_value()
    # value is float, if control is int convert it
    if self.coget.control_type is int:
      value = int(value)
    # set new value into control variable
    self.coget.__set__(self,value,self.widget)


class WALStatusBar(WALWidget):
  "StatusBar widget abstractor"

  def __init__(self,coget,statusbar):

    WALWidget.__init__(self,coget,statusbar)

    # check for supported control type
    if self.coget.control_type != str:
      raise Error, \
        "Control type '%s' not supported with StatusBar widget" % \
	self.coget.control_type


class WALTextView(WALWidget):
  "TextView widget abstractor"

  def __init__(self,coget,textview):

    WALWidget.__init__(self,coget,textview)

    # check for supported control type
    if not self.coget.control_type in (str,):
      raise Error,"Control type '%s' not supported with TextView widget" % \
        self.coget.control_type


  def _value_changed(self,*args):
    "TextView value_changed signal handler"
    # set new value into control variable
    self.coget.__set__(self,self.get_value(),self.widget)


class WALToggleButton(WALWidget):
  "ToggleButton widget abstractor"

  def __init__(self,coget,togglebutton):

    WALWidget.__init__(self,coget,togglebutton)

    # check for supported control type
    if self.coget.control_type != bool:
      raise Error,"Control type '%s' not supported with ToggleButton widget" \
          % self.coget.control_type


class WALNull(WALWidget):
  "Null Abstraction Layer abstract class (debug aid)"

  def __init__(self,coget,widget):
    WALWidget.__init__(self,coget,widget)
  
  def set_value(self,value):
    pass

  def get_value(self):
    pass
    
  def _value_changed(self,value):
    pass


class Error(Exception):
  "A generic error exception"

  def __init__(self, value):
    self.value = value

  def __str__(self):
    return repr(self.value)


#### END
