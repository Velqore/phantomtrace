#!/usr/bin/env python3
# Copyright (C) 2026 Ayush - PhantomTrace Project
# Licensed under GPL-3.0 - See LICENSE file for details

import os
import sys
import struct
from pathlib import Path
from datetime import datetime, timedelta
import random
import ctypes
from typing import Dict, Optional, List


class MetadataPhantom:
    def __init__(self):
        self.modified_files = []
        self.is_windows = sys.platform.startswith('win')
        
    def strip_all_metadata(self, filepath: str) -> bool:
        path = Path(filepath)
        
        if not path.exists():
            print(f"❌ File not found: {filepath}")
            return False
            
        try:
            ext = path.suffix.lower()
            
            if ext in ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff', '.webp']:
                return self._strip_image(path)
            elif ext == '.pdf':
                return self._strip_pdf(path)
            elif ext in ['.docx', '.xlsx', '.pptx', '.doc', '.xls', '.ppt']:
                return self._strip_office(path)
            elif ext in ['.mp3', '.mp4', '.avi', '.mkv', '.flac', '.wav']:
                return self._strip_media(path)
            else:
                print(f"⚠️  Unsupported: {ext}")
                return False
                
        except Exception as e:
            print(f"❌ Error: {e}")
            return False
    
    def _strip_image(self, path: Path) -> bool:
        try:
            from PIL import Image
            
            img = Image.open(path)
            data = list(img.getdata())
            clean = Image.new(img.mode, img.size)
            clean.putdata(data)
            
            tmp = path.with_suffix(path.suffix + '.tmp')
            clean.save(tmp, quality=95, optimize=False)
            os.replace(tmp, path)
            
            self.modified_files.append(str(path))
            print(f"✅ Cleaned: {path.name}")
            return True
            
        except ImportError:
            print("⚠️  Pillow not installed: pip install Pillow")
            return False
        except Exception as e:
            print(f"❌ Failed: {e}")
            return False
    
    def _strip_pdf(self, path: Path) -> bool:
        try:
            import PyPDF2
            
            reader = PyPDF2.PdfReader(path)
            writer = PyPDF2.PdfWriter()
            
            # Copy pages without metadata
            for page in reader.pages:
                writer.add_page(page)
            
            # Write without metadata
            temp_path = path.with_suffix('.tmp')
            with open(temp_path, 'wb') as output:
                writer.write(output)
            
            os.replace(temp_path, path)
            
            self.modified_files.append(str(path))
            print(f"✅ Stripped PDF metadata from: {path.name}")
            return True
            
        except ImportError:
            print("⚠️  PyPDF2 not installed. Install with: pip install PyPDF2")
            return False
        except Exception as e:
            print(f"❌ Failed to strip PDF metadata: {e}")
            return False
    
    def _strip_office_metadata(self, path: Path) -> bool:
        try:
            import zipfile
            import shutil
            
            if path.suffix.lower() not in ['.docx', '.xlsx', '.pptx']:
                return False
            
            # Office files are ZIP archives
            temp_dir = path.parent / f".{path.name}_temp"
            temp_dir.mkdir(exist_ok=True)
            
            # Extract
            with zipfile.ZipFile(path, 'r') as zip_ref:
                zip_ref.extractall(temp_dir)
            
            # Remove metadata files
            metadata_files = [
                'docProps/core.xml',
                'docProps/app.xml',
                'docProps/custom.xml'
            ]
            
            for meta_file in metadata_files:
                meta_path = temp_dir / meta_file
                if meta_path.exists():
                    meta_path.unlink()
            
            # Repack
            temp_path = path.with_suffix('.tmp')
            with zipfile.ZipFile(temp_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
                for file in temp_dir.rglob('*'):
                    if file.is_file():
                        zipf.write(file, file.relative_to(temp_dir))
            
            # Cleanup and replace
            import shutil
            shutil.rmtree(temp_dir)
            os.replace(temp_path, path)
            
            self.modified_files.append(str(path))
            print(f"✅ Stripped Office metadata from: {path.name}")
            return True
            
        except Exception as e:
            print(f"❌ Failed to strip Office metadata: {e}")
            return False
    
    def _strip_media_metadata(self, path: Path) -> bool:
        """Remove metadata from media files (audio/video)"""
        try:
            import mutagen
            
            audio = mutagen.File(path)
            if audio is not None:
                audio.delete()
                audio.save()
                
                self.modified_files.append(str(path))
                print(f"✅ Stripped media metadata from: {path.name}")
                return True
            return False
            
        except ImportError:
            print("⚠️  Mutagen not installed. Install with: pip install mutagen")
            return False
        except Exception as e:
            print(f"❌ Failed to strip media metadata: {e}")
            return False
    
    def manipulate_timestamps(self, filepath: str, randomize: bool = True, 
                             target_date: Optional[datetime] = None) -> bool:
        """
        Manipulate file timestamps with nanosecond precision (NTFS)
        """
        path = Path(filepath)
        
        if not path.exists():
            print(f"❌ File not found: {filepath}")
            return False
        
        try:
            if randomize:
                # Random date within past 5 years
                days_back = random.randint(1, 1825)
                target = datetime.now() - timedelta(days=days_back)
            else:
                target = target_date or datetime.now()
            
            # Convert to timestamp
            timestamp = target.timestamp()
            
            # Set access and modification times
            os.utime(filepath, (timestamp, timestamp))
            
            # Windows-specific: Set creation time with nanosecond precision
            if self.is_windows:
                self._set_windows_creation_time(path, target)
            
            self.modified_files.append(str(path))
            print(f"✅ Manipulated timestamps for: {path.name}")
            return True
            
        except Exception as e:
            print(f"❌ Failed to manipulate timestamps: {e}")
            return False
    
    def _set_windows_creation_time(self, path: Path, dt: datetime):
        """Set Windows creation time with high precision"""
        if not self.is_windows:
            return
        
        try:
            # Convert to Windows FILETIME
            timestamp = int((dt.timestamp() + 11644473600) * 10000000)
            
            # Open file handle
            handle = ctypes.windll.kernel32.CreateFileW(
                str(path), 0x40000000, 0, None, 3, 0x80, None
            )
            
            if handle == -1:
                return
            
            # Set creation time
            filetime = ctypes.c_ulonglong(timestamp)
            ctypes.windll.kernel32.SetFileTime(
                handle,
                ctypes.byref(filetime),  # creation time
                None,  # access time
                None   # modification time
            )
            
            ctypes.windll.kernel32.CloseHandle(handle)
            
        except Exception as e:
            print(f"⚠️  Could not set Windows creation time: {e}")
    
    def inject_fake_metadata(self, filepath: str, fake_data: Dict[str, str]) -> bool:
        """Inject fake metadata into files"""
        path = Path(filepath)
        
        if not path.exists():
            return False
        
        try:
            ext = path.suffix.lower()
            
            if ext in ['.jpg', '.jpeg']:
                return self._inject_image_exif(path, fake_data)
            elif ext == '.pdf':
                return self._inject_pdf_metadata(path, fake_data)
            
        except Exception as e:
            print(f"❌ Failed to inject metadata: {e}")
            return False
    
    def _inject_image_exif(self, path: Path, fake_data: Dict) -> bool:
        """Inject fake EXIF data into images"""
        try:
            from PIL import Image
            import piexif
            
            img = Image.open(path)
            
            exif_dict = {
                "0th": {},
                "Exif": {},
                "GPS": {},
                "1st": {},
            }
            
            # Inject fake data
            if "camera" in fake_data:
                exif_dict["0th"][piexif.ImageIFD.Make] = fake_data["camera"].encode()
            
            if "location" in fake_data:
                # Add fake GPS coordinates
                exif_dict["GPS"][piexif.GPSIFD.GPSLatitude] = fake_data.get("lat", "0,0,0")
                exif_dict["GPS"][piexif.GPSIFD.GPSLongitude] = fake_data.get("lon", "0,0,0")
            
            exif_bytes = piexif.dump(exif_dict)
            img.save(path, exif=exif_bytes)
            
            print(f"✅ Injected fake EXIF into: {path.name}")
            return True
            
        except ImportError:
            print("⚠️  piexif not installed. Install with: pip install piexif")
            return False
        except Exception as e:
            print(f"❌ Failed to inject EXIF: {e}")
            return False
    
    def _inject_pdf_metadata(self, path: Path, fake_data: Dict) -> bool:
        """Inject fake metadata into PDF"""
        try:
            import PyPDF2
            
            reader = PyPDF2.PdfReader(path)
            writer = PyPDF2.PdfWriter()
            
            for page in reader.pages:
                writer.add_page(page)
            
            # Add fake metadata
            writer.add_metadata({
                '/Author': fake_data.get('author', 'Unknown'),
                '/Creator': fake_data.get('creator', 'Microsoft Word'),
                '/Producer': fake_data.get('producer', 'Adobe PDF'),
                '/Title': fake_data.get('title', 'Document'),
            })
            
            temp_path = path.with_suffix('.tmp')
            with open(temp_path, 'wb') as output:
                writer.write(output)
            
            os.replace(temp_path, path)
            
            print(f"✅ Injected fake PDF metadata into: {path.name}")
            return True
            
        except Exception as e:
            print(f"❌ Failed to inject PDF metadata: {e}")
            return False
    
    def batch_process_directory(self, directory: str, operation: str = "strip") -> int:
        """Process all files in a directory"""
        dir_path = Path(directory)
        count = 0
        
        if not dir_path.is_dir():
            print(f"❌ Not a directory: {directory}")
            return 0
        
        for file in dir_path.rglob('*'):
            if file.is_file():
                if operation == "strip":
                    if self.strip_all_metadata(str(file)):
                        count += 1
                elif operation == "timestamps":
                    if self.manipulate_timestamps(str(file)):
                        count += 1
        
        print(f"\n✅ Processed {count} files")
        return count
    
    def get_report(self) -> List[str]:
        """Get list of modified files"""
        return self.modified_files.copy()


if __name__ == "__main__":
    phantom = MetadataPhantom()
    print("🔧 Metadata Phantom - Metadata Manipulation Module")
    print("=" * 60)
