#!/usr/bin/python
import wx
a = wx.PySimpleApp()
f = wx.Frame(None,size=(200,200))
r = wx.RadioBox(f,-1,'test',choices=['a'])
print r.__class__ ==  wx.RadioBox
f.Show()
a.MainLoop()

