from PySide6.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, QMessageBox, QVBoxLayout
from PySide6.QtCore import QTimer


class FocusAndEyeDistanceApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Focus Timer & Eye Distance Sensor")
        self.setGeometry(100, 100, 400, 400)
        
        self.focus_time = 0.0  # User-defined focus time in minutes
        self.elapsed_time = 0.0  # Time elapsed in tracking
        self.time_factor = 10  # Scaling factor for faster testing
        self.safe_distance = 65
        
        # Focus Timer UI
        self.timer_label = QLabel("Enter focus time (minutes, enter 0 to skip):", self)
        self.timer_input = QLineEdit(self)
        self.start_timer_button = QPushButton("Start Timer", self)
        
        self.progress_notification = QLabel("", self)
        self.progress_notification.setStyleSheet("QLabel { color: black; padding: 5px; border-radius: 5px; border: 1px solid black; font-weight: bold; }")
        self.progress_notification.hide()
        
        # Eye Distance Sensor UI
        self.label = QLabel("Enter distance (cm):", self)
        self.input_field = QLineEdit(self)
        self.check_button = QPushButton("Check Distance", self)
        self.break_notification = QLabel("", self)
        self.break_notification.setStyleSheet("QLabel { background-color: #ADD8E6; color: black; padding: 5px; border-radius: 5px; }")
        self.break_notification.hide()
        
        layout = QVBoxLayout()
        layout.addWidget(self.timer_label)
        layout.addWidget(self.timer_input)
        layout.addWidget(self.start_timer_button)
        layout.addWidget(self.progress_notification)
        layout.addWidget(self.label)
        layout.addWidget(self.input_field)
        layout.addWidget(self.check_button)
        layout.addWidget(self.break_notification)
        self.setLayout(layout)
        
        self.start_timer_button.clicked.connect(self.start_timer)
        self.check_button.clicked.connect(self.check_distance)
        
        # Timers
        self.progress_timer = QTimer(self)
        self.progress_timer.timeout.connect(self.update_progress)
        
        self.break_timer = QTimer(self)
        self.break_timer.timeout.connect(self.show_break_notification)
        self.break_timer.start(10000)

    def start_timer(self):
        try:
            self.focus_time = float(self.timer_input.text())
        except ValueError:
            self.progress_notification.setText("Invalid input. Please enter a number.")
            self.progress_notification.setStyleSheet("QLabel { background-color: darkred; color: white; padding: 5px; border-radius: 5px; border: 1px solid black; }")
            self.progress_notification.show()
            return
        
        if self.focus_time == 0:
            self.timer_label.hide()
            self.timer_input.hide()
            self.start_timer_button.hide()
            return
        
        self.elapsed_time = 0
        self.progress_timer.start(int(6000 / self.time_factor))  # Adjusted for testing

    def update_progress(self):
        self.elapsed_time += (1 / self.time_factor)
        progress = (self.elapsed_time / self.focus_time) * 100
        
        if progress >= 100:
            self.progress_notification.setText("Focus session complete! Great job!")
            self.progress_notification.setStyleSheet("QLabel { background-color: #90EE90; color: black; padding: 5px; border-radius: 5px; border: 1px solid black; }")
            self.progress_notification.show()
            self.progress_timer.stop()
            QTimer.singleShot(3000, self.hide_focus_section)
        elif progress >= 90:
            self.progress_notification.setText("Almost there! Just a little more to go.")
            self.progress_notification.setStyleSheet("QLabel { background-color: #FFFF99; color: black; padding: 5px; border-radius: 5px; border: 1px solid black; }")
        elif progress >= 50:
            self.progress_notification.setText("You're halfway through! Keep going!")
            self.progress_notification.setStyleSheet("QLabel { background-color: #FFA500; color: black; padding: 5px; border-radius: 5px; border: 1px solid black; }")
        
        self.progress_notification.show()
    
    def hide_focus_section(self):
        self.progress_notification.hide()
        self.timer_label.hide()
        self.timer_input.hide()
        self.start_timer_button.hide()

    def check_distance(self):
        try:
            distance = float(self.input_field.text())
        except ValueError:
            QMessageBox.critical(self, "Error", "Invalid input. Please enter a number.")
            return
        
        if distance < self.safe_distance:
            warning_box = QMessageBox(self)
            warning_box.setIcon(QMessageBox.Critical)
            warning_box.setWindowTitle("Warning: Myopia Risk")
            warning_box.setText("Your viewing distance is too close. Please move further away to reduce myopia risk.")
            warning_box.setStyleSheet("QLabel{color: black; font-weight: bold;} QMessageBox {background-color: #E57373;}")
            warning_box.exec()
    
    def show_break_notification(self):
        self.break_notification.setText("Remember to take a short break away from the screen to reduce eye strain!")
        self.break_notification.show()
        QTimer.singleShot(5000, self.break_notification.hide)


if __name__ == "__main__":
    app = QApplication([])
    window = FocusAndEyeDistanceApp()
    window.show()
    app.exec()