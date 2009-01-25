# .+
# .context    : Application View Controller
# .title      : AVC core
# .kind	      : python source
# .author     : Fabrizio Pollastri
# .site	      : Revello - Italy
# .creation   :	3-Nov-2006
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


# import required modules
import copy				# object deep copy
import sys				# command line option reading


class error(Exception):
  "A generic error exception"
  def __init__(self, value):
    self.value = value
  def __str__(self):
    return repr(self.value)


## load proper AVC widget toolkit binding according with the widget toolkit
# imported by application program

# supported toolkit names indexed by python binding module names
TOOLKITS = { 'gtk':'GTK+','qt':'Qt3','PyQt4':'Qt4','javax':'SWING', \
  'Tkinter':'Tkinter','wx':'wxWidgets'}

# avc toolkit bindings indexed by python binding module names
AVC_BINDINGS = { 'gtk':'avcgtk','qt':'avcqt3','PyQt4':'avcqt4', \
  'javax':'avcswing','Tkinter':'avctk', 'wx':'avcwx'}

AVC_PREFIX = 'avc.'

# test which widget toolkit binding module is imported: if none raise an error.
for toolkit in TOOLKITS.keys():
  if sys.modules.has_key(toolkit):
    break
else:
  raise error,'No supported toolkit found: import it before AVC import.'

# found a supported toolkit: import its AVC binding
real = __import__(AVC_PREFIX + AVC_BINDINGS[toolkit],globals(),locals(),
  [AVC_BINDINGS[toolkit]])


# command line option switches
OPT_VERBOSITY = '--avc-verbosity'

# separator between widget name part 1 and 2
WIDGET_NAME_SEP = '__'

# advanced connection control data keys
HEADER = 0		#???????????
DATA = 1		#???????????
ROOT_ROWS = 0		#???????????
ROW_DATA = 0		#???????????

# AVC common data
class AVCCD:
  def __init__(self):
    self.verbosity = 0
    self.view_period = 0.1
    self.cogets = {}
    self.connections = {}
    self.connections_updates = {}
    self.connected_widgets = {}
    self.timer = None
avccd = AVCCD()


class AVC(object):
  "AVC programming interface"

  def avc_init(self,verbosity=0,view_period=0.1):
    "Init AVC core logic"

    # save parameters as globals
    avccd.verbosity = verbosity
    avccd.view_period = view_period

    # if any, get options from command line and override init arguments
    try:
      opt_switch_index = sys.argv.index(OPT_VERBOSITY)
      avccd.verbosity = int(sys.argv[opt_switch_index+1])
    except:
      pass

    # if verbosity > 0 , print header
    if avccd.verbosity > 0:
      print 'AVC ' + '0.6.0' + ' - Activity Report'
      print 'widget toolkit binding: ' + TOOLKITS[toolkit]
      print 'program: ' + sys.argv[0]  
      print 'verbosity: ' + str(avccd.verbosity)
      if avccd.view_period:
        print 'connection update mode: periodic, period=' + \
          str(avccd.view_period) + ' sec'
      else:
        print 'connection update mode: immediate'

    # do init specific to widget toolkit
    real.init(avccd.verbosity,view_period)

    # connect widgets-variables in __main__ namespace
    self.avc_connect(real.toplevel_widgets())

    # if a sampled (periodic) update of all controls views is required,
    # start a periodic call to view update function.
    if avccd.view_period != 0.0:
      avccd.timer = real.timer(view_update,avccd.view_period)


  def avc_connect(self,toplevel):
    """
    For each widget at or below toplevel, having a matching name with
    an attribute of object_ object, create a widget-attribute connection.
    """

    # force top level widgets to be a list
    if toplevel.__class__ != list:
      toplevel = [toplevel]

    if avccd.verbosity > 3:
      print 'widget tree scansion from top level ' + str(toplevel)

    # for each widget in GUI ... 
    for widget, widget_name in get_widget(toplevel):

      # if widget is not supported: go to next widget
      if not real.WIDGETS_MAP.has_key(widget.__class__):

        if avccd.verbosity > 3:
	  print '  skip unsupported widget ' + \
	    widget.__class__.__name__ + ',"' + widget_name + '"'

        continue

      # if the widget is already connected: go to next widget. 
      if avccd.connected_widgets.has_key(widget):

        if avccd.verbosity > 3:
	  print '  skip already connected widget ' + \
	    widget.__class__.__name__ + ',"' + widget_name + '"'

        continue
	
      # control name is the widget name part before WIDGET_NAME_SEP string,
      # if present, otherwise is the whole widget name.
      control_name = widget_name.split(WIDGET_NAME_SEP)[0]

      # if no object attribute with the same name: go to next widget. 
      if not hasattr(self,control_name):

        if avccd.verbosity > 3:
	  print '  skip unmatched widget ' + \
	    widget.__class__.__name__ + ',"' + widget_name + '"'

        continue
	
      ## there exists an application attribute with the same name

      # if the connection exists, get it from connections dictionary,
      # if the connection does not exists, create it.
      connection = avccd.connections.setdefault((control_name,self), \
        Connection(getattr(self,control_name)))

      # add widget to connection and mark widget as connected
      connection.add_widget(control_name,self,widget,widget_name)
      avccd.connected_widgets[widget] = connection


