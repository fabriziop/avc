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

from gtkmvc import Model		#---
from gtkmvc import Controller		#--
from gtkmvc import View			#- MVC support

from random import randint		# random integer generator


class ExampleModel(Model):
  """
  The model contains the integer values of 3 sliders and the sum of these
  3 values.
  """

  __properties__ = {
    'slider1' : 0,
    'slider2' : 0,
    'slider3' : 0,
    'sliders_sum' : 0, 
    }

  def __init__(self):
    Model.__init__(self)
    return

  def reset(self):
    self.slider1 = 0
    self.slider2 = 0
    self.slider3 = 0
    self.sliders_sum = 0


class ExampleController(Controller):
  """
  MVC processing, keep model values coherent with view. Widgets handlers.
  """

  def __init__(self, model):
    Controller.__init__(self, model)
    return

  def register_view(self, view):
    Controller.register_view(self, view)

    # sets initial values for the view
    self.view.set_sliders_sum_value(self.model.sliders_sum)
    self.view.set_slider1_value(self.model.slider1)
    self.view.set_slider2_value(self.model.slider2)
    self.view.set_slider3_value(self.model.slider3)

    return


  ## gtk signals

  def on_destroy(self, window):
    gtk.main_quit()
    return True

  ## widgets handlers

  def on_button_reset_clicked(self, button):
    self.model.reset()
    return

  def on_button_random_clicked(self, button):
    self.model.slider1 = randint(0,100)
    self.model.slider2 = randint(0,100)
    self.model.slider3 = randint(0,100)
    self.model.sliders_sum = self.model.slider1 + self.model.slider2 + \
      self.model.slider3
    return

  def on_slider1_value_changed(self, slider):
    self.model.slider1 = slider.get_value()
    self.model.sliders_sum = self.model.slider1 + self.model.slider2 + \
      self.model.slider3
    return

  def on_slider2_value_changed(self, slider):
    self.model.slider2 = slider.get_value()
    self.model.sliders_sum = self.model.slider1 + self.model.slider2 + \
      self.model.slider3
    return

  def on_slider3_value_changed(self, slider):
    self.model.slider3 = slider.get_value()
    self.model.sliders_sum = self.model.slider1 + self.model.slider2 + \
      self.model.slider3
    return

    
  ## observable properties
    
  def property_slider1_value_change(self, model, old, new):
    self.view.set_slider1_value(new)
    return
    
  def property_slider2_value_change(self, model, old, new):
    self.view.set_slider2_value(new)
    return
    
  def property_slider3_value_change(self, model, old, new):
    self.view.set_slider3_value(new)
    return
    
  def property_sliders_sum_value_change(self, model, old, new):
    self.view.set_sliders_sum_value(new)
    return
    

class ExampleView(View):
    """
    Create GUI from Glade descriptor. Widgets setting values methods.
    """
    
    GLADE = "gtk_sum.glade"		# GUI glade descriptor

    def __init__(self, ctrl):
        View.__init__(self, ctrl, self.GLADE)
        return

    def set_sliders_sum_value(self, val):
        self['sliders_sum'].set_markup("<big><b>%d</b></big>" % val)
        return

    def set_slider1_value(self, val):
        self['slider1'].set_value(val)
        return

    def set_slider2_value(self, val):
        self['slider2'].set_value(val)
        return

    def set_slider3_value(self, val):
        self['slider3'].set_value(val)
        return


#### MAIN

model = ExampleModel()
controller = ExampleController(model)
view = ExampleView(controller)

gtk.main()

#### END
