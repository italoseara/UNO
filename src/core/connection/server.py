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
        self.__host = host
        self.__port = port
        self.__running = False

        self.__clients = {}
        self.__server = None

        self.__match = Match()

    def start(self):
        self.__server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.__server.bind((self.__host, self.__port))
        self.__server.settimeout(1)  # Evita que o servidor fique preso no accept
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
                self.add_client(client)
            except KeyboardInterrupt:
                self.stop()
            except OSError:  # Timeout
                pass

    def stop(self):
        print("Stopping server...")
        self.__running = False
        self.__server.close()

    def add_client(self, client: socket.socket):
        client_id = 0
        while client_id in self.__clients.keys():
            client_id += 1

        self.__clients[client_id] = client

        # Start client thread
        client_thread = threading.Thread(target=self.handle_client, args=(client, client_id))
        client_thread.start()

    def remove_client(self, client_id: int):
        client = self.__clients.pop(client_id)
        client.close()

    def handle_client(self, client: socket.socket, client_id: int):
        client.send(str.encode(str(client_id)))  # Send client id

        while client_id in self.__clients.keys():
            try:
                data = client.recv(4096).decode()
                match data.split(" "):
                    case ["restart"]:
                        self.__match.restart()
                    case ["play", card]:
                        self.__match.play(client_id, card)
                    case ["get"]:
                        pass
                    case _:
                        break

                client.send(pickle.dumps(self.__match))
            except Exception as e:
                print(e)
                break

        print(f"Client {client_id} disconnected")
        self.remove_client(client_id)

        if len(self.__clients) == 0:
            self.__match.restart()


if __name__ == "__main__":
    server = Server("localhost", 5555)
    server.start()
