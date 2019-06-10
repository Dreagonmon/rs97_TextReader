# -*- coding: utf-8 -*-
# --ScreenFrame subclass--
import pygame, os, codecs, ui
if os.path.exists("debug.lock"):
    import devicewin as device
else :
    import device
from ui import ScreenFrame
from configloader import config, string, Config
from widgets import ListWidget, TextWidget
class WidgetFrame(ScreenFrame):
    # A ScreenFrame with simple widget manager
    def __init__(self,screen):
        super(WidgetFrame,self).__init__(screen)
        self.widgets = [] #(widget,(left,top,right,bottom))
    def force_update(self):
        for wid,rect in self.widgets:
            frame = self.frame.subsurface(rect)
            wid.force_update(frame)
    def update(self):
        # update from bottom to top
        for i in range(len(self.widgets)):
            widget_info = self.widgets[i]
            rect = widget_info[1]
            frame = self.frame.subsurface(rect)
            flag = widget_info[0].update(frame)
            if flag:
                self.flip()
    def event(self,events):
        # travel from top to bottom
        for i in range(len(self.widgets)-1,-1,-1):
            widget_info = self.widgets[i]
            flag = widget_info[0].event(events)
            if flag:
                break
    def push_widget(self,widget,rect):
        self.widgets.append((widget,rect))
    def remove_widget(self):
        if len(self.widgets) > 0:
            self.widgets.pop()
    def get_widgets(self):
        return self.widgets

class FileManagerFrame(WidgetFrame):
    def __init__(self,screen,path='.',open_file_callback=None):
        super(FileManagerFrame,self).__init__(screen)
        self.__path = os.path.abspath(path)
        self.__ofc = open_file_callback # __ofc(filepath)
        self.__file_list = []
        self.loadconf()
        self.init()
    def init(self):
        self.refresh()
        self.__file_list_widget = ListWidget(self.__file_list,callback=self.__file_list_callback)
        self.push_widget(self.__file_list_widget,self.frame.get_rect())
    def loadconf(self):
        self.__coding = config.get("GLOBAL","syspath.coding","UTF-8")
    def refresh(self):
        # clear file list
        while len(self.__file_list) > 0:
            del self.__file_list[0]
        # applist
        file_list = os.listdir(codecs.encode(self.__path,self.__coding))
        if self.__path != os.path.abspath("/"):
            self.__file_list.append(u"..")
        for fname in file_list:
            ext = os.path.splitext(fname)[1]
            ext = codecs.decode(ext,self.__coding)
            fname = codecs.decode(fname,self.__coding)
            filepath = os.path.join(self.__path,fname)
            if os.path.isdir(codecs.encode(filepath,self.__coding)):
                self.__file_list.append(fname)
            elif ext.lower() == u".txt":
                self.__file_list.append(fname)
        self.__file_list.sort()
    def __file_list_callback(self,index,key):
        filepath = os.path.join(self.__path,self.__file_list[index])
        if key == device.K_B:
            self.__path = os.path.join(self.__path,u"..")
            self.__path = os.path.abspath(self.__path)
            self.refresh()
            self.__file_list_widget.reset()
        elif key == device.K_A:
            if os.path.isdir(codecs.encode(filepath,self.__coding)):
                self.__path = filepath
                self.__path = os.path.abspath(self.__path)
                self.refresh()
                self.__file_list_widget.reset()
            else:
                if self.__ofc != None:
                    ui.remove_frame()
                    self.__ofc(filepath)
                    wframe = ui.get_frame()
                    wframe.force_update()
                else :
                    # None will result in unknown action
                    ui.remove_frame()
                    wframe = ui.get_frame()
                    wframe.force_update()

