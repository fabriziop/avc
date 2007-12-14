#!/usr/bin/python
# .+
#
# .identifier :	$Id:$
# .context    : Application View Controller
# .title      : A spin control replicated into a label (wx)
# .kind	      : python source
# .author     : Fabrizio Pollastri
# .site	      : Revello - Italy
# .creation   :	24-Nov-2007
# .copyright  : (c) 2007 Fabrizio Pollastri.
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


import wx				# wx tool kit bindings

from avc.avcwx import *			# AVC for wx


class Example(wx.PySimpleApp,AVC):
  """
  A spin control whose value is replicated into a static text
  """

  def __init__(self):

    ## create GUI

    # init wx application base class
    wx.PySimpleApp.__init__(self)

    # create widgets: a top level window, a label and a spin control.
    root = wx.Frame(None,title='AVC wx spin control example',size=(320,60))
    label = wx.StaticText(root,label='%s',name='spin_value__label',
      size=(100,20))
    spin = wx.SpinCtrl(root,name='spin_value__spin',size=(100,25))

    # layout the label and the spin control horizontally into the window
    hsizer = wx.BoxSizer(wx.HORIZONTAL)
    hsizer.Add((20,10),proportion=1)
    hsizer.Add(label,proportion=0.5,flag=wx.CENTER)
    hsizer.Add(spin,proportion=0.5,flag=wx.CENTER)
    hsizer.Add((20,10),proportion=1)
    root.SetSizer(hsizer)
    root.Show()

    ## the variable holding the spin button value
    self.spin_value = 0


#### MAIN

example = Example()			# instantiate the application
example.avc_init()			# connect widgets with variables
example.MainLoop()		 	# run wx event loop until quit

#### END
