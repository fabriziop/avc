#!/usr/bin/python

import wx

a = wx.PySimpleApp()
f = wx.Frame(None,size=(200,200))
f.Show()

def timeout(event):
  print 'timeout'
  yield 0

timer = wx.Timer(f,wx.NewId())
f.Bind(wx.EVT_TIMER,timeout,timer)
timer.Start(1000,oneShot=False)

a.MainLoop()