class ReaderFrame(WidgetFrame):
    def __init__(self,screen,filepath):
        super(ReaderFrame,self).__init__(screen)
        # don`t read bookmark
        self.__fp = filepath
        # only support 
        if os.path.splitext(filepath)[1].lower() != u".txt":
            import sys
            sys.exit()
        self.loadconf()
        self.init()
    def loadconf(self):
        self.__coding = config.get("GLOBAL","syspath.coding","UTF-8") # sys path coding
        self.__fcoding = config.get("READER","file.coding","UTF-8") # text coding
        self.__bar_height = int(config.get("READER","statusbar.height","30")) # future statusbar
        self.__buffer_size = int(config.get("READER","buffer.size","1536"))
        self.__pd_left = int(config.get("READER","padding.left","8"))
        self.__pd_top = int(config.get("READER","padding.top","8"))
        self.__pd_right = int(config.get("READER","padding.right","8"))
        self.__pd_bottom = int(config.get("READER","padding.bottom","8"))
        bgcs = config.get("READER","color.bg","0,0,0")
        bgcs = bgcs.split(",")
        self.__bgc = (int(bgcs[0]),int(bgcs[1]),int(bgcs[2]))
        # bookmark
        book_dir,book_name = os.path.split(self.__fp)
        bookmark = os.path.join(book_dir,u"."+book_name+u".bookmark")
        self.__bookmark = bookmark
        self.__bookinfo = Config(codecs.encode(self.__bookmark,self.__coding))
        self.__text_start = self.__bookinfo.getint("BOOK","text.pos",0) # str start pos
        self.__text_pos = self.__bookinfo.getint("BOOK","display.pos",0) # display pos
    def init(self):
        #print(txtf_pos)
        self.__locked_bri = 50 # remember brightness
        self.__lock = False
        self.__is_loading = True
        self.__text = ""
        self.__file = None
        self.load_text()
        self.push_widget(self.__loading_widget,self.frame.get_rect())
    def load_text(self):
        if self.__file == None:
            self.__loading_widget = TextWidget("")
            self.__file = codecs.open(codecs.encode(self.__fp,self.__coding),"r",self.__fcoding,errors="replace")
        try:
            stri = self.__file.read(102400)
            self.__text = self.__text + stri
            ended = False
            if len(stri) == 0:
                ended = True
        except:
            ended = True
        if ended:
            # load end
            self.__file.close()
            self.__is_loading = False
            self.remove_widget()
            self.__text_widget = TextWidget("",config_section="READER")
            self.__text_widget.attach_start(self.__text[self.__text_start:self.__text_start+self.__buffer_size*3])
            self.__text_widget.set_pos(self.__text_pos)
            txtf_pos = self.frame.get_rect()
            txtf_pos.left = txtf_pos.left + self.__pd_left
            txtf_pos.top = txtf_pos.top + self.__pd_top
            txtf_pos.width = txtf_pos.width - (self.__pd_left+self.__pd_right)
            txtf_pos.height = txtf_pos.height - (self.__pd_top+self.__pd_bottom)
            self.push_widget(self.__text_widget,txtf_pos)
            self.update()
        else:
            self.__loading_widget.cut_start(99999) # clear text
            self.__loading_widget.attach_start("Loading..."+str(self.__file.tell()))
            self.__loading_widget.set_pos(0)
        pass
    # buffer size is 3 times than setting!
    def buffer_text_backword(self):
        pos = self.__text_widget.get_pos()
        if (pos < self.__buffer_size) and (self.__text_start > 0):
            npos = self.__text_start - self.__buffer_size
            if npos < 0:
                npos = 0
            if npos == self.__text_start:
                return # don`t need update
            count = self.__text_start - npos
            self.__text_widget.cut_end(count)
            self.__text_widget.attach_start(self.__text[npos:npos+count])
            self.__text_start = npos
        pass
    def buffer_text_forword(self):
        pos = self.__text_widget.get_pos()
        if (pos >= self.__buffer_size*2) and (self.__text_start < len(self.__text)-self.__buffer_size*3):
            npos = self.__text_start + self.__buffer_size
            if npos > len(self.__text)-self.__buffer_size*3:
                npos = len(self.__text)-self.__buffer_size*3
            if npos <= self.__text_start:
                return # don`t need update
            count = npos - self.__text_start
            start = self.__text_start + self.__buffer_size*3
            self.__text_widget.cut_start(count)
            self.__text_widget.attach_end(self.__text[start:start+count])
            self.__text_start = npos
        pass
    def event(self,events):
        # when loading, ignore any operation
        if self.__is_loading:
            return
        for event in events:
            if event.type != pygame.KEYDOWN:
                continue
            if event.key == device.K_START:
                if self.__lock:
                    device.setBrightness(self.__locked_bri)
                    self.__lock = False
                else:
                    self.__locked_bri = device.getBrightness()
                    device.setBrightness(0)
                    self.__lock = True
            if self.__lock:
                # when locked, do nothing
                return
            if event.key == device.K_UP:
                self.__text_widget.move_up_line()
                self.buffer_text_backword()
            elif event.key == device.K_DOWN:
                self.__text_widget.move_down_line()
                self.buffer_text_forword()
            elif (event.key == device.K_LEFT) or (event.key == device.K_L):
                self.__text_widget.move_up_page()
                self.buffer_text_backword()
            elif (event.key == device.K_RIGHT) or (event.key == device.K_R):
                self.__text_widget.move_down_page()
                self.buffer_text_forword()
            elif event.key == device.K_Y or event.key == device.K_END:
                self.__bookinfo.put("BOOK","text.pos",self.__text_start)
                self.__bookinfo.put("BOOK","display.pos",self.__text_widget.get_pos())
                self.__bookinfo.save()
        pass

    def update(self):
        # when loading, show loading progress
        if self.__lock:
            # when locked, do not update
            return
        if self.__is_loading:
            self.load_text()
        else:
            fw = self.frame.get_width()
            fh = self.frame.get_height()
            # left padding
            self.frame.subsurface((0,0,self.__pd_left,fh)).fill(self.__bgc)
            # top padding
            self.frame.subsurface((0,0,fw,self.__pd_top)).fill(self.__bgc)
            # right padding
            self.frame.subsurface((fw-self.__pd_right,0,self.__pd_right,fh)).fill(self.__bgc)
            # top padding
            self.frame.subsurface((0,fh-self.__pd_bottom,fw,self.__pd_bottom)).fill(self.__bgc)
        super(ReaderFrame,self).update()