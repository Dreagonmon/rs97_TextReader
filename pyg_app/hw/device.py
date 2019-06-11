import os
__lockpath = os.path.dirname(__file__)
__lockpath = os.path.join(__lockpath,"debug.lock")
# print(__lockpath)
if os.path.exists(__lockpath):
    from .devicewin import *
else :
    from .devicers97 import *