# core functions

def get_widget(widgets):
  """
  Widget tree iterator. Start from toplevel widgets and traverse their
  widgets trees in breath first mode returning for each widget its
  pointer and name.
  """
  # for each toplevel widget ...
  while widgets:
    children = []
    # for each widget in this level ...
    for widget in widgets:
      # return pointer and name of widget
      yield (widget,real.widget_name(widget))
      children += real.widget_children(widget)
      # children of this level are widgets of next level
      widgets = children


def view_update():
  "Periodically update views for all scheduled cogets"

  for connection in avccd.connections_updates.keys():
    setter = avccd.connections_updates[connection]
    # set the new control value in all widgets binded to this control
    # excluding the setting widget, if setter is a widget.
    for wal_widget in connection.wal_widgets:
      if wal_widget != setter:
        wal_widget.write(connection.control_value)

  # clear all update requests
  avccd.connections_updates = {}


class Connection:
  "Widgets-variable connection"

  def __init__(self,control_value=None):

    # set storage for control value, type, connected wal widget list,
    # value changed handler and coget
    self.control_value = control_value
    self.control_type = control_value.__class__
    self.wal_widgets = []
    self.set_handler = None
    self.object_ = None
    self.coget = None


  def add_widget(self,control_name,object_,widget,widget_name):
    "Add one widget to current connection"

    ## if it is the first widget, setup connection control data and coget

    if not self.wal_widgets:

      # save connection object instance
      self.object_ = object_

      # if exists a object method with the name control_name+'_changed',
      # store it, it will be called when a widget set a new control value.
      if hasattr(object_,control_name + '_changed'):
        self.set_handler = getattr(object_,control_name + '_changed')

      # if the corresponding coget does not exists, create it, if exists,
      # get it from cogets dictionary.
      if avccd.cogets.has_key((control_name,object_.__class__)):
        self.coget = avccd.cogets[(control_name,object_.__class__)]
      else:
        self.coget = avccd.cogets[(control_name,object_.__class__)] = \
          Coget(control_name,object_)
        # set coget as an property in place of application variable.
        setattr(object_.__class__,control_name,self.coget)
	
      # save connection reference into coget
      self.coget.add_connection(self)

      if avccd.verbosity > 0:
        print '  creating connection "' + control_name + '" in ' + str(object_)
        print '    type: ' + str(self.control_type)
        print '    initial value: ' + str(self.control_value)
        if self.set_handler:
          print '    connected handler '+'"'+control_name+'_changed"'

    # map the connected widget into the corresponding abstract widget
    print 'widget=',widget,widget.__class__
    print 'mapped widget=',real.WIDGETS_MAP[widget.__class__]
    wal_widget = eval(real.WIDGETS_MAP[widget.__class__])

    if avccd.verbosity > 1:
      print '  add widget ' + widget.__class__.__name__ + \
        ',"' + widget_name + '" to connection "' + control_name + '"'

    # add it to the wal widget list
    self.wal_widgets.append(wal_widget(self,widget))

    # init it with the control value
    self.wal_widgets[-1].write(self.control_value)


  def remove_widget(self,wal_widget):
    """
    Remove one widget from current connection. If it is the last
    one in the connection, delete the connection.
    """

    self.wal_widgets.remove(wal_widget)

    if avccd.verbosity > 1:
      print 'removing widget ' + wal_widget.widget.__class__.__name__ + \
        ' from connection "' + self.coget.control_name + \
	'" of ' + str(self.object_)

    # clear wal widget data
    del wal_widget.connection
    del wal_widget.widget

    # if connection has no more widgets delete it
    if not self.wal_widgets:

      if avccd.verbosity > 0:
        print 'removing connection "' + self.coget.control_name + \
          '" from ' + str(self.object_)

      # delete connection from general connection dictionary
      del avccd.connections[(self.coget.control_name,self.object_)]

      # delete connection from coget
      self.coget.remove_connection(self)

      # delete connection from those with a pending update
      if avccd.connections_updates.has_key(self):
        del avccd.connections_updates[self]

      # clear connection data
      del self.control_value
      del self.control_type
      del self.wal_widgets
      del self.set_handler
      del self.object_
      del self.coget


