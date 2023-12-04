import socket
import pickle

from typing import Any
from core.game.match import Match


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
    def server_running(ip: str, port: int) -> bool:
        """Verifica se o servidor está online"""

        if port < 1 or port > 65535:
            return False

        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.connect((ip, port))
            return True
        except socket.error:
            return False

    @staticmethod
    def port_in_use(port: int) -> bool:
        """Verifica se a porta está em uso"""

        if port < 1 or port > 65535:
            return False

        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.bind(("localhost", port))
            return False
        except socket.error:
            return True

    def connect(self) -> int:
        """Conecta o cliente ao servidor"""

        self.__client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.__client.connect((self.__host, self.__port))
        self.__client.settimeout(0.2)  # Evita que o cliente fique preso no recv
        self.__running = True

        print(f"[Network] Connected to {self.__host}:{self.__port}")
        while True:
            try:
                return int(self.__client.recv(1024).decode())
            except socket.error:
                pass

    def disconnect(self):
        """Desconecta o cliente do servidor"""

        print("[Network] Disconnecting client...")
        self.__running = False
        self.__client.close()

    def send(self, data: dict[str, Any]) -> Match | None:
        """Envia dados para o servidor

        Args:
            data (dict[str, Any]): Dados a serem enviados para o servidor

        Returns:
            Match: Partida atualizada

        Examples:
            >>> network = Network("localhost", 5555)
            >>> network.send({"type": "GET"})
            Match(...)
        """

        if self.__running:
            data["id"] = self.__id

            try:
                self.__client.send(pickle.dumps(data))  # Envia dados para o servidor
                return pickle.loads(self.__client.recv(131072))  # Retorna a partida (32kb)
            except socket.error as e:
                print(f"[Network] Error: {e}")
            except pickle.UnpicklingError:
                return None
            except UnicodeDecodeError:
                return None
            except EOFError:
                return None
