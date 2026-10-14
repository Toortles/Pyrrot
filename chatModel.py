from PySide6.QtCore import QAbstractListModel, QModelIndex, Qt, Slot, QByteArray
from PySide6.QtQml import QmlElement

QML_IMPORT_NAME = "Pyrrot"
QML_IMPORT_MAJOR_VERSION = 1

@QmlElement
class ChatModel(QAbstractListModel):
    MessageRole = Qt.UserRole + 1
    KindRole = Qt.UserRole + 2

    def __init__(self, parent=None):
        super().__init__(parent)
        self._messages = []

    def rowCount(self, parent=QModelIndex()):
        return len(self._messages)

    def data(self, index, role=Qt.DisplayRole):
        if not index.isValid() or not (0 <= index.row() < len(self._messages)):
            return None
        msg = self._messages[index.row()]
        if role == self.MessageRole:
            return msg["messages"]
        if role == self.KindRole:
            return msg["kind"]

        return None

    def roleNames(self):
        return {
            self.MessageRole: QByteArray(b"message"),
            self.KindRole: QByteArray(b"kind"),
        }

    @Slot(str, bool)
    def addMessage(self, text, kind):
        row = len(self._messages)
        self.beginInsertRows(QModelIndex(), row, row)
        self._messages.append({"messages": text, "kind": kind})
        self.endInsertRows()