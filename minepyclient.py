import socket

host = '192.168.1.'  # as both code is running on same pc
client_socket = 0

def connect(ip, port) :
        global client_socket, host
        client_socket = socket.socket() # instantiate
        try :
            client_socket.connect((host+str(ip), port))  # connect to the server
            print('connect success :', host+str(ip))
        except :
            print('connect fail...', host+str(ip))
            client_socket.close()

def client_program(msg):
        global client_socket
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
