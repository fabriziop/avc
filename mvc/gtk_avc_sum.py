#!/usr/bin/python
# .+
#
# .identifier :	$Id:$
# .context    : Application View Controller
# .title      : Sum of 3 sliders with reset and random buttons (GTK)
# .kind	      : python source
# .author     : Fabrizio Pollastri
# .site	      : Revello - Italy
# .creation   :	11-Dec-2007
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


import gtk				# gimp tool kit bindings
import gtk.glade			# glade bindings

from avc.avcgtk import *		# AVC for GTK

from random import randint		# random integer generator
GLADE_XML = 'gtk_sum.glade'		# GUI glade descriptor


class Example(AVC):
  """
  The sum of the values of 3 sliders is displayed in a label widget. The
  sliders values can be reset to zero by the 'reset' button or set to random
  values by the 'random' button.
  """

  def __init__(self):

    # create GUI
    self.glade = gtk.glade.XML(GLADE_XML)

    # autoconnect GUI signal handlers
    self.glade.signal_autoconnect(self)

    # the connected variables
    self.sliders_sum = 0
    self.slider1 = 0
    self.slider2 = 0
    self.slider3 = 0
    self.random = False
    self.reset = False


  ## GUI signal handler

  def on_destroy(self,window):
    "Terminate program at window destroy"
    gtk.main_quit()

  ## AVC widget handlers

  def reset_changed(self,value):
    "Reset sliders and sum"
    if not value:
      self.slider1 = 0
      self.slider2 = 0
      self.slider3 = 0
      self.sliders_sum = 0

  def random_changed(self,value):
    "Set sliders to 3 random values and update sum"
    if not value:
      self.slider1 = randint(0,100)
      self.slider2 = randint(0,100)
      self.slider3 = randint(0,100)
      self.sliders_sum = self.slider1 + self.slider2 + self.slider3

  def slider1_changed(self,value):
    "Update sum"
    self.sliders_sum = self.slider1 + self.slider2 + self.slider3

  # clone slider 2 and 3 handlers from slider 1 handler
  slider2_changed = slider1_changed
  slider3_changed = slider1_changed


#### MAIN

example = Example()			# instantiate the application
example.avc_init()			# connect widgets with variables
gtk.main()			 	# run GTK event loop until quit

#### END
