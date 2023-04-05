import socket
import pickle
import os
import time

networking_enabled = False
server_data = ""
file_path = "server.txt"

networking_file_path = "networking.txt"
if os.path.exists(networking_file_path):
    with open(networking_file_path, "r") as f:
        networking_enabled = f.read()
        print("Networking enabled (change in HELP menu): " + networking_enabled)


# Check if the file exists, and create it if it doesn't
if not os.path.exists(file_path):
    with open(file_path, "w") as f:
        with open(file_path, "r") as f:
            if networking_enabled:
                print("Networking enabled! But server.txt is blank! Please update it in the help menu, or alter it manually.")
else:
    with open(file_path, "r") as g:
        print("Network file detected! IP: " + str(g.read()))
class Network:
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server = str(server_data)
        self.port = 5555
        self.addr = (self.server, self.port)
        self.game = self.connect()

    def connect(self):
        try:
            self.client.connect(self.addr)
            return pickle.loads(self.client.recv(2048))
        except socket.error as e:
            print(e)

    def send(self, data):
        try:
            self.client.send(pickle.dumps(data))
            return pickle.loads(self.client.recv(2048))
        except socket.error as e:
            print(e)