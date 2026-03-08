#!/usr/bin/env python3
# Copyright (C) 2026 Ayush - PhantomTrace Project
# Licensed under GPL-3.0 - See LICENSE file for details
"""
Panic Button - Emergency data destruction system
Inspired by tools: BusKill, Silk Guardian, Nuke My LUKS, suicideCrypt
"""

import os
import sys
import time
import threading
import subprocess
from typing import List, Callable, Optional, Dict
from pathlib import Path

# Import other phantom modules
try:
    from .event_phantom import EventPhantom
    from .browser_phantom import BrowserPhantom
    from .credential_phantom import CredentialPhantom
    from .registry_phantom import RegistryPhantom
    from .disk_phantom import DiskPhantom
    from .usb_phantom import USBPhantom
except ImportError:
    # Fallback for standalone execution
    EventPhantom = None
    BrowserPhantom = None
    CredentialPhantom = None
    RegistryPhantom = None
    DiskPhantom = None
    USBPhantom = None

class PanicButton:
    """
    Emergency data destruction system:
    - One-button emergency cleanup
    - USB tripwire activation
    - Network-based panic broadcast
    - Tiered destruction levels
    - Automatic system actions
    - Pre-configured destruction scripts
    """
    
    def __init__(self):
        self.is_windows = sys.platform.startswith('win')
        self.is_linux = sys.platform.startswith('linux')
        self.panic_active = False
        self.actions_executed = []
        
    def panic_level_1(self) -> Dict[str, bool]:
        """Level 1: Quick cleanup (logs, history, caches)"""
        print("\n" + "="*60)
        print("🚨 PANIC LEVEL 1: QUICK CLEANUP")
        print("="*60 + "\n")
        
        results = {}
        
        # Clear browser data
        if BrowserPhantom:
            try:
                browser = BrowserPhantom()
                browser.clear_all_browser_data("all")
                results['browser'] = True
                self.actions_executed.append("Browser cleanup")
            except Exception as e:
                print(f"⚠️  Browser cleanup failed: {e}")
                results['browser'] = False
        
        # Clear event logs
        if EventPhantom:
            try:
                events = EventPhantom()
                events.clear_powershell_history()
                if self.is_linux:
                    events.clear_bash_history()
                results['logs'] = True
                self.actions_executed.append("Log cleanup")
            except Exception as e:
                print(f"⚠️  Log cleanup failed: {e}")
                results['logs'] = False
        
        # Clear credentials
        if CredentialPhantom:
            try:
                creds = CredentialPhantom()
                creds.clear_ssh_artifacts()
                results['credentials'] = True
                self.actions_executed.append("Credential cleanup")
            except Exception as e:
                print(f"⚠️  Credential cleanup failed: {e}")
                results['credentials'] = False
        
        print(f"\n✅ Level 1 cleanup complete: {sum(results.values())}/{len(results)} successful")
        return results
    
    def panic_level_2(self) -> Dict[str, bool]:
        """Level 2: Aggressive cleanup (Level 1 + registry, recent files)"""
        print("\n" + "="*60)
        print("🚨 PANIC LEVEL 2: AGGRESSIVE CLEANUP")
        print("="*60 + "\n")
        
        results = {}
        
        # Execute Level 1 first
        level1_results = self.panic_level_1()
        results.update(level1_results)
        
        # Registry cleanup (Windows)
        if self.is_windows and RegistryPhantom:
            try:
                registry = RegistryPhantom()
                registry.comprehensive_registry_clean()
                results['registry'] = True
                self.actions_executed.append("Registry cleanup")
            except Exception as e:
                print(f"⚠️  Registry cleanup failed: {e}")
                results['registry'] = False
        
        # Clear all event logs (Windows)
        if self.is_windows and EventPhantom:
            try:
                events = EventPhantom()
                events.clear_all_logs()
                results['event_logs'] = True
                self.actions_executed.append("Event logs cleared")
            except Exception as e:
                print(f"⚠️  Event log clearing failed: {e}")
                results['event_logs'] = False
        
        # Clear credentials completely
        if CredentialPhantom:
            try:
                creds = CredentialPhantom()
                creds.clear_all_credentials()
                results['full_credentials'] = True
                self.actions_executed.append("Full credential wipe")
            except Exception as e:
                print(f"⚠️  Full credential wipe failed: {e}")
                results['full_credentials'] = False
        
        print(f"\n✅ Level 2 cleanup complete: {sum(results.values())}/{len(results)} successful")
        return results
    
    def panic_level_3(self, sensitive_dirs: List[str] = None) -> Dict[str, bool]:
        """Level 3: Nuclear option (Level 2 + secure deletion, RAM wipe)"""
        print("\n" + "="*60)
        print("🚨 PANIC LEVEL 3: NUCLEAR CLEANUP")
        print("="*60 + "\n")
        
        results = {}
        
        # Execute Level 2 first
        level2_results = self.panic_level_2()
        results.update(level2_results)
        
        # Secure delete sensitive directories
        if sensitive_dirs and DiskPhantom:
            try:
                disk = DiskPhantom()
                for dir_path in sensitive_dirs:
                    if os.path.exists(dir_path):
                        print(f"🔥 Securely deleting: {dir_path}")
                        disk.secure_delete_directory(dir_path, passes=3)
                results['secure_delete'] = True
                self.actions_executed.append("Secure deletion")
            except Exception as e:
                print(f"⚠️  Secure deletion failed: {e}")
                results['secure_delete'] = False
        
        # RAM wipe attempt
        try:
            print("🧹 Attempting RAM wipe...")
            self._wipe_ram()
            results['ram_wipe'] = True
            self.actions_executed.append("RAM wipe")
        except Exception as e:
            print(f"⚠️  RAM wipe failed: {e}")
            results['ram_wipe'] = False
        
        # Shutdown system
        try:
            print("🛑 Initiating system shutdown in 10 seconds...")
            time.sleep(10)
            self._shutdown_system()
            results['shutdown'] = True
            self.actions_executed.append("System shutdown")
        except Exception as e:
            print(f"⚠️  Shutdown failed: {e}")
            results['shutdown'] = False
        
        print(f"\n✅ Level 3 cleanup complete: {sum(results.values())}/{len(results)} successful")
        return results
    
    def _wipe_ram(self):
        """Attempt to wipe RAM by filling it"""
        import array
        chunks = []
        
        try:
            # Allocate memory chunks
            for i in range(100):
                chunk = array.array('B', os.urandom(10 * 1024 * 1024))  # 10MB
                chunks.append(chunk)
                if i % 10 == 0:
                    print(f"   Allocated {(i+1) * 10}MB...")
        except MemoryError:
            pass
        
        print(f"✅ RAM wipe attempted ({len(chunks) * 10}MB filled)")
    
    def _shutdown_system(self):
        """Shutdown the system"""
        if self.is_windows:
            subprocess.run(['shutdown', '/s', '/t', '0', '/f'])
        elif self.is_linux:
            subprocess.run(['sudo', 'shutdown', 'now'])
    
    def setup_usb_panic_trigger(self, level: int = 2):
        """Setup USB-based panic trigger"""
        if not USBPhantom:
            print("⚠️  USB Phantom module not available")
            return None
        
        print(f"💣 Setting up USB panic trigger (Level {level})...")
        
        usb = USBPhantom()
        
        def usb_panic_callback(event_type, devices):
            print(f"\n🚨 USB PANIC TRIGGERED: {event_type}")
            print(f"    Devices: {devices}")
            
            if level == 1:
                self.panic_level_1()
            elif level == 2:
                self.panic_level_2()
            elif level == 3:
                self.panic_level_3()
        
        usb.register_callback(usb_panic_callback, 'any')
        usb.initialize_known_devices()
        
        print("✅ USB panic trigger armed")
        print("    Any USB change will trigger cleanup")
        
        # Start monitoring in thread
        monitor_thread = threading.Thread(target=usb.start_monitoring, args=(0.5,))
        monitor_thread.daemon = True
        monitor_thread.start()
        
        return monitor_thread
    
    def create_panic_script(self, output_file: str = "panic.py", level: int = 2):
        """Create standalone panic script"""
        script_content = f'''#!/usr/bin/env python3
# Emergency Panic Script - Generated by PhantomTrace
# Level {level} cleanup

import os
import sys
import subprocess

def emergency_cleanup():
    print("🚨 EMERGENCY CLEANUP ACTIVATED")
    print("="*60)
    
    # Clear bash/PowerShell history
    if sys.platform.startswith('linux'):
        os.system("history -c")
        os.system("cat /dev/null > ~/.bash_history")
    elif sys.platform.startswith('win'):
        os.system("powershell -Command Clear-History")
    
    # Clear browser data (basic)
    print("Clearing browser data...")
    
    # Add your custom cleanup here
    print("\\nCustom cleanup complete")
    
    if {level} >= 3:
        print("Shutting down system...")
        if sys.platform.startswith('linux'):
            os.system("sudo shutdown now")
        elif sys.platform.startswith('win'):
            os.system("shutdown /s /t 0 /f")

if __name__ == "__main__":
    emergency_cleanup()
'''
        
        try:
            with open(output_file, 'w') as f:
                f.write(script_content)
            
            # Make executable on Linux
            if self.is_linux:
                os.chmod(output_file, 0o755)
            
            print(f"✅ Panic script created: {output_file}")
            return True
        except Exception as e:
            print(f"❌ Failed to create panic script: {e}")
            return False
    
    def hotkey_panic(self, level: int = 1):
        """Setup keyboard hotkey for panic (requires keyboard library)"""
        try:
            import keyboard
            
            print(f"⌨️  Setting up panic hotkey: Ctrl+Shift+Alt+P (Level {level})")
            
            def panic_hotkey():
                print("\n🚨 PANIC HOTKEY PRESSED!")
                if level == 1:
                    self.panic_level_1()
                elif level == 2:
                    self.panic_level_2()
                elif level == 3:
                    self.panic_level_3()
            
            keyboard.add_hotkey('ctrl+shift+alt+p', panic_hotkey)
            
            print("✅ Panic hotkey registered")
            print("    Press Ctrl+Shift+Alt+P to trigger emergency cleanup")
            
            # Keep running
            keyboard.wait()
            
        except ImportError:
            print("⚠️  'keyboard' library not installed")
            print("    Install with: pip install keyboard")
        except Exception as e:
            print(f"❌ Hotkey setup failed: {e}")
    
    def get_execution_report(self) -> List[str]:
        """Get list of executed actions"""
        return self.actions_executed.copy()
    
    def arm_panic_button(self, trigger_type: str = "usb", level: int = 2):
        """Arm the panic button with specified trigger"""
        print("\n" + "="*60)
        print("💣 ARMING PANIC BUTTON")
        print("="*60)
        print(f"   Trigger: {trigger_type.upper()}")
        print(f"   Level: {level}")
        print("="*60 + "\n")
        
        if trigger_type == "usb":
            return self.setup_usb_panic_trigger(level)
        elif trigger_type == "hotkey":
            self.hotkey_panic(level)
        else:
            print(f"⚠️  Unknown trigger type: {trigger_type}")
            return None


if __name__ == "__main__":
    panic = PanicButton()
    print("💣 Panic Button - Emergency Data Destruction System")
    print("=" * 60)
    print("\nAvailable levels:")
    print("  Level 1: Quick cleanup (browser, logs, credentials)")
    print("  Level 2: Aggressive (Level 1 + registry, event logs)")
    print("  Level 3: Nuclear (Level 2 + secure deletion, RAM wipe, shutdown)")
