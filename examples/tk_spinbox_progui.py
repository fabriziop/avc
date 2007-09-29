#!/usr/bin/python
# .+
#
# .identifier :	$Id: mdgY.py,v 1.6 2005/01/04 10:00:13 fabrizio Exp $
# .context    : Application View Controller
# .title      : A spin control replicated into a text label (Tk)
# .kind	      : python source
# .author     : Fabrizio Pollastri
# .site	      : Revello - Italy
# .creation   :	1-Jun_2007
# .copyright  : (c) 2007 Fabrizio Pollastri
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


from Tkinter import *			# Tk interface

from avc.avctk import *			# AVC for Tk


class Example(AVC):
  """
  A spin control whose value is replicated into a label
  """

  def __init__(self):

    # create GUI
    self.root = Tk()
    self.root.title('AVC Tk spin box example')
    self.frame = Frame(self.root,name='frame')
    self.frame.pack()
    self.label = Label(self.frame,name='spin_value__label')
    self.label.pack(side=LEFT)
    self.spin_box = Spinbox(self.frame,name='spin_value__spinbox',
      increment=1.0,to=100)
    self.spin_box.pack(side=RIGHT)

    # the variable holding the spin control value
    self.spin_value = 0


#### MAIN

example = Example()			# instantiate the application
example.avc_init()			# connect widgets with variables
Tkinter.mainloop()		 	# run Tk event loop until quit

#### END
