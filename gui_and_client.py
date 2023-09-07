import socket
import tkinter as tk
import keyboard
from PyQt5.QtWidgets import QApplication, QMainWindow
from generated_ui import Ui_Dialog  # Replace with the name of your UI class
import datetime  


def send_command(command):
    client_socket.send(command.encode())


class MyMainWindow(QMainWindow, Ui_Dialog):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        # Connect buttons to send commands
        self.pushButton.clicked.connect(lambda: send_command('w'))
        self.pushButton_2.clicked.connect(lambda: send_command('s'))
        self.pushButton_3.clicked.connect(lambda: send_command('a'))
        self.pushButton_4.clicked.connect(lambda: send_command('d'))
        self.pushButton_5.clicked.connect(lambda: send_command('e'))
        self.pushButton_6.clicked.connect(lambda: send_command('3'))
        self.pushButton_7.clicked.connect(lambda: send_command('t'))

        self.toolButton.clicked.connect(self.handle_time_button)

         # Create a QTimer to update the time display every second
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_time)
        self.timer.start(1000)  # Update every 1000 milliseconds (1 second)

    def update_time(self):
        current_time = datetime.datetime.now().strftime("%H:%M:%S")
        self.lcdNumber.display(current_time)


if __name__ == '__main__':
    app = QApplication([])
    main_window = MyMainWindow()
    main_window.show()
    
    # Set up socket client
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(('192.168.1.16', 8001))  # Replace with your Pi's IP
    
    while True:
        if keyboard.is_pressed('q'):
            break
        elif keyboard.is_pressed('w'):
            MyMainWindow.send_command('w')
            print("w")
        elif keyboard.is_pressed('s'):
            MyMainWindow.send_command('s')
            print("s")
        elif keyboard.is_pressed('a'):
            MyMainWindow.send_command('a')
        elif keyboard.is_pressed('d'):
            MyMainWindow.send_command('d')

    client_socket.close()
    app.exec_()
