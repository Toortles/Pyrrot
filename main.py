# main.py
import sys
from pathlib import Path
from PySide6.QtCore import QUrl
from PySide6.QtGui import QGuiApplication
from PySide6.QtQml import QQmlApplicationEngine

from chatModel import ChatModel
from ChatController import ChatController

app = QGuiApplication(sys.argv)
engine = QQmlApplicationEngine()

chat_model = ChatModel()
controller = ChatController(chat_model)
engine.rootContext().setContextProperty("chatController", controller)
engine.rootContext().setContextProperty("chatModel", chat_model)

engine.load(QUrl.fromLocalFile(str(Path(__file__).parent / "GUI/Main.qml")))
if not engine.rootObjects():
    sys.exit(-1)

sys.exit(app.exec())