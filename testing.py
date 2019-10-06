from minepyclient import *
init('1.168.0.53', 10000)

import random
def makeDiaRandom(x1, y1, z1, x2, y2, z2) :
    x = random.randint(x1, x2)
    y = random.randint(y1, y2)
    z = random.randint(z1, z2)

    setblock(x, y, z, 42)
    return x, y, z

pos = getpos('oimqA')
pos[0] = int(pos[0])
pos[1] = int(pos[1])
pos[2] = int(pos[2])

import time
while True :
    x, y, z = makeDiaRandom(pos[0]-50, pos[1]-10, pos[2]-50,
                            pos[0]+50, pos[1]+20, pos[2]+50)
    say = "i_make_dia_x_"+str(x)+"_y_"+str(y)+"_z_"+str(z)
    chat(say)
    time.sleep(0.2)
