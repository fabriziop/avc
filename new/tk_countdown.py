#!/usr/bin/python
# .+
#
# .identifier :	$Id:$
# .context    : Application View Controller
# .title      : A counter with count speed control (Tk)
# .kind	      : python source
# .author     : Fabrizio Pollastri
# .site	      : Torino - Italy
# .creation   :	12-May-2008
# .copyright  : (c) 2008 Fabrizio Pollastri.
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

from avc import *			# AVC for Tk

from random import randint		# random integer generator

TCL_MAIN = 'tk_countdown_main.tcl'	# main GUI as tcl script
TCL_CD = 'tk_countdown.tcl'		# count down GUI as tcl script
TOPLEVEL_NAME = 'countdown'		# name of the top level widget
COUNTDOWN_PERIOD = 500			# count down at 2 unit per second
MAX_CREATION_PERIOD = 4000		# create a new count down at 1/2 this


class Countdown(AVC):
  """
  A countdown counter displayed in a Label widget. Count starts at given
  value. When count reaches zero the counter and its GUI are destroyed.
  """

  def __init__(self,count_start=10):

    # create GUI
    self.root = Tk()
    self.root.eval('set argc {}; set argv {}; proc ::main {argc argv} {};')
    self.root.tk.evalfile(TCL_CD)

    # init the counter variable 
    self.counter = count_start

    # connect counter variable with label widget
    self.avc_connect(self.root)

    # start count down
    self.root.after(COUNTDOWN_PERIOD,self.decrementer)


  def decrementer(self):
    "Counter decrementer. Return False to destroy previous timer."
    self.counter -= 1
    if self.counter:
      # if counter not zero: reschedule count timer
      self.root.after(COUNTDOWN_PERIOD,self.decrementer)
    else:
      # counter reached zero: destroy this countdown and its GUI
      self.root.destroy()


class Example(AVC):
  """
  Continuosly create at random intervals windows with a countdown from 10 to 0.
  When a countdown reaches zero, its window is destroyed. Also create a main
  window with a "close all" button.
  """

  def __init__(self):

    # create GUI
    self.root = Tk()
    self.root.eval('set argc {}; set argv {}; proc ::main {argc argv} {};')
    self.root.tk.evalfile(TCL_MAIN)

    # terminate program at toplevel window destroy: connect toplevel
    # destroy signal to termination handler.
    self.root.bind_class('Toplevel','<Destroy>',lambda event: self.root.quit())

    # create the first countdown
    self.new_countdown()

    # close all button connected variable
    self.close_all = False

    # connect counter variable with label widget
    self.avc_connect(self.root)


  def new_countdown(self,count_start=10):
    "Create a new countdown"

    # create a new countdown
    Countdown(count_start)

    # autocall after a random delay
    self.root.after(randint(1,MAX_CREATION_PERIOD),self.new_countdown) 


  def close_all_changed(self,value):
    "Terminate program at 'close all' button pressing"
    self.root.quit()


#### MAIN

example = Example()			# instantiate the application
Tkinter.mainloop()		 	# run Tk event loop until quit

#### END
