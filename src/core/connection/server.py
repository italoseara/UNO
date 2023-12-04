import socket
import pickle
import threading
from typing import Any

from core.game.match import Match


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
        self.__server.settimeout(1)  # Evita que o servidor fique preso no accept
        self.__server.listen(4)
        self.__running = True
        print(f"[Server] Server is running on port {self.__port}")

        while self.__running:
            try:
                client, address = self.__server.accept()
                self.__add_client(client)
            except KeyboardInterrupt:
                self.stop()
            except OSError:  # Timeout
                pass

    def stop(self):
        """Para o servidor"""

        print("[Server] Stopping server...")
        self.__running = False
        self.__server.close()

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

        nickname = self.__match.remove_player(client_id)
        if nickname is not None:
            print(f"[Server] {nickname} left the match")

    def __handle_client(self, client: socket.socket, client_id: int) -> None:
        """Lida com as requisições do cliente

        Args:
            client (socket.socket): Socket do cliente
            client_id (int): ID do cliente
        """

        client.send(str.encode(str(client_id)))  # Envia o id do cliente quando ele se conecta pela primeira vez

        while client_id in self.__clients.keys():
            try:
                data: dict[str, Any] = pickle.loads(client.recv(1024))

                match data["type"].upper():
                    case "GET":
                        # Não faz nada, já que a partida é enviada no final do loop
                        pass
                    case "JOIN":
                        if self.__match.is_full():
                            print(f"[Server] {data['nickname']} tried joining the match")
                            client.send(pickle.dumps("full"))
                            break  # Sai do loop

                        print(f"[Server] {data['nickname']} joined the match")
                        self.__match.add_player(client_id, data["nickname"])
                    case "START":
                        if client_id == 0:  # Apenas o host pode iniciar a partida
                            self.__match.start()
                    case "PLAY":
                        if self.__match.turn == client_id:
                            self.__match.play(client_id, data["index"])
                    case "DRAW":
                        if self.__match.turn == client_id and self.__match.can_draw(client_id):
                            self.__match.draw(client_id)
                    case _:
                        print(f"[Server] Unknown request: {data['type']}")
                        break

                client.send(pickle.dumps(self.__match))  # Envia a partida atualizada para o cliente
            except Exception:
                break

        self.__remove_client(client_id)
