import socket
import threading

class NetworkManager():
    def __init__(self):
        # This needs to initialize all the class variables needed to supply a
        # easy-to-use network manager without hanging
        print("Created a network manager!")

    def connect(self, target_ip: str, port: int):
        pass
        #This will be included in the client side code but also called from inputted command

    def disconnect(self):
        # This will handle disconnects by closing app or by command
        pass

    def _host(self, port: int):
        # This will handle creating host and accepting connections
        pass

    def _client(self):
        # This will handle client connection if there's a host out there
        pass

    def __listen_worker(self):
        # This will handle listening to other peers
        pass

    def __send_worker(self):
        # Worker on seperate thread to send messages
        pass