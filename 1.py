# -*- coding: cp936 -*-
import wx
app=wx.App()
basicframe = wx.Frame(None,title="Xx�ļ��±�")
panel = wx.Panel(basicframe)
openbutton = wx.Button(basicframe,label='�򿪼��±�')
savebutton = wx.Button(basicframe,label='������±�')
selectfile = wx.TextCtrl(basicframe)
inputframe = wx.TextCtrl(basicframe,style=wx.TE_MULTILINE|wx.HSCROLL)
topbox = wx.BoxSizer()
topbox.Add(selectfile,proportion=1,flag=wx.EXPAND)
topbox.Add(openbutton,proportion=0,flag=wx.LEFT,border=5)
topbox.Add(savebutton,proportion=0,flag=wx.LEFT,border=5)

bottombox =wx.BoxSizer(wx.VERTICAL)#�ڶ���box���½ṹ���֣��������һ����Box
bottombox.Add(topbox,proportion=0,flag=wx.EXPAND|wx.ALL,border=5)
bottombox.Add(inputframe,proportion=1,flag=wx.EXPAND|wx.LEFT|wx.BOTTOM|wx.RIGHT,border=5)

panel.SetSizer(bottombox)

basicframe.Show()
app.MainLoop()