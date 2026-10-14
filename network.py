import socket
import threading
from PySide6.QtCore import QObject, Signal

class NetworkManager(QObject):
    messageReceived = Signal(str)

    def __init__(self, status_callback=None):
        super().__init__()
        self.port = 9000
        self.status_callback = status_callback if status_callback is not None else print
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.conn, self.addr = None, None
        # This needs to initialize all the class variables needed to supply a
        # easy-to-use network manager without hanging

    def _status(self, message: str):
        self.status_callback(message)

    def send_message(self, message: str):
        if self.conn is None:
            self._status("No connection established. Connect first with: \'/connect\'")
            return False
        
        self.conn.sendall((message + "\n").encode())
        return True

    def connect(self, target_ip: str):
        self._status(f"Trying to connect to {target_ip}:{self.port}")
        
        try:
            self._client(target_ip)
            self._status(f"Connected to {target_ip}:{self.port}")
        except Exception as e:
            self._status(f"Couldn't connect to host: {e}. Falling back to host...")
            self._host()      

    def disconnect(self):
        connection = self.conn
        self.conn = None
        if connection is not None:
            connection.close()
        if self.socket is not connection:
            self.socket.close()
        self._status("Closed network connection")

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
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.socket.settimeout(5.0)
            self.socket.connect((target_ip, self.port))
            self.socket.settimeout(None)
            self.conn = self.socket
            self.addr = (target_ip, self.port)
            listener = threading.Thread(target=self.__receive_worker, args=(self.conn, self.addr), daemon=True)
            listener.start()
            return
        except Exception:
            raise
        

    def __listen_worker(self):
        while True:
            try:
                connection, address = self.socket.accept()
            except OSError:
                return

            self.conn, self.addr = connection, address
            self.__receive_worker(connection, address)

    def __receive_worker(self, connection, address):
        buffer = bytearray()

        while True:
            try:
                data = connection.recv(4096)
                if not data:
                    break

                buffer.extend(data)
                while b"\n" in buffer:
                    raw_msg, _, remainder = buffer.partition(b"\n")
                    buffer = bytearray(remainder)

                    if raw_msg.endswith(b"\r"):
                        raw_msg = raw_msg[:-1]

                    self.messageReceived.emit(raw_msg.decode())
            except Exception:
                break

        if self.conn is connection:
            self.conn = None
        self._status(f"Client: {address[0]} disconnected.")

    def __del__(self):
        self.disconnect()
        self.socket.close()
        self.conn.close()