"""P-256 key agreement for a local educational fingerprint comparison."""
import hashlib
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives.kdf.hkdf import HKDF


class KeyAgreement:
    def __init__(self):
        self._private = ec.generate_private_key(ec.SECP256R1())

    @property
    def public_pem(self):
        return self._private.public_key().public_bytes(serialization.Encoding.PEM, serialization.PublicFormat.SubjectPublicKeyInfo).decode('ascii')

    def derive_key(self, peer_pem):
        if not isinstance(peer_pem, str) or not peer_pem.strip() or len(peer_pem) > 4096:
            raise ValueError('Paste a P-256 public key in PEM format (up to 4096 characters)')
        try:
            peer = serialization.load_pem_public_key(peer_pem.strip().encode('ascii'))
        except (ValueError, UnicodeError) as exc:
            raise ValueError('Invalid public-key PEM') from exc
        if not isinstance(peer, ec.EllipticCurvePublicKey) or not isinstance(peer.curve, ec.SECP256R1):
            raise ValueError('Only P-256 elliptic-curve public keys are supported')
        own_bytes = self._private.public_key().public_bytes(serialization.Encoding.DER, serialization.PublicFormat.SubjectPublicKeyInfo)
        peer_bytes = peer.public_bytes(serialization.Encoding.DER, serialization.PublicFormat.SubjectPublicKeyInfo)
        if own_bytes == peer_bytes:
            raise ValueError('Use the other participant\'s public key, not your own')
        transcript = b''.join(sorted([own_bytes, peer_bytes]))
        salt = hashlib.sha256(transcript).digest()
        shared = self._private.exchange(ec.ECDH(), peer)
        return HKDF(algorithm=hashes.SHA256(), length=32, salt=salt, info=b'qml-ecdh-demo-v1').derive(shared)

    def fingerprint(self, peer_pem):
        return hashlib.sha256(self.derive_key(peer_pem)).hexdigest()


def self_test():
    alice, bob = KeyAgreement(), KeyAgreement()
    return alice.fingerprint(bob.public_pem) == bob.fingerprint(alice.public_pem)
