# -*- coding: utf-8 -*-
import pygame

# --UI super class--
class ScreenFrame(object):
    # Frame is a fullscreen UI that handle
    # updating dispaly and enevts at the sametime
    # top level user interface
    # > update()
    # > event(events)
    # should be override by subclass
    # super(CLASS,self).__init__(screen) must be called
    def __init__(self,screen):
        # init
        self.frame = pygame.Surface(screen.get_size())
        self.frame.convert()
        self.screen = screen
        pass
    def flip(self):
        # Called to refresh total display,
        # Shoule not be override!
        # Try to call this at the end of update()
        self.screen.blit(self.frame,(0,0))
        pygame.display.flip()
    def force_update(self):
        # redraw on screen
        pass
    def update(self):
        # Try to update display on every frame
        pass
    def event(self,events):
        # Handle events
        pass
class Widget(object):
    # Widget can be draw within a frame
    def force_update(self,frame):
        # Refresh on the frame ignore any case.
        pass
    def update(self,frame):
        # Called by ScreenFrame object when update.
        # The frame is an pygame.Surface object
        # that may be a part of the ScreenFrame.
        # Widget should not care about position,
        # just try to draw within the frame.
        # Return True if refresh is needed,
        # else return False(most because of nothing changed)
        return False
    def event(self,events):
        # Called by ScreenFrame when events arrived.
        # Return True if this event is done,
        # and do not want to pass to another widget.
        return False

# --windows manager--
_frames = []
# get top frame -- current frame
def get_frame():
    global _frames
    if len(_frames) > 0:
        return _frames[-1]
    else:
        return None
# remove top frame -- destory frame
def remove_frame():
    global _frames
    if len(_frames) > 0:
        _frames.pop()
        return True
    else:
        return False
# push top frame -- new frame
def push_frame(scrframe):
    global _frames
    _frames.append(scrframe)
