#!/usr/bin/env python3
# Copyright (C) 2026 Ayush - PhantomTrace Project
# Licensed under GPL-3.0 - See LICENSE file for details
"""
Registry Phantom - Windows Registry manipulation
Windows-specific anti-forensics for registry artifacts
"""

import os
import sys
import subprocess
from typing import List, Dict, Optional

class RegistryPhantom:
    """
    Windows Registry operations:
    - Clear recent files/docs
    - Remove run/RunOnce entries
    - Clear UserAssist (tracks program execution)
    - Remove typed URLs/paths
    - Clear MRU (Most Recently Used) lists
    - Delete shellbags (folder viewing history)
    - Remove Windows Timeline data
    - Clear Jump Lists
    """
    
    def __init__(self):
        if not sys.platform.startswith('win'):
            print("⚠️  Registry Phantom requires Windows")
            self.is_windows = False
        else:
            self.is_windows = True
        
        self.cleaned_keys = []
    
    def clear_recent_docs(self) -> bool:
        """Clear recent documents from registry"""
        if not self.is_windows:
            return False
        
        keys_to_clear = [
            'HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\Explorer\\RecentDocs',
            'HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\Explorer\\ComDlg32\\OpenSavePidlMRU',
            'HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\Explorer\\ComDlg32\\LastVisitedPidlMRU'
        ]
        
        cleared = 0
        for key in keys_to_clear:
            try:
                result = subprocess.run(
                    ['reg', 'delete', key, '/f'],
                    capture_output=True,
                    text=True
                )
                if result.returncode == 0:
                    cleared += 1
                    self.cleaned_keys.append(key)
            except:
                pass
        
        if cleared > 0:
            print(f"✅ Cleared {cleared} recent document registry keys")
            return True
        return False
    
    def clear_run_mru(self) -> bool:
        """Clear Run dialog MRU"""
        if not self.is_windows:
            return False
        
        key = 'HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\Explorer\\RunMRU'
        
        try:
            result = subprocess.run(
                ['reg', 'delete', key, '/f'],
                capture_output=True
            )
            
            if result.returncode == 0:
                self.cleaned_keys.append(key)
                print("✅ Cleared Run dialog MRU")
                return True
        except:
            pass
        
        return False
    
    def clear_userassist(self) -> bool:
        """Clear UserAssist (tracks program execution)"""
        if not self.is_windows:
            return False
        
        # UserAssist stores execution history
        base_key = 'HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\Explorer\\UserAssist'
        
        try:
            # Get subkeys
            result = subprocess.run(
                ['reg', 'query', base_key],
                capture_output=True,
                text=True
            )
            
            if result.returncode == 0:
                lines = result.stdout.split('\n')
                cleared = 0
                
                for line in lines:
                    if 'UEME_' in line or '{' in line:
                        subkey = line.strip()
                        if subkey:
                            try:
                                subprocess.run(
                                    ['reg', 'delete', subkey + '\\Count', '/f'],
                                    capture_output=True
                                )
                                cleared += 1
                            except:
                                pass
                
                if cleared > 0:
                    print(f"✅ Cleared UserAssist execution tracking ({cleared} keys)")
                    self.cleaned_keys.append(base_key)
                    return True
        except:
            pass
        
        return False
    
    def clear_typed_urls(self) -> bool:
        """Clear typed URLs in Internet Explorer/Edge"""
        if not self.is_windows:
            return False
        
        keys = [
            'HKCU\\Software\\Microsoft\\Internet Explorer\\TypedURLs',
            'HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\Explorer\\TypedPaths'
        ]
        
        cleared = 0
        for key in keys:
            try:
                result = subprocess.run(
                    ['reg', 'delete', key, '/f'],
                    capture_output=True
                )
                if result.returncode == 0:
                    cleared += 1
                    self.cleaned_keys.append(key)
            except:
                pass
        
        if cleared > 0:
            print(f"✅ Cleared typed URLs/paths")
            return True
        return False
    
    def clear_mru_lists(self) -> int:
        """Clear all MRU (Most Recently Used) lists"""
        if not self.is_windows:
            return 0
        
        mru_locations = [
            'HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\Explorer\\ComDlg32\\OpenSavePidlMRU',
            'HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\Explorer\\ComDlg32\\LastVisitedPidlMRU',
            'HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\Explorer\\RunMRU',
            'HKCU\\Software\\Microsoft\\Search Assistant\\ACMru',
            'HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\Applets\\Wordpad\\Recent File List',
            'HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\Applets\\Paint\\Recent File List'
        ]
        
        cleared = 0
        for key in mru_locations:
            try:
                result = subprocess.run(
                    ['reg', 'delete', key, '/f'],
                    capture_output=True
                )
                if result.returncode == 0:
                    cleared += 1
                    self.cleaned_keys.append(key)
            except:
                pass
        
        if cleared > 0:
            print(f"✅ Cleared {cleared} MRU lists")
        
        return cleared
    
    def clear_shellbags(self) -> bool:
        """Clear shellbags (folder viewing history)"""
        if not self.is_windows:
            return False
        
        shellbag_keys = [
            'HKCU\\Software\\Microsoft\\Windows\\Shell\\BagMRU',
            'HKCU\\Software\\Microsoft\\Windows\\Shell\\Bags',
            'HKCU\\Software\\Classes\\Local Settings\\Software\\Microsoft\\Windows\\Shell\\BagMRU',
            'HKCU\\Software\\Classes\\Local Settings\\Software\\Microsoft\\Windows\\Shell\\Bags'
        ]
        
        cleared = 0
        for key in shellbag_keys:
            try:
                result = subprocess.run(
                    ['reg', 'delete', key, '/f'],
                    capture_output=True
                )
                if result.returncode == 0:
                    cleared += 1
                    self.cleaned_keys.append(key)
            except:
                pass
        
        if cleared > 0:
            print(f"✅ Cleared shellbags ({cleared} keys)")
            return True
        return False
    
    def clear_jump_lists(self) -> bool:
        """Clear Windows Jump Lists"""
        if not self.is_windows:
            return False
        
        try:
            username = os.getenv('USERNAME')
            jump_list_paths = [
                f'C:\\Users\\{username}\\AppData\\Roaming\\Microsoft\\Windows\\Recent\\AutomaticDestinations',
                f'C:\\Users\\{username}\\AppData\\Roaming\\Microsoft\\Windows\\Recent\\CustomDestinations'
            ]
            
            cleared = 0
            for path in jump_list_paths:
                if os.path.exists(path):
                    import shutil
                    try:
                        shutil.rmtree(path)
                        os.makedirs(path, exist_ok=True)
                        cleared += 1
                    except:
                        pass
            
            if cleared > 0:
                print(f"✅ Cleared Jump Lists")
                return True
        except Exception as e:
            print(f"⚠️  Error clearing jump lists: {e}")
        
        return False
    
    def clear_windows_timeline(self) -> bool:
        """Clear Windows Timeline/Activity History"""
        if not self.is_windows:
            return False
        
        key = 'HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\Explorer\\ActivityHistoryCache'
        
        try:
            result = subprocess.run(
                ['reg', 'delete', key, '/f'],
                capture_output=True
            )
            
            if result.returncode == 0:
                self.cleaned_keys.append(key)
                
                # Also delete the database files
                username = os.getenv('USERNAME')
                activity_db = f'C:\\Users\\{username}\\AppData\\Local\\ConnectedDevicesPlatform\\L.{username}\\ActivitiesCache.db'
                
                if os.path.exists(activity_db):
                    try:
                        os.remove(activity_db)
                    except:
                        pass
                
                print("✅ Cleared Windows Timeline")
                return True
        except:
            pass
        
        return False
    
    def clear_prefetch_references(self) -> bool:
        """Clear registry references to prefetch files"""
        if not self.is_windows:
            return False
        
        # Prefetch tracking in registry
        key = 'HKLM\\SYSTEM\\CurrentControlSet\\Control\\Session Manager\\Memory Management\\PrefetchParameters'
        
        try:
            # Disable prefetch temporarily
            subprocess.run(
                ['reg', 'add', key, '/v', 'EnablePrefetcher', '/t', 'REG_DWORD', '/d', '0', '/f'],
                capture_output=True
            )
            
            print("✅ Disabled prefetch tracking")
            return True
        except:
            return False
    
    def comprehensive_registry_clean(self) -> Dict[str, int]:
        """Perform comprehensive registry cleaning"""
        if not self.is_windows:
            print("⚠️  Registry operations require Windows")
            return {}
        
        print("🧹 Starting comprehensive registry cleaning...")
        
        results = {}
        results['recent_docs'] = 1 if self.clear_recent_docs() else 0
        results['run_mru'] = 1 if self.clear_run_mru() else 0
        results['userassist'] = 1 if self.clear_userassist() else 0
        results['typed_urls'] = 1 if self.clear_typed_urls() else 0
        results['mru_lists'] = self.clear_mru_lists()
        results['shellbags'] = 1 if self.clear_shellbags() else 0
        results['jump_lists'] = 1 if self.clear_jump_lists() else 0
        results['timeline'] = 1 if self.clear_windows_timeline() else 0
        
        print("\n✅ Registry cleaning complete")
        return results
    
    def get_report(self) -> List[str]:
        """Get list of cleaned registry keys"""
        return self.cleaned_keys.copy()


if __name__ == "__main__":
    phantom = RegistryPhantom()
    print("📝 Registry Phantom - Windows Registry Cleaning")
    print("=" * 60)
