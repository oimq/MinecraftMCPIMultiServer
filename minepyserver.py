from minecraft import *
import socket

def convdatatofunc(data) :
        fname = data[0:data.index('(')]
        arglist = data[data.index('(')+1:data.index(')')].replace(" ", "").split(',')
        arglist = list(map(lambda x : int(x) if x.replace('-', '').isdigit() else x, filter(lambda v : v != '', arglist)))
        print('function :',fname, ', arguments :', arglist)
        return fname, arglist
funclist = [setblock, setpos, getblock]
'''
funclist = [setpos, getpos, setblock, setblocks, getblock,
                    getblockwithdata, chat, setting, hit, hitlastest,
                    hitfirst, stop, getseconds, setx, sety, setz,
                    getx, gety, getz]
'''
strlist = list(map(lambda x : str(x)[10:str(x).index(' at ')], funclist))
datalist = {1:"gold", 45:"stone", 42:"iron", 57:"diamond", 0:"air"}

def run_server(server_socket) :
        server_socket.listen(5)
        conn, address = server_socket.accept()
        print("Connection from: " + str(address))
        while True:
                try :
                        data = conn.recv(1024).decode()
                        if not data :
                            break
                        print('data :',data)
                        fname, fargs = convdatatofunc(str(data))
                        try :
                           if ((not 1 in fargs) and (not 57 in fargs) and (not 42 in fargs) and (not 41 in fargs)) and (fname == 'setblock') :
                                   data = "wrong block!"
                           elif fname in strlist :
                                   results = funclist[strlist.index(fname)](*fargs)
                                                                           
                                   if results == 45 :
                                           data = "gold"
                                   elif results == 1 :
                                           data = "stone"
                                   elif results == 42 :
                                           data = "iron"
                                   elif results == 57 :
                                           data = "diamond"
                                   elif results == 0 :
                                           data = "air"
                                   else :
                                           data = "block's id is " + str(results)
                           else :
                                data = "Run failed... Check the function name."
                        except:
                           data = "Run failed... Check the code."
                        conn.send(data.encode())
                except KeyboardInterrupt :
                        print("KeyboardInterrupt occur, server is down")
                        conn.close()
                except Exception :
                        print("error occur :", Exception)
        conn.close()

def start_server(_port) :
        host = '192.168.1.'
        port = _port
        e = 0
        server_socket = socket.socket()
        for ip in range(1, 256, 1) :
                try :
                        server_socket.bind((host+str(ip), port))
                        print('bind success :', host+str(ip))
                        run_server(server_socket)
                        exit()
                except :
                        e = 1
                        
