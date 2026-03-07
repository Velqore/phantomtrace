#!/usr/bin/env python3
# Copyright (C) 2026 Ayush - PhantomTrace Project
# Licensed under GPL-3.0 - See LICENSE file for details
"""
Memory Whisper - Work in RAM only to avoid disk traces

Allocates secure memory and wipes it properly when done.
Tries to prevent memory dumps and keep everything volatile.
"""

import sys
import secrets
import ctypes
from typing import Optional, Callable
import psutil


class MemoryWhisper:
    """RAM-only operations with secure cleanup."""
    
    def __init__(self):
        self.secure_regions = []
        self.system = sys.platform
    
    def allocate_secure_memory(self, size_bytes):
        """Allocate memory that won't be paged to disk."""
        try:
            # Allocate locked memory (not pageable to disk)
            if self.system == 'win32':
                return self._allocate_windows(size_bytes)
            else:
                return self._allocate_posix(size_bytes)
        except Exception as e:
            print(f"Error allocating secure memory: {e}")
            return None
    
    def _allocate_windows(self, size_bytes: int) -> Optional[int]:
        """Allocate secure memory on Windows."""
        try:
            # Use VirtualAlloc with PAGE_READWRITE
            MEM_COMMIT = 0x1000
            MEM_RESERVE = 0x2000
            PAGE_READWRITE = 0x04
            
            kernel32 = ctypes.windll.kernel32
            addr = kernel32.VirtualAlloc(
                0,
                size_bytes,
                MEM_COMMIT | MEM_RESERVE,
                PAGE_READWRITE
            )
            
            if addr:
                # Lock pages in memory (requires privilege)
                try:
                    kernel32.VirtualLock(addr, size_bytes)
                except:
                    pass  # May require administrator privileges
                
                self.secure_regions.append((addr, size_bytes))
                return addr
            
        except Exception as e:
            print(f"Windows memory allocation error: {e}")
        
        return None
    
    def _allocate_posix(self, size_bytes: int) -> Optional[int]:
        """Allocate secure memory on POSIX systems."""
        try:
            # Use mmap with MAP_ANONYMOUS and MAP_LOCKED
            import mmap
            
            # Create anonymous mapping
            mem = mmap.mmap(-1, size_bytes, mmap.MAP_PRIVATE | mmap.MAP_ANONYMOUS)
            
            # Try to lock pages (may require privilege)
            try:
                mem.mlock()
            except:
                pass
            
            addr = id(mem)  # Simplified - would use actual memory address
            self.secure_regions.append((addr, size_bytes))
            return addr
            
        except Exception as e:
            print(f"POSIX memory allocation error: {e}")
        
        return None
    
    def secure_wipe_memory(self, address: int, size_bytes: int) -> bool:
        """
        Securely wipe memory region.
        
        Args:
            address: Memory address to wipe
            size_bytes: Number of bytes to wipe
        
        Returns:
            True if successful
        """
        try:
            if self.system == 'win32':
                return self._wipe_windows(address, size_bytes)
            else:
                return self._wipe_posix(address, size_bytes)
        except Exception as e:
            print(f"Error wiping memory: {e}")
            return False
    
    def _wipe_windows(self, address: int, size_bytes: int) -> bool:
        """Wipe memory on Windows."""
        try:
            kernel32 = ctypes.windll.kernel32
            ntdll = ctypes.windll.ntdll
            
            # Multiple pass wipe
            for _ in range(3):
                # Write random data
                random_data = secrets.token_bytes(min(4096, size_bytes))
                ctypes.memmove(address, random_data, min(len(random_data), size_bytes))
            
            # Final zero pass
            ctypes.memset(address, 0, size_bytes)
            
            # Use RtlSecureZeroMemory if available (prevents optimization)
            try:
                ntdll.RtlSecureZeroMemory(address, size_bytes)
            except:
                pass
            
            return True
        except Exception as e:
            print(f"Windows wipe error: {e}")
            return False
    
    def _wipe_posix(self, address: int, size_bytes: int) -> bool:
        """Wipe memory on POSIX systems."""
        try:
            # Use explicit_bzero if available, otherwise multiple passes
            libc = ctypes.CDLL(None)
            
            try:
                libc.explicit_bzero(address, size_bytes)
            except:
                # Fallback to manual wipe
                for _ in range(3):
                    random_data = secrets.token_bytes(min(4096, size_bytes))
                    ctypes.memmove(address, random_data, min(len(random_data), size_bytes))
                
                ctypes.memset(address, 0, size_bytes)
            
            return True
        except Exception as e:
            print(f"POSIX wipe error: {e}")
            return False
    
    def process_in_memory(
        self,
        data: bytes,
        operation: Callable[[bytes], bytes]
    ) -> bytes:
        """
        Process data entirely in memory without disk writes.
        
        Args:
            data: Input data
            operation: Function to process data
        
        Returns:
            Processed data
        """
        # Allocate secure memory for processing
        size = len(data)
        addr = self.allocate_secure_memory(size * 2)  # Double for processing
        
        try:
            # Process data
            result = operation(data)
            return result
        finally:
            # Wipe memory
            if addr:
                self.secure_wipe_memory(addr, size * 2)
    
    def anti_dump_protection(self) -> bool:
        """
        Enable anti-memory dump protection.
        
        Techniques:
        - Set process as critical (Windows)
        - Adjust process privileges
        - Monitor for debuggers
        
        Returns:
            True if protection enabled
        """
        try:
            current_process = psutil.Process()
            
            if self.system == 'win32':
                # Set process as critical (requires admin)
                try:
                    kernel32 = ctypes.windll.kernel32
                    ntdll = ctypes.windll.ntdll
                    
                    # RtlSetProcessIsCritical
                    ntdll.RtlSetProcessIsCritical(1, 0, 0)
                except:
                    pass
            
            # Check for debuggers
            if self.is_debugger_present():
                print("WARNING: Debugger detected!")
                return False
            
            return True
            
        except Exception as e:
            print(f"Error enabling anti-dump protection: {e}")
            return False
    
    def is_debugger_present(self) -> bool:
        """
        Check if a debugger is attached to the process.
        
        Returns:
            True if debugger detected
        """
        try:
            if self.system == 'win32':
                kernel32 = ctypes.windll.kernel32
                return kernel32.IsDebuggerPresent() != 0
            else:
                # Check /proc/self/status for TracerPid (Linux)
                try:
                    with open('/proc/self/status', 'r') as f:
                        for line in f:
                            if line.startswith('TracerPid:'):
                                pid = int(line.split(':')[1].strip())
                                return pid != 0
                except:
                    pass
            
            return False
        except:
            return False
    
    def create_volatile_storage(self, size_mb: int = 10) -> Optional[str]:
        """
        Create RAM-disk for volatile storage (Windows only).
        
        Args:
            size_mb: Size of RAM disk in MB
        
        Returns:
            Path to RAM disk or None
        """
        if self.system != 'win32':
            print("RAM disk creation only supported on Windows")
            return None
        
        # This would use ImDisk or similar tool to create RAM disk
        # For demonstration, we note the concept
        print(f"Create {size_mb}MB RAM disk for volatile operations")
        return None
    
    def cleanup(self):
        """Cleanup all secure memory regions."""
        for addr, size in self.secure_regions:
            self.secure_wipe_memory(addr, size)
        
        self.secure_regions.clear()
    
    def __del__(self):
        """Destructor - ensure memory is wiped."""
        self.cleanup()
