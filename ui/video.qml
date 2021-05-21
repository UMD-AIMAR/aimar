import QtQuick 2.4
import QtQuick.Controls 2.2
import QtQuick.Layouts 1.4
import QtMultimedia 5.12
import org.kde.kirigami 2.4 as Kirigami
import Mycroft 1.0 as Mycroft

Mycroft.Delegate {
    id: root

    Item {
        anchors.fill: parent

        Rectangle {
            id: videoBox
            width: 480
            height: 270
            anchors.verticalCenter: parent.verticalCenter

            MediaPlayer {
                id: player
                source: sessionData.videoSource
                autoPlay: true
            }

            VideoOutput {
                source: player
                anchors.fill: parent
                focus : visible // to receive focus and capture key events when visible
            }

            Image {
                id: photoPreview
            }
        }

        Rectangle {
            width: 480
            height: 120
            color: "black"
            anchors.top: videoBox.bottom

            Text {
                color: "white"
                text: sessionData.headerText
                font.pointSize: 20
                anchors.fill: parent
                horizontalAlignment: Text.AlignHCenter
                verticalAlignment: Text.AlignVCenter
            }
        }
    }
}
