import socket
import pickle

from typing import Any


class Network:
    __id: int
    __host: str
    __port: int

    __running: bool
    __client: socket.socket | None

    def __init__(self, host: str, port: int):
        self.__host = host
        self.__port = port
        self.__client = None
        self.__id = self.connect()

    @staticmethod
    def check_port(ip: str, port: int) -> bool:
        if port < 1 or port > 65535:
            return False
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        result = sock.connect_ex((ip, port))
        sock.close()
        return result != 0

    def connect(self) -> int:
        self.__client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.__client.connect((self.__host, self.__port))
        self.__running = True

        print(f"Connected to {self.__host}:{self.__port}")
        return int(self.__client.recv(2048).decode())

    def disconnect(self):
        print("Disconnecting client...")
        self.__running = False
        self.__client.close()

    def send(self, data: str) -> Any:
        if self.__running:
            try:
                self.__client.send(str.encode(data))
                return pickle.loads(self.__client.recv(4096))
            except socket.error as e:
                print(e)
