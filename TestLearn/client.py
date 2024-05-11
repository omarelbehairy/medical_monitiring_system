import socket 

HEADER = 64 #first message will be of 64 bytes, it will contain the length of the message
PORT = 5050
FORMAT = 'utf-8' # format of the message we will send
DISCONNECT_MESSSAGE = "!DISCONNECT" 
SERVER = "192.168.1.8" # get server ip address of current machine
ADDR = (SERVER,PORT) # tuple of server ip address and port number
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # AF_INET is the type of address we will use, SOCK_STREAM is the type of connection we will use
client.connect(ADDR) # connect to the server


def send(msg):
    message = msg.encode(FORMAT) # encode the message to bytes
    msg_length = len(message) # get the length of the message
    send_length = str(msg_length).encode(FORMAT) # encode the length to bytes
    send_length += b' ' * (HEADER - len(send_length)) # add padding to the message
    client.send(send_length) # send the length of the message
    client.send(message) # send the message
    print(client.recv(2048).decode(FORMAT)) # receive a response

send("Hello World")    
input()
send("Hello Everyone") 
input()   
send("!DISCONNECT")