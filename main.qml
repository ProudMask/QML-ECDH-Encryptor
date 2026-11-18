import QtQuick
import QtQuick.Controls
import QtQuick.Layouts

ApplicationWindow {
    id: window
    visible: true
    width: 720
    height: 650
    title: "ECDH Key Agreement Demo"
    function derive() { result.text = backend.deriveFingerprint(peer.text) }
    ScrollView {
        anchors.fill: parent
        contentWidth: availableWidth
        ColumnLayout {
            width: parent.width
            spacing: 14
            Label { text: "P-256 key agreement"; font.pixelSize: 26; Layout.margins: 12 }
            Label { text: "Open two instances. Exchange public keys, then compare the derived-key fingerprints."; wrapMode: Text.WordWrap; Layout.fillWidth: true; Layout.margins: 12 }
            Label { text: "Your public key (copy this to the other instance)"; Layout.leftMargin: 12 }
            TextArea { objectName: "publicKey"; text: backend ? backend.publicKey : ""; readOnly: true; selectByMouse: true; textFormat: TextEdit.PlainText; font.family: "monospace"; Layout.fillWidth: true; Layout.margins: 12 }
            Label { text: "Other participant's public key"; Layout.leftMargin: 12 }
            TextArea { id: peer; objectName: "peerKey"; placeholderText: "Paste the complete BEGIN PUBLIC KEY PEM block"; selectByMouse: true; textFormat: TextEdit.PlainText; wrapMode: TextEdit.WrapAnywhere; Layout.fillWidth: true; Layout.preferredHeight: 130; Layout.margins: 12; onTextChanged: result.text = "" }
            Button { text: "Derive fingerprint"; enabled: peer.text.trim().length > 0; onClicked: window.derive(); Layout.leftMargin: 12 }
            Label { id: result; objectName: "result"; textFormat: Text.PlainText; wrapMode: Text.WrapAnywhere; Layout.fillWidth: true; Layout.margins: 12 }
            Label { text: "Local learning demo only. Fingerprint agreement does not authenticate identity. No messages are encrypted."; wrapMode: Text.WordWrap; Layout.fillWidth: true; Layout.margins: 12 }
        }
    }
}
