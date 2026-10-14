from PySide6.QtCore import QObject, Signal, Slot

from commands import CommandParser
from network import NetworkManager

class ChatController(QObject):
    messageToDisplay = Signal(str, str)

    def __init__(self, chat_model, parent=None):
        super().__init__(parent)
        self.chat_model = chat_model
        self.messageToDisplay.connect(self._appendMessage)

        network = NetworkManager(status_callback=self._show_status)
        network.messageReceived.connect(self._show_incoming)
        self.parser = CommandParser(network, status_callback=self._show_status)

    def _show_status(self, text):
        self.messageToDisplay.emit(text, "system")

    @Slot(str)
    def _show_incoming(self, text):
        self.messageToDisplay.emit(text, "incoming")

    @Slot(str, str)
    def _appendMessage(self, text, kind):
        self.chat_model.addMessage(text, kind)

    @Slot(str)
    def processMessage(self, text):
        if self.parser.process(text):
            self.messageToDisplay.emit(text, "outgoing")