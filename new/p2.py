#!/usr/bin/python

import wx

a = wx.PySimpleApp()
f = wx.Frame(None,size=(200,200))
t = wx.TextCtrl(f,-1,'aaa')
f.Show()

def get_text(event):
  print 'get text value = ', t.GetValue(),map(ord,t.GetValue())

def set_text(event):
  print 'set text before setting value = ', t.GetValue()
  t.SetValue('bbb')
  print 'set text after setting value = ', t.GetValue()
  
t.Bind(wx.EVT_TEXT,get_text)

timer = wx.Timer(f,wx.NewId())
f.Bind(wx.EVT_TIMER,set_text,timer)
timer.Start(1000,oneShot=True)

a.MainLoop()
