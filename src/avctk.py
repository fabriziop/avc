# .+
# .context    : Application View Controller
# .title      : AVC Tk bindings
# .kind	      : python source
# .author     : Fabrizio Pollastri
# .site	      : Revello - Italy
# .creation   :	7-Nov-2006
# .copyright  : (c) 2006 Fabrizio Pollastri, all right reserved.
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

import Tkinter				# Tk interface

from avc.avccore import *		# AVC core


#### AVC TK INTERFACE

## redifinition of BaseWidget __init__ in Tkinter with a "monkey patch".
# The same as the original, but without any call to tcl interpreter.
# Needed to instantiate the python widget of a already existing tcl widget.

def _dummy_call(*args):
  return

def _basewidget_new_init(self, master, widgetName, cnf={}, kw={}, extra=()):
  """
  Construct a widget with the parent widget MASTER, a name WIDGETNAME
  and appropriate options.
  """
  if kw:
    cnf = Tkinter._cnfmerge((cnf, kw))
  self.widgetName = widgetName
  Tkinter.BaseWidget._setup(self, master, cnf)


class AVC(AVCCore):
  "AVC Tk bindings"

  _binding = 'Tk'


  #### GENERAL ABSTRACTION METHODS

  def _complete_widget_tree(self,widget):
    """
    Since direct usage of the tcl interpreter (call to "eval","evalfile" or
    "call") do not create any widget instance in python, complete the python
    widget tree instantiating the corresponding widget class from Tkinter
    for each widget created by the tcl interpreter.
    Do the work by visiting in deep first mode the widget tree with the tcl
    interpreter commands.
    Also build the list of all top level widgets.
    """
    children_path = widget.tk.eval('winfo children ' + str(widget)).split()
    for child_path in children_path:
      child_name = child_path.split('.')[-1]
      # if python widget do not exists, create it.
      if not widget.children.has_key(child_name):
        class_name = widget.tk.eval('winfo class ' + child_path)
        eval('Tkinter.' + class_name + '(widget,name="' + child_name + '")')
      # if widget is a toplevel window, append it to top level widgets list.
      if child_path == widget.tk.eval('winfo toplevel ' + child_path):
        self._toplevel_widgets += [widget.nametowidget(child_path)]
      # go deep into widgets tree
      for child in widget.children.values():
        self._complete_widget_tree(child)

  def avc_init(self,*args,**kwargs):
    "Init and start all AVC activities"
    # get the root top level widgets and store it in a list
    self._toplevel_widgets = [Tkinter._default_root]
    # replace Tkinter basewidget init, with the one not calling tcl interpreter
    basewidget_original_init = Tkinter.BaseWidget.__init__
    Tkinter.BaseWidget.__init__ = _basewidget_new_init
    toplevel_original_title = Tkinter.Wm.title
    Tkinter.Wm.title = _dummy_call
    # complete the python widget tree, if necessary
    self._complete_widget_tree(self._toplevel_widgets[0])
    # restore original basewidget init
    Tkinter.BaseWidget.__init__ = basewidget_original_init
    Tkinter.Wm.title = toplevel_original_title
    # do common init
    AVCCore.avc_init(self,*args,**kwargs)
    # if a timer is defined, start a timer calling back 'function' every
    # 'period' seconds. Return timer id.
    try:
      if self._timer_function:
        return self._toplevel_widgets[0].after(
          int(self._timer_period * 1000.0),self._timer_wrap)
    except:
      pass

  def _widget_children(self,widget):
    "Return the list of all children of the widget"
    return widget.children.values()

  def _widget_name(self,widget):
    """
    Return the widget name. Try first to get avc_name attribute. If this
    fails, get Tk widget name keeping the last part only.
    """
    try:
      return widget.avc_name
    except:
      return str(widget).split('.')[-1]

  def _null_writer(self,widget,value):
    "The widget null writer"
    pass

  def avc_timer(self,function,period):
    """
    Store timer parameters. Timer is started at avc_init time because "after"
    method need an instance of root window or widget.
    """
    self._timer_function = function
    self._timer_period = period

  def _timer_wrap(self):
    "Call given function reschedule it after return"
    self._timer_function()
    return self._toplevel_widgets[0].after(int(self._timer_period * 1000.0),
      self._timer_wrap)


  #### WIDGETS ABSTRACTION LAYER (widget toolkit side)

  class _Button(AVCCore._Button):
    "Tk Button widget abstractor"

    def _init(self):

      # create button press status variable
      self.widget.value = False

      # connect relevant signals
      self.widget.bind("<ButtonPress-1>",
        lambda dummy: self.coget.__set__(self,True,self.widget))
      self.widget.bind("<ButtonRelease-1>",
        lambda dummy: self.coget.__set__(self,False,self.widget))


    def get_value(self):
      "Get button status"
      return self.widget.value

    def set_value(self,value):
      "Set button status"
      self.widget.value = value


  class _Entry(AVCCore._Entry):
    "Tk Entry widget abstractor"

    def _init(self):

      # connect relevant signals to handlers
      self.widget.bind("<Return>",self._value_changed)


    def _get_value(self):
      "Get text from Entry"
      return self.widget.get()
    
    def set_value(self,value):
      "Set text into Entry"
      self.widget.delete(0,Tkinter.END)
      self.widget.insert(0,str(value))

 
  class _Label(AVCCore._Label):
    "Tk Label widget abstractor"

    def _get_value(self):
      "Get value into Label"
      return self.widget.cget('text')

    def _set_value(self,value):
      "Set text into Label"
      self.widget.config(text=value)


  class _RadioButton(AVCCore._RadioButton):
    "Tk RadioButton widget abstractor"

    def _init(self):

      # if not yet done, get existing (by default) variable with pressed
      # button index.
      if not hasattr(self.coget,'active_index_name'):
        self.coget.active_index_name = str(self.widget.cget("variable"))
    
      # connect relevant signals
      self.widget.bind("<ButtonRelease-1>",self._value_changed)


    def get_value(self):
      "Get index of activated button"
      return int(str(self.widget.getvar(self.coget.active_index_name)))

    def set_value(self,value):
      "Set activate button indexed by value"
      self.widget.setvar(self.coget.active_index_name,value)


  class _Slider(AVCCore._Slider):
    "Tk Scale widget abstractor"

    def _init(self):

      # connect relevant signals to handlers
      self.widget.config(command=self._value_changed)
 

    def _get_value(self):
      "Get Slider value"
      return self.widget.get()

    def set_value(self,value):
      "Set Slider value"
      self.widget.set(str(value))


  class _SpinButton(AVCCore._SpinButton):
    "Tk SpinButton widget abstractor"

    def _init(self):

      # connect relevant signals to handlers
      self.widget.bind("<Return>",self._value_changed)
      self.widget.config(command=self._value_changed)


    def _get_value(self):
      "Get spin button value"
      return self.widget.get()

    def set_value(self,value):
      "Set spinbutton value"
      self.widget.delete(0,Tkinter.END)
      self.widget.insert(0,str(value))
 

  class _TextView(AVCCore._TextView):
    "Tk TextView widget abstractor"

    def _init(self):

      # connect relevant signals to handlers
      self.widget.bind("<Return>",self._value_changed)


    def get_value(self):
      "Get text from TextView"
      return self.widget.get("1.0",Tkinter.END)
    
    def set_value(self,value):
      "Set text into TextView"
      self.widget.delete("1.0",Tkinter.END)
      self.widget.insert("1.0",str(value))


  class _ToggleButton(AVCCore._ToggleButton):
    "Tk ToggleButton widget abstractor"

    def _init(self):

      # get and save button value variable name
      self.value_name = str(self.widget.cget('variable'))

      # connect relevant signals
      self.widget.bind("<ButtonRelease-1>",self._value_changed)


    def get_value(self):
      "Get button status"
      return bool(int(self.widget.getvar(self.value_name)))

    def set_value(self,value):
      "Set button status"
      self.widget.setvar(self.value_name,int(value))


  ## mapping between the real widget and the wal widget

  _WIDGETS_MAP = { \
  Tkinter.Button: _Button,\
  Tkinter.Checkbutton: _ToggleButton, \
  Tkinter.Entry: _Entry, \
  Tkinter.Label: _Label, \
  Tkinter.Radiobutton: _RadioButton, \
  Tkinter.Scale: _Slider, \
  Tkinter.Spinbox: _SpinButton,
  Tkinter.Text: _TextView}

#### END

