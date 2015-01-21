# -*- coding: cp936 -*-

#!/usr/bin/env python 
# -*- coding: utf-8 -*- 
 
'''''
    Function:������ʾ
    Input��NONE
    Output: NONE
    author: yanbo_yang
    date:2014/01/15
'''''
import wx 
import wx.lib.buttons 
import cPickle 
import os
import wx.grid
import psutil
class GetProc():
    pidandname={}
    def getpid(self):
        self.proclist=psutil.pids()
        return self.proclist
    def getlistnum(self):
        self.listnum=len(self.proclist)
        return self.listnum
    def getpidname(self):
        for i in self.getpid()[1:]:
            try:
                self.pidandname[i]=psutil.Process().name()
            except NameError:
                print "'%s' Process is not allowing us to view the CPU Usage!" % i

        return self.pidandname 
       
class ControlPanel(wx.Panel): 
    BMP_SIZE = 16  
    BMP_BORDER = 3 
    NUM_COLS = 4 
    SPACING = 1 
     
    colorList = ('Black', 'Yellow', 'Red', 'Green', 'Blue', 'Purple', 
                 'Brown', 'Aquamarine', 'Forest Green', 'Light Blue', 
                 'Goldenrod', 'Cyan', 'Orange', 'Navy', 'Dark Grey', 
                 'Light Grey') 
    maxThickness = 16 
     
    def __init__(self, parent, ID): 
        wx.Panel.__init__(self, parent, ID, style = wx.RAISED_BORDER)  
        buttonSize = (self.BMP_SIZE + 2 * self.BMP_BORDER, 
                      self.BMP_SIZE + 2 * self.BMP_BORDER) 
        Grid = ProcessTable(self) #������ɫgrid sizer
        box = wx.BoxSizer(wx.VERTICAL) #ʹ�ô�ֱ��box szier����grid sizer 
        box.Add(Grid, 0, wx.ALL, self.SPACING) #����0��ʾ�ڴ�ֱ������չʱ���ı�ߴ�
        self.SetSizer(box)
        self.Fit()
       
        #thicknessGrid = self.createThicknessGrid(buttonSize) #��������grid sizer 
        #self.layout(colorGrid, thicknessGrid) 
         
    def createColorGrid(self, parent, buttonSize): 
        self.colorMap = {} 
        self.colorButtons = {} 
        colorGrid = wx.GridSizer(cols = self.NUM_COLS, hgap = 2, vgap = 2) 
        for eachColor in self.colorList: 
            bmp = self.MakeBitmap(eachColor) 
            b = wx.lib.buttons.GenBitmapToggleButton(self, -1, bmp, size = buttonSize) 
            b.SetBezelWidth(1) 
            b.SetUseFocusIndicator(False) 
            self.Bind(wx.EVT_BUTTON, self.OnSetColour, b) 
            colorGrid.Add(b, 0) 
            self.colorMap[b.GetId()] = eachColor 
            self.colorButtons[eachColor] = b 
        self.colorButtons[self.colorList[0]].SetToggle(True) 
        return colorGrid 
     
    def createThicknessGrid(self, buttonSize): 
        self.thicknessIdMap = {} 
        self.thicknessButtons = {} 
        thicknessGrid = wx.GridSizer(cols = self.NUM_COLS, hgap = 2, vgap = 2) 
        for x in range(1, self.maxThickness + 1): 
            b = wx.lib.buttons.GenToggleButton(self, -1, str(x), size = buttonSize) 
            b.SetBezelWidth(1) 
            b.SetUseFocusIndicator(False) 
            self.Bind(wx.EVT_BUTTON, self.OnSetThickness, b) 
            thicknessGrid.Add(b, 0) 
            self.thicknessIdMap[b.GetId()] = 2 
            self.thicknessButtons[x] = b 
        self.thicknessButtons[1].SetToggle(True) 
        return thicknessGrid 
     
    def layout(self, colorGrid, thicknessGrid): 
        box = wx.BoxSizer(wx.VERTICAL) #ʹ�ô�ֱ��box szier����grid sizer 
        box.Add(colorGrid, 0, wx.ALL, self.SPACING) #����0��ʾ�ڴ�ֱ������չʱ���ı�ߴ� 
        box.Add(thicknessGrid, 0, wx.ALL, self.SPACING) 
        self.SetSizer(box) 
        box.Fit(self) 
             
    def OnSetColour(self, event): 
        color = self.colorMap[event.GetId()] 
        if color != self.paint.color: 
            self.colorButtons[self.paint.color].SetToggle(False) 
        self.paint.SetColor(color) 
         
    def OnSetThickness(self, event): 
        thickness = self.thicknessIdMap[event.GetId()] 
        if thickness != self.paint.thickness: 
            self.thicknessButtons[self.paint.thickness].SetToggle(False) 
        self.paint.SetThickness(thickness) 
 
    def MakeBitmap(self, color): 
        bmp = wx.EmptyBitmap(16, 15) 
        dc = wx.MemoryDC(bmp) 
        dc.SetBackground(wx.Brush(color)) 
        dc.Clear() 
        dc.SelectObject(wx.NullBitmap) 
        return bmp
