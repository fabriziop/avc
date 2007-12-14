#!/usr/bin/python

import wx
from wx import xrc

a = wx.PySimpleApp()
#x = xrc.XmlResource('wx_showcase.xml')
#f = x.LoadFrame(None,'frame_1')
f = wx.Frame(None,200,'test')
c = wx.CheckBox(f,100,label='high speed')
f.Show()

def checked(event):
  #print 'checked=',event.IsChecked()
  event.Skip()
  print 'event obj value=',event.GetEventObject().GetValue()
  event.Skip()
  print 'event obj value=',event.GetEventObject().GetValue()

c.Bind(wx.EVT_LEFT_UP,checked)

#b.Bind(wx.EVT_LEFT_UP,clicked)
#b.Bind(wx.EVT_BUTTON,clicked)

a.MainLoop()
