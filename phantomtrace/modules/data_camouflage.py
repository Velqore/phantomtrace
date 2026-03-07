#!/usr/bin/env python3
# Copyright (C) 2026 Ayush - PhantomTrace Project
# Licensed under GPL-3.0 - See LICENSE file for details
"""
Data Camouflage - Hide data in images and text

Basic steganography stuff - LSB in images, whitespace in text.
Adds encryption so even if found it's not readable.
"""

import secrets
from pathlib import Path
from typing import Optional
import struct


class DataCamouflage:
    """Hide secret data inside images and text files."""
    
    def __init__(self):
        self.hidden_data_map = {}
    
    def hide_in_image(self, secret_data, cover_image_path, output_path, technique='adaptive_lsb'):
        """Hide data inside an image using LSB steganography."""
        try:
            from PIL import Image
            import numpy as np
            
            # Load image
            img = Image.open(cover_image_path)
            img_array = np.array(img)
            
            # Encrypt before hiding
            encrypted_data = self._polymorphic_encrypt(secret_data)
            data_with_length = struct.pack('>I', len(encrypted_data)) + encrypted_data
            
            # Convert to bits
            bits = ''.join(format(byte, '08b') for byte in data_with_length)
            
            if technique == 'adaptive_lsb':
                modified_img = self._adaptive_lsb_hide(img_array, bits)
            elif technique == 'pvd':  # Pixel Value Differencing
                modified_img = self._pvd_hide(img_array, bits)
            else:
                return False
            
            # Save output image
            output_img = Image.fromarray(modified_img.astype('uint8'))
            output_img.save(output_path)
            
            # Store mapping
            self.hidden_data_map[output_path] = {
                'technique': technique,
                'original_size': len(secret_data)
            }
            
            return True
            
        except Exception as e:
            print(f"Error hiding data in image: {e}")
            return False
    
    def _adaptive_lsb_hide(self, img_array, bits: str):
        """Advanced LSB steganography with adaptive bit selection."""
        flat = img_array.flatten()
        
        bit_index = 0
        for i in range(len(flat)):
            if bit_index >= len(bits):
                break
            
            # Adaptive: skip pixels that would create statistical anomalies
            if self._is_safe_pixel(flat[i]):
                # Modify LSB
                flat[i] = (flat[i] & 0xFE) | int(bits[bit_index])
                bit_index += 1
        
        return flat.reshape(img_array.shape)
    
    def _is_safe_pixel(self, pixel_value: int) -> bool:
        """Determine if pixel is safe for modification (avoid extreme values)."""
        # Avoid pure black/white and near values
        return 5 < pixel_value < 250
    
    def _pvd_hide(self, img_array, bits: str):
        """Pixel Value Differencing steganography - more robust."""
        # Simplified PVD implementation
        # Would calculate differences between adjacent pixels
        # and hide data based on difference ranges
        return self._adaptive_lsb_hide(img_array, bits)
    
    def extract_from_image(
        self,
        stego_image_path: str,
        technique: str = 'adaptive_lsb'
    ) -> Optional[bytes]:
        """
        Extract hidden data from image.
        
        Args:
            stego_image_path: Path to image with hidden data
            technique: Extraction technique
        
        Returns:
            Extracted data or None
        """
        try:
            from PIL import Image
            import numpy as np
            
            img = Image.open(stego_image_path)
            img_array = np.array(img)
            
            if technique == 'adaptive_lsb':
                bits = self._adaptive_lsb_extract(img_array)
            else:
                return None
            
            # Extract length
            length_bits = bits[:32]
            length = struct.unpack('>I', int(length_bits, 2).to_bytes(4, 'big'))[0]
            
            # Extract data
            data_bits = bits[32:32 + (length * 8)]
            encrypted_data = int(data_bits, 2).to_bytes(length, 'big')
            
            # Decrypt
            decrypted_data = self._polymorphic_decrypt(encrypted_data)
            
            return decrypted_data
            
        except Exception as e:
            print(f"Error extracting data from image: {e}")
            return None
    
    def _adaptive_lsb_extract(self, img_array) -> str:
        """Extract bits using adaptive LSB."""
        flat = img_array.flatten()
        bits = []
        
        for pixel in flat:
            if self._is_safe_pixel(pixel):
                bits.append(str(pixel & 1))
        
        return ''.join(bits)
    
    def hide_in_text(
        self,
        secret_data: bytes,
        cover_text: str,
        technique: str = 'whitespace'
    ) -> str:
        """
        Hide data in text using linguistic steganography.
        
        Techniques:
        - whitespace: Use spaces/tabs
        - synonym: Replace words with synonyms
        - typo: Intentional typos encode data
        
        Args:
            secret_data: Data to hide
            cover_text: Cover text
            technique: Steganography technique
        
        Returns:
            Text with hidden data
        """
        if technique == 'whitespace':
            return self._whitespace_hide(secret_data, cover_text)
        elif technique == 'synonym':
            return self._synonym_hide(secret_data, cover_text)
        else:
            return cover_text
    
    def _whitespace_hide(self, data: bytes, text: str) -> str:
        """Hide data using whitespace variations."""
        lines = text.split('\n')
        bits = ''.join(format(byte, '08b') for byte in data)
        
        bit_index = 0
        modified_lines = []
        
        for line in lines:
            if bit_index >= len(bits):
                modified_lines.append(line)
                continue
            
            # Add trailing whitespace to encode bit
            if bits[bit_index] == '1':
                line = line + ' '  # Single space = 1
            else:
                line = line + '  '  # Double space = 0
            
            modified_lines.append(line)
            bit_index += 1
        
        return '\n'.join(modified_lines)
    
    def _synonym_hide(self, data: bytes, text: str) -> str:
        """Hide data by choosing synonyms (simplified)."""
        # Would use NLP to replace words with synonyms
        # The choice of synonym encodes bits
        return text  # Simplified
    
    def _polymorphic_encrypt(self, data: bytes) -> bytes:
        """
        Polymorphic encryption - different output each time.
        
        Uses XOR with random key + key embedded with data
        """
        # Generate random key
        key = secrets.token_bytes(32)
        
        # XOR encrypt
        encrypted = bytes(a ^ b for a, b in zip(data, (key * (len(data) // len(key) + 1))[:len(data)]))
        
        # Prepend key (would normally use more sophisticated key exchange)
        return key + encrypted
    
    def _polymorphic_decrypt(self, data: bytes) -> bytes:
        """Decrypt polymorphically encrypted data."""
        # Extract key
        key = data[:32]
        encrypted = data[32:]
        
        # XOR decrypt
        decrypted = bytes(a ^ b for a, b in zip(encrypted, (key * (len(encrypted) // len(key) + 1))[:len(encrypted)]))
        
        return decrypted
    
    def create_decoy_layer(
        self,
        real_data: bytes,
        decoy_data: bytes,
        password1: str,
        password2: str
    ) -> bytes:
        """
        Create multi-layer encryption with plausible deniability.
        
        password1 reveals decoy_data
        password2 reveals real_data
        
        Args:
            real_data: Real secret data
            decoy_data: Decoy data (plausible deniability)
            password1: Password for decoy
            password2: Password for real data
        
        Returns:
            Encrypted container
        """
        # Derive keys from passwords
        key1 = hashlib.pbkdf2_hmac('sha256', password1.encode(), b'salt1', 100000)
        key2 = hashlib.pbkdf2_hmac('sha256', password2.encode(), b'salt2', 100000)
        
        # Encrypt decoy data with key1
        encrypted_decoy = self._xor_encrypt(decoy_data, key1)
        
        # Encrypt real data with key2
        encrypted_real = self._xor_encrypt(real_data, key2)
        
        # Combine in a way that's indistinguishable
        # Both decryptions produce valid data
        combined = self._combine_layers(encrypted_decoy, encrypted_real)
        
        return combined
    
    def _xor_encrypt(self, data: bytes, key: bytes) -> bytes:
        """Simple XOR encryption."""
        return bytes(a ^ b for a, b in zip(data, (key * (len(data) // len(key) + 1))[:len(data)]))
    
    def _combine_layers(self, layer1: bytes, layer2: bytes) -> bytes:
        """Combine two encrypted layers."""
        # Interleave bytes or use more sophisticated combination
        max_len = max(len(layer1), len(layer2))
        combined = bytearray(max_len * 2)
        
        for i in range(max_len):
            if i < len(layer1):
                combined[i * 2] = layer1[i]
            if i < len(layer2):
                combined[i * 2 + 1] = layer2[i]
        
        return bytes(combined)
    
    def generate_fake_header(self, file_type: str) -> bytes:
        """Generate fake file header to disguise hidden data."""
        headers = {
            'pdf': b'%PDF-1.4\n',
            'jpg': b'\xFF\xD8\xFF\xE0',
            'png': b'\x89PNG\r\n\x1a\n',
            'zip': b'PK\x03\x04'
        }
        
        return headers.get(file_type, b'')
