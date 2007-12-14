#!/usr/bin/python
# .+
#
# .identifier :	$Id:$
# .context    : Application View Controller
# .title      : A counter with count speed control (GTK)
# .kind	      : python source
# .author     : Fabrizio Pollastri
# .site	      : Revello - Italy
# .creation   :	17-Nov-2006
# .copyright  : (c) 2006 Fabrizio Pollastri.
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


import gtk				# gimp tool kit bindings
import gtk.glade			# glade bindings

from avc.avcgtk import *		# AVC for GTK

GLADE_XML = 'avc_basic.glade'		# GUI glade descriptor


class Example(AVC):
  """
  A counter displayed in a Label widget whose count speed can be
  accelerated by checking a check button.
  """

  def __init__(self):

    # create GUI
    self.glade = gtk.glade.XML(GLADE_XML)

    # autoconnect GUI signal handlers
    self.glade.signal_autoconnect(self)

    # the counter variable and its reset value
    self.counter = 0
    self.reset_value = 0
    self.reset = False
    self.increment = False


  def on_destroy(self,window):
    "Terminate program at window destroy"
    gtk.main_quit()

  def reset_changed(self,value):
    "Reset counter to the reset value"
    if not value:
      self.counter = self.reset_value

  def increment_changed(self,value):
    "Increment counter by 1"
    if not value:
      self.counter += 1


#### MAIN

example = Example()			# instantiate the application
example.avc_init()			# connect widgets with variables
gtk.main()			 	# run GTK event loop until quit

#### END
