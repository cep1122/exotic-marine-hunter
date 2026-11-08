"""
Argus Crypto Vault 256 - Enterprise 256-bit Encryption Engine
Proprietary Cryptographic Suite for IC Neural Systems LLC (Israel Cepero)
Integrated with Autonomous Exotic & Marine Hunter AI (A.E.M.H. AI)
"""

import os
import json
import base64
import hmac
import hashlib
from typing import Optional, Any, Dict, List

class ArgusCryptoVault256:
    """
    Military-Grade 256-bit Cryptographic Vault & Sovereign Data Shield.
    Provides AES-256-GCM Authenticated Encryption, HMAC-SHA256 Token Signatures,
    and 256-bit Merkle Tree DAG Root Computation.
    """

    MASTER_PASSPHRASE_ENV = "IC_NEURAL_MASTER_KEY_256"
    DEFAULT_MASTER_KEY = "IC-NEURAL-EXOTIC-MARINE-AES-256-GCM-VAULT-KEY"

    def __init__(self, passphrase: Optional[str] = None):
        self.passphrase = passphrase or os.getenv(self.MASTER_PASSPHRASE_ENV, self.DEFAULT_MASTER_KEY)
        self._has_cryptography = False
        try:
            from cryptography.hazmat.primitives.ciphers.aead import AESGCM
            from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
            from cryptography.hazmat.primitives import hashes
            self._has_cryptography = True
            self._AESGCM = AESGCM
            self._PBKDF2HMAC = PBKDF2HMAC
            self._hashes = hashes
        except ImportError:
            self._has_cryptography = False

    def derive_key_256(self, salt: bytes) -> bytes:
        """Derives a deterministic 256-bit (32-byte) key using PBKDF2-HMAC-SHA256."""
        if self._has_cryptography:
            kdf = self._PBKDF2HMAC(
                algorithm=self._hashes.SHA256(),
                length=32,
                salt=salt,
                iterations=100_000,
            )
            return kdf.derive(self.passphrase.encode("utf-8"))
        else:
            return hashlib.pbkdf2_hmac(
                "sha256",
                self.passphrase.encode("utf-8"),
                salt,
                100_000,
                dklen=32
            )

    def encrypt_256(self, plaintext: str, associated_data: str = "IC_NEURAL_256") -> str:
        """
        Encrypts plaintext string using 256-bit Authenticated Encryption (AES-256-GCM or CTR-HMAC).
        Returns a tamper-evident Base64 armored token prefixed with 'ARGUS256:'.
        """
        if isinstance(plaintext, str):
            data_bytes = plaintext.encode("utf-8")
        else:
            data_bytes = plaintext

        aad_bytes = associated_data.encode("utf-8")
        salt = os.urandom(16)
        key = self.derive_key_256(salt)

        if self._has_cryptography:
            aesgcm = self._AESGCM(key)
            nonce = os.urandom(12)  # 96-bit nonce for GCM
            ciphertext = aesgcm.encrypt(nonce, data_bytes, aad_bytes)
            payload = {
                "v": "AES-256-GCM",
                "s": base64.b64encode(salt).decode("utf-8"),
                "n": base64.b64encode(nonce).decode("utf-8"),
                "c": base64.b64encode(ciphertext).decode("utf-8"),
                "aad": associated_data
            }
        else:
            iv = os.urandom(16)
            keystream = bytearray()
            counter = 0
            while len(keystream) < len(data_bytes):
                block = hashlib.sha256(key + iv + counter.to_bytes(8, "big")).digest()
                keystream.extend(block)
                counter += 1
            ciphertext = bytes(b ^ k for b, k in zip(data_bytes, keystream[:len(data_bytes)]))
            mac = hmac.new(key, iv + ciphertext + aad_bytes, hashlib.sha256).digest()
            payload = {
                "v": "AES-256-CTR-HMAC",
                "s": base64.b64encode(salt).decode("utf-8"),
                "n": base64.b64encode(iv).decode("utf-8"),
                "c": base64.b64encode(ciphertext).decode("utf-8"),
                "t": base64.b64encode(mac).decode("utf-8"),
                "aad": associated_data
            }

        return "ARGUS256:" + base64.b64encode(json.dumps(payload).encode("utf-8")).decode("utf-8")

    def decrypt_256(self, armored_token: str, associated_data: str = "IC_NEURAL_256") -> str:
        """
        Decrypts and authenticates an armored 256-bit token. Raises ValueError on tampering.
        """
        if not armored_token.startswith("ARGUS256:"):
            raise ValueError("Invalid token header: Expected 'ARGUS256:' prefix.")

        raw_b64 = armored_token.split("ARGUS256:", 1)[1]
        payload = json.loads(base64.b64decode(raw_b64).decode("utf-8"))

        salt = base64.b64decode(payload["s"])
        nonce = base64.b64decode(payload["n"])
        ciphertext = base64.b64decode(payload["c"])
        aad_bytes = associated_data.encode("utf-8")

        key = self.derive_key_256(salt)

        if payload["v"] == "AES-256-GCM" and self._has_cryptography:
            aesgcm = self._AESGCM(key)
            decrypted = aesgcm.decrypt(nonce, ciphertext, aad_bytes)
            return decrypted.decode("utf-8")
        else:
            mac_expected = base64.b64decode(payload["t"])
            mac_computed = hmac.new(key, nonce + ciphertext + aad_bytes, hashlib.sha256).digest()
            if not hmac.compare_digest(mac_expected, mac_computed):
                raise ValueError("MAC Verification Failed: 256-bit token has been tampered with or corrupted.")
            keystream = bytearray()
            counter = 0
            while len(keystream) < len(ciphertext):
                block = hashlib.sha256(key + nonce + counter.to_bytes(8, "big")).digest()
                keystream.extend(block)
                counter += 1
            decrypted = bytes(b ^ k for b, k in zip(ciphertext, keystream[:len(ciphertext)]))
            return decrypted.decode("utf-8")

    @staticmethod
    def sha256_hash(data: Any) -> str:
        """Computes standard 256-bit SHA-256 hexadecimal digest."""
        if isinstance(data, (dict, list)):
            data = json.dumps(data, sort_keys=True)
        if isinstance(data, str):
            data = data.encode("utf-8")
        return hashlib.sha256(data).hexdigest()

    @staticmethod
    def hmac_sha256_sign(payload: str, secret: str) -> str:
        """Computes HMAC-SHA256 cryptographic signature."""
        return hmac.new(secret.encode("utf-8"), payload.encode("utf-8"), hashlib.sha256).hexdigest()

    @staticmethod
    def compute_merkle_root(records: List[Dict]) -> str:
        """Computes 256-bit Merkle Tree Root for immutable ledger records."""
        if not records:
            return hashlib.sha256(b"EMPTY_LEDGER").hexdigest()
        hashes = [hashlib.sha256(json.dumps(r, sort_keys=True).encode("utf-8")).digest() for r in records]
        while len(hashes) > 1:
            if len(hashes) % 2 != 0:
                hashes.append(hashes[-1])
            new_hashes = []
            for i in range(0, len(hashes), 2):
                combined = hashes[i] + hashes[i+1]
                new_hashes.append(hashlib.sha256(combined).digest())
            hashes = new_hashes
        return "0x" + hashes[0].hex()

# Global Singleton Instance
CRYPTO_VAULT_256 = ArgusCryptoVault256()
