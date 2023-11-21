import sys
import socket
import pickle
import threading

from core.match import Match


class Server:
    __host: str
    __port: int
    __running: bool

    __clients: dict[int, socket.socket]
    __server: socket.socket | None

    __match: Match

    def __init__(self, host: str, port: int):
        """Inicializa o servidor

        Args:
            host (str): Endereço do servidor
            port (int): Porta do servidor
        """

        self.__host = host
        self.__port = port
        self.__running = False

        self.__clients = {}
        self.__server = None

        self.__match = Match()

    def start(self) -> None:
        """Inicia o servidor"""

        self.__server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.__server.bind((self.__host, self.__port))
        self.__server.listen(4)
        self.__running = True
        print(f"Server is running on port {self.__port}")

        while self.__running:
            try:
                client, address = self.__server.accept()
                if self.__match.ready:
                    client.close()
                    continue

                if len(self.__clients) == 4:
                    self.__match.ready = True

                print(f"Client connected from {address[0]}:{address[1]}")
                self.__add_client(client)
            except KeyboardInterrupt:
                self.stop()

    def stop(self) -> None:
        """Para o servidor"""

        print("Stopping server...")
        self.__running = False
        self.__server.close()
        sys.exit()

    def __add_client(self, client: socket.socket) -> None:
        """Adiciona um cliente ao servidor

        Args:
            client (socket.socket): Socket do cliente
        """

        client_id = 0
        while client_id in self.__clients.keys():
            client_id += 1

        self.__clients[client_id] = client

        # Start client thread
        client_thread = threading.Thread(target=self.__handle_client, args=(client, client_id))
        client_thread.start()

    def __remove_client(self, client_id: int) -> None:
        """Remove um cliente do servidor

        Args:
            client_id (int): ID do cliente
        """

        client = self.__clients.pop(client_id)
        client.close()

    def __handle_client(self, client: socket.socket, client_id: int) -> None:
        """Lida com as requisições do cliente

        Args:
            client (socket.socket): Socket do cliente
            client_id (int): ID do cliente
        """

        client.send(str.encode(str(client_id)))  # Send client id

        while client_id in self.__clients.keys():
            try:
                # TODO: Handle client requests
                # data = client.recv(4096).decode()
                # match data.split(" "):
                #     case ["restart"]:
                #         self.__match.restart()
                #     case ["play", card]:
                #         self.__match.play(client_id, card)
                #     case ["get"]:
                #         pass
                #     case _:
                #         break

                client.send(pickle.dumps(self.__match))  # Envia a partida atualizada para o cliente
            except Exception as e:
                print(e)
                break

        print(f"Client {client_id} disconnected")
        self.__remove_client(client_id)

        if len(self.__clients) == 0:
            self.__match.restart()
