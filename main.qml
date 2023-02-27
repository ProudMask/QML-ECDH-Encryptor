import QtQuick 2.15
import QtQuick.Controls 2.15

ApplicationWindow {
    title: "ECDH Key Exchange"
    width: 400
    height: 300

    TextField {
        id: other_party_public_key_field
        placeholderText: "Enter other party's public key"
        anchors.centerIn: parent
    }

    Button {
        id: derive_key_button
        text: "Derive Shared Secret"
        anchors.top: other_party_public_key_field.bottom
        anchors.horizontalCenter: 
other_party_public_key_field.horizontalCenter
        onClicked: {
            // Call the Python method to derive the shared secret
            var shared_secret = 
ECDHKeyExchange.derive_shared_secret(other_party_public_key_field.text)

            // Display the shared secret in a label
            shared_secret_label.text = "Shared Secret: " + shared_secret
        }
    }

    Label {
        id: shared_secret_label
        anchors.top: derive_key_button.bottom
        anchors.horizontalCenter: derive_key_button.horizontalCenter
    }
}
