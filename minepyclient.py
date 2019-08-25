import socket

def connect(host, port) :
    global client_socket
    client_socket = socket.socket() # instantiate
    try :
        client_socket.connect((host, port))  # connect to the server
    except :
        print('connect fail...', host)
        client_socket.close()
    print('connect success :', host)

def client_program(msg):
    global client_socket
    if client_socket == 0 :
        return "The Connection with Server is not exists."
    message = msg  # take input
    client_socket.send(message.encode())  # send message
    data = client_socket.recv(1024).decode()  # receive response
    return data

    #return 'Received from server : ' + data  # show in terminal
    #client_socket.close()  # close the connection

def setblock(x, y, z, blockid) :
    string = 'setblock('+str(x)+','+str(y)+','+str(z)+','+str(blockid)+')'
    print(client_program(string))

def setblocks(x1, y1, z1, x2, y2, z2, blockid) :
    string = 'setblocks('+str(x1)+','+str(y1)+','+str(z1)+','+str(x2)+','+str(y2)+','+str(z2)+','+str(blockid)+')'
    print(client_program(string))

def getblock(x, y, z) :
    string = 'getblock('+str(x)+','+str(y)+','+str(z)+')'
    print(client_program(string))

def getblockid(x, y, z) :
    string = 'getblock('+str(x)+','+str(y)+','+str(z)+')'
    string = client_program(string)
    index = "ID : "
    index = string.index(index)+len(index)
    return int(string[index:index+1])

def setpos(x, y, z, username="default") :
    string = "setpos("+username+','+str(x)+','+str(y)+','+str(z)+")"
    print(client_program(string))

def getpos(username="default") :
    string = "getpos("+username+")"
    string = client_program(string)
    if string.startswith("Run") :
        return None
    else :
        return list(map(float, string.split(", ")))

def chat(msg) :
    string = "chat("+msg+")"
    print(client_program(string))

client_socket = 0

def init_set() :
    global client_socket
    print("Welcome to Minecraft Code Avengers Client Program.")
    print("-------------------------------------------------")
    host = input("First, Enter the Server address : ")
    port = int(input("Second, Enter the Server PORT number : "))
    print("-------------------------------------------------")
    print("Thank for Server's information. Now we connect...")
    try :
        connect(host, port)
    except Exception as e :
        print(client_socket)
        print("Connection error. Please restart to server.", str(e))

def init(host="localhost", port=10000) :
    global client_socket
    print("Welcome to Minecraft Code Avengers Client Program.")
    print("-------------------------------------------------")
    try :
        connect(host, port)
    except Exception as e :
        print(client_socket)
        print("Connection error. Please restart to server.", str(e))

import atexit
@atexit.register
def close_connection() :
    global client_socket
    print(client_program("exit"))
    client_socket.close()

if __name__ == "__main__" :
    init()

