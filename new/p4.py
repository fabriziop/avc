#!/usr/bin/python

import wx

a = wx.PySimpleApp()
f1 = wx.Frame(None,size=(200,200))
b1 = wx.Button(f1,-1,'button1')
#f2 = wx.Frame(None,size=(200,200))
#b2 = wx.Button(f2,-1,'button2')
f1.Show()
#f2.Show()
print b1.GetClassDefaultAttributes()
c = b1.GetBackgroundColour().Get()
print c, type(c)
z = 0.7
new_back = (c[0] * z, c[1] * z, c[2] * z)
print c,new_back
#b2.SetBackgroundColour(new_back)

def hand(event):
  print b1.GetBackgroundColour()
 # print b1.GetBackgroundStyle()
  event.Skip()

def h2(event):  
  #b1.Bind(wx.EVT_LEFT_UP,hand)
  ce = wx.CommandEvent(commandType=wx.wxEVT_COMMAND_BUTTON_CLICKED)
  b1.Command(ce)

timer = wx.Timer(f1)
f1.Bind(wx.EVT_TIMER,h2,timer)
timer.Start(1000,oneShot=True)

a.MainLoop()
