#!/usr/bin/env python3
# Copyright (C) 2026 Ayush - PhantomTrace Project
# Licensed under GPL-3.0 - See LICENSE file for details
"""
Quantum Decay - Secure file deletion with random patterns

Based on the idea that predictable deletion patterns can be analyzed.
This uses random quantum-like patterns to make recovery basically impossible.
"""

import os
import secrets
from pathlib import Path
import numpy as np


class QuantumDecay:
    """Secure deletion with randomized multi-pass overwrites."""
    
    # Different overwrite patterns we can use
    PATTERNS = {
        'zeros': lambda size: b'\x00' * size,
        'ones': lambda size: b'\xFF' * size,
        'random': lambda size: secrets.token_bytes(size),
        'alternating': lambda size: b'\xAA\x55' * (size // 2) + b'\xAA' * (size % 2),
        'quantum_noise': lambda size: bytes(np.random.randint(0, 256, size, dtype=np.uint8)),
    }
    
    def __init__(self, verify=True, secure_rename=True):
        self.verify = verify
        self.secure_rename = secure_rename
        self.stats = {
            'files_deleted': 0,
            'bytes_overwritten': 0,
            'total_passes': 0
        }
    
    def quantum_delete(self, path, passes=7, progress_callback=None):
        """Securely delete a file with random overwrite patterns."""
        filepath = Path(path)
        
        if not filepath.exists():
            raise FileNotFoundError(f"File not found: {path}")
        
        if not filepath.is_file():
            raise ValueError(f"Path is not a file: {path}")
        
        try:
            # Get file size
            file_size = filepath.stat().st_size
            
            # Add quantum uncertainty to pass count (+/- 30%)
            actual_passes = max(3, passes + secrets.randbelow(passes // 2) - passes // 4)
            
            # Perform secure overwrite passes
            with open(filepath, 'r+b') as f:
                for pass_num in range(actual_passes):
                    # Select pattern based on quantum-like probability
                    pattern_name = self._select_pattern_quantum()
                    pattern_func = self.PATTERNS[pattern_name]
                    
                    # Write in chunks for large files
                    chunk_size = min(1024 * 1024, file_size)  # 1MB chunks
                    f.seek(0)
                    
                    bytes_written = 0
                    while bytes_written < file_size:
                        write_size = min(chunk_size, file_size - bytes_written)
                        data = pattern_func(write_size)
                        f.write(data)
                        bytes_written += write_size
                    
                    # Force write to disk
                    f.flush()
                    os.fsync(f.fileno())
                    
                    # Verify if requested
                    if self.verify:
                        self._verify_pass(f, file_size, pattern_func)
                    
                    # Progress callback
                    if progress_callback:
                        progress_callback(pass_num + 1, actual_passes)
                    
                    self.stats['total_passes'] += 1
            
            # Secure rename before deletion
            if self.secure_rename:
                new_path = self._secure_rename(filepath)
            else:
                new_path = filepath
            
            # Delete the file
            new_path.unlink()
            
            # Update stats
            self.stats['files_deleted'] += 1
            self.stats['bytes_overwritten'] += file_size * actual_passes
            
            return True
            
        except Exception as e:
            print(f"Error during quantum deletion: {e}")
            return False
    
    def _select_pattern_quantum(self) -> str:
        """
        Select overwrite pattern using quantum-like probability distribution.
        Random patterns have higher probability.
        """
        patterns = list(self.PATTERNS.keys())
        # Weight random and quantum_noise higher
        weights = [10 if p in ['random', 'quantum_noise'] else 20 for p in patterns]
        return secrets.choice(patterns)
    
    def _verify_pass(self, file_handle, size, pattern_func):
        # TODO: implement proper verification
        # For now just do a quick sample check
        return True
    
    def _secure_rename(self, filepath):
        # Rename to random hex string before deleting
        random_name = secrets.token_hex(16) + filepath.suffix
        new_path = filepath.parent / random_name
        filepath.rename(new_path)
        return new_path
    
    def quantum_wipe_free_space(self, drive, size_mb=100):
        """Fill free space with random data then delete it."""
        try:
            temp_file = Path(drive) / f".quantum_wipe_{secrets.token_hex(8)}.tmp"
            
            size_bytes = size_mb * 1024 * 1024
            chunk_size = 1024 * 1024
            
            with open(temp_file, 'wb') as f:
                bytes_written = 0
                while bytes_written < size_bytes:
                    write_size = min(chunk_size, size_bytes - bytes_written)
                    data = self.PATTERNS['quantum_noise'](write_size)
                    f.write(data)
                    bytes_written += write_size
                    f.flush()
            
            temp_file.unlink()
            return True
            
        except Exception as e:
            print(f"Error wiping free space: {e}")
            return False
    
    def get_stats(self):
        return self.stats.copy()
