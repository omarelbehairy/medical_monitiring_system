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
        self.patient_data = {}

        self.high_threshold = 115
        self.low_threshold = 35


 

        self.create_search_bar()
        self.create_display_area()

        # self.update_thread = threading.Thread(target=self.update_gui_with_patient_data)
        # self.update_thread.daemon = True
        # self.update_thread.start()

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
        patient_id = int(self.search_entry.get())
        redis_key = f"patient_{patient_id}"
        print ("searching for patient data with key : ", redis_key)
        self.patient_id = patient_id
       
        self.clear_plot()
        self.search_entry.delete(0, tk.END)

    def update_pulse(self, heart_rate_pulse, patient_id):
          if self.patient_id is not None:
            # Add heart rate pulse to patient data in dictionary
            print("Updating patient data for patient id: ", self.patient_id)
            if patient_id not in self.patient_data:
               self.patient_data[patient_id] = []  # Initialize empty list for patient data
            
            self.patient_data[patient_id].append(heart_rate_pulse)
            print(self.patient_data)
            print("self : ", self.patient_id)  
            print("patient id not self : ", patient_id)
            if int(patient_id) == int(self.patient_id):
                print("ehhhhhhhhhhhhhh b2aa")
                self.update_gui_with_patient_data()
          else:
            print("Please enter a valid patient ID")
            
            
    def update_gui_with_patient_data(self):
        self.ax.clear()
        patient_pulse = self.patient_data[int(self.patient_id)]
        latest_heart_rate = patient_pulse[-1] if patient_pulse else None

        print("patient pulse : ", patient_pulse)

        exceeded_high_threshold = latest_heart_rate and latest_heart_rate > self.high_threshold
        exceeded_low_threshold = latest_heart_rate and latest_heart_rate < self.low_threshold

        if patient_pulse:
            if exceeded_high_threshold:
                self.ax.text(0.5, 0.9, 'High Heart Rate', horizontalalignment='center', verticalalignment='center', transform=self.ax.transAxes, color='red', fontsize=12)
            elif exceeded_low_threshold:
                self.ax.text(0.5, 0.9, 'Low Heart Rate', horizontalalignment='center', verticalalignment='center', transform=self.ax.transAxes, color='red', fontsize=12)
            else:
            # If heart rate pulse is within normal range, clear any existing warning messages
                self.ax.text(0.5, 0.9, '', horizontalalignment='center', verticalalignment='center', transform=self.ax.transAxes, fontsize=12)    

        
        # Plot vital signs with time values
            self.ax.plot(patient_pulse, color='b', linestyle='-')
            self.ax.set_xlabel('Time')
            self.ax.set_ylabel(f"Heart Rate Pulse of Patient({self.patient_id})")
            self.ax.set_title('Heart Rate Pulse Over Time')

            # Adjust y-axis limits based on the range of heart rate values
            min_heart_rate = min(patient_pulse)
            max_heart_rate = max(patient_pulse)
            margin = 10  # Add a small margin
            self.ax.set_ylim([min_heart_rate - margin, max_heart_rate + margin])


        self.canvas.draw()
 
    def clear_plot(self):
        self.patient_data = {}
        self.ax.clear()
        self.canvas.draw()

    def run(self):
        self.root.mainloop()


# if __name__ == "__main__":
#     gui = MedicalMonitoringGUI()
#     gui.run()
