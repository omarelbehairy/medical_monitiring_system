import tkinter as tk
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import json 
from Redis.redis_master import RedisMaster  # Importing the RedisMaster class from the redis_master.py file
from clientt import Client
import threading
import time
import socket
SERVER_PORT = 5050
FORMAT = 'utf-8' # format of the message we will send
#SERVER_HOST = "192.168.1.8" # get server ip address of current machine
SERVER_HOST =  socket.gethostbyname(socket.gethostname()) 
ADDR = (SERVER_HOST,SERVER_PORT) # tuple of server ip address and port number



#C:\ML\Real-Time Medical Monitoring System\medical_monitiring_system    
class MedicalMonitoringGUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Medical Data Monitoring System")
        self.patient_id = None
        self.heart_rate_pulse = []

 

        self.create_search_bar()
        self.create_display_area()

        self.update_thread = threading.Thread(target=self.update_gui_with_patient_data)
        self.update_thread.daemon = True
        self.update_thread.start()

    def create_search_bar(self):
        self.search_bar = ttk.Label(self.root, text="Enter Patient ID:")
        self.search_bar.grid(row=0, column=0, padx=10, pady=10)

        self.search_entry = tk.Entry(self.root)
        self.search_entry.grid(row=0, column=1, padx=10, pady=10)

        self.search_button = tk.Button(self.root, text="Search", command=self.search_patient)
        self.search_button.grid(row=0, column=2, padx=10, pady=10)

    def create_display_area(self):
        self.figure, self.ax = plt.subplots()    
        self.canvas = FigureCanvasTkAgg(self.figure, self.root)
        self.canvas.get_tk_widget().grid(row=1, column=0, columnspan=3, padx=10, pady=10)

    def search_patient(self):
        patient_id = self.search_entry.get()
        redis_key = f"patient_{patient_id}"
        print ("searching for patient data with key : ", redis_key)
        self.patient_id = patient_id
        self.search_entry.delete(0, tk.END)

    def update_pulse(self, heart_rate_pulse):
        self.heart_rate_pulse.append(heart_rate_pulse)
        self.update_gui_with_patient_data()
            
    def update_gui_with_patient_data(self):

        self.ax.clear()
        
        # Extract vital signs data
        print(self.heart_rate_pulse)


        # Plot vital signs with time values
        self.ax.plot(self.heart_rate_pulse, color='b', linestyle='-')
        self.ax.set_xlabel('Time')
        self.ax.set_ylabel('Heart Rate Pulse')
        self.ax.set_title('Heart Rate Pulse Over Time')

        # Adjust y-axis limits based on the range of heart rate values
        if self.heart_rate_pulse:
            min_heart_rate = min(self.heart_rate_pulse)
            max_heart_rate = max(self.heart_rate_pulse)
            margin = 10  # Add a small margin
            self.ax.set_ylim([min_heart_rate - margin, max_heart_rate + margin])


        self.canvas.draw()


    # def continuously_update_plot(self, patient_data):
    #     if self.patient_id:
    #             redis_key = f"patient_{self.patient_id}"
    #             patient_data = self.redis_master.get_key_value(redis_key)
    #             print("patient data : ", patient_data)
    #             if patient_data:
    #                 heart_rate_pulse = patient_data[-1]['heart_rate_pulse']  # Get the latest heart rate pulse
    #                 self.heart_rate_pulse.append(heart_rate_pulse)
    #                 print("heart rate pulse : ", heart_rate_pulse)
    #                 self.update_gui_with_patient_data()
    #             else:
    #                 print("No patient data found")
    #     else:
    #         print("No patient ID entered")
    #     time.sleep(1)  # Adjust the interval as needed
 

    def run(self):
        self.root.mainloop()


# if __name__ == "__main__":
#     gui = MedicalMonitoringGUI()
#     gui.run()
