import os
os.environ.setdefault('QT_QPA_PLATFORM', 'offscreen')
os.environ.setdefault('QT_QUICK_BACKEND', 'software')
from pathlib import Path
import unittest
from PySide6.QtCore import QObject, QUrl, QMetaObject
from PySide6.QtGui import QGuiApplication
from PySide6.QtQml import QQmlApplicationEngine
from key_agreement import KeyAgreement
from main import make_backend


class QMLTests(unittest.TestCase):
    def test_qml_load_and_python_slot(self):
        app = QGuiApplication.instance() or QGuiApplication([])
        backend = make_backend()
        engine = QQmlApplicationEngine()
        engine.rootContext().setContextProperty('backend', backend)
        engine.load(QUrl.fromLocalFile(str(Path(__file__).resolve().parents[1] / 'main.qml')))
        self.assertEqual(len(engine.rootObjects()), 1)
        root = engine.rootObjects()[0]
        peer = KeyAgreement()
        root.findChild(QObject, 'peerKey').setProperty('text', peer.public_pem)
        self.assertTrue(QMetaObject.invokeMethod(root, 'derive'))
        app.processEvents()
        result = root.findChild(QObject, 'result').property('text')
        self.assertEqual(result, 'Derived-key fingerprint: ' + peer.fingerprint(backend.publicKey))
        self.assertTrue(backend.deriveFingerprint('invalid').startswith('Error:'))
        root.close()
        engine.deleteLater()
        app.processEvents()


if __name__ == '__main__':
    unittest.main()