class ProcessTable(wx.grid.Grid):
    def __init__(self,parent):
        wx.grid.Grid.__init__(self,parent)
        self.CreateGrid(70,2)
        self.SetColLabelValue( 0, "Process Id" )
        self.SetColLabelValue( 1, "Process Name" )
        self.SetMinSize((340,1000))
        self.SetColSize ( 1, 160 )
        self.SetColSize ( 0, 80 )
        a=GetProc()
        dic=a.getpidname()
        i=0
        for pid,name in dic.items():
            self.SetCellValue(i,0,str(pid))
            self.SetCellValue(i,1,name)
            i=i+1
   # grid.CreateGrid(5,5)
    #for row in range(5):
     #   for col in range(5):
      #      self.grid.SetCellValue(row, col, "(%s,%s)" % (row, col))
        
       # grid.SetCellSize(2, 2, 2, 3)       
        #grid.SetColSize(1, 125) 
        #grid.SetRowSize(1, 100)
class ProcessorsPanel(wx.Panel): 
        def __init__(self, parent, ID): 
            wx.Panel.__init__(self, parent, ID, style = wx.RAISED_BORDER)
           
         
        def InitBuffer(self): 
            size = self.GetClientSize() 
             
            #����������豸������ 
            self.buffer = wx.EmptyBitmap(size.width, size.height) 
            dc = wx.BufferedDC(None, self.buffer)
           
             
            #ʹ���豸������ 
            dc.SetBackground(wx.Brush(self.GetBackgroundColour())) 
            dc.Clear() 
            self.DrawLines(dc) 
            self.reInitBuffer = False 
             
        def GetLinesData(self): 
            return self.lines[:] 
         
        def SetLinesData(self, lines): 
            self.lines = lines[:] 
            self.InitBuffer() 
            self.Refresh() 
             
        def OnLeftDown(self, event): 
            self.curLine = [] 
             
            #��ȡ���λ�� 
            self.pos = event.GetPositionTuple() 
            self.CaptureMouse() 
             
        def OnLeftUp(self, event): 
            if self.HasCapture(): 
                self.lines.append((self.color, 
                                   self.thickness, 
                                   self.curLine)) 
                self.curLine = [] 
                self.ReleaseMouse() 
                 
        def OnMotion(self, event): 
            if event.Dragging() and event.LeftIsDown(): 
                dc = wx.BufferedDC(wx.ClientDC(self), self.buffer) 
                self.drawMotion(dc, event) 
            event.Skip() 
         
        def drawMotion(self, dc, event): 
            dc.SetPen(self.pen) 
            newPos = event.GetPositionTuple() 
            coords = self.pos + newPos 
            self.curLine.append(coords) 
            dc.DrawLine(*coords) 
            self.pos = newPos 
             
        def OnSize(self, event): 
            self.reInitBuffer = True 
         
        def OnIdle(self, event): 
            if self.reInitBuffer: 
                self.InitBuffer() 
                self.Refresh(False) 
         
        def OnPaint(self, event): 
            dc = wx.BufferedPaintDC(self, self.buffer) 
             
        def DrawLines(self, dc): 
            for colour, thickness, line in self.lines: 
                pen = wx.Pen(colour, thickness, wx.SOLID) 
                dc.SetPen(pen) 
                for coords in line: 
                    dc.DrawLine(*coords) 
         
        def SetColor(self, color): 
            self.color = color 
            self.pen = wx.Pen(self.color, self.thickness, wx.SOLID) 
             
        def SetThickness(self, num): 
            self.thickness = num 
            self.pen = wx.Pen(self.color, self.thickness, wx.SOLID) 
             
