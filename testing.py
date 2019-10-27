
from minecraft import *
import time

def writetrace() :
    trace = list()
    for count in range(100) :
        trace.insert(0, getpos())
        chat("write oimqA")
        time.sleep(0.1)
    return trace

def timemachine(tracelist) :
    chat("now_turn_back_the_clock!")
    time.sleep(0.1)
    for pos in tracelist :
        setpos(pos.x, pos.y, pos.z)
        print(pos.x, pos.y, pos.z)
        time.sleep(0.1)

tracelist = writetrace()
print(tracelist)
timemachine(tracelist)
