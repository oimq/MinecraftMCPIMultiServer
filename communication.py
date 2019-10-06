
'''
This is for test minepyclient, minepyturtle
'''


import time
from minepyclient import *
init("1.168.0.53", 10000)

# lawn block
x1 = 339
y1 = 75
z1 = -55
block1 = getblock(x1, y1, z1)

# specify block
x2 = 344
y2 = 76
z2 = -63
block2 = getblock(x2, y2, z2)

while block1 == 2 :
    if block2 == 57 :
        count = 5
        while count > 0 :
            chat("countdown : " + str(count))
            time.sleep(1)
            count = count - 1
        setblocks(x1-1, y1, z1-1, x1+1, 		y1, z1+1, 51)
    elif block2 == 41 :
        chat("correct block is more 		expensive.")
    else :
        chat("that is wrong block.")
    time.sleep(0.1)
    block1 = getblock(x1, y1, z1)
    block2 = getblock(x2, y2, z2)
chat("explosion!!!!!")







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