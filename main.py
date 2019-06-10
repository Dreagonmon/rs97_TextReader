# -*- coding: utf-8 -*-
import pygame, os, sys, codecs, traceback
from pygame.locals import *
import ui, configloader
if os.path.exists("debug.lock"):
    import devicewin as device
else :
    import device
MAX_FPS = 15
# init
device.init()
clock = pygame.time.Clock()
# pygame.key.set_repeat(50, 50)
screen = device.getScreen()

#test start
menu = u"Press SELECT to select file"
# menu = [u"1",u"2",u"3",u"4",u"5",u"6",u"7",u"8",u"9",u"10",u"11",u"12",u"13",u"14",u"15",u"16",u"17",u"18"]
def callb(key):
    global menu
    if key == device.K_B:
        print("kb")
    elif key == device.K_SELECT:
        wframe = screenframes.FileManagerFrame(screen,open_file_callback=ofb)
        ui.push_frame(wframe)
    pass
def ofb(fp):
    print(codecs.encode(fp,configloader.config.get("GLOBAL","syspath.coding","UTF-8")))
    wframe = screenframes.ReaderFrame(screen,fp)
    ui.push_frame(wframe)
try:
    screen.fill((0, 0, 0))
    pygame.display.flip()
    # init config file
    config_file = configloader.global_conf.get("GLOBAL","config","config/config.cfg")
    local_file = configloader.global_conf.get("GLOBAL","local","local/zh-cn.cfg")
    configloader.init_config(config_file)
    configloader.init_string(local_file)
    # path
    import codecs
    import screenframes, widgets
    # base frame
    if len(sys.argv) > 1:
        coding = configloader.config.get("GLOBAL","syspath.coding","UTF-8")
        path = codecs.decode(sys.argv[1],coding)
        path = os.path.abspath(codecs.encode(path,coding))
        path = codecs.decode(path,coding)
        wframe = screenframes.ReaderFrame(screen,path)
        ui.push_frame(wframe)
    else:
        wframe = screenframes.WidgetFrame(screen)
        widg = widgets.TextWidget(menu,callback=callb)
        wframe.push_widget(widg,(8,8,screen.get_width()-16,screen.get_height()-16))
        ui.push_frame(wframe)
    while True:
        events = pygame.event.get()
        # get top frame
        frame = ui.get_frame()
        if frame == None:
            clock.tick(MAX_FPS)
            continue
        # send event
        if len(events) > 0:
            frame.event(events)
        # update UI
        frame.update()
        # exit function
        for event in events:
            if event.type is KEYDOWN:
                k = event.key
                if k == device.K_END:
                    device.deinit()
                    sys.exit()
        #limit frame rate
        clock.tick(MAX_FPS)
        pass
    pass
except Exception as ex:
    errstr = str(ex)
    lasttext = traceback.format_exc()
    print(lasttext)
    pass


# Error collection
while True:
    background = pygame.Surface((320,240))
    background = background.convert()
    background.fill((0, 127, 255))
    # Display some text
    font = pygame.font.Font(None, 16)
    text = font.render(errstr, 1, (10, 10, 10))
    textpos = text.get_rect()
    textpos.centerx = background.get_rect().centerx
    background.blit(text, textpos)
    
    screen.blit(background, (0, 0))
    pygame.display.flip()
    for event in pygame.event.get():
        if event.type is KEYDOWN:
            sys.exit()
