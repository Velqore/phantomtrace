#!/usr/bin/env python3
# Copyright (C) 2026 Ayush - PhantomTrace Project
# Licensed under GPL-3.0 - See LICENSE file for details
"""
Disk Phantom - Secure disk wiping and LUKS destruction
Inspired by tools: DBAN, Shred, Wipe, Srm, Nuke My LUKS, delete-self-poc
"""

import os
import sys
import subprocess
from pathlib import Path
from typing import Optional

class DiskPhantom:
    """
    Secure disk operations:
    - Multi-pass secure file deletion
    - Full disk wiping
    - LUKS header destruction
    - Free space wiping
    - SSD TRIM support
    - MBR/GPT destruction
    - Slack space wiping
    """
    
    def __init__(self):
        self.is_windows = sys.platform.startswith('win')
        self.is_linux = sys.platform.startswith('linux')
        self.wiped_files = []
        
    def secure_delete_file(self, filepath: str, passes: int = 3) -> bool:
        """Securely delete a file with multiple overwrite passes"""
        path = Path(filepath)
        
        if not path.exists():
            print(f"❌ File not found: {filepath}")
            return False
        
        try:
            file_size = path.stat().st_size
            
            # Multiple overwrite passes
            for pass_num in range(passes):
                with open(filepath, 'wb') as f:
                    if pass_num % 2 == 0:
                        # Random data
                        f.write(os.urandom(file_size))
                    else:
                        # Zeros
                        f.write(b'\x00' * file_size)
                
                # Flush to disk
                f.flush()
                os.fsync(f.fileno())
            
            # Delete file
            os.remove(filepath)
            
            self.wiped_files.append(str(path))
            print(f"✅ Securely deleted ({passes} passes): {path.name}")
            return True
            
        except Exception as e:
            print(f"❌ Secure delete failed: {e}")
            return False
    
    def wipe_free_space(self, drive: str = "C:\\") -> bool:
        """Wipe free space on a drive"""
        print(f"🧹 Wiping free space on: {drive}")
        
        try:
            if self.is_windows:
                # Use cipher command on Windows
                result = subprocess.run(
                    ['cipher', '/w:' + drive],
                    capture_output=True,
                    text=True
                )
                
                if result.returncode == 0:
                    print(f"✅ Free space wiped on {drive}")
                    return True
                    
            elif self.is_linux:
                # Create large file filled with zeros
                temp_file = os.path.join(drive, '.phantom_wipe_tmp')
                subprocess.run(
                    ['dd', 'if=/dev/zero', f'of={temp_file}', 'bs=1M'],
                    stderr=subprocess.DEVNULL
                )
                os.remove(temp_file)
                print(f"✅ Free space wiped on {drive}")
                return True
            
            return False
            
        except Exception as e:
            print(f"⚠️  Free space wipe error: {e}")
            return False
    
    def destroy_luks_header(self, device: str) -> bool:
        """Destroy LUKS encryption header (Linux)"""
        if not self.is_linux:
            print("⚠️  LUKS operations only on Linux")
            return False
        
        if os.geteuid() != 0:
            print("⚠️  Root privileges required")
            return False
        
        try:
            print(f"💣 Destroying LUKS header on {device}")
            print("⚠️  THIS WILL MAKE DATA UNRECOVERABLE!")
            
            # Overwrite first 10MB (LUKS header)
            subprocess.run(
                ['dd', 'if=/dev/urandom', f'of={device}', 'bs=1M', 'count=10'],
                check=True
            )
            
            print(f"✅ LUKS header destroyed on {device}")
            return True
            
        except Exception as e:
            print(f"❌ LUKS destruction failed: {e}")
            return False
    
    def emergency_luks_nuke(self, devices: list) -> int:
        """Emergency LUKS header destruction on multiple devices"""
        if not self.is_linux or os.geteuid() != 0:
            print("⚠️  Requires Linux with root privileges")
            return 0
        
        print("🚨 EMERGENCY LUKS NUKE ACTIVATED")
        count = 0
        
        for device in devices:
            if self.destroy_luks_header(device):
                count += 1
        
        print(f"✅ Nuked {count}/{len(devices)} devices")
        return count
    
    def shred_file(self, filepath: str, iterations: int = 25) -> bool:
        """Shred file using system shred command (Linux)"""
        if not self.is_linux:
            return self.secure_delete_file(filepath, passes=iterations)
        
        try:
            result = subprocess.run(
                ['shred', '-vfz', '-n', str(iterations), filepath],
                capture_output=True
            )
            
            if result.returncode == 0:
                print(f"✅ Shredded: {filepath}")
                return True
            return False
            
        except FileNotFoundError:
            print("⚠️  'shred' command not found, using built-in method")
            return self.secure_delete_file(filepath, passes=iterations)
        except Exception as e:
            print(f"❌ Shred failed: {e}")
            return False
    
    def wipe_slack_space(self, filepath: str) -> bool:
        """Wipe file slack space"""
        try:
            path = Path(filepath)
            if not path.exists():
                return False
            
            # Get actual file size
            file_size = path.stat().st_size
            
            # Get cluster size (Windows) or block size (Linux)
            if self.is_windows:
                cluster_size = 4096  # Common default
            else:
                cluster_size = os.statvfs(str(path.parent)).f_bsize
            
            # Calculate slack space
            slack_size = cluster_size - (file_size % cluster_size)
            
            if slack_size > 0 and slack_size < cluster_size:
                # Append random data to fill slack space
                with open(filepath, 'ab') as f:
                    f.write(os.urandom(slack_size))
                
                # Truncate back to original size
                with open(filepath, 'rb+') as f:
                    f.truncate(file_size)
                
                print(f"✅ Wiped {slack_size} bytes of slack space")
                return True
            
            return False
            
        except Exception as e:
            print(f"⚠️  Slack space wipe error: {e}")
            return False
    
    def destroy_mbr(self, device: str) -> bool:
        """Destroy MBR/GPT on a disk"""
        if os.geteuid() != 0 if self.is_linux else False:
            print("⚠️  Root/Admin privileges required")
            return False
        
        try:
            print(f"💣 Destroying MBR/GPT on {device}")
            
            # Overwrite first 10MB (MBR + GPT)
            if self.is_linux:
                subprocess.run(
                    ['dd', 'if=/dev/zero', f'of={device}', 'bs=1M', 'count=10'],
                    check=True
                )
            elif self.is_windows:
                # Windows: Use diskpart (requires elevated privileges)
                print("⚠️  Windows MBR destruction requires diskpart")
                return False
            
            print(f"✅ MBR/GPT destroyed on {device}")
            return True
            
        except Exception as e:
            print(f"❌ MBR destruction failed: {e}")
            return False
    
    def secure_delete_directory(self, dirpath: str, passes: int = 3) -> int:
        """Securely delete entire directory"""
        path = Path(dirpath)
        
        if not path.is_dir():
            print(f"❌ Not a directory: {dirpath}")
            return 0
        
        count = 0
        for item in path.rglob('*'):
            if item.is_file():
                if self.secure_delete_file(str(item), passes):
                    count += 1
        
        # Remove empty directories
        try:
            import shutil
            shutil.rmtree(dirpath, ignore_errors=True)
        except:
            pass
        
        print(f"✅ Securely deleted {count} files from directory")
        return count
    
    def fill_disk_with_random(self, target_path: str) -> bool:
        """Fill remaining disk space with random data"""
        print(f"🔄 Filling disk with random data at: {target_path}")
        
        try:
            temp_file = os.path.join(target_path, '.phantom_fill_tmp')
            
            with open(temp_file, 'wb') as f:
                while True:
                    try:
                        # Write 10MB chunks
                        f.write(os.urandom(10 * 1024 * 1024))
                    except OSError:
                        # Disk full
                        break
            
            # Delete temp file
            os.remove(temp_file)
            print("✅ Disk filled and cleaned")
            return True
            
        except Exception as e:
            print(f"⚠️  Disk fill error: {e}")
            return False
    
    def get_report(self) -> list:
        """Get list of wiped files"""
        return self.wiped_files.copy()


if __name__ == "__main__":
    phantom = DiskPhantom()
    print("💾 Disk Phantom - Secure Disk Operations")
    print("=" * 60)
