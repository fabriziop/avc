#!/usr/bin/python

import wx

class MyApp(wx.App):
  def OnInit(self):
    frame = wx.Frame(None,-1,"TEST")
    id=wx.NewId()
    self.list=wx.ListCtrl(frame,id,style=wx.LC_REPORT)
    self.list.InsertColumn(0,"HEADER 0")
    self.list.InsertStringItem(0,"ITEM 0")
    frame.Show(True)
    # start a wx timer calling back toggle header every 2 seconds."
    self.timer1 = wx.Timer(frame,wx.NewId())
    frame.Bind(wx.EVT_TIMER,self.toggle_header,self.timer1)
    self.timer1.Start(2000,oneShot=False)
    return True


  def toggle_header(self,event):
    column = self.list.GetColumn(0)
    print column.GetText()
    if column.GetText() == 'HEADER 0':
      column.SetText('HEADER 0 TOGGLED')
      self.list.SetColumn(0,column)
    else:
      column.SetText('HEADER 0')
      self.list.SetColumn(0,column)
    print column.GetText()


app = MyApp(0)
app.MainLoop()

