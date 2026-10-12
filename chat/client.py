import sys
import socket
import threading
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QTextEdit, QLineEdit, QPushButton, QLabel, QInputDialog)
from PyQt6.QtCore import pyqtSignal, QObject

class ClientSignals(QObject):
    msg_received = pyqtSignal(str)

class ChatClientGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.client_socket = None
        self.nickname = ""
        self.signals = ClientSignals()
        self.signals.msg_received.connect(self.append_message)

        self.init_ui()
        self.get_nickname_and_connect()

    def init_ui(self):
        self.setWindowTitle("TCP CHAT")
        self.resize(450, 550)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        self.chat_window = QTextEdit()

        self.chat_window.setReadOnly(True)
        main_layout.addWidget(self.chat_window)

        input_layout = QHBoxLayout()

        self.msg_input = QLineEdit()
        self.msg_input.setPlaceholderText("Մուտքագրեք հաղորթագրություն")
        self.msg_input.returnPressed.connect(self.send_msg)
        input_layout.addWidget(self.msg_input)


        self.send_button = QPushButton("Ուղարկել")
        self.send_button.clicked.connect(self.send_msg)
        input_layout.addWidget(self.send_button)

        main_layout.addLayout(input_layout)

    def get_nickname_and_connect(self):
        text, ok = QInputDialog.getText(self, 'Մուտք', 'Մուտքագրեք Ձեր մուտքանունը')
        if ok and text:
            self.nickname = text
            self.connect_to_server()
        else:
            sys.exit()

    def receive_msg(self):
        while True:
            try:
                msg = self.client_socket.recv(1024).decode('utf-8')
                if msg == "NICK":
                    self.client_socket.send(self.nickname.encode('utf-8'))
                else:
                    self.signals.msg_received.emit(msg)
            except:
                self.signals.msg_received.emit('[Disconnected] Server die!')
                self.client_socket.close()
                break

    def connect_to_server(self):
        try:
            self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.client_socket.connect(('127.0.0.1', 5555   ))

            receive_thread = threading.Thread(target=self.receive_msg)
            receive_thread.daemon = True
            receive_thread.start()
        except Exception as error:
            self.chat_window.append(f"[ERROR] Ձախողում! {error}")

    def send_msg(self):
        msg = self.msg_input.text().strip()
        if msg and self.client_socket:
            full_msg = f"{self.nickname}: {msg}"
            try:
                self.client_socket.send(full_msg.encode('utf-8'))
                self.msg_input.clear()
            except:
                self.chat_window.append(f"[ERROR] Հաղորդագրությունը չի ուղարկվել")
    def append_message(self, msg):
        self.chat_window.append(msg)

    def closeEvent(self, event):
        if self.client_socket:
            self.client_socket.close
        
        event.accept()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    gui = ChatClientGUI()
    gui.show()
    sys.exit(app.exec())
                
# ENV