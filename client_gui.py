import socket
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton
from PyQt5.QtCore import QTimer
from keyboard import is_pressed
import pyqtgraph as pg

class RemoteControlGUI(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle('Remote Control GUI')

        layout = QVBoxLayout()

        self.tachometer = pg.PlotWidget(title='Tachometer')
        self.tachometer_plot = self.tachometer.plot(pen='r')
        layout.addWidget(self.tachometer)

        commands = ['w', 's', 'a', 'd', 'e', '3', 't']

        for command in commands:
            button = QPushButton(command, self)
            button.clicked.connect(lambda _, cmd=command: self.send_command(cmd))
            layout.addWidget(button)

        self.setLayout(layout)

        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.connect(('192.168.1.16', 8002))  # Replace with your Pi's IP

        self.speed = 0
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_tachometer)
        self.timer.start(100)  # Update every 100 ms

    def send_command(self, command):
        self.client_socket.send(command.encode())

    def update_tachometer(self):
        self.tachometer_plot.setData([0, self.speed])

    def keyPressEvent(self, event):
        key = event.key()
        if key == ord('w'):
            self.send_command('w')
            self.speed += 10
        elif key == ord('s'):
            self.send_command('s')
            self.speed -= 10
        elif key == ord('a'):
            self.send_command('a')
        elif key == ord('d'):
            self.send_command('d')
        elif key == ord('e'):
            self.send_command('e')
        elif key == ord('3'):
            self.send_command('3')
            self.speed += 20
        elif key == ord('t'):
            self.send_command('t')
            self.speed -= 20
        elif key == ord('q'):
            self.quit_and_send()

    def quit_and_send(self):
        self.client_socket.send('q'.encode())
        self.client_socket.close()
        self.close()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    gui = RemoteControlGUI()
    gui.show()
    sys.exit(app.exec_())
