from minecraft import *
import socket
import threading

def convdatatofunc(data) :
        fname = data[0:data.index('(')]
        arglist = data[data.index('(')+1:data.index(')')].replace(" ", "").split(',')
        arglist = list(map(lambda x : float(x) if  (x.replace('-', '')).replace('.', '').isdigit() else x, filter(lambda v : v != '', arglist)))
        print('function :',fname, ', arguments :', arglist)
        print('------------------------------------------')
        return fname, arglist
funclist = [setblock, getpos, getblock, setblocks, chat, setpos]
'''
funclist = [setpos, getpos, setblock, setblocks, getblock,
                    getblockwithdata, chat, setting, hit, hitlastest,
                    hitfirst, stop, getseconds, setx, sety, setz,
                    getx, gety, getz]
'''
strlist = list(map(lambda x : str(x)[10:str(x).index(' at ')], funclist))
datalist = {1:"stone", 41:"gold", 42:"iron", 57:"diamond", 8:"water",
            9:"water", 27:"rail", 152:"redstone-block", 169:"sea_lantern",
            79:"ice", 46:"tnt", 10:"lava", 51:"fire", 17:"tree1", 18:"tree2", 103:"melon"
            ,175:'flower'}
playerlist = {}

def communicate(sock, address, setblocksflag) :
    while True :
        try :
            data = sock.recv(1024).decode()
            if not data : continue
            if data == "exit" :
                break
            print('origin :', address, ', data :', data)
            fname, fargs = convdatatofunc(str(data))
            try :
                if (fname == 'setblock') :
                    data = "anonymous"
                    for key in datalist :
                        if fargs[-1] == key :
                            results = funclist[strlist.index(fname)](*fargs)
                            data = "block " + datalist[key] + " is set, position : [ x("\
                                   + str(fargs[0]) + "), y(" + str(fargs[1]) + "), z(" + str(fargs[2]) + ") ]"
                    if data == "anonymous" :
                        data = "Run failed... These blocks are only permitted : stone, gold, iron, diamond"
                        if 0 in datalist :
                            data += ", air"

                elif (fname == 'getblock') :
                    results = funclist[strlist.index(fname)](*fargs)
                    if results == None :
                        data = "Run failed... Check the function name."
                    else :
                        # data = "Identified block ID : " + str(results) + ", position : [ x(" \
                        #        + str(fargs[0]) + "), y(" + str(fargs[1]) + "), z(" + str(fargs[2]) + ") ]"
                        data = str(results)

                elif (fname == 'getpos') :
                    results = funclist[strlist.index(fname)](*fargs)
                    print("Right name : "+str(results.x)+", "+str(results.y)+", "+str(results.z))
                    data = str(results.x)+", "+str(results.y)+", "+str(results.z)

                elif (fname == 'setpos') :
                    if getpos(fargs[0]) == getpos() :
                        print("Wrong name : "+fargs[0])
                        data = "Run failed... Wrong username are received : "+fargs[0]
                    else :
                        funclist[strlist.index(fname)](*fargs)
                        data = "We set "+fargs[0]+" positiion to "+str(fargs[1])+', '+str(fargs[2])+', '+str(fargs[3])

                elif (fname == 'setblocks') :
                    if setblocksflag :
                        data = "anonymous"
                        for key in datalist :
                            if fargs[-1] == key :
                                results = funclist[strlist.index(fname)](*fargs)
                                data = "block " + datalist[key] + " is set, position : [ x1(" \
                                       + str(fargs[0]) + "), y1(" + str(fargs[1]) + "), z1(" + str(fargs[2]) + "), x2(" \
                                       + str(fargs[3]) + "), y2(" + str(fargs[4]) + "), z2(" + str(fargs[5]) + ") ]"
                        if data == "anonymous" :
                            data = "Run failed... These blocks are only permitted : stone, gold, iron, diamond"
                            if 0 in datalist :
                                data += ", air"
                    else :
                        data = "Sorry, the setblocks function are blocked now."

                elif (fname == 'chat') :
                    funclist[strlist.index(fname)](data[5:-1])
                    #data = fargs[0]

                else :
                    data = "Run failed... Check the function name."
            except Exception as e:
                print("Wrong code execution :", e)
                data = "Run failed... Check the code."

            sock.send(data.encode())
        except KeyboardInterrupt :
            print("KeyboardInterrupt occur, server is down")
            break
        except Exception :
            print("error occur :", Exception)
            break
    sock.send("The connection is over.".encode())
    print("%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")
    print("Close the connection : " + str(address))
    print("%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")
    sock.close()

def communicate_with_client(sock, address, setblocksflag) :
    global strlist, datalist, playerlist
    print("%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")
    print("Connection from : " + str(address))
    print("%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")
    communicate(sock, address, setblocksflag)

def run_server(server_socket) :
    setblocksflag = (input("Do you want to block the setblocks mode? (y or n) : ") == 'n')
    if (input("Do you want to forbid the air block? (y or n) : ") == 'n') :
        datalist[0] = "air"
    print("-------------- start server --------------")
    server_socket.listen(5)
    while True :
            conn, address = server_socket.accept()
            t = threading.Thread(target=communicate_with_client, args=(conn, address, setblocksflag))
            t.daemon = True
            t.start()

def start_server(port) :
    host = socket.gethostbyname(socket.gethostname())
    e = 0
    server_socket = socket.socket()
    #for ip in range(1, 256, 1) :
    try :
        server_socket.bind((host, port))
        print('bind success :', host)
        run_server(server_socket)
        exit()
    except :
        print('bind failed.')
        e = 1
                        
if __name__ == "__main__" :
    print("Welcome to access the Minecraft Server")
    start_server(int(input("Please enter the PORT number : ")))
    print("Server would be terminated. Bye.")