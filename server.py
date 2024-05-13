import socket 
import json
import threading 
import redis
from Redis.redis_master import RedisMaster  # Importing the RedisMaster class from the redis_master.py file
from medical_monitor_gui import MedicalMonitoringGUI

PORT = 5050
FORMAT = 'utf-8' # format of the message we will send
SERVER = socket.gethostbyname(socket.gethostname()) # get server ip address of current machine
ADDR = (SERVER,PORT) # tuple of server ip address and port number

class Server:
    def __init__(self):
        self.next_patient_id = 1
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind(ADDR)
        self.server_socket.listen(5)
        print(f"Server listening on {SERVER}")
        # Create a Redis client
        self.redis_master = RedisMaster()
        self.redis_master.connect()

       # self.gui = MedicalMonitoringGUI(redis_master=self.redis_master)


    def handle_client(self,client_socket, patient_id):
        while True:
            data = client_socket.recv(1024)
            if not data:
                break

            try:
                data_decoded = json.loads(data.decode(FORMAT))
                print("Received data:", data_decoded)  # Print received data


            except json.JSONDecodeError:
                print("Invalid JSON data received from client")
                break
            vital_signs = data_decoded
            redis_key = f"patient_{patient_id}"
            # Retrieve existing data from Redis
            # existing_data = self.redis_master.get_key_value(redis_key)
            # if existing_data:
            #     existing_data = json.loads(existing_data)
            #     existing_data.append(vital_signs)
            #     print(f"Existing data: {existing_data}")
            # else:
            #     existing_data = [vital_signs]

            self.redis_master.set_key_value(redis_key, json.dumps(vital_signs))
            print(json.dumps(vital_signs))  
            print(f"Data stored in Redis: patient_{ patient_id } - {vital_signs}")   


            # self.gui.continuously_update_plot(existing_data)

        client_socket.close()     
 

    def run_server(self):
        try:
            #self.gui.run()
            while True:
                client_socket, client_address = self.server_socket.accept()
                print(f"New connection from {client_address}")

                #Assign patinet ID to the client
                patient_id = self.next_patient_id
                self.next_patient_id += 1
                #start a new thread to handle the client
                client_thread = threading.Thread(target=self.handle_client, args=(client_socket,patient_id))
                client_thread.start()
                print(f"Patient connections: {threading.active_count() - 1}")

        except KeyboardInterrupt:
            print("Server shutting down...")
        finally:
            self.server_socket.close()
            self.redis_master.disconnect() 

if __name__ == "__main__":
    server = Server()
    server.run_server()
