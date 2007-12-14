#!//usr/bin/python

import gtk

from gtkmvc import Model
from gtkmvc import Controller
from gtkmvc import View

from random import randint


class ExampleModel(Model):
  """
  Our model contains a numeric counter and a numeric value that
  holds the value that the counter must be assigned to when we the
  model is reset
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
  Handles signal processing, and keeps alignment of model and view
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


  # gtk signals
  def on_destroy(self, window):
    gtk.main_quit()
    return True

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

    
  # observable properties
    
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
    """This handles only the graphical representation of the
    application. The widgets set is loaded from glade file"""
    
    GLADE = "gtk_sum.glade"

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
