#!/usr/bin/env python3
# Copyright (C) 2026 Ayush - PhantomTrace Project
# Licensed under GPL-3.0 - See LICENSE file for details

import os
from cryptography.hazmat.primitives.ciphers.aead import AESGCM, ChaCha20Poly1305
from cryptography.hazmat.primitives.kdf.argon2 import Argon2id
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend


class AdvancedEncryption:
    
    def __init__(self):
        self.backend = default_backend()
        self.encrypted_data = {}
    
    def derive_key(self, password, salt=None, length=32):
        if salt is None:
            salt = os.urandom(16)
        
        # Argon2id parameters
        kdf = Argon2id(
            salt=salt,
            length=length,
            iterations=2,
            lanes=1,
            memory_cost=65536,
        )
        
        key = kdf.derive(password.encode())
        return key, salt
    
    def encrypt_aes_gcm(self, data, password, associated_data=None):
        # Derive key from password
        key, salt = self.derive_key(password)
        
        # Generate IV
        iv = os.urandom(12)
        
        # Create cipher
        cipher = AESGCM(key)
        
        # Encrypt
        ciphertext = cipher.encrypt(iv, data, associated_data)
        
        # Return salt + iv + ciphertext
        result = salt + iv + ciphertext
        return result
    
    def decrypt_aes_gcm(self, encrypted_data, password, associated_data=None):
        # Extract components
        salt = encrypted_data[:16]
        iv = encrypted_data[16:28]
        ciphertext = encrypted_data[28:]
        
        # Derive key
        key, _ = self.derive_key(password, salt)
        
        # Create cipher
        cipher = AESGCM(key)
        
        # Decrypt
        plaintext = cipher.decrypt(iv, ciphertext, associated_data)
        return plaintext
    
    def encrypt_chacha20_poly1305(self, data, password, associated_data=None):
        # Derive key
        key, salt = self.derive_key(password)
        
        # Generate nonce
        nonce = os.urandom(12)
        
        # Create cipher
        cipher = ChaCha20Poly1305(key)
        
        # Encrypt
        ciphertext = cipher.encrypt(nonce, data, associated_data)
        
        # Return salt + nonce + ciphertext
        result = salt + nonce + ciphertext
        return result
    
    def decrypt_chacha20_poly1305(self, encrypted_data, password, associated_data=None):
        # Extract components
        salt = encrypted_data[:16]
        nonce = encrypted_data[16:28]
        ciphertext = encrypted_data[28:]
        
        # Derive key
        key, _ = self.derive_key(password, salt)
        
        # Create cipher
        cipher = ChaCha20Poly1305(key)
        
        # Decrypt
        plaintext = cipher.decrypt(nonce, ciphertext, associated_data)
        return plaintext
    
    def create_sealed_box(self, data, public_key):
        from cryptography.hazmat.primitives.asymmetric import ec
        from cryptography.hazmat.primitives import serialization
        
        # Generate ephemeral key pair
        private_key = ec.generate_private_key(ec.SECP256R1(), self.backend)
        
        # DH shared secret
        shared_key = private_key.exchange(ec.ECDH(), public_key)
        
        # Derive encryption key from shared secret
        kdf = Argon2(
            algorithm=hashes.SHA256(),
            length=32,
            salt=b'saltbox',
            time_cost=2,
            memory_cost=65536,
            parallelism=1,
        )
        
        key = kdf.derive(shared_key)
        
        # Encrypt
        cipher = AESGCM(key)
        nonce = os.urandom(12)
        ciphertext = cipher.encrypt(nonce, data, None)
        
        # Return ephemeral public key + nonce + ciphertext
        ephemeral_public = private_key.public_key().public_bytes(
            encoding=serialization.Encoding.X962,
            format=serialization.PublicFormat.UncompressedPoint
        )
        
        return ephemeral_public + nonce + ciphertext
    
    def generate_key_pair(self):
        from cryptography.hazmat.primitives.asymmetric import ec
        from cryptography.hazmat.primitives import serialization
        
        private_key = ec.generate_private_key(ec.SECP256R1(), self.backend)
        public_key = private_key.public_key()
        
        private_pem = private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.NoEncryption()
        )
        
        public_pem = public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        )
        
        return private_pem, public_pem
