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
# but WITHOUT ANY WARRANTY; without even the implied warranty ofxi
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


GLADE_XML = 'example2_gtk.glade'	# GUI glade descriptor
LOW_SPEED = 500				#--
HIGH_SPEED = 100			#- low and high speed period (ms)


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

    # the counter variable and its speed status
    self.counter = 0
    self.high_speed = False

    # start counter incrementer at low speed
    gobject.timeout_add(LOW_SPEED,self.incrementer) 


  def incrementer(self):
    """
    Counter incrementer: increment period = LOW_SPEED, if high speed is False,
    increment period = HIGH_SPEED otherwise. Return False to destroy previous
    timer.
    """
    self.counter += 1
    if self.high_speed:
      period = HIGH_SPEED
    else:
      period = LOW_SPEED
    gobject.timeout_add(period,self.incrementer) 
    return False


  def on_destroy(self,window):
    "Terminate program at window destroy"
    gtk.main_quit()


#### MAIN

example = Example()			# instantiate the application
example.avc_init()			# connect widgets with variables
gtk.main()			 	# run GTK event loop until quit

#### END