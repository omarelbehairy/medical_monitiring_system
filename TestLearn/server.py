import socket
import threading #allow to separate code 


HEADER = 64 #first message will be of 64 bytes, it will contain the length of the message
PORT = 5050
FORMAT = 'utf-8' # format of the message we will send
DISCONNECT_MESSSAGE = "!DISCONNECT" 
SERVER = socket.gethostbyname(socket.gethostname()) # get server ip address of current machine
print(socket.gethostname()) #DESKTOP-QB4O65F, name that represent current computer on network
ADDR = (SERVER,PORT) # tuple of server ip address and port number


server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # AF_INET is the type of address we will use, SOCK_STREAM is the type of connection we will use
server.bind(ADDR) # bind the socket to the address
#AF_INET is the address family for IPv4
#SOCK_STREAM is the socket type for TCP
#SOCK_DGRAM is the socket type for UDP


#handle all communication between client and server(individual connection)
#this function is for each client
def handle_client(conn, addr):
    print(f"[NEW CONNECTION] {addr} connected.")

    connected = True
    while connected:
        msg_length = conn.recv(HEADER).decode(FORMAT) #receive the message length
        if msg_length:
            msg_length = int(msg_length)
            msg = conn.recv(msg_length).decode(FORMAT) #receive the message
            if msg==DISCONNECT_MESSSAGE:
                connected = False
            print(f"[{addr}] {msg}")
            conn.send("Msg received".encode(FORMAT))    

    conn.close()


#start the server and listen for incoming connections and distribute them to handle_client function
def start():
    server.listen()
    print(f"[LISTENING] Server is listening on {SERVER}")
    while True:
        conn, addr = server.accept() #addr-->ip address and port of client, conn-->socket object
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()
        print(f"[ACTIVE CONNECTIONS] {threading.active_count() - 1}")



print("[STARTING] server is starting...")
start()