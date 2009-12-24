#!/usr/bin/python

import wx				# wx tool kit bindings
from wx import xrc			# xml resource support

from avc import *			# AVC

import copy				# object cloning support

WXGLADE_XML = 'wx_listtreectrl.xrc'	# GUI wxGlade descriptor

UPDATE_PERIOD = 2000			# ms


class Example(wx.PySimpleApp,AVC):
  """
  Showcase of display capabilities for the list control and tree control widgets
  """

  def __init__(self):

    # init wx application base class
    wx.PySimpleApp.__init__(self)

    # create GUI
    xml_resource = xrc.XmlResource(WXGLADE_XML)
    self.root = xml_resource.LoadFrame(None,'frame_1')
    self.root.Show()

    # connected variables
    self.list = {'head':['col1 int','col2 str'], \
      'body':[[1,'one'],[2,'two'],[3,'three']]}
    self.list_work = copy.deepcopy(self.list)
    self.tree = {'body':{ \
      # root rows
      '1':'one', \
      '2':'two', \
      # children of root row '1'
      '1.1':'one one', \
      '1.2':'one two', \
      # children of root row '2'
      '2.1':'two one', \
      '2.2':'two two'}}

    # start a wx timer calling back 'function' every 'period' seconds."
    self.timer1 = wx.Timer(self.root,wx.NewId())
    self.root.Bind(wx.EVT_TIMER,self.update_wrap,self.timer1)
    self.timer1.Start(UPDATE_PERIOD,oneShot=False)


  def update_wrap(self,event):
    "Discard event argument and call the real update iterator"
    self.update().next()

  def update(self):
    """
    Tabular data rows data are rolled down.
    """
    rows_num = len(self.list['body'])
    while True:
      # save last row of data
      last_row = self.list_work['body'][-1]
      # shift down one position each data row
      for i in range(1,rows_num): 
        self.list_work['body'][-i] = \
          self.list_work['body'][-1-i]
      # copy last row into first position
      self.list_work['body'][0] = last_row
      # copy working copy into connected variable
      self.list_work['head'] = ['aaa','bbb']
      self.list = self.list_work
      yield True


#### MAIN

example = Example()			# instantiate the application
example.avc_init()			# connect widgets with variables
example.MainLoop()			# run wx event loop until quit

#### END
