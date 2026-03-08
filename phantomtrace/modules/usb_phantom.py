#!/usr/bin/env python3
# Copyright (C) 2026 Ayush - PhantomTrace Project
# Licensed under GPL-3.0 - See LICENSE file for details
"""
USB Phantom - USB device monitoring and kill switch
Inspired by tools: USB Kill, BusKill, Silk Guardian, USB Death, xxUSBSentinel
"""

import os
import sys
import time
import threading
import subprocess
from typing import List, Dict, Callable, Optional
from pathlib import Path

class USBPhantom:
    """
    USB security and kill switch:
    - Monitor USB device changes
    - Trigger actions on USB insertion/removal
    - Emergency system shutdown on USB change
    - Whitelist/blacklist USB devices
    - USB tripwire for physical security
    - Data destruction on unauthorized USB
    """
    
    def __init__(self):
        self.is_windows = sys.platform.startswith('win')
        self.is_linux = sys.platform.startswith('linux')
        self.monitoring = False
        self.known_devices = set()
        self.callbacks = []
        self.whitelist = set()
        
    def get_current_usb_devices(self) -> List[Dict]:
        """Get list of currently connected USB devices"""
        devices = []
        
        try:
            if self.is_windows:
                # Use WMIC on Windows
                result = subprocess.run(
                    ['wmic', 'path', 'Win32_USBHub', 'get', 'DeviceID,Description'],
                    capture_output=True,
                    text=True
                )
                
                lines = result.stdout.strip().split('\n')[1:]
                for line in lines:
                    if line.strip():
                        devices.append({'id': line.strip(), 'type': 'usb'})
                        
            elif self.is_linux:
                # Use lsusb on Linux
                result = subprocess.run(
                    ['lsusb'],
                    capture_output=True,
                    text=True
                )
                
                for line in result.stdout.strip().split('\n'):
                    if line:
                        devices.append({'id': line.strip(), 'type': 'usb'})
        
        except Exception as e:
            print(f"⚠️  Error getting USB devices: {e}")
        
        return devices
    
    def initialize_known_devices(self):
        """Initialize the list of known USB devices"""
        current = self.get_current_usb_devices()
        self.known_devices = set([d['id'] for d in current])
        print(f"✅ Initialized with {len(self.known_devices)} known USB device(s)")
    
    def detect_usb_change(self) -> Dict[str, List]:
        """Detect USB device changes (additions/removals)"""
        current = set([d['id'] for d in self.get_current_usb_devices()])
        
        added = current - self.known_devices
        removed = self.known_devices - current
        
        return {
            'added': list(added),
            'removed': list(removed)
        }
    
    def register_callback(self, callback: Callable, event_type: str = "any"):
        """Register a callback function for USB events"""
        self.callbacks.append({
            'function': callback,
            'type': event_type  # 'added', 'removed', or 'any'
        })
        print(f"✅ Registered callback for: {event_type}")
    
    def start_monitoring(self, interval: float = 1.0):
        """Start monitoring USB devices"""
        if self.monitoring:
            print("⚠️  Monitoring already active")
            return
        
        self.monitoring = True
        self.initialize_known_devices()
        
        print(f"👁️  USB monitoring started (interval: {interval}s)")
        print("Press Ctrl+C to stop...")
        
        try:
            while self.monitoring:
                time.sleep(interval)
                
                changes = self.detect_usb_change()
                
                if changes['added']:
                    print(f"\n⚠️  USB DEVICE ADDED:")
                    for device in changes['added']:
                        print(f"    + {device}")
                    
                    # Execute callbacks
                    for cb in self.callbacks:
                        if cb['type'] in ['added', 'any']:
                            cb['function']('added', changes['added'])
                    
                    # Update known devices
                    self.known_devices.update(changes['added'])
                
                if changes['removed']:
                    print(f"\n⚠️  USB DEVICE REMOVED:")
                    for device in changes['removed']:
                        print(f"    - {device}")
                    
                    # Execute callbacks
                    for cb in self.callbacks:
                        if cb['type'] in ['removed', 'any']:
                            cb['function']('removed', changes['removed'])
                    
                    # Update known devices
                    self.known_devices.difference_update(changes['removed'])
                    
        except KeyboardInterrupt:
            print("\n🛑 Monitoring stopped")
            self.monitoring =False
    
    def stop_monitoring(self):
        """Stop USB monitoring"""
        self.monitoring = False
        print("🛑 USB monitoring stopped")
    
    def emergency_shutdown(self, reason: str = "USB Kill Switch Triggered"):
        """Immediately shutdown the system"""
        print(f"\n🚨 EMERGENCY SHUTDOWN: {reason}")
        
        try:
            if self.is_windows:
                # Immediate shutdown on Windows
                subprocess.run(['shutdown', '/s', '/t', '0', '/f'], check=False)
            elif self.is_linux:
                # Immediate shutdown on Linux
                subprocess.run(['sudo', 'shutdown', 'now'], check=False)
        except Exception as e:
            print(f"❌ Shutdown failed: {e}")
    
    def emergency_ram_wipe(self):
        """Attempt to wipe RAM before shutdown"""
        print("🧹 Wiping RAM...")
        
        try:
            # Allocate and fill memory with random data
            import array
            chunks = []
            
            # Try to allocate progressively larger chunks
            for _ in range(100):
                try:
                    chunk = array.array('B', os.urandom(10 * 1024 * 1024))  # 10MB chunks
                    chunks.append(chunk)
                except MemoryError:
                    break
            
            print(f"✅ Allocated and filled {len(chunks) * 10}MB")
            
        except Exception as e:
            print(f"⚠️  RAM wipe error: {e}")
    
    def setup_kill_switch(self, action: str = "shutdown"):
        """Setup USB kill switch that triggers on ANY USB change"""
        print(f"💣 Setting up USB kill switch (action: {action})")
        
        def kill_switch_callback(event_type, devices):
            print(f"\n🚨 KILL SWITCH TRIGGERED: {event_type}")
            print(f"    Devices: {devices}")
            
            if action == "shutdown":
                self.emergency_shutdown("USB kill switch triggered")
            elif action == "wipe":
                self.emergency_ram_wipe()
                self.emergency_shutdown("After RAM wipe")
            elif action == "lock":
                self.lock_system()
        
        self.register_callback(kill_switch_callback, 'any')
        print("✅ Kill switch armed")
        
        # Start monitoring in a thread
        monitor_thread = threading.Thread(target=self.start_monitoring, args=(0.5,))
        monitor_thread.daemon = True
        monitor_thread.start()
        
        return monitor_thread
    
    def lock_system(self):
        """Lock the system immediately"""
        print("🔒 Locking system...")
        
        try:
            if self.is_windows:
                subprocess.run(['rundll32.exe', 'user32.dll,LockWorkStation'])
            elif self.is_linux:
                # Try common lock commands
                for cmd in [['xdg-screensaver', 'lock'], 
                           ['gnome-screensaver-command', '--lock'],
                           ['loginctl', 'lock-session']]:
                    try:
                        subprocess.run(cmd, check=False)
                        break
                    except:
                        continue
        except Exception as e:
            print(f"⚠️  Lock failed: {e}")
    
    def whitelist_current_devices(self):
        """Add all current devices to whitelist"""
        current = self.get_current_usb_devices()
        self.whitelist.update([d['id'] for d in current])
        print(f"✅ Whitelisted {len(current)} current device(s)")
    
    def check_whitelist(self, device_id: str) -> bool:
        """Check if device is whitelisted"""
        return device_id in self.whitelist
    
    def monitor_with_whitelist(self):
        """Monitor USB devices and alert on non-whitelisted devices"""
        print("🛡️  Monitoring with whitelist protection...")
        
        def whitelist_callback(event_type, devices):
            if event_type == 'added':
                for device in devices:
                    if not self.check_whitelist(device):
                        print(f"\n🚨 UNAUTHORIZED USB DEVICE: {device}")
                        print("    Device not in whitelist!")
                        # Could trigger additional actions here
        
        self.register_callback(whitelist_callback, 'added')
        self.start_monitoring()
    
    def simulate_buskill(self, cable_device: str = ""):
        """
        Simulate BusKill behavior - trigger on specific USB removal
        BusKill uses a USB cable as a tripwire
        """
        print("💣 BusKill Mode: Waiting for tripwire removal...")
        
        if not cable_device:
            # Use first available USB device as tripwire
            devices = self.get_current_usb_devices()
            if devices:
                cable_device = devices[0]['id']
                print(f"    Tripwire device: {cable_device[:50]}...")
            else:
                print("❌ No USB devices found for tripwire")
                return
        
        def buskill_callback(event_type, devices):
            if event_type == 'removed':
                for device in devices:
                    if cable_device in device:
                        print(f"\n🚨 TRIPWIRE PULLED!")
                        self.emergency_shutdown("BusKill tripwire activated")
        
        self.register_callback(buskill_callback, 'removed')
        self.start_monitoring()
    
    def log_usb_activity(self, log_file: str = "usb_activity.log"):
        """Log all USB activity to a file"""
        def log_callback(event_type, devices):
            timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
            with open(log_file, 'a') as f:
                f.write(f"[{timestamp}] {event_type.upper()}: {devices}\n")
            print(f"📝 Logged to {log_file}")
        
        self.register_callback(log_callback, 'any')
        print(f"✅ USB activity logging to: {log_file}")
    
    def get_usb_stats(self) -> Dict:
        """Get USB device statistics"""
        return {
            'known_devices': len(self.known_devices),
            'whitelisted': len(self.whitelist),
            'monitoring': self.monitoring,
            'callbacks': len(self.callbacks)
        }


if __name__ == "__main__":
    phantom = USBPhantom()
    print("🔌 USB Phantom - USB Monitoring & Kill Switch")
    print("=" * 60)
    
    # Show current devices
    devices = phantom.get_current_usb_devices()
    print(f"\nCurrently connected USB devices: {len(devices)}")
    for i, dev in enumerate(devices[:5], 1):
        print(f"  {i}. {dev['id'][:80]}")
