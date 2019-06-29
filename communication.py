
'''
This is for test minepyclient, minepyturtle
'''
'''
from minepyclient import *
init("192.168.1.101", 10000)
print(getpos("cit3"))
print(getblockid(100, 100, 100))
setblocks(168, 91, 367, 168, 80, 350, 41)
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
