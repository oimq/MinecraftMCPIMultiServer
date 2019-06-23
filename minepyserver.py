from minecraft import *
import socket
import threading

def convdatatofunc(data) :
        fname = data[0:data.index('(')]
        arglist = data[data.index('(')+1:data.index(')')].replace(" ", "").split(',')
        arglist = list(map(lambda x : int(x) if x.replace('-', '').isdigit() else x, filter(lambda v : v != '', arglist)))
        print('function :',fname, ', arguments :', arglist)
        print('------------------------------------------')
        return fname, arglist
funclist = [setblock, setpos, getblock]
'''
funclist = [setpos, getpos, setblock, setblocks, getblock,
                    getblockwithdata, chat, setting, hit, hitlastest,
                    hitfirst, stop, getseconds, setx, sety, setz,
                    getx, gety, getz]
'''
strlist = list(map(lambda x : str(x)[10:str(x).index(' at ')], funclist))
datalist = {1:"stone", 41:"gold", 42:"iron", 57:"diamond"}
playerlist = {}

def communicate(sock, address) :
    while True :
        try :
            data = sock.recv(1024).decode()
            if not data : continue
            print('data :',data)
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
                elif (fname == 'getblock') :
                    results = funclist[strlist.index(fname)](*fargs)
                    if results == None :
                        data = "Run failed... Check the function name."
                    else :
                        data = "Identified block ID : " + str(results) + ", position : [ x(" \
                               + str(fargs[0]) + "), y(" + str(fargs[1]) + "), z(" + str(fargs[2]) + ") ]"
                else :
                    data = "Run failed... Check the function name."
            except:
                    data = "Run failed... Check the code."
            sock.send(data.encode())
        except KeyboardInterrupt :
            print("KeyboardInterrupt occur, server is down")
            break
        except Exception :
            print("error occur :", Exception)
            break
    sock.close()

def communicate_with_client(sock, address) :
    global strlist, datalist, playerlist
    print("Connection from: " + str(address))
    communicate(sock, address)

def run_server(server_socket) :
    print("------------- start server -------------")
    server_socket.listen(5)
    while True :
            conn, address = server_socket.accept()
            t = threading.Thread(target=communicate_with_client, args=(conn, address,))
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
    print("Welcome to access Minecraft Code Avengers Server")
    start_server(int(input("Please enter the PORT number : ")))
    print("Server would be terminated. Bye.")