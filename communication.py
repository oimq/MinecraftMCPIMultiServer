
'''
This is for test minepyclient, minepyturtle
'''

from minepyclient import *
init("1.168.0.53", 10000)
import time

x = 1
y = 80
z = 107
while True :
    setblocks(x-1, y, z-1, x+1, y, z+1, 169)
    time.sleep(0.3)
    setblocks(x-1, y, z-1, x+1, y, z+1, 57)
    time.sleep(0.3)


'''
from minepyturtle import *
init("192.168.1.101", 10000)
turtle.setname("cit3")
turtle.penup()
turtle.forward(10)
turtle.pendown()
turtle.penblock(46)
turtle.circle(10)
turtle.show()
'''