import sys
import socket
import pickle
import threading

from core.match import Match


class Server:
    host: str
    port: int
    running: bool

    clients: dict[int, socket.socket]
    server: socket.socket | None

    match: Match

    def __init__(self, host: str, port: int):
        self.host = host
        self.port = port
        self.running = False

        self.clients = {}
        self.server = None

        self.match = Match()

    def start(self):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind((self.host, self.port))
        self.server.listen(4)
        self.running = True
        print(f"Server is running on port {self.port}")

        while self.running:
            try:
                client, address = self.server.accept()
                if self.match.ready:
                    client.close()
                    continue

                if len(self.clients) == 4:
                    self.match.ready = True

                print(f"Client connected from {address[0]}:{address[1]}")
                self.add_client(client)
            except KeyboardInterrupt:
                self.stop()

    def stop(self):
        print("Stopping server...")
        self.running = False
        self.server.close()
        sys.exit()

    def add_client(self, client: socket.socket):
        client_id = 0
        while client_id in self.clients.keys():
            client_id += 1

        self.clients[client_id] = client

        # Start client thread
        client_thread = threading.Thread(target=self.handle_client, args=(client, client_id))
        client_thread.start()

    def remove_client(self, client_id: int):
        client = self.clients.pop(client_id)
        client.close()

    def handle_client(self, client: socket.socket, client_id: int):
        client.send(str.encode(str(client_id)))  # Send client id

        while client_id in self.clients.keys():
            try:
                data = client.recv(4096).decode()
                match data.split(" "):
                    case ["restart"]:
                        self.match.restart()
                    case ["play", card]:
                        self.match.play(client_id, card)
                    case ["get"]:
                        pass
                    case _:
                        break

                client.send(pickle.dumps(self.match))
            except Exception as e:
                print(e)
                break

        print(f"Client {client_id} disconnected")
        self.remove_client(client_id)

        if len(self.clients) == 0:
            self.match.restart()


if __name__ == "__main__":
    server = Server("localhost", 5555)
    server.start()
