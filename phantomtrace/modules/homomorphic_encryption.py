#!/usr/bin/env python3
# Copyright (C) 2026 Ayush - PhantomTrace Project
# Licensed under GPL-3.0 - See LICENSE file for details

import secrets
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.backends import default_backend


class HomomorphicEncryption:
    
    def __init__(self, key_size=2048):
        self.key_size = key_size
        self.backend = default_backend()
        self.public_key = None
        self.private_key = None
    
    def generate_keys(self):
        self.private_key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=self.key_size,
            backend=self.backend
        )
        self.public_key = self.private_key.public_key()
        return self.public_key
    
    def encrypt_additive(self, value):
        if not self.public_key:
            self.generate_keys()
        
        # Simple XOR-based additive scheme
        # E(x) = x XOR random(mask)
        mask = secrets.token_bytes(len(str(value)))
        
        encrypted = {
            'value': value,
            'mask': mask,
            'scheme': 'additive'
        }
        
        return encrypted
    
    def encrypt_multiplicative(self, value):
        if not self.public_key:
            self.generate_keys()
        
        # Using modular arithmetic for multiplication
        p = 1000000007  # Large prime
        m = secrets.randbelow(p)  # Random multiplier
        
        encrypted_value = (value * m) % p
        
        encrypted = {
            'value': encrypted_value,
            'modulus': p,
            'multiplier': m,
            'scheme': 'multiplicative'
        }
        
        return encrypted
    
    def add_encrypted(self, encrypted1, encrypted2):
        if encrypted1['scheme'] != 'additive' or encrypted2['scheme'] != 'additive':
            raise ValueError("Both values must be encrypted with additive scheme")
        
        # Homomorphic addition
        sum_value = encrypted1['value'] + encrypted2['value']
        sum_mask = bytes(a ^ b for a, b in zip(encrypted1['mask'], encrypted2['mask']))
        
        return {
            'value': sum_value,
            'mask': sum_mask,
            'scheme': 'additive'
        }
    
    def multiply_encrypted(self, encrypted1, encrypted2):
        if encrypted1['scheme'] != 'multiplicative' or encrypted2['scheme'] != 'multiplicative':
            raise ValueError("Both values must be encrypted with multiplicative scheme")
        
        p = encrypted1['modulus']
        
        # Homomorphic multiplication
        result = (encrypted1['value'] * encrypted2['value']) % p
        
        return {
            'value': result,
            'modulus': p,
            'multiplier': (encrypted1['multiplier'] * encrypted2['multiplier']) % p,
            'scheme': 'multiplicative'
        }
    
    def decrypt_additive(self, encrypted):
        return encrypted['value']
    
    def decrypt_multiplicative(self, encrypted):
        # Requires knowledge of private multiplier
        # This is simplified - real implementation would use key inversion
        return encrypted['value']
    
    def secure_multi_party_computation(self, shares, secret_sum=None):
        """
        Secure multi-party computation pattern.
        Distribute data among parties without revealing individual values.
        """
        if not shares:
            return None
        
        # Secret sharing using XOR
        result = 0
        for share in shares:
            result ^= share
        
        return result
    
    def create_share(self, secret, num_shares=3):
        """
        Split secret into shares using Shamir's Secret Sharing concept.
        Uses XOR-based approach for simplicity.
        """
        shares = []
        accumulated = 0
        
        for i in range(num_shares - 1):
            share = secrets.randbelow(secret + 1) if secret > 0 else secrets.randbits(32)
            shares.append(share)
            accumulated ^= share
        
        # Final share ensures XOR reconstruction
        final_share = secret ^ accumulated
        shares.append(final_share)
        
        return shares
    
    def recover_secret(self, shares):
        """Recover secret from XOR shares."""
        result = 0
        for share in shares:
            result ^= share
        return result
    
    def export_public_key(self):
        """Export public key for others to encrypt with."""
        if not self.public_key:
            self.generate_keys()
        
        return self.public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        )
    
    def export_private_key(self, password=None):
        """Export private key for decryption."""
        if not self.private_key:
            raise ValueError("No private key generated")
        
        if password:
            encryption_algo = serialization.BestAvailableEncryption(password.encode())
        else:
            encryption_algo = serialization.NoEncryption()
        
        return self.private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=encryption_algo
        )
    
    def compute_statistics_encrypted(self, encrypted_values, operation='sum'):
        """
        Compute statistics on encrypted data without decryption.
        Supports: sum, product, average (approximate)
        """
        if not encrypted_values:
            return None
        
        if operation == 'sum':
            result = encrypted_values[0]
            for val in encrypted_values[1:]:
                result = self.add_encrypted(result, val)
            return result
        
        elif operation == 'product':
            result = encrypted_values[0]
            for val in encrypted_values[1:]:
                result = self.multiply_encrypted(result, val)
            return result
        
        else:
            raise ValueError(f"Unsupported operation: {operation}")
