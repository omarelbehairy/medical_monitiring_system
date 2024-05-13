import tkinter as tk
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import json 
import threading 
import socket
import random
import time
import medical_monitor_gui 
SERVER_PORT = 5050
FORMAT = 'utf-8' # format of the message we will send
#SERVER_HOST = "192.168.1.8" # get server ip address of current machine
SERVER_HOST =  socket.gethostbyname(socket.gethostname()) 
ADDR = (SERVER_HOST,SERVER_PORT) # tuple of server ip address and port number

class Client:
    def __init__(self):
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.connect(ADDR) # connect to the server


    def generate_vital_signs(self):
        #generate random vital signs
        """
        high heart rate levels: rate>=100 beats per minute

        """
        heart_rate_pulse = random.randint(30, 140)

        return heart_rate_pulse
    

    def send_vital_signs(self, heart_rate_pulse):
        try:
            data = {'heart_rate_pulse': heart_rate_pulse}
            data_json = json.dumps(data)
            print('dataJson',data_json)
            self.client_socket.send(data_json.encode(FORMAT))
            print('ENCODEDJSON',data_json.encode(FORMAT))

        except Exception as e:
            print("Error in sending vital signs",e)



    def close(self):
        if self.client_socket:
            self.client_socket.close()
    def run(self):
        try:
            while True:
                heart_rate_pulse = self.generate_vital_signs()
                self.send_vital_signs(heart_rate_pulse)
                print(f"Heart rate pulse: {heart_rate_pulse}bpm")

                

                time.sleep(random.uniform(1, 2))

        except KeyboardInterrupt:
            print("Client shutting down...")
            self.close()

if __name__ == "__main__":
    client = Client()
    client.run()