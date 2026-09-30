import socket
import threading

class NetworkManager():
    def __init__(self, status_callback=None):
        self.port = 9000
        self.status_callback = status_callback if status_callback is not None else print
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.conn, self.addr = None, None
        # This needs to initialize all the class variables needed to supply a
        # easy-to-use network manager without hanging

    def _status(self, message: str):
        self.status_callback(message)

    def send_message(self, message: str):
        self.socket.sendall(message.encode())

    def connect(self, target_ip: str):
        self._status(f"Trying to connect to {target_ip}:{self.port}")
        try:
            self._client(target_ip)
            self._status(f"Connected to {target_ip}:{self.port}")
        except Exception as e:
            self._status(f"Couldn't connect to host: {e}.\nFalling back to host...")
            self._host()
            

    def disconnect(self):
        self.socket.close()
        self._status("Disconnected from network.")

    def _host(self):
        self.socket.close()
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.socket.bind(("0.0.0.0", self.port))
        self.socket.listen(5)

        listener = threading.Thread(target=self.__listen_worker, daemon=True)
        listener.start()

        self._status(f"Listening on port {self.port}")

    def _client(self, target_ip: str):
        try:
            self.socket.settimeout(5.0)
            self.socket.connect((target_ip, self.port))
            return
        except Exception:
            raise
        

    def __listen_worker(self):
        while True:
            self.conn, self.addr = self.socket.accept()
            try:
                data = self.conn.recv(1024)

                if not data:
                    self._status(f"{self.addr[0]} disconnected.")
                    self.disconnect()
                    break

                self._status(f"{self.addr[0]}: {data.decode()}")
            except Exception:
                break

        self._status(f"Client: {self.addr[0]} disconnected.")