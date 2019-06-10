import pygame,pygame.locals
# key define
K_UP     =       pygame.K_w
K_DOWN   =       pygame.K_s
K_LEFT   =       pygame.K_a
K_RIGHT  =       pygame.K_d
K_L      =       pygame.K_q
K_R      =       pygame.K_e
K_A      =       pygame.K_l
K_B      =       pygame.K_k
K_X      =       pygame.K_i
K_Y      =       pygame.K_j
K_SELECT =       pygame.K_v
K_START  =       pygame.K_b
K_END    =       pygame.K_ESCAPE
K_VOL_UP =       pygame.K_2
K_VOL_DOWN =     pygame.K_1
K_BRIGHTNESS  =  pygame.K_TAB

screen = None
def init():
    global screen
    pygame.init()
    screen = pygame.display.set_mode((320,240), pygame.locals.HWACCEL, 16)
    pass
def deinit():
    pass

def getScreen():
    global screen
    return screen

def setBrightness(level):
    print("Brightness:",level)
    pass

def getBrightness():
    return 30
