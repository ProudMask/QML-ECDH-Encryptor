import subprocess
import sys
import unittest
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import ec, rsa
from key_agreement import KeyAgreement


class AgreementTests(unittest.TestCase):
    def test_independent_agreement(self):
        alice, bob = KeyAgreement(), KeyAgreement()
        self.assertEqual(alice.derive_key(bob.public_pem), bob.derive_key(alice.public_pem))
        self.assertEqual(alice.fingerprint(bob.public_pem), bob.fingerprint(alice.public_pem))

    def test_invalid_input(self):
        participant = KeyAgreement()
        for value in ('', 'bad', 'x' * 4097, 'مرحبا', participant.public_pem):
            with self.assertRaises(ValueError):
                participant.fingerprint(value)

    def test_wrong_key_type(self):
        participant = KeyAgreement()
        for private in (ec.generate_private_key(ec.SECP384R1()), rsa.generate_private_key(public_exponent=65537, key_size=2048)):
            pem = private.public_key().public_bytes(serialization.Encoding.PEM, serialization.PublicFormat.SubjectPublicKeyInfo).decode()
            with self.assertRaises(ValueError):
                participant.fingerprint(pem)

    def test_cli_and_import(self):
        result = subprocess.run([sys.executable, 'main.py', '--self-test'], capture_output=True, text=True, check=True, timeout=10)
        self.assertIn('PASS', result.stdout)
        result = subprocess.run([sys.executable, '-c', "import main, sys; assert 'PySide6' not in sys.modules"], capture_output=True, text=True, timeout=10)
        self.assertEqual(result.returncode, 0)
        self.assertEqual(result.stdout, '')


if __name__ == '__main__':
    unittest.main()
