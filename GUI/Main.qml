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
        spacing: 1

        // Top chat log area
        Rectangle {     
            Layout.fillWidth: true
            Layout.fillHeight: true
            border.width: 1
            border.color: "blue"

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
                        color: row.kind === "outgoing" ? "#218aff"
                             : row.kind === "system" ? "#e8e8e8"
                             : "#aeb9cc"

                        anchors.horizontalCenter: row.kind === "system" ? parent.horizontalCenter : undefined
                        anchors.right: row.kind === "outgoing" ? parent.right : undefined
                        anchors.left: row.kind === "incoming" ? parent.left : undefined

                        // Text inside bubble
                        TextEdit {
                            id: label
                            color: row.kind === "system" ? "black": "white"
                            font.pointSize: row.kind === "system" ? 8 : 14
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

        // Bottom Input Area
        Rectangle {
            border.width: 1
            border.color: "red"
            Layout.fillWidth: true
            Layout.alignment: Qt.AlignBottom
            Layout.minimumHeight: 45

            RowLayout {
                anchors.fill: parent
                anchors.margins: 6
                spacing: 6

                TextField {
                    id: inputField
                    Layout.fillWidth: true
                    placeholderText: "Enter a command/message..."
                    onAccepted: send()

                    function send() {
                        const message = inputField.text.trim()
                        if (message === "") return

                        chatController.processMessage(message)
                        inputField.text = ""
                    }

                    Keys.onPressed: (event) => {
                        if (event.key == Qt.Key_Return) {
                            send()
                        }
                    }
                }

                Button {
                    Layout.minimumWidth: 75
                    text: "Send"
                    onClicked: inputField.send()
                }
            }
        }
    }
}