#!/usr/bin/env python3
# Copyright (C) 2026 Ayush - PhantomTrace Project
# Licensed under GPL-3.0 - See LICENSE file for details
"""
Temporal Fog - Mess with file timestamps

Changes file creation/modification times to break timeline analysis.
Can make files look older/newer and break correlations between timestamps.
"""

import os
import secrets
from datetime import datetime, timedelta
from pathlib import Path
from typing import Optional
import platform


class TemporalFog:
    """Manipulate file timestamps to confuse forensic timelines."""
    
    def __init__(self):
        self.system = platform.system()
        self.modifications = []
    
    def apply_fog(self, path, days_offset=None, randomize=True, break_correlation=True):
        """Change file timestamps to mess with forensic timeline."""
        filepath = Path(path)
        
        if not filepath.exists():
            raise FileNotFoundError(f"Path not found: {path}")
        
        try:
            # Generate timestamp set
            timestamps = self._generate_fog_timestamps(
                days_offset=days_offset,
                randomize=randomize,
                break_correlation=break_correlation
            )
            
            # Apply to filesystem
            self._apply_filesystem_timestamps(filepath, timestamps)
            
            # Apply to file metadata if applicable
            if filepath.is_file():
                self._apply_metadata_timestamps(filepath, timestamps)
            
            # Record modification
            self.modifications.append({
                'path': str(filepath),
                'timestamp': datetime.now(),
                'timestamps_applied': timestamps
            })
            
            return True
            
        except Exception as e:
            print(f"Error applying temporal fog: {e}")
            return False
    
    def _generate_fog_timestamps(
        self,
        days_offset: Optional[int],
        randomize: bool,
        break_correlation: bool
    ) -> dict:
        """
        Generate fogged timestamps.
        
        Creates timestamps that:
        - Are offset from current time
        - Have random entropy
        - Break typical Created < Modified < Accessed pattern
        """
        base_time = datetime.now()
        
        if days_offset is None:
            # Random offset between -365 and +30 days
            days_offset = secrets.randbelow(396) - 365
        
        base_time = base_time + timedelta(days=days_offset)
        
        if break_correlation:
            # Create impossible timestamp sequences
            # Modified can be before Created!
            created = base_time + timedelta(
                hours=secrets.randbelow(24),
                minutes=secrets.randbelow(60),
                seconds=secrets.randbelow(60)
            )
            
            modified = base_time + timedelta(
                days=secrets.randbelow(60) - 30,
                hours=secrets.randbelow(24),
                minutes=secrets.randbelow(60)
            )
            
            accessed = base_time + timedelta(
                days=secrets.randbelow(90) - 45,
                hours=secrets.randbelow(24),
                minutes=secrets.randbelow(60)
            )
        else:
            # Maintain logical order but with entropy
            created = base_time
            modified = created + timedelta(
                days=secrets.randbelow(30),
                hours=secrets.randbelow(24)
            )
            accessed = modified + timedelta(
                days=secrets.randbelow(7),
                hours=secrets.randbelow(24)
            )
        
        if randomize:
            # Add microsecond-level entropy
            created = self._add_microsecond_entropy(created)
            modified = self._add_microsecond_entropy(modified)
            accessed = self._add_microsecond_entropy(accessed)
        
        return {
            'created': created,
            'modified': modified,
            'accessed': accessed
        }
    
    def _add_microsecond_entropy(self, dt: datetime) -> datetime:
        """Add random microseconds to timestamp."""
        return dt.replace(microsecond=secrets.randbelow(1000000))
    
    def _apply_filesystem_timestamps(self, filepath: Path, timestamps: dict):
        """Apply timestamps to filesystem."""
        # Convert to Unix timestamps
        atime = timestamps['accessed'].timestamp()
        mtime = timestamps['modified'].timestamp()
        
        # Set access and modified times
        os.utime(filepath, (atime, mtime))
        
        # Note: Created time (birth time) is harder to change and OS-specific
        # Windows: requires low-level API calls
        # Linux: often not changeable
        # macOS: can be changed with specific tools
        
        if self.system == 'Windows':
            self._set_windows_created_time(filepath, timestamps['created'])
    
    def _set_windows_created_time(self, filepath: Path, created: datetime):
        """Set Windows creation time (requires admin or specific permissions)."""
        try:
            import ctypes
            from ctypes import wintypes
            
            # This is a simplified version - production code would use
            # SetFileTime Windows API
            # For now, we'll note it in the modification log
            pass
        except Exception:
            pass
    
    def _apply_metadata_timestamps(self, filepath: Path, timestamps: dict):
        """Apply timestamps to file metadata (EXIF, document properties, etc.)."""
        suffix = filepath.suffix.lower()
        
        if suffix in ['.jpg', '.jpeg', '.png', '.tiff']:
            self._modify_image_exif(filepath, timestamps)
        elif suffix in ['.pdf']:
            self._modify_pdf_metadata(filepath, timestamps)
        elif suffix in ['.docx', '.xlsx', '.pptx']:
            self._modify_office_metadata(filepath, timestamps)
    
    def _modify_image_exif(self, filepath: Path, timestamps: dict):
        """Modify image EXIF timestamps."""
        try:
            from PIL import Image
            from PIL.ExifTags import TAGS
            
            # This would modify EXIF DateTime, DateTimeOriginal, DateTimeDigitized
            # Simplified for demonstration
            pass
        except ImportError:
            pass
    
    def _modify_pdf_metadata(self, filepath: Path, timestamps: dict):
        """Modify PDF metadata timestamps."""
        # Would use PyPDF2 or similar to modify Creation/Modification dates
        pass
    
    def _modify_office_metadata(self, filepath: Path, timestamps: dict):
        """Modify Microsoft Office document metadata."""
        # Would use python-docx or similar to modify document properties
        pass
    
    def create_timeline_gap(
        self,
        directory: str,
        gap_start: datetime,
        gap_end: datetime
    ) -> int:
        """
        Create a suspicious gap in file timeline.
        Useful for demonstrating anti-forensics or creating decoys.
        
        Args:
            directory: Directory to process
            gap_start: Start of gap period
            gap_end: End of gap period
        
        Returns:
            Number of files modified
        """
        dir_path = Path(directory)
        count = 0
        
        for filepath in dir_path.rglob('*'):
            if filepath.is_file():
                # Move timestamps outside the gap
                stat = filepath.stat()
                mtime = datetime.fromtimestamp(stat.st_mtime)
                
                if gap_start <= mtime <= gap_end:
                    # Move before gap
                    new_time = gap_start - timedelta(days=secrets.randbelow(30) + 1)
                    self.apply_fog(str(filepath), days_offset=None, randomize=True)
                    count += 1
        
        return count
    
    def inject_temporal_entropy(self, directory: str, percentage: float = 0.3) -> int:
        """
        Randomly modify timestamps of a percentage of files in directory.
        Creates noise in forensic timeline analysis.
        
        Args:
            directory: Directory to process
            percentage: Percentage of files to modify (0.0 to 1.0)
        
        Returns:
            Number of files modified
        """
        dir_path = Path(directory)
        files = [f for f in dir_path.rglob('*') if f.is_file()]
        
        num_to_modify = int(len(files) * percentage)
        files_to_modify = secrets.SystemRandom().sample(files, num_to_modify)
        
        for filepath in files_to_modify:
            self.apply_fog(str(filepath), randomize=True, break_correlation=True)
        
        return num_to_modify
    
    def get_modifications(self) -> list:
        """Return list of all timestamp modifications made."""
        return self.modifications.copy()
