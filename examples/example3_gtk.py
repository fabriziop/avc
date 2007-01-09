#!/usr/bin/python
# .+
#
# .identifier :	$Id:$
# .context    : Application View Controller
# .title      : A table of all supported widget/control type conbinations (GTK)
# .kind	      : python source
# .author     : Fabrizio Pollastri
# .site	      : Revello - Italy
# .creation   :	19-Nov-2006
# .copyright  : (c) 2006 Fabrizio Pollastri.
# .license    : GNU General Public License (see .copying below)
#
# .copying
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
#
# .-


import gobject				#--
import gtk				#- gimp tool kit bindings
import gtk.glade			# glade bindings

from avc.avcgtk import *		# AVC for GTK


GLADE_XML = 'example3_gtk.glade'	# GUI glade descriptor
INCREMENTER_PERIOD = 333		# ms


class Example(AVC):
  "A table of all supported widget/control type combinations"

  def __init__(self):

    # create GUI
    self.glade = gtk.glade.XML(GLADE_XML)

    # autoconnect GUI signal handlers
    self.glade.signal_autoconnect(self)

    # the control variables
    self.boolean1 = False
    self.boolean2 = False
    self.radio = 0
    self.integer = 0
    self.float = 0.0
    self.string = ''

    # start variables incrementer
    increment = self.incrementer()
    gobject.timeout_add(INCREMENTER_PERIOD,increment.next) 


  def incrementer(self):
    """
    Booleans are toggled, radio button index is rotated from first to last,
    integer is incremented by 1, float by 0.5, string is appended a char
    untill maxlen when string is cleared. Return True to keep timer alive.
    """
    while True:

      self.boolean1 = not self.boolean1
      yield True

      self.boolean2 = not self.boolean2
      yield True

      if self.radio >= 2:
        self.radio = 0
      else:
        self.radio += 1
      yield True

      self.integer += 1
      yield True

      self.float += 0.5
      yield True

      if len(self.string) >= 20:
        self.string = 'A'
      else:
        self.string += 'A'
      yield True


  def on_destroy(self,window):
    "Terminate program at window destroy"
    gtk.main_quit()


#### MAIN

example = Example()			# instantiate the application
example.avc_init()			# connect widgets with variables
gtk.main()			 	# run GTK event loop until quit

#### END