import QtQuick
import QtQuick.Controls.Imagine
import QtQuick.Layouts

Window {
    width: 1280
    height: 800
    visible: true
    title: "Pyrrot - Qt"


    ColumnLayout {
        anchors.fill: parent
        spacing: 0

        // Chat log area
        Rectangle {
            Layout.fillWidth: true
            Layout.fillHeight: true
            color: "#1e1e1e"

            ListView {
                id: chatView
                anchors.fill: parent
                anchors.margins: 6
                clip: true
                spacing: 6
                boundsBehavior: Flickable.StopAtBounds
                ScrollBar.vertical: ScrollBar {}

                model: chatModel

                delegate: Item {
                    id: row
                    required property string message
                    required property string kind

                    width: ListView.view.width
                    height: bubble.height

                    TextMetrics {
                        id: metrics
                        font: label.font
                        text: row.message
                    }

                    Rectangle {
                        id: bubble
                        readonly property real pad: 10
                        readonly property real maxWidth: row.width * 0.7

                        // Shrink to fit short messages
                        width: Math.min(metrics.advanceWidth, maxWidth - 2 * pad) + 2 * pad
                        height: label.implicitHeight + 2 * pad
                        radius: 8
                        color: row.kind === "outgoing" ? "#218aff" : row.kind === "system" ? "#1e1e1e" : "#aeb9cc"

                        anchors.horizontalCenter: row.kind === "system" ? parent.horizontalCenter : undefined
                        anchors.right: row.kind === "outgoing" ? parent.right : undefined
                        anchors.left: row.kind === "incoming" ? parent.left : undefined

                        // Text inside bubble
                        TextEdit {
                            id: label
                            color: row.kind === "system" ? "grey" : "white"
                            font.pointSize: row.kind === "system" ? 10 : 14
                            x: bubble.pad
                            y: bubble.pad
                            width: bubble.width - 2 * bubble.pad
                            text: row.message
                            wrapMode: TextEdit.Wrap
                            readOnly: true
                            selectByMouse: true
                        }
                    }
                }

                onCountChanged: Qt.callLater(positionViewAtEnd)
            }
        }

        // Seperator
        Rectangle {
            Layout.fillWidth: true
            height: 1
            color: "#444444"
        }

        // Bottom Input Area
        Rectangle {
            Layout.fillWidth: true
            Layout.alignment: Qt.AlignBottom
            Layout.minimumHeight: 45
            color: "#1e1e1e"

            RowLayout {
                anchors.fill: parent
                anchors.margins: 6
                spacing: 4

                TextField {
                    id: inputField
                    Layout.fillWidth: true
                    color: "#EEEEEE"
                    padding: 8
                    placeholderText: "Enter a command/message..."
                    placeholderTextColor: "#cccccc"
                    
                    background: Rectangle {
                        color: "#2e2e2e"
                        border.color: "#444444"
                        border.width: 1
                        topLeftRadius: 10
                        bottomLeftRadius: 10
                        topRightRadius: 4
                        bottomRightRadius: 4
                    }

                    onAccepted: send()
                    function send() {
                        const message = inputField.text.trim();
                        if (message === "")
                            return;
                        chatController.processMessage(message);
                        inputField.text = "";
                    }

                    Keys.onPressed: event => {
                        if (event.key == Qt.Key_Return) {
                            send();
                        }
                    }
                }

                Button {
                    Layout.minimumWidth: 75
                    text: "<font color='#eeeeee'>Send</font>"
                    padding: 8

                    background: Rectangle {
                        color: "#2e2e2e"
                        border.color: "#444444"
                        border.width: 1
                        topRightRadius: 10
                        bottomRightRadius: 10
                        topLeftRadius: 4
                        bottomLeftRadius: 4
                    }

                    onClicked: inputField.send()
                }
            }
        }
    }
}
