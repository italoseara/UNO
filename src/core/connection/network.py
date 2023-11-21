import socket
import pickle

from typing import Any
from core.match import Match


class Network:
    __id: int
    __host: str
    __port: int

    __running: bool
    __client: socket.socket | None

    def __init__(self, host: str, port: int):
        """Inicializa a conexão com o servidor

        Args:
            host (str): Endereço do servidor
            port (int): Porta do servidor
        """

        self.__host = host
        self.__port = port
        self.__client = None
        self.__id = self.connect()

    @property
    def id(self) -> int:
        return self.__id

    @staticmethod
    def check_port(ip: str, port: int) -> bool:
        if port < 1 or port > 65535:
            return False
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        result = sock.connect_ex((ip, port))
        sock.close()
        return result != 0

    def connect(self) -> int:
        """Conecta o cliente ao servidor"""

        self.__client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.__client.connect((self.__host, self.__port))
        self.__running = True

        print(f"Connected to {self.__host}:{self.__port}")
        return int(self.__client.recv(2048).decode())

    def disconnect(self):
        """Desconecta o cliente do servidor"""

        print("Disconnecting client...")
        self.__running = False
        self.__client.close()

    def send(self, data: dict[str, Any]) -> Match:
        """Envia dados para o servidor

        Args:
            data (dict[str, Any]): Dados a serem enviados para o servidor

        Returns:
            Match: Partida atualizada

        Examples:
            >>> network = Network("localhost", 5555)
            >>> network.send({"id": 1, "type": "GET"})
            Match(...)
        """

        if self.__running:
            try:
                self.__client.send(pickle.dumps(data))  # Envia dados para o servidor
                return pickle.loads(self.__client.recv(4096))  # Retorna a partida
            except socket.error as e:
                print(e)