class Coget(object):
  "A control object as data descriptor"

  def __init__(self,control_name,object_):
    "Create the coget control and bind it to one attribute in object"
    # save argument
    self.control_name = control_name
    self.connections = []

  def add_connection(self,connection):
    "Add a connection"
    self.connections.append(connection)

  def remove_connection(self,connection):
    "Remove a connection. If it is the last one, delete coget."
    self.connections.remove(connection)
    if not self.connections:
      del avccd.cogets[(self.control_name,connection.object_.__class__)]
      del self.control_name
      del self.connections

  def __get__(self,object_,classinfo):
    "Get control value"
    return avccd.connections[(self.control_name,object_)].control_value


  def __set__(self,object_,value,setter=None,connection=None):
    """
    Set a new control value into application control variable. If setter
    is a widget (setter != None), call the application set handler, if exists.
    Update control view in all widgets binded to the control, if setter is
    a widget, do not update it.
    """

    # if not given, get or create connection
    if not connection:
      # if the connection exists, get it from connections dictionary,
      # otherwise, create it.
      if avccd.connections.has_key((self.control_name,object_)):
        connection = avccd.connections[(self.control_name,object_)]
      else:
        connection = avccd.connections[(self.control_name,object_)] = \
          Connection(value)
        return

    # if control old value equal to the new one, return immediately.
    if value == connection.control_value:
      return

    # set new control value: if control is a mutable sequence (list) or
    # mapping (dict), a full copy inside the coget is needed to test if it
    # is really changed.
    if connection.control_type in (list,dict):
      connection.control_value = copy.deepcopy(value)
    else:
      connection.control_value = value

    # if setter is a widget, call the application set handler for this
    # control, if exists.
    if setter and connection.set_handler:
      connection.set_handler(value)

    # if a sampled view update is required, schedule this coget for
    # view update.
    if avccd.view_period != 0.0:
      avccd.connections_updates[connection] = setter
      return
      
    # if an immediate update is required, set the new control value
    # in all widgets binded to this control excluding the setting
    # widget, if setter is a widget.
    for wal_widget in connection.wal_widgets:
      if wal_widget != setter:
        wal_widget.write(value)


  def __delete__(self,instance):
    "Cogets cannot be deleted"
    raise error,"Trying to delete "+ str(self) +": Cogets cannot be deleted."


#### WIDGETS ABSTRACTION LAYER (coget side)

class Widget:
  "Widget Abstraction Layer abstract class"

  def __init__(self,connection,widget,allowed_types=None):
  
    # check for supported control type
    if allowed_types and not connection.control_type in allowed_types:
      raise error, "Control type '%s' not supported with '%s' widget" % \
        (connection.control_type.__name__,widget.__class__.__name__)

    # save references
    self.connection = connection
    self.widget = widget

    # connect signal common to all widgets
    self.connect_delete(widget,self.delete)


  def read(self):
    raise error,"Method \"read\" of abstract class Widget is undefined"

  def write(self,value):
    raise error,"Method \"write\" of abstract class Widget is undefined"

  def value_changed(self,*args):
    "widget value changed handler"
    # set new value into control variable
    Coget.__set__(
      self.connection.coget,'',self.read(),self,self.connection)
 
  def delete(self,*args):
    "delete widget from connection"
    self.connection.remove_widget(self)


class Button(real.Button,Widget):
  "Button widget abstractor"

  def __init__(self,connection,button):
    # generic abstract widget init
    Widget.__init__(self,connection,button,(bool,))
    # real widget init
    real.Button.__init__(self)


class ComboBox(real.ComboBox,Widget):
  "ComboBox widget abstractor"

  def __init__(self,connection,combobox):
    # generic abstract widget init
    Widget.__init__(self,connection,combobox,(int,))
    # real widget init
    real.ComboBox.__init__(self)


class Entry(real.Entry,Widget):
  "Entry widget abstractor"

  def __init__(self,connection,entry):
    # generic abstract widget init
    Widget.__init__(self,connection,entry,(float,int,str))
    # real widget init
    real.Entry.__init__(self)

  def read(self):
    "Get Entry value"
    return self.connection.control_type(real.Entry.read(self))


