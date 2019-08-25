
'''
This is for test minepyclient, minepyturtle
'''
from minepyclient import *
init("1.168.0.53", 10000)
print(getpos("cit4"))
setpos(100, 100, 100, "cit4")
# print(getblockid(100, 100, 100))
chat("hello!")
#setblocks(168, 91, 367, 168, 80, 350, 41)
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