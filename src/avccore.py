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

import copy				# object deep copy
import sys				# command line option reading


#### AVC CORE

class AVCCore(object):
  "Application View Controller Core"

  # command line option switches
  _OPT_VERBOSITY = '--avc-verbosity'

  # separator between widget name part 1 and 2
  _WIDGET_NAME_SEP = '__'


  def avc_init(self,verbosity=0,view_period=0.1):
    "Init AVC core logic"

    # save parameters
    self._verbosity = verbosity
    self._view_period = view_period

    # if any, get options from command line and override init arguments
    try:
      opt_switch_index = sys.argv.index(self._OPT_VERBOSITY)
      self._verbosity = int(sys.argv[opt_switch_index+1])
    except:
      pass

    # if verbosity > 0 , print header
    if self._verbosity > 0:
      print '++++\nAVC ' + '0.5.0' + ' - Activity Report'
      print 'widget toolkit binding: ' + self._binding
      print 'program: ' + sys.argv[0]  
      print 'verbosity: ' + str(self._verbosity)
      if self._view_period:
        print 'connection update mode: periodic, period=' + \
	  str(self._view_period) + ' sec'
      else:
        print 'connection update mode: immediate'

    # if a sampled (periodic) update of all controls views is required,
    # start a periodic call to view update function.
    if self._view_period:
      self._coget_updates = {}
      self.avc_timer(self._view_update,view_period) 

    # bind widgets to controls
    bindings = self._bind()

    # create all cogets
    self._create_cogets(bindings)

    # if verbosity > 0 , end with a final line
    if self._verbosity > 0:
      print '----'

  def _bind(self):
    """
    Bind widgets to application attributes (controls). Each widget whose
    part 1 of name is equal to an application attribute with the same name
    (the control name) is associated to the control name.
    Return a dictionary of bindings, keyed by control names. Each binding
    is a list of all the widgets associated to the control.
    """

    # if verbosity > 2: print header
    if self._verbosity > 3:
      print 'widget tree scansion at init ...'

    # bindings by control names
    bindings = {}
    
    # for each widget in GUI ... 
    for widget, widget_name in self._get_widget():

      # control name is the widget name part before WIDGET_NAME_SEP string,
      # if present, otherwise is the whole widget name.
      control_name = widget_name.split(self._WIDGET_NAME_SEP)[0]

      # if widget is not supported: go to next widget
      if not self._WIDGETS_MAP.has_key(widget.__class__):
        if self._verbosity > 3:
	  print '  skip unsupported widget ' + \
	    widget.__class__.__name__ + ',"' + widget_name + '"'
        continue

      # if no application attribute with the same name: go to next widget. 
      if not hasattr(self,control_name):
        if self._verbosity > 3:
	  print '  skip unmatched widget ' + \
	    widget.__class__.__name__ + ',"' + widget_name + '"'
        continue
	
      # exists an application attribute with the same name, append widget
      # to current control binding
      widgets = bindings.get(control_name,[])
      widgets.append(widget)
      bindings[control_name] = widgets
      if self._verbosity > 3:
        print '  add widget ' + widget.__class__.__name__ + \
	  ',"' + widget_name + '" to connection "' + control_name + '"'

    return bindings

	
  def _create_cogets(self,bindings):
    """
    Create a coget for each existing pair of unique part 1 of widget names
    (assumed as coget name) and an application attribute with the same name.
    Sets a dictionary of cogets, keyed by coget names.
    """
    # for each widget check if it belongs to a coget, if yes associate it to
    # the coget with a specific widget abstractor.
    self._cogets = {}			# cogets by control names
    for control_name in bindings.keys():
      self._cogets[control_name] = \
          self._Coget(control_name,self,bindings[control_name])


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

      # if verbosity > 1: print header
      if application._verbosity > 0:
        print 'creating connection "' + control_name + '" ...'
	print '  type: ' + str(self.control_type)
	print '  initial value: ' + str(self.control_value_initial)

      # storage for control value
      self.control_value = None

      # set control as an application property with get and set functions
      # as defined below
      setattr(application.__class__,control_name,self)

      # map the list of binded widgets into a list of abstract widgets
      self.wal_widgets = []
      for widget in widgets:
        if application._verbosity > 1:
          print '  widget: ' + str(widget) + ',"' + \
	    application._widget_name(widget) + '"'
        wal_widget = application._WIDGETS_MAP.get(widget.__class__,None)
        self.wal_widgets.append(wal_widget(self,widget))
    
      # if exists an application method with the name control_name+'_changed',
      # store it, it will be called when a widget set a new control value.
      if hasattr(application,control_name + '_changed'):
        self.set_handler = getattr(application,control_name + '_changed')
        if application._verbosity > 1:
          print '  connected handler ' + '"' + control_name + '_changed"'
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

      # if a sampled view update is required, schedule this coget for
      # view update.
      if self.application._view_period != 0.0:
        self.application._coget_updates[self] = setter
        return
      
      # if an immediate update is required, set the new control value
      # in all widgets binded to this control excluding the setting
      # widget, if setter is a widget.
      for wal_widget in self.wal_widgets:
        if wal_widget.widget != setter:
          wal_widget.set_value(value)


    def __delete__(self,instance):
      "Cogets cannot be deleted"
      raise error,"Trying to delete "+ str(self) +": Cogets cannot be deleted."


  #### WIDGETS ABSTRACTION LAYER (coget side)

  class _Widget:
    "Widget Abstraction Layer abstract class"

    def __init__(self,coget,widget,allowed_types=None):
  
      # check for supported control type
      if allowed_types and not coget.control_type in allowed_types:
        raise error, \
          "Control type '%s' not supported with '%s' widget" % \
	  (coget.control_type.__name__,widget.__class__.__name__)

      # save references
      self.coget = coget
      self.widget = widget


    def set_value(self,value):
      raise error,"Method \"set_value\" of abstract class _Widget is undefined"

    def get_value(self):
      raise error,"Method \"get_value\" of abstract class _Widget is undefined"
 
    def _value_changed(self,*args):
      "widget value changed handler"
      # set new value into control variable
      self.coget.__set__(self,self.get_value(),self.widget)


  class _Button(_Widget):
    "Button widget abstractor"

    def __init__(self,coget,button):

      # generic abstract widget init
      AVCCore._Widget.__init__(self,coget,button,(bool,))
      
      # real widget init
      self._init()


  class _ComboBox(_Widget):
    "ComboBox widget abstractor"

    def __init__(self,coget,combobox):

      # generic abstract widget init
      AVCCore._Widget.__init__(self,coget,combobox,(int,))

      # real widget init
      self._init()


  class _Entry(_Widget):
    "Entry widget abstractor"

    def __init__(self,coget,entry):

      # generic abstract widget init
      AVCCore._Widget.__init__(self,coget,entry,(float,int,str))

      # real widget init
      self._init()

    def get_value(self):
      "Get Entry value"
      return self.coget.control_type(self._get_value())


  class _Label(_Widget):
    "Label widget abstractor"

    def __init__(self,coget,label):

      # generic abstract widget init
      AVCCore._Widget.__init__(self,coget,label)

      # check for generic python object
      if coget.control_type in (bool,float,int,list,str,tuple):
        self.object = False
	control_value = coget.control_value_initial
      else:
        self.object = True
	control_value = coget.control_value_initial.__dict__
        
      # get default format string, if any.
      self.format = self.get_value()

      # check for a working format
      try:
        if coget.control_type == list:
          junk = self.format % tuple(control_value)
        else:
          junk = self.format % control_value
        if coget.application._verbosity > 2:
	  print '    valid format string: "' + self.format + '"'
      except:
        if coget.application._verbosity > 2:
	  if self.format:
	    print '    invalid format string: "' + self.format + '"'
	  else:
	    print '    no format string'
        self.format = None


    def get_value(self):
      "Get value from Label"
      # if control type is a generic object do not coerce to its type
      if self.object:
        return self._get_value()
      # if control type not a generic object,first try to coerce to control type
      try:
        return self.coget.control_type(eval(self._get_value()))
      # if fail, return value as string, needed for format string initial get.
      except:
        return self._get_value()

    def set_value(self,value):
      "Set text into Label"
      if self.format:
        if self.object:
          self._set_value(self.format % value.__dict__)
	else:
          if type(value) == list:
            value = tuple(value)
          self._set_value(self.format % value)
      else:
        self._set_value(str(value))


  class _RadioButton(_Widget):
    "RadioButton widget abstractor"

    def __init__(self,coget,radiobutton):

      # generic abstract widget init
      AVCCore._Widget.__init__(self,coget,radiobutton,(int,))

      # real widget init
      self._init()


  class _Slider(_Widget):
    "Slider widget abstractor"

    def __init__(self,coget,slider):

      # generic abstract widget init
      AVCCore._Widget.__init__(self,coget,slider,(float,int))

      # real widget init
      self._init()


    def get_value(self):
      "Get Slider value"
      return self.coget.control_type(self._get_value())


  class _SpinButton(_Widget):
    "SpinButton widget abstractor"

    def __init__(self,coget,spinbutton):

      # generic abstract widget init
      AVCCore._Widget.__init__(self,coget,spinbutton,(float,int))

      # real widget init
      self._init()


    def get_value(self):
      "Get spinbutton value"
      return self.coget.control_type(self._get_value())


  class _StatusBar(_Widget):
    "StatusBar widget abstractor"

    def __init__(self,coget,statusbar):

      # generic abstract widget init
      AVCCore._Widget.__init__(self,coget,statusbar,(str,))


  class _TextView(_Widget):
    "TextView widget abstractor"

    def __init__(self,coget,textview):

      # generic abstract widget init
      AVCCore._Widget.__init__(self,coget,textview,(str,))

      # real widget init
      self._init()


  class _ToggleButton(_Widget):
    "ToggleButton widget abstractor"

    def __init__(self,coget,togglebutton):

      # generic abstract widget init
      AVCCore._Widget.__init__(self,coget,togglebutton,(bool,))

      # real widget init
      self._init()


  class _Null(_Widget):
    "Null Abstraction Layer abstract class (debug aid)"

    def __init__(self,coget,widget):
      AVCCore._Widget.__init__(self,coget,widget)
  
    def set_value(self,value):
      pass

    def get_value(self):
      pass
    
    def _value_changed(self,value):
      pass


class error(Exception):
  "A generic error exception"

  def __init__(self, value):
    self.value = value

  def __str__(self):
    return repr(self.value)


#### END