class Label(real.Label,Widget):
  "Label widget abstractor"

  def __init__(self,connection,label):

    # generic abstract widget init
    Widget.__init__(self,connection,label)

    # check for generic python object
    if connection.control_type in (bool,float,int,list,str,tuple,dict):
      self.is_object = False
      control_value = connection.control_value
    else:
      self.is_object = True
      control_value = connection.control_value.__dict__
        
    # get default format string, if any.
    self.format = str(self.read())

    # check for a working format
    try:
      if connection.control_type == list:
        junk = self.format % tuple(control_value)
      elif connection.control_type == dict:
        junk = self.format % control_value
        if junk == self.format:
          raise
      else:
        junk = self.format % control_value
      if avccd.verbosity > 2:
        print '    valid format string: "' + self.format + '"'
    except:
      if avccd.verbosity > 2:
        if self.format:
          print '    invalid format string: "' + self.format + '"'
        else:
          print '    no format string'
      self.format = None

    # real widget init
    real.Label.__init__(self)


  def read(self):
    "Get value from Label"
    # if control type is a generic object do not coerce to its type
    if self.is_object:
      return real.Label.read(self)
    # if control type not a generic object,first try to coerce to control type
    try:
      return self.connection.control_type(eval(real.Label.read(self)))
    # if fail, return value as string, needed for format string initial get.
    except:
      return real.Label.read(self)

  def write(self,value):
    "Set text into Label"
    if self.format:
      if self.is_object:
        real.Label.write(self,self.format % value.__dict__)
      else:
        if type(value) == list:
          value = tuple(value)
        real.Label.write(self,self.format % value)
    else:
      real.Label.write(self,str(value))


class ProgressBar(real.ProgressBar,Widget):
  "ProgressBar widget abstractor"

  def __init__(self,connection,progressbar):
    # generic abstract widget init
    Widget.__init__(self,connection,progressbar,(float,int))
    # real widget init
    real.ProgressBar.__init__(self)

  def read(self):
    "Get Entry value"
    return self.connection.control_type(real.Entry.read(self))


class RadioButton(real.RadioButton,Widget):
  "RadioButton widget abstractor"

  def __init__(self,connection,radiobutton):
    # generic abstract widget init
    Widget.__init__(self,connection,radiobutton,(int,))
    # real widget init
    real.RadioButton.__init__(self)


class Slider(real.Slider,Widget):
  "Slider widget abstractor"

  def __init__(self,connection,slider):
    # generic abstract widget init
    Widget.__init__(self,connection,slider,(float,int))
    # real widget init
    real.Slider.__init__(self)

  def read(self):
    "Get Slider value"
    return self.connection.control_type(real.Slider.read(self))


class SpinButton(real.SpinButton,Widget):
  "SpinButton widget abstractor"

  def __init__(self,connection,spinbutton):
    # generic abstract widget init
    Widget.__init__(self,connection,spinbutton,(float,int))
    # real widget init
    real.SpinButton.__init__(self)

  def read(self):
    "Get spinbutton value"
    return self.connection.control_type(real.SpinButton.read(self))


class StatusBar(real.StatusBar,Widget):
  "StatusBar widget abstractor"

  def __init__(self,connection,statusbar):
    # generic abstract widget init
    Widget.__init__(self,connection,statusbar,(str,))
    # real widget init
    real.StatusBar.__init__(self)


class TextView(real.TextView,Widget):
  "TextView widget abstractor"

  def __init__(self,connection,textview):
    # generic abstract widget init
    Widget.__init__(self,connection,textview,(str,))
    # real widget init
    real.TextView.__init__(self)


class ToggleButton(real.ToggleButton,Widget):
  "ToggleButton widget abstractor"

  def __init__(self,connection,togglebutton):
    # generic abstract widget init
    Widget.__init__(self,connection,togglebutton,(bool,))
    # real widget init
    real.ToggleButton.__init__(self)


class TreeView(real.TreeView,Widget):
  "TreeView widget abstractor"

  def __init__(self,connection,treeview):

    # generic abstract widget init
    Widget.__init__(self,connection,treeview,(list,))

    # check for allowed control type
    control_len = len(connection.control_value)
    if control_len < 2:
      raise error, "%s widget control list must have two items: " \
        + "'HEADER' and 'DATA'." % treeview.__class__.__name__
    header = connection.control_value[HEADER]
    if type(header) != list:
      raise error, "%s widget do not allow '%s' type as header, use a list." \
      % (treeview.__class__.__name__,type(header).__name__)
    data = connection.control_value[DATA]
    if type(data) == list:
      self.is_tree = False
    elif type(data) == dict:
      self.is_tree = True
    else:
      raise error, "%s widget do not allow '%s' type as data," \
      + "use a list for tabular data or a dictionary for tree data." \
      % (treeview.__class__.__name__,type(data).__name__)
    if not data:
      raise error, "%s widget do not allow empty list as data." \
      % widget.__class__.__name__

    # save data row types and column number
    if self.is_tree:
      self.row_types = map(type,data[data[ROOT_ROWS][0]][ROW_DATA])
    else:
      if type(data[0]) == list:
        self.row_types = map(type,data[0])
      else:
        self.row_types = [type(data[0])]
    self.cols_num = len(self.row_types)

    # check for header size equal to column number
    if len(header) != self.cols_num:
      raise error, "%s widget require header lenght equal to data row size." \
      % treeview.__class__.__name__

    # real widget init
    real.TreeView.__init__(self)


#### END
