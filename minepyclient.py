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

    return 'Received from server: ' + data  # show in terminal

    #client_socket.close()  # close the connection

def setblock(x, y, z, blockid) :
        string = 'setblock('+str(x)+','+str(y)+','+str(z)+','+str(blockid)+')'
        print(client_program(string))

def getblock(x, y, z) :
        string = 'getblock('+str(x)+','+str(y)+','+str(z)+')'
        print(client_program(string))

def getblockid(x, y, z) :
        string = 'getblock('+str(x)+','+str(y)+','+str(z)+')'
        string = client_program(string)
        return int(string.split(" ")[-1])

client_socket = 0

def init() :
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

def init(host, port) :
    global client_socket
    print("Welcome to Minecraft Code Avengers Client Program.")
    print("-------------------------------------------------")
    try :
        connect(host, port)
    except Exception as e :
        print(client_socket)
        print("Connection error. Please restart to server.", str(e))


if __name__ == "__main__" :
    init()