class PaintFrame(wx.Frame): 
     
    def __init__(self, parent): 
        self.title = "Process Frame" 
        wx.Frame.__init__(self, parent, -1, self.title, size = (800, 600)) 
        self.processor = ProcessorsPanel(self, -1) 
         
        #״̬�� 
        #self.paint.Bind(wx.EVT_MOTION, self.OnPaintMotion) 
        self.InitStatusBar() 
         
        #�����˵� 
        self.CreateMenuBar() 
         
        self.filename = "" 
         
        #����������ʹ�õ���� 
        self.CreatePanel() 
     
    def CreatePanel(self): 
        controlPanel = ControlPanel(self, -1) 
        box = wx.BoxSizer(wx.HORIZONTAL) #����ˮƽ��box sizer 
        box.Add(controlPanel, 0, wx.EXPAND) #ˮƽ������չʱ���ı�ߴ� 
        box.Add(self.processor, -1, wx.EXPAND)
      
        self.SetSizer(box)
        #self.Fit()
         
 
         
    def InitStatusBar(self): 
        self.statusbar = self.CreateStatusBar() 
        #��״̬���ָ�Ϊ3������,����Ϊ1:2:3 
        self.statusbar.SetFieldsCount(3) 
        self.statusbar.SetStatusWidths([-1, -2, -3])    
         
    def OnPaintMotion(self, event): 
         
        #����״̬��1���� 
        self.statusbar.SetStatusText(u"���λ�ã�" + str(event.GetPositionTuple()), 0) 
         
        #����״̬��2���� 
        self.statusbar.SetStatusText(u"��ǰ�������ȣ�%s" % len(self.paint.curLine), 1) 
         
        #����״̬��3���� 
        self.statusbar.SetStatusText(u"������Ŀ��%s" % len(self.paint.lines), 2)    
              
        event.Skip() 
         
    def MenuData(self): 
        '''''
                   �˵�����
        ''' 
        #��ʽ���˵����ݵĸ�ʽ������(��ǩ, (��Ŀ))�����У���Ŀ���Ϊ����ǩ, ��������, ������, ��ѡ��kind 
        #��ǩ����Ϊ2����Ŀ�ĳ�����3��4 
        return [("&File", (             #һ���˵��� 
                           ("&New", "New paint file", self.OnNew),             #�����˵��� 
                           ("&Open", "Open paint file", self.OnOpen), 
                           ("&Save", "Save paint file", self.OnSave), 
                           ("", "", ""),                                       #�ָ��� 
                           ("&Color", ( 
                                       ("&Black", "", self.OnColor, wx.ITEM_RADIO),  #�����˵����ѡ 
                                       ("&Red", "", self.OnColor, wx.ITEM_RADIO), 
                                       ("&Green", "", self.OnColor, wx.ITEM_RADIO),  
                                       ("&Blue", "", self.OnColor, wx.ITEM_RADIO), 
                                       ("&Other", "", self.OnOtherColor, wx.ITEM_RADIO))), 
                           ("", "", ""), 
                           ("&Quit", "Quit", self.OnCloseWindow))) 
               ]   
    def CreateMenuBar(self): 
        '''''
        �����˵�
        ''' 
        menuBar = wx.MenuBar() 
        for eachMenuData in self.MenuData(): 
            menuLabel = eachMenuData[0] 
            menuItems = eachMenuData[1] 
            menuBar.Append(self.CreateMenu(menuItems), menuLabel)  
        self.SetMenuBar(menuBar) 
         
    def CreateMenu(self, menuData): 
        '''''
        ����һ���˵�
        ''' 
        menu = wx.Menu() 
        for eachItem in menuData: 
            if len(eachItem) == 2: 
                label = eachItem[0] 
                subMenu = self.CreateMenu(eachItem[1]) 
                menu.AppendMenu(wx.NewId(), label, subMenu) #�ݹ鴴���˵��� 
            else: 
                self.CreateMenuItem(menu, *eachItem) 
        return menu 
     
    def CreateMenuItem(self, menu, label, status, handler, kind = wx.ITEM_NORMAL): 
        '''''
        �����˵�������
        ''' 
        if not label: 
            menu.AppendSeparator() 
            return 
        menuItem = menu.Append(-1, label, status, kind) 
        self.Bind(wx.EVT_MENU, handler,menuItem) 
     
    def OnNew(self, event): 
        pass 
     
    def OnOpen(self, event): 
        '''''
        �򿪿��ļ��Ի���
        ''' 
        file_wildcard = "Paint files(*.paint)|*.paint|All files(*.*)|*.*"  
        dlg = wx.FileDialog(self, "Open paint file...", 
                            os.getcwd(),  
                            style = wx.OPEN, 
                            wildcard = file_wildcard) 
        if dlg.ShowModal() == wx.ID_OK: 
            self.filename = dlg.GetPath() 
            self.ReadFile() 
            self.SetTitle(self.title + '--' + self.filename) 
        dlg.Destroy() 
         
         
     
    def OnSave(self, event):  
        '''''
        �����ļ�
        ''' 
        if not self.filename: 
            self.OnSaveAs(event) 
        else: 
            self.SaveFile() 
             
    def OnSaveAs(self, event): 
        '''''
        �����ļ�����Ի���
        ''' 
        file_wildcard = "Paint files(*.paint)|*.paint|All files(*.*)|*.*"  
        dlg = wx.FileDialog(self,  
                            "Save paint as ...", 
                            os.getcwd(), 
                            style = wx.SAVE | wx.OVERWRITE_PROMPT, 
                            wildcard = file_wildcard) 
        if dlg.ShowModal() == wx.ID_OK: 
            filename = dlg.GetPath() 
            if not os.path.splitext(filename)[1]: #���û���ļ�����׺ 
                filename = filename + '.paint' 
            self.filename = filename 
            self.SaveFile() 
            self.SetTitle(self.title + '--' + self.filename) 
        dlg.Destroy()     
                    
     
    def OnColor(self, event): 
        '''''
        ���Ļ�������
        ''' 
        menubar = self.GetMenuBar() 
        itemid = event.GetId() 
        item = menubar.FindItemById(itemid) 
        color = item.GetLabel() #��ȡ�˵������� 
        self.paint.SetColor(color) 
         
    def OnOtherColor(self, event): 
        '''''
        ʹ����ɫ�Ի���
        ''' 
        dlg = wx.ColourDialog(self) 
        dlg.GetColourData().SetChooseFull(True)   #������ɫ�������� 
        if dlg.ShowModal() == wx.ID_OK: 
            self.paint.SetColor(dlg.GetColourData().GetColour()) #����ѡ�����û�����ɫ 
        dlg.Destroy() 
         
    def OnCloseWindow(self, event): 
        self.Destroy() 
         
    def SaveFile(self): 
        '''''
        �����ļ�
        ''' 
        if self.filename: 
            data = self.paint.GetLinesData() 
            f = open(self.filename, 'w') 
            cPickle.dump(data, f) 
            f.close() 
                      
    def ReadFile(self): 
        if self.filename: 
            try: 
                f = open(self.filename, 'r') 
                data = cPickle.load(f) 
                f.close() 
                self.paint.SetLinesData(data) 
            except cPickle.UnpicklingError: 
                wx.MessageBox("%s is not a paint file." 
                              % self.filename, "error tip", 
                              style = wx.OK | wx.ICON_EXCLAMATION) 
      

         
if __name__ == '__main__': 
    app = wx.PySimpleApp() 
    frame = PaintFrame(None) 
    frame.Show(True) 
    app.MainLoop()  