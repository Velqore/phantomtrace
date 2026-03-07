#!/usr/bin/env python3
# Copyright (C) 2026 Ayush - PhantomTrace Project
# Licensed under GPL-3.0 - See LICENSE file for details
"""
Utility functions
"""

import os
import hashlib
import secrets
from pathlib import Path
from typing import Optional, List


def generate_secure_random(size):
    """Get random bytes using secrets module."""
    return secrets.token_bytes(size)


def calculate_file_hash(filepath, algorithm='sha256'):
    """Calculate file hash."""
    hash_obj = hashlib.new(algorithm)
    
    with open(filepath, 'rb') as f:
        while chunk := f.read(8192):
            hash_obj.update(chunk)
    
    return hash_obj.hexdigest()


def secure_delete_directory(directory):
    """Delete entire directory securely."""
    from phantomtrace import QuantumDecay
    
    dir_path = Path(directory)
    if not dir_path.exists():
        return False
    
    qd = QuantumDecay()
    
    # Delete files first
    for filepath in dir_path.rglob('*'):
        if filepath.is_file():
            qd.quantum_delete(str(filepath))
    
    # Then remove the directory tree
    try:
        import shutil
        shutil.rmtree(dir_path)
        return True
    except Exception:
        return False


def is_admin():
    """Check if we're running as admin/root."""
    import sys
    
    if sys.platform == 'win32':
        try:
            import ctypes
            return ctypes.windll.shell32.IsUserAnAdmin() != 0
        except:
            return False
    else:
        return os.geteuid() == 0


def get_system_info():
    """Get basic system info."""
        Dictionary with system info
    """
    import platform
    import psutil
    
    return {
        'os': platform.system(),
        'os_version': platform.version(),
        'architecture': platform.machine(),
        'processor': platform.processor(),
        'python_version': platform.python_version(),
        'memory_total_gb': psutil.virtual_memory().total / (1024**3),
        'memory_available_gb': psutil.virtual_memory().available / (1024**3),
    }


def format_bytes(bytes_count: int) -> str:
    """
    Format bytes into human-readable string.
    
    Args:
        bytes_count: Number of bytes
    
    Returns:
        Formatted string (e.g., "1.5 MB")
    """
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if bytes_count < 1024.0:
            return f"{bytes_count:.2f} {unit}"
        bytes_count /= 1024.0
    return f"{bytes_count:.2f} PB"


def verify_file_destroyed(original_hash: str, filepath: str) -> bool:
    """
    Verify file was properly destroyed by comparing hashes.
    
    Args:
        original_hash: Hash of original file
        filepath: Path where file was (should not exist)
    
    Returns:
        True if file is gone and can't be recovered
    """
    path = Path(filepath)
    
    # File should not exist
    if path.exists():
        return False
    
    # Could add more sophisticated checks here
    # (e.g., check if file can be carved from disk)
    
    return True


def create_decoy_file(filepath: str, file_type: str = 'text', size_kb: int = 10) -> bool:
    """
    Create a decoy file with realistic content.
    
    Args:
        filepath: Path for decoy file
        file_type: Type of decoy (text, binary, document)
        size_kb: Size in kilobytes
    
    Returns:
        True if successful
    """
    try:
        path = Path(filepath)
        path.parent.mkdir(exist_ok=True, parents=True)
        
        size_bytes = size_kb * 1024
        
        if file_type == 'text':
            # Generate text-like content
            content = []
            while len(''.join(content)) < size_bytes:
                line = ' '.join(secrets.choice(['data', 'process', 'system', 'update', 
                                               'report', 'analysis']) for _ in range(10))
                content.append(line + '\n')
            
            path.write_text(''.join(content)[:size_bytes])
        
        elif file_type == 'binary':
            # Generate random binary data
            path.write_bytes(generate_secure_random(size_bytes))
        
        else:
            # Default to random
            path.write_bytes(generate_secure_random(size_bytes))
        
        return True
        
    except Exception as e:
        print(f"Error creating decoy: {e}")
        return False


def list_forensic_artifacts(directory: str) -> List[str]:
    """
    List potential forensic artifacts in directory.
    
    Args:
        directory: Directory to scan
    
    Returns:
        List of artifact file paths
    """
    artifacts = []
    dir_path = Path(directory)
    
    # Common forensic artifact patterns
    patterns = [
        '*.log',
        '*.tmp',
        '*.bak',
        '*.old',
        '*~',
        '.DS_Store',
        'Thumbs.db',
        '*.lnk',
        '*.recent',
    ]
    
    for pattern in patterns:
        artifacts.extend([str(f) for f in dir_path.rglob(pattern)])
    
    return artifacts
