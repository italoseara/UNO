import socket
import pickle

from typing import Any


class Network:
    id: int
    host: str
    port: int
    running: bool
    client: socket.socket | None

    def __init__(self, host: str, port: int):
        self.host = host
        self.port = port
        self.client = None
        self.id = self.connect()

    def connect(self) -> int:
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect((self.host, self.port))
        self.running = True

        print(f"Connected to {self.host}:{self.port}")
        return int(self.client.recv(2048).decode())

    def disconnect(self):
        print("Disconnecting client...")
        self.running = False
        self.client.close()

    def send(self, data: str) -> Any:
        if self.running:
            try:
                self.client.send(str.encode(data))
                return pickle.loads(self.client.recv(4096))
            except socket.error as e:
                print(e)
