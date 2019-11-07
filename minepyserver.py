from minecraft import *
import socket
import threading
import time

SEP_S, SEP_E = '+'*50, '-'*50
debug = True
def ppe(*args) :
    global debug, SEP_E
    if debug : print(SEP_E); print(*args); print(SEP_E)

def pps(*args) :
    global debug, SEP_S
    if debug : print(SEP_S); print(*args); print(SEP_S)

# Convert data to function format.
def convdatatofunc(data) :
    if '(' in data and ')' in data :
        sinx = data.index('(')
        func = data[:sinx]
        args = data[sinx+1:-1].replace(" ", "").split(',')
        args = list(map(lambda x : float(x) if x.replace('-', '').replace('.', '').isdigit() else x, filter(lambda v : v != '', args)))
        ppe('function name :', func, ', arguments :', args)
        return func, args
    else : return None, None


# Minecraft functions
''' All Minecraft Functions
funclist = [setpos, getpos, setblock, setblocks, getblock, getblockwithdata, chat, setting, hit, hitlastest,
            hitfirst, stop]
notlist = [hit, hitlastest, hitfirst, ]
'''

# Implemented functions
funclist = [setblock, getpos, getblock, setblocks, chat, setpos, setting, getblockwithdata]
# String version
sfunclist = list(map(lambda x : str(x)[10:str(x).index(' at ')], funclist))

# Minecraft entities
datalist = {0:"air", 1:"stone", 41:"gold", 42:"iron", 57:"diamond", 8:"water",
            9:"water", 27:"rail", 152:"redstone-block", 169:"sea_lantern",
            79:"ice", 46:"tnt", 10:"lava", 51:"fire", 17:"tree1", 18:"tree2", 103:"melon",175:'flower'}

playerlist = {'192.168.1.102':'oimqA'}
oplist = ['192.168.1.102']

def run_function(fname, *fargs) :
    try :
        results = funclist[sfunclist.index(fname)](*fargs)
        return results
    except :
        raise (Exception("Run fail... Please Check the commands."))
        return None

results = None
# Communication for connected user.
def communicate(sock, address) :
    global results
    while True :
        try :
            data = sock.recv(1024).decode()
            if not data : continue
            elif data == 'exit' : break

            if debug : ppe('origin :', address, ', data :', data)
            fname, fargs = convdatatofunc(str(data))

            if not fname in sfunclist : raise Exception('Error : Function <'+fname+'> is not defined.')

            if (fname == 'setblock') :
                block_id = fargs[-1]
                if block_id in datalist :
                    results = funclist[sfunclist.index(fname)](*fargs)
                    data = datalist[block_id] + " block is set, position : x({}), y({}), z({}).".format(*fargs[:3])
                else :
                    data = "Run failed... These blocks are only permitted : "+', '.join(datalist.values())

            elif (fname == 'setblocks') :
                block_id = fargs[-1]
                if block_id in datalist :
                    results = funclist[sfunclist.index(fname)](*fargs)
                    data = datalist[block_id] \
                           + " blocks are set, position : x1({}), y1({}), z1({}), x2({}), y2({}), z2({}).".format(*fargs[:6])
                else :
                    data = "Run failed... These blocks are only permitted : "+', '.join(datalist.values())

            elif (fname == 'setpos') :
                player_name = fargs[0]
                if address[0] in playerlist and playerlist[address[0]] != player_name :
                    data = "Please access only your character."
                else :
                    funclist[sfunclist.index(fname)](*fargs)
                    data = player_name \
                           + " player is set, position : x({}), y({}), z({}).".format(*fargs[1:4])

            elif (fname == 'chat') :
                funclist[sfunclist.index(fname)](data[5:-1])
                data = 'you said that "'+data[5:-1]+'"'

            elif (fname == 'getblock') :
                results = funclist[sfunclist.index(fname)](*fargs)
                data = str(results)

            elif (fname == 'getblockwithdata') :
                results = funclist[sfunclist.index(fname)](*fargs)
                data = str(tuple(results))[1:-1]

            elif (fname == 'getpos') :
                results = funclist[sfunclist.index(fname)](*fargs)
                data = str(results.x)+","+str(results.y)+","+str(results.z)

            elif (fname == 'setting') :
                if address[0] in oplist :
                    funclist[sfunclist.index(fname)](*fargs)
                    data = 'setting done.'

            sock.send(data.encode())

        # Signals and errors handling
        except EOFError as eof :
            sock.send("The connection with server is over.".encode())
            pps("Close the connection : " + str(address))
            data = "Bye."
            sock.send(data.encode())
            break
        except KeyboardInterrupt :
            print("KeyboardInterrupt occur, server is down")
            data = "Server is down."
            sock.send(data.encode())
            break
        except Exception as e:
            print("Error occur :", str(e))
            data = str(e)
            sock.send(data.encode())
            break
    sock.close()

# Thread for Client
def th_communicate_with_client(sock, address) :
    pps("User", address, "is joined.")
    communicate(sock, address)
    pps("User", address, "is exit.")

# Thread for Server
# def th_management_with_server() :

def deciside_block_mode() :
    global datalist, sfunclist
    if (input("Do you want to forbid the air block? (y or n) : ") == 'y') :
        del(datalist[0])
    if (input("Do you want to block the setblocks mode? (y or n) : ") == 'y') :
        sfunclist.remove('setblocks')
    if (input("Do you want to block the setpos mode? (y or n) : ") == 'y') :
        sfunclist.remove('setpos')

def run_server(server_socket) :
    deciside_block_mode()
    pps("Now, the server begin to listening clients!")
    server_socket.listen(5)
    while True :
            conn, address = server_socket.accept()
            t = threading.Thread(target=th_communicate_with_client, args=(conn, address))
            t.daemon = True
            t.start()

def start_server() :
    server_socket = socket.socket()
    host = socket.gethostbyname(socket.gethostname())
    while True :
        try :
            server_socket.bind((host, int(input("Please enter the PORT number : "))))
            print('bind success :', host)
            run_server(server_socket)
            break
        except KeyboardInterrupt as kbi :
            break
        except Exception as e :
            print(e.__str__(), '\nbind failed. we restart server after 5 seconds.')
            time.sleep(5)
    server_socket.close()

if __name__ == "__main__" :
    print("Welcome to access the Minecraft Server")
    start_server()
    print("Server would be terminated. Bye.")
    exit()