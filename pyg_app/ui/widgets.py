# -*- coding: utf-8 -*-
# --Widget subclass--
import os, pygame
from ..hw import device
from ..data.configloader import config
from .ui import Widget
class ListWidget(Widget):
    # A widget that display list and manager select curser
    def __init__(self,strlist,callback=None,show_curser=True,config_section="GLOBAL"):
        # strlist: a list, each element must be str
        # callback: callback(int: select_pos,pygame_event_key: key)
        # show_curser: show current selection
        self.strlist = strlist
        self.callback = callback
        self.show_curser = show_curser
        self.__sec = config_section
        # curser and current list position
        self.__first_line = 0
        self.__curser = 0
        self.__maxline = 0 # cache last render lines number
        self.loadconf()
    def loadconf(self):
        # font and color
        fontpath = config.get(self.__sec,"font.file",None)
        fontsize = config.getint(self.__sec,"font.size",16)
        self.__font = pygame.font.Font(fontpath, fontsize)
        self.__linehight = config.getint(self.__sec,"line.height",30)
        bgcs = config.get(self.__sec,"color.bg","0,0,0")
        bgcs = bgcs.split(",")
        fgcs = config.get(self.__sec,"color.fg","255,255,255")
        fgcs = fgcs.split(",")
        self.__bgc = (int(bgcs[0]),int(bgcs[1]),int(bgcs[2])) # background color
        self.__fgc = (int(fgcs[0]),int(fgcs[1]),int(fgcs[2])) # froeground color
        self.__needupdate = True
    def force_update(self,frame):
        self.__needupdate = True
    def update(self,frame):
        if not self.__needupdate:
            return False
        self.__needupdate = False # only refresh when needed
        frame.fill(self.__bgc)
        fw, fh = frame.get_size() # frame size
        self.__maxline = fh // self.__linehight # max line number
        # draw text line by line
        typestr = type("")
        for l in range(self.__maxline):
            ipos = self.__first_line + l
            if ipos >= len(self.strlist):
                break
            text = self.strlist[ipos]
            timg = None
            if self.show_curser and self.__curser == ipos:
                self.__font.set_underline(True)
                timg = self.__font.render(text,1,self.__fgc)
                self.__font.set_underline(False)
                pass
            else:
                timg = self.__font.render(text,1,self.__fgc)
            top = l*self.__linehight
            tpos = timg.get_rect()
            tpos.centery = top + (self.__linehight // 2)
            tpos.centerx = fw // 2
            frame.blit(timg,tpos)
        return True
    def event(self,events):
        flag = False
        for event in events:
            if event.type != pygame.KEYDOWN:
                continue
            if event.key == device.K_UP:
                self.move_up_line()
                flag = True
            elif event.key == device.K_DOWN:
                self.move_down_line()
                flag = True
            elif event.key == device.K_LEFT:
                self.move_up_page()
                flag = True
            elif event.key == device.K_RIGHT:
                self.move_down_page()
                flag = True
            elif self.callback != None:
                self.callback(self.__curser,event.key)
                flag = True
        # if do nothing, return False
        return flag
    # operate
    def reset(self):
        self.__first_line = 0
        self.__curser = 0
        self.__needupdate = True
    def catch_curser(self):
        # adjust display position
        if self.__first_line >= len(self.strlist):
            self.__curser = self.__first_line = len(self.strlist) - 1
        
        if self.__first_line > self.__curser:
            self.__first_line = self.__curser
        if self.__first_line < self.__curser - self.__maxline + 1:
            self.__first_line = self.__curser - self.__maxline + 1
        if self.__first_line < 0:
            self.__first_line = 0
    def move_up_line(self):
        if self.__curser == 0:
            self.__curser = len(self.strlist)-1
        else:
            self.__curser = self.__curser-1
        self.catch_curser()
        self.__needupdate = True
    def move_up_page(self):
        for l in range(self.__maxline):
            if self.__curser == 0:
                break
            self.__curser = self.__curser - 1
        self.catch_curser()
        self.__needupdate = True
    def move_down_line(self):
        if self.__curser == len(self.strlist)-1:
            self.__curser = 0
        else:
            self.__curser = self.__curser+1
        self.catch_curser()
        self.__needupdate = True
    def move_down_page(self):
        for l in range(self.__maxline):
            if self.__curser == len(self.strlist)-1:
                break
            self.__curser = self.__curser + 1
        self.catch_curser()
        self.__needupdate = True
    def get_curser(self):
        return self.__curser

class TextWidget(Widget):
    # A widget display some text
    def __init__(self,strtext,callback=None,config_section="GLOBAL"):
        # strlist: a str text
        # callback: callback(pygame_event_key: key)
        self.callback = callback
        self.__strtext = strtext
        self.__sec = config_section
        # control display postion
        # self.__first_line = 0 # current line
        self.__first_char = 0 # current char
        self.__frame_width = 0 # cache frame width
        self.__frame_line = 0 # cache frame line
        self.loadconf()
        self.__metrics = self.__font.metrics(self.__strtext)
    def loadconf(self):
        # font and color
        fontpath = config.get(self.__sec,"font.file",None)
        fontsize = config.getint(self.__sec,"font.size",16)
        self.__font = pygame.font.Font(fontpath, fontsize)
        self.__linehight = config.getint(self.__sec,"line.height",24)
        bgcs = config.get(self.__sec,"color.bg","0,0,0")
        bgcs = bgcs.split(",")
        fgcs = config.get(self.__sec,"color.fg","255,255,255")
        fgcs = fgcs.split(",")
        self.__bgc = (int(bgcs[0]),int(bgcs[1]),int(bgcs[2])) # background color
        self.__fgc = (int(fgcs[0]),int(fgcs[1]),int(fgcs[2])) # froeground color
        self.__needupdate = True
    def __line_width(self,cpos,fw,text,metrics=None,forward=True):
        # Test how many chars can be render in a line
        # cpos: char start pos in text
        # fw: frame width
        # text: text to be test
        # metrics: Font.metrice() result, when measure multline, pass to avoid useless call
        # forward: if we should measure forward, or backward
        # Return char number that can render
        # Keep in mind that newline can`t be processed.
        # \r\n may not be count...
        if metrics == None:
            metrics = self.__font.metrics(text)
        cnum = 0
        lwidth = 0
        while lwidth < fw:
            # cpos in text
            if forward and (cpos>=len(metrics) or cpos<0):
                break
            if (not forward) and (cpos<1 or cpos>len(metrics)):
                break
            # deal with newline...
            if forward:
                ch = text[cpos]
            else:
                ch = text[cpos-1]
            if ch=='\r' or ch=='\n':
                # if start with \r\n, ignore
                # else return 
                if lwidth > 0:
                    return cnum
                else:
                    cnum = cnum + 1
                    if forward:
                        cpos = cpos + 1
                    else:
                        cpos = cpos - 1
                    continue
            # get current char width
            if forward:
                cw = metrics[cpos][4]
            else:
                cw = metrics[cpos-1][4]
            # current line width
            lwidth = lwidth + cw
            if lwidth <= fw:
                cnum = cnum + 1
            # next loop
            if forward:
                cpos = cpos + 1
            else:
                cpos = cpos - 1
        return cnum
    def force_update(self,frame):
        self.__needupdate = True
        pass
    def update(self,frame):
        if not self.__needupdate:
            return False
        self.__needupdate = False # only refresh when needed
        self.__frame_width = frame.get_width()
        self.__frame_line = frame.get_height() // self.__linehight
        frame.fill(self.__bgc)
        # DEAL WITH MUTILINE TEXT
        pos = self.__first_char
        metrics = self.__metrics
        for l in range(self.__frame_line):
            if self.__first_char >= len(self.__strtext):
                break
            tc = self.__line_width(pos,frame.get_width(),self.__strtext,metrics=metrics,forward=True)
            linetext = self.__strtext[pos:pos+tc].replace('\r','').replace('\n','')
            pos = pos + tc
            timg = self.__font.render(linetext,1,self.__fgc)
            top = l*self.__linehight
            tpos = timg.get_rect()
            tpos.centery = top + (self.__linehight // 2)
            tpos.left = 0
            frame.blit(timg,tpos)
        #
        return True
    def move_up_line(self):
        tc = self.__line_width(self.__first_char,self.__frame_width,self.__strtext,metrics=self.__metrics,forward=False)
        self.__first_char = self.__first_char - tc
        self.__needupdate = True
        return tc
    def move_up_page(self):
        cnum = 0
        metrics = self.__metrics
        for l in range(self.__frame_line):
            tc = self.__line_width(self.__first_char,self.__frame_width,self.__strtext,metrics=metrics,forward=False)
            self.__first_char = self.__first_char - tc
            cnum = cnum + tc
        self.__needupdate = True
        return cnum
    def move_down_line(self):
        tc = self.__line_width(self.__first_char,self.__frame_width,self.__strtext,metrics=self.__metrics,forward=True)
        self.__first_char = self.__first_char + tc
        self.__needupdate = True
        return tc
    def move_down_page(self):
        cnum = 0
        metrics = self.__metrics
        for l in range(self.__frame_line):
            tc = self.__line_width(self.__first_char,self.__frame_width,self.__strtext,metrics=metrics,forward=True)
            self.__first_char = self.__first_char + tc
            cnum = cnum + tc
        self.__needupdate = True
        return cnum
    def set_pos(self,pos):
        if pos < 0:
            self.__first_char = 0
        elif pos >= len(self.__strtext):
            self.__first_char = len(self.__strtext)
        else:
            self.__first_char = pos
        self.__needupdate = True
    def get_pos(self):
        return self.__first_char
    def attach_start(self,stri,auto_reload=True):
        self.__strtext = stri + self.__strtext
        self.__first_char = self.__first_char + len(stri)
        if auto_reload:
            self.__metrics = self.__font.metrics(stri) + self.__metrics
        self.__needupdate = True
    def cut_start(self,length,auto_reload=True):
        if length > len(self.__strtext):
            length = len(self.__strtext)
        cut = self.__strtext[:length]
        self.__strtext = self.__strtext[length:]
        self.__first_char = self.__first_char - length
        if self.__first_char < 0:
            self.__first_char = 0
        if auto_reload:
            self.__metrics = self.__metrics[length:]
        self.__needupdate = True
        return cut
    def attach_end(self,stri,auto_reload=True):
        self.__strtext = self.__strtext + stri
        if auto_reload:
            self.__metrics = self.__metrics + self.__font.metrics(stri)
        self.__needupdate = True
    def cut_end(self,length,auto_reload=True):
        if length > len(self.__strtext):
            length = len(self.__strtext)
        length = len(self.__strtext) - length
        cut = self.__strtext[length:]
        self.__strtext = self.__strtext[:length]
        if self.__first_char >= len(self.__strtext):
            self.__first_char = len(self.__strtext)
        if auto_reload:
            self.__metrics = self.__metrics[:length]
        self.__needupdate = True
        return cut
    def event(self,events):
        flag = False
        for event in events:
            if event.type != pygame.KEYDOWN:
                continue
            if event.key == device.K_UP:
                self.move_up_line()
                flag = True
            elif event.key == device.K_DOWN:
                self.move_down_line()
                flag = True
            elif event.key == device.K_LEFT:
                self.move_up_page()
                flag = True
            elif event.key == device.K_RIGHT:
                self.move_down_page()
                flag = True
            elif self.callback != None:
                self.callback(event.key)
                flag = True
        # if do nothing, return False
        return flag
