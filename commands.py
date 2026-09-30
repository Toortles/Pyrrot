from network import NetworkManager

class CommandParser:
    def __init__(self, net_manager: NetworkManager):
        print("Created parser!")
        self.net_manager = net_manager
        self.commands = {
            "/connect": self._cmd_connect,
            "/disconnect": self._cmd_disconnect,
            "/status": self._cmd_status
        }

    def process(self, user_input: str):
        user_input = user_input.strip()
        if not user_input:
            return

        if user_input.startswith('/'):
            parts = user_input.split(' ', 1)
            command = parts[0].lower()
            args = parts[1] if len(parts) > 1 else ""

            command_function = self.commands.get(command)
            if command_function:
                return command_function(args)
            else:
                return "Not a command"

        return user_input

    def _handle_message(self, text: str):
        self.net_manager.send_message(text)

    def _cmd_connect(self, args: str):
        self.net_manager.connect(args)
        pass

    def _cmd_disconnect(self, args: str):
        self.net_manager.disconnect()
        pass

    def _cmd_status(self, args: str):
        # This will get current connection status
        print("This is status")
        pass

    