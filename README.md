# QML ECDH Key Agreement Demo

A Qt Quick interface for a local P-256 key-agreement experiment. Each instance creates a fresh private key, exposes only its public PEM, and displays a SHA-256 fingerprint of the derived key after receiving the peer's public key. The historical repository name is retained, but no message encryption is implemented.

## Run

Python 3.10 or later on a system supported by the dependency versions:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python main.py --self-test
python main.py
```

Open a second instance in another terminal. Copy the complete public-key PEM from each window into the other window's peer field. Click Derive fingerprint in both; the fingerprints should match. Restarting an instance generates a new private key and invalidates the previous comparison. Nothing is saved or transmitted automatically.

The self-test prints only a PASS/FAIL result and does not need a display or Qt imports. The desktop interface requires Qt platform libraries and a graphical session. The `PySide6-Essentials` package supplies the Qt Core/Gui/Qml/Quick modules used here.

## Method and fixes

The Python backend is retained and registered before QML loading. Public PEM is exposed as a Qt property, multiline peer input is supported, and root-object creation is checked before starting the event loop. This replaces broken imports and nonexistent key-generation calls in the PySide2 prototype.

ECDH shared bytes pass through HKDF-SHA256. The salt is SHA-256 of both public keys' DER encodings sorted lexicographically, so both participants use the same public context. The fixed HKDF info identifies this demo version. The UI shows only a SHA-256 fingerprint of the derived 32-byte key, never the raw shared secret or derived key.

Invalid, oversized, wrong-curve, non-EC, and own-key inputs are rejected. The unused Qt SSL configuration is removed because this program makes no network connection; setting a TLS default would not authenticate a manually pasted ECDH key.

## Verify

```bash
python -m unittest discover -s tests -v
```

Core tests cover independent agreement, malformed/unsupported keys, own-key rejection, self-test behavior, and import without launching Qt. The QML smoke check loads the UI with an offscreen Qt backend and invokes the Python slot using a second instance's public key; see tests/test_qml.py. On a headless machine, run that check with `QT_QPA_PLATFORM=offscreen QT_QUICK_BACKEND=software`.

## Limitations

Fingerprint equality is a consistency check, not peer authentication. This custom learning demo does not provide a complete protocol, authenticated identities, replay protection, message encryption, persistence, or transport. It is not suitable as a secure messaging product and has not undergone a protocol audit. There is no ML model.

References: [Qt context setup](https://doc.qt.io/qtforpython-6/PySide6/QtQml/QQmlContext.html), [cryptography ECDH](https://cryptography.io/en/stable/hazmat/primitives/asymmetric/ec/), [HKDF](https://cryptography.io/en/stable/hazmat/primitives/key-derivation-functions/#hkdf).
