import queue
import socket
import threading

class NetworkManager:
    def __init__(self, port: int = 9000, timeout: float = 3.0):
        self.port = port
        self.timeout = timeout
        self.is_host = False
        self.socket = None
        self.inbound = queue.Queue()
        self.status_cb = None
        self.listener = any

    def start_connection(self, target_ip: str, status_cb):
        self.status_cb = status_cb
        self.target_ip = target_ip
        connect_worker = threading.Thread(
            target=self.connection_worker,
            args=(target_ip, status_cb),
            daemon=True
        )

        connect_worker.start()

    def connection_worker(self, target_ip: str, status_cb):
        status_cb("Attempting to connect to peer...")

        client_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_sock.settimeout(self.timeout)

        try:
            client_sock.connect((target_ip, self.port))
            client_sock.settimeout(None)
            self.socket = client_sock
            self.is_host = False
            self.listener = threading.Thread(target=self.listener_worker, daemon=True)
            self.listener.start()
            status_cb(f"Connected to host at {target_ip}.")
            return

        except (socket.timeout, ConnectionRefusedError, OSError) as e:
            client_sock.close()
            status_cb("No host found. Switching to host mode...")

        # Hosting fallback
        try:
            server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            server_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            server_sock.bind(("0.0.0.0", self.port))
            server_sock.listen(1)

            status_cb(f"Hosting on port {self.port}. Waiting for connection...")

            # Wait for incoming
            conn, addr = server_sock.accept()
            self.socket = conn
            self.is_host = True
            self.listener = threading.Thread(target=self.listener_worker, daemon=True)
            self.listener.start()
            status_cb(f"Peer connected from {addr[0]}")
        
        except Exception as e:
            status_cb(f"Failed to start as host: {e}")

    def listener_worker(self):
        while self.socket:
            try:
                data = self.socket.recv(1024)
                if not data:
                    break

                self.inbound.put(data.decode())

            except Exception:
                break

    def send_message(self, message: str):
        if not self.socket:
            return

        try:
            self.socket.sendall(message.encode())
        except Exception:
            self.handle_disconnect()

    def get_queued_messages(self) -> list:
        messages = []
        while not self.inbound.qsize() == 0:
            try:
                messages.append(self.inbound.get_nowait())
            except queue.Empty:
                continue

        return messages
    
