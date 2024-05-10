import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton
from PyQt5.QtGui import QPainter, QPen
from PyQt5.QtCore import Qt
import redis
import numpy as np
import matplotlib.pyplot as plt

class VitalSignsWidget(QWidget):
    def __init__(self, parent=None):
        super(VitalSignsWidget, self).__init__(parent)
        self.vital_signs_data = {}  # Dictionary to store vital signs data
        self.search_result_label = QLabel()
        self.search_lineedit = QLineEdit()
        self.search_button = QPushButton("Search")
        self.chart_canvas = ChartCanvas()

        # Connect search button clicked event to search function
        self.search_button.clicked.connect(self.search_patient)

        # Layout setup
        search_layout = QHBoxLayout()
        search_layout.addWidget(QLabel("Patient ID:"))
        search_layout.addWidget(self.search_lineedit)
        search_layout.addWidget(self.search_button)

        main_layout = QVBoxLayout()
        main_layout.addLayout(search_layout)
        main_layout.addWidget(self.search_result_label)
        main_layout.addWidget(self.chart_canvas)

        self.setLayout(main_layout)

    def search_patient(self):
        patient_id = self.search_lineedit.text()
        # Retrieve patient data from Redis (replace with actual Redis retrieval code)
        # For demonstration, generating random data
        self.vital_signs_data = self.retrieve_data_from_redis(patient_id)

        if self.vital_signs_data:
            self.search_result_label.setText(f"Patient {patient_id} found.")
            self.chart_canvas.plot_vital_signs(self.vital_signs_data)
        else:
            self.search_result_label.setText(f"Patient {patient_id} not found.")

    def retrieve_data_from_redis(self, patient_id):
        # Mock function to simulate data retrieval from Redis
        # Replace with actual Redis retrieval code
        if patient_id == "123":
            return {"Heart Rate": np.random.randint(60, 100, size=10),
                    "Blood Pressure": np.random.randint(80, 120, size=10)}
        else:
            return None

class ChartCanvas(QWidget):
    def __init__(self, parent=None):
        super(ChartCanvas, self).__init__(parent)
        self.vital_signs_data = {}

    def plot_vital_signs(self, data):
        self.vital_signs_data = data
        self.update()

    def paintEvent(self, event):
        qp = QPainter(self)
        qp.setRenderHint(QPainter.Antialiasing)

        # Plot vital signs data
        if self.vital_signs_data:
            pen = QPen(Qt.blue, 2, Qt.SolidLine)
            qp.setPen(pen)

            # Plot heart rate
            hr_values = self.vital_signs_data.get("Heart Rate", [])
            if hr_values:
                hr_points = [(i * 50, 200 - val) for i, val in enumerate(hr_values)]
                for i in range(len(hr_points) - 1):
                    qp.drawLine(*hr_points[i], *hr_points[i + 1])

            # Plot blood pressure
            bp_values = self.vital_signs_data.get("Blood Pressure", [])
            if bp_values:
                bp_points = [(i * 50, 200 - val) for i, val in enumerate(bp_values)]
                for i in range(len(bp_points) - 1):
                    qp.drawLine(*bp_points[i], *bp_points[i + 1])

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = QWidget()
    window.setWindowTitle('Vital Signs Monitoring')
    widget = VitalSignsWidget()
    layout = QVBoxLayout()
    layout.addWidget(widget)
    window.setLayout(layout)
    window.show()
    sys.exit(app.exec_())
