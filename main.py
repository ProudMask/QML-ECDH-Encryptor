"""Launch the QML key-agreement demo or run its headless self-test."""
import argparse
from pathlib import Path
import sys
from key_agreement import KeyAgreement, self_test


def make_backend():
    from PySide6.QtCore import QObject, Property, Slot

    class ECDHBackend(QObject):
        def __init__(self):
            super().__init__()
            self.agreement = KeyAgreement()

        @Property(str, constant=True)
        def publicKey(self):
            return self.agreement.public_pem

        @Slot(str, result=str)
        def deriveFingerprint(self, peer_pem):
            try:
                return 'Derived-key fingerprint: ' + self.agreement.fingerprint(peer_pem)
            except ValueError as exc:
                return 'Error: ' + str(exc)

    return ECDHBackend()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--self-test', action='store_true')
    args = parser.parse_args()
    if args.self_test:
        success = self_test()
        print('Independent key agreement: ' + ('PASS' if success else 'FAIL'))
        return 0 if success else 1
    from PySide6.QtCore import QUrl
    from PySide6.QtGui import QGuiApplication
    from PySide6.QtQml import QQmlApplicationEngine
    app = QGuiApplication(sys.argv[:1])
    backend = make_backend()
    engine = QQmlApplicationEngine()
    # Register before loading QML and retain both Python objects through app.exec().
    engine.rootContext().setContextProperty('backend', backend)
    engine.load(QUrl.fromLocalFile(str(Path(__file__).resolve().with_name('main.qml'))))
    if not engine.rootObjects():
        print('Unable to load main.qml', file=sys.stderr)
        return 1
    return app.exec()


if __name__ == '__main__':
    raise SystemExit(main())
