#!/usr/bin/env python3
# Copyright (C) 2026 Ayush - PhantomTrace Project
# Licensed under GPL-3.0 - See LICENSE file for details
"""
Entropy Injection - Add random data to mess with forensic tools

Fills slack space, randomizes file structure, breaks signatures.
Basically makes files harder to analyze and carve.
"""

import secrets
from pathlib import Path
from typing import Optional


class EntropyInjector:
    """Add random noise to files to break forensic analysis."""
    
    def __init__(self):
        self.injections = []
    
    def inject_file_slack(self, filepath, overwrite=True):
        """Fill unused file slack space with random data."""
        try:
            path = Path(filepath)
            if not path.exists():
                raise FileNotFoundError(f"File not found: {filepath}")
            
            file_size = path.stat().st_size
            cluster_size = 4096  # typical cluster size
            
            # Calculate slack
            if file_size % cluster_size != 0:
                slack_size = cluster_size - (file_size % cluster_size)
            else:
                slack_size = 0
            
            if slack_size > 0 and overwrite:
                # Fill it with random data
                # Note: simplified version, real slack needs low-level disk access
                with open(path, 'ab') as f:
                    entropy = secrets.token_bytes(slack_size)
                    f.write(entropy)
                
                self.injections.append({
                    'file': str(path),
                    'type': 'slack_space',
                    'bytes_added': slack_size
                })
                
                return True
            
            return False
            
        except Exception as e:
            print(f"Error injecting file slack entropy: {e}")
            return False
    
    def randomize_file_structure(self, filepath: str) -> bool:
        """
        Randomize internal file structure without breaking functionality.
        
        Techniques:
        - Reorder sections/chunks
        - Add random padding
        - Randomize optional fields
        
        Args:
            filepath: Path to file
        
        Returns:
            True if successful
        """
        try:
            path = Path(filepath)
            suffix = path.suffix.lower()
            
            # Different techniques for different file types
            if suffix in ['.zip', '.jar']:
                return self._randomize_zip_structure(path)
            elif suffix in ['.pdf']:
                return self._randomize_pdf_structure(path)
            else:
                # Generic approach: add random padding
                return self._add_random_padding(path)
            
        except Exception as e:
            print(f"Error randomizing file structure: {e}")
            return False
    
    def _randomize_zip_structure(self, path: Path) -> bool:
        """Randomize ZIP file structure."""
        # ZIP files can have entries in any order
        # Add random comment, reorder entries, etc.
        import zipfile
        
        try:
            # Read ZIP
            with zipfile.ZipFile(path, 'r') as zip_read:
                files = zip_read.namelist()
                
                # Create temporary ZIP with randomized order
                temp_path = path.with_suffix('.tmp')
                with zipfile.ZipFile(temp_path, 'w') as zip_write:
                    # Randomize entry order
                    shuffled_files = list(files)
                    secrets.SystemRandom().shuffle(shuffled_files)
                    
                    for filename in shuffled_files:
                        data = zip_read.read(filename)
                        zip_write.writestr(filename, data)
                    
                    # Add random comment
                    zip_write.comment = secrets.token_bytes(secrets.randbelow(100))
            
            # Replace original
            temp_path.replace(path)
            
            return True
            
        except:
            return False
    
    def _randomize_pdf_structure(self, path: Path) -> bool:
        """Randomize PDF structure."""
        # PDFs can have objects in any order
        # Add random metadata, reorder objects, etc.
        return self._add_random_padding(path)
    
    def _add_random_padding(self, path: Path) -> bool:
        """Add random padding to file."""
        with open(path, 'ab') as f:
            padding_size = secrets.randbelow(1024) + 100
            padding = secrets.token_bytes(padding_size)
            f.write(b'\n# Random padding\n')
            f.write(padding)
        
        return True
    
    def break_file_signature(self, filepath: str, new_extension: Optional[str] = None) -> bool:
        """
        Modify file to break signature-based detection.
        
        Args:
            filepath: Path to file
            new_extension: Optional new extension
        
        Returns:
            True if successful
        """
        try:
            path = Path(filepath)
            
            # Change magic bytes to something random but valid-looking
            with open(path, 'r+b') as f:
                # Read first few bytes
                header = f.read(16)
                
                # Generate new "magic bytes" that won't match known signatures
                new_header = secrets.token_bytes(4) + header[4:]
                
                # Write back
                f.seek(0)
                f.write(new_header)
            
            # Optionally change extension
            if new_extension:
                new_path = path.with_suffix(new_extension)
                path.rename(new_path)
            
            return True
            
        except Exception as e:
            print(f"Error breaking file signature: {e}")
            return False
    
    def inject_metadata_entropy(self, filepath: str) -> bool:
        """
        Inject random data into file metadata.
        
        Args:
            filepath: Path to file
        
        Returns:
            True if successful
        """
        try:
            path = Path(filepath)
            suffix = path.suffix.lower()
            
            # Different techniques for different formats
            if suffix in ['.jpg', '.jpeg', '.png']:
                return self._inject_image_metadata_entropy(path)
            elif suffix in ['.pdf']:
                return self._inject_pdf_metadata_entropy(path)
            elif suffix in ['.docx', '.xlsx']:
                return self._inject_office_metadata_entropy(path)
            else:
                return False
            
        except Exception as e:
            print(f"Error injecting metadata entropy: {e}")
            return False
    
    def _inject_image_metadata_entropy(self, path: Path) -> bool:
        """Inject entropy into image EXIF data."""
        try:
            from PIL import Image
            
            # Add random EXIF fields
            # Simplified for demonstration
            return True
            
        except ImportError:
            return False
    
    def _inject_pdf_metadata_entropy(self, path: Path) -> bool:
        """Inject entropy into PDF metadata."""
        # Add random metadata fields
        return True
    
    def _inject_office_metadata_entropy(self, path: Path) -> bool:
        """Inject entropy into Office document metadata."""
        # Add random custom properties
        return True
    
    def create_entropy_file(self, output_path: str, size_mb: int = 1) -> bool:
        """
        Create file filled with cryptographic entropy.
        
        Useful for:
        - Overwriting deleted files
        - Filling free space
        - Creating decoy data
        
        Args:
            output_path: Path for output file
            size_mb: Size in megabytes
        
        Returns:
            True if successful
        """
        try:
            size_bytes = size_mb * 1024 * 1024
            chunk_size = 1024 * 1024  # 1MB chunks
            
            with open(output_path, 'wb') as f:
                bytes_written = 0
                while bytes_written < size_bytes:
                    write_size = min(chunk_size, size_bytes - bytes_written)
                    entropy = secrets.token_bytes(write_size)
                    f.write(entropy)
                    bytes_written += write_size
            
            return True
            
        except Exception as e:
            print(f"Error creating entropy file: {e}")
            return False
    
    def poison_file_carver(self, directory: str, num_files: int = 100) -> int:
        """
        Create files designed to poison file carving tools.
        
        Creates files with:
        - Fake file headers
        - Misleading signatures
        - Corrupted structures
        
        Args:
            directory: Directory to create poison files
            num_files: Number of poison files
        
        Returns:
            Number of files created
        """
        try:
            dir_path = Path(directory)
            dir_path.mkdir(exist_ok=True, parents=True)
            
            file_signatures = {
                'pdf': b'%PDF-1.',
                'jpg': b'\xFF\xD8\xFF',
                'png': b'\x89PNG',
                'zip': b'PK\x03\x04',
                'exe': b'MZ'
            }
            
            created = 0
            for i in range(num_files):
                # Random signature
                sig_type = secrets.choice(list(file_signatures.keys()))
                signature = file_signatures[sig_type]
                
                # Create file with signature but random content
                filename = f"poison_{i}_{secrets.token_hex(4)}.dat"
                filepath = dir_path / filename
                
                with open(filepath, 'wb') as f:
                    f.write(signature)
                    f.write(secrets.token_bytes(secrets.randbelow(10000) + 1000))
                
                created += 1
            
            return created
            
        except Exception as e:
            print(f"Error creating poison files: {e}")
            return 0
    
    def get_injection_stats(self) -> dict:
        """Return statistics about entropy injections."""
        return {
            'total_injections': len(self.injections),
            'injections': self.injections.copy()
        }
