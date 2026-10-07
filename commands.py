from network import NetworkManager

class CommandParser:
    def __init__(self, net_manager: NetworkManager, status_callback=None):
        self.status_callback = status_callback if status_callback is not None else print
        self.net_manager = net_manager
        self.commands = {
            "/connect": self._cmd_connect,
            "/disconnect": self._cmd_disconnect,
            "/status": self._cmd_status,
            "/help": self._cmd_help
        }

    def process(self, user_input: str):
        if not user_input:
            return
        formatted = user_input.strip()

        if formatted.startswith('/'):
            parts = formatted.split(' ', 1)
            command = parts[0].lower()
            args = parts[1] if len(parts) > 1 else ""

            command_function = self.commands.get(command)
            if command_function:
                return command_function(args)
                
        
        self._handle_message(user_input)

    def _handle_message(self, text: str):
        self.net_manager.send_message(text)
        

    def _cmd_connect(self, args: str):
        self.net_manager.connect(args)
        

    def _cmd_disconnect(self, args: str):
        self.net_manager.disconnect()
        

    def _cmd_status(self, args: str):
        # This will get current connection status
        self.net_manager._status(f'''Connection status: {'Connected' if self.net_manager.conn else 'Disconnected'} 
                       Peer: {self.net_manager.addr[0] if self.net_manager.addr else 'N/A'}''')

    def _cmd_help(self, args: str):
        help_text = "Available commands:\n"
        for cmd in self.commands.keys():
            help_text += f"{cmd}\n"
        self.status_callback(help_text)


    