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
            id: imageBox
            width: 480
            height: sessionData.imageHeight
            color: "black"
            anchors.verticalCenter: parent.verticalCenter

            Image {
                source: sessionData.imageSource
                anchors.fill: parent
            }
        }

        Rectangle {
            width: 480
            height: 120
            color: "black"
            anchors.top: imageBox.bottom

            Text {
                color: "white"
                text: sessionData.headerText
                font.pointSize: 20
                anchors.fill: parent
                horizontalAlignment: Text.AlignHCenter
                verticalAlignment: Text.AlignVCenter
                wrapMode: Text.WordWrap
            }
        }
    }
}
