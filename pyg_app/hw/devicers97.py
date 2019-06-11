# -*- coding: utf-8 -*-
import os, pygame,pygame.locals
# key define
K_UP     =       pygame.K_UP
K_DOWN   =       pygame.K_DOWN
K_RIGHT  =       pygame.K_RIGHT
K_LEFT   =       pygame.K_LEFT
K_L      =       pygame.K_TAB
K_R      =       pygame.K_BACKSPACE
K_A      =       pygame.K_LCTRL
K_B      =       pygame.K_LALT
K_X      =       pygame.K_SPACE
K_Y      =       pygame.K_LSHIFT
K_SELECT =       pygame.K_ESCAPE
K_START  =       pygame.K_RETURN
K_END    =       pygame.K_END
K_VOL_UP =       pygame.K_2
K_VOL_DOWN =     pygame.K_1
K_BRIGHTNESS  =  pygame.K_3

screen = None
# init screen
def init():
    global screen
    pygame.init()
    pygame.mouse.set_visible(False)
    screen = pygame.display.set_mode((320,240), pygame.locals.HWSURFACE, 16)
    try:
        os.system('echo 2 > /proc/jz/lcd_a320')
    except Exception as ex:
        pass
def deinit():
    try:
        os.system('echo 0 > /proc/jz/lcd_a320')
    except Exception as ex:
        pass

# get device`s pygame screen
def getScreen():
    global screen
    return screen

# set brightness from 0 to 100
def setBrightness(level):
    try:
        os.system('echo ' + str(level)  +  ' > /proc/jz/lcd_backlight')
    except Exception as ex:
        pass

# get brightness
def getBrightness():
    bri = 30
    with open("/proc/jz/lcd_backlight","r") as bf:
        bri = int(bf.readline())
    return bri
