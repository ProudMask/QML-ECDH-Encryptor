import sys
import os

from PySide2.QtCore import QObject, QUrl, Property, Slot, QCoreApplication
from PySide2.QtGui import QGuiApplication
from PySide2.QtQml import QQmlApplicationEngine
from PySide2.QtNetwork import QSslSocket, QSsl, QSslKey, QSslCertificate, 
QAbstractSocket

from cryptography.hazmat.primitives.asymmetric.ec import 
EllipticCurvePublicKey, EllipticCurvePrivateKey, ECDH
from cryptography.hazmat.primitives.serialization import 
load_pem_private_key, load_pem_public_key, PublicFormat
from cryptography.hazmat.primitives import serialization, hashes

class ECDHKeyExchange(QObject):
    def __init__(self):
        super().__init__()

        # Generate our private key
        self.private_key = EllipticCurvePrivate.generate()

        # Serialize our public key and expose it as a property
        self.public_key = self.private_key.public_key()
        self.serialized_public_key = self.public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        ).decode('utf-8')
    
    @Slot(str, result=str)
    def derive_shared_secret(self, other_party_public_key_str):
        # Deserialize the other party's public key
        other_party_public_key = load_pem_public_key(
            bytes(other_party_public_key_str, 'utf-8'),
            backend=default_backend()
        )

        # Perform ECDH key agreement to derive the shared secret
        shared_secret = self.private_key.exchange(
            ECDH(),
            other_party_public_key
        )

        # Hash the shared secret to derive the final key
        key = hashes.Hash(hashes.SHA256(), backend=default_backend())
        key.update(shared_secret)
        final_key = key.finalize()

        # Serialize the final key and return it
        return final_key.hex()

if __name__ == '__main__':
    # Initialize the Qt application
    app = QGuiApplication(sys.argv)

    # Register the ECDHKeyExchange class as a QML type
    engine = QQmlApplicationEngine()
    qml_file = os.path.join(os.path.dirname(__file__), 'main.qml')
    engine.load(QUrl.fromLocalFile(qml_file))
    qml_root_object = engine.rootObjects()[0]
    engine.rootContext().setContextProperty('ECDHKeyExchange', 
ECDHKeyExchange())

    # Enable SSL support in the Qt network module
    QSslSocket.setDefaultProtocol(QSsl.TlsV1_2)

    # Start the Qt event loop
    sys.exit(app.exec_())
