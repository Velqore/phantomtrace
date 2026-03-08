#!/usr/bin/env python3
# Copyright (C) 2026 Ayush - PhantomTrace Project
# Licensed under GPL-3.0 - See LICENSE file for details
"""
Credential Phantom - Credential extraction and clearing
Inspired by tools: chntpw, lazagne, Mimipenguin
"""

import os
import sys
import subprocess
import platform
import hashlib
import sqlite3
import json
from pathlib import Path
from typing import List, Dict, Optional

class CredentialPhantom:
    """
    Credential operations for anti-forensics:
    - Extract stored passwords (browser, application)
    - Clear credential caches
    - Dump Linux user passwords (mimipenguin-style)
    - Clear Windows credential manager
    - Reset SAM database hashes (offline)
    - Clear browser saved passwords
    - Remove SSH keys and known_hosts
    """
    
    def __init__(self):
        self.is_windows = sys.platform.startswith('win')
        self.is_linux = sys.platform.startswith('linux')
        self.extracted_creds = []
        
    def clear_browser_passwords(self, browser: str = "all") -> int:
        """Clear saved passwords from browsers"""
        cleared = 0
        
        browsers = ['chrome', 'firefox', 'edge', 'brave'] if browser == "all" else [browser]
        
        for browser_name in browsers:
            if self.is_windows:
                cleared += self._clear_browser_windows(browser_name)
            elif self.is_linux:
                cleared += self._clear_browser_linux(browser_name)
        
        print(f"✅ Cleared passwords from {cleared} browser(s)")
        return cleared
    
    def _clear_browser_windows(self, browser: str) -> int:
        """Clear browser data on Windows"""
        try:
            username = os.getenv('USERNAME')
            paths = {
                'chrome': f'C:\\Users\\{username}\\AppData\\Local\\Google\\Chrome\\User Data\\Default\\Login Data',
                'edge': f'C:\\Users\\{username}\\AppData\\Local\\Microsoft\\Edge\\User Data\\Default\\Login Data',
                'brave': f'C:\\Users\\{username}\\AppData\\Local\\BraveSoftware\\Brave-Browser\\User Data\\Default\\Login Data',
                'firefox': f'C:\\Users\\{username}\\AppData\\Roaming\\Mozilla\\Firefox\\Profiles'
            }
            
            db_path = paths.get(browser)
            if not db_path or not os.path.exists(db_path):
                return 0
            
            if browser == 'firefox':
                # Firefox uses different structure
                return self._clear_firefox_passwords(db_path)
            else:
                # Chrome-based browsers
                return self._clear_chromium_passwords(db_path)
                
        except Exception as e:
            print(f"⚠️  Error clearing {browser}: {e}")
            return 0
    
    def _clear_browser_linux(self, browser: str) -> int:
        """Clear browser data on Linux"""
        try:
            home = os.path.expanduser('~')
            paths = {
                'chrome': f'{home}/.config/google-chrome/Default/Login Data',
                'firefox': f'{home}/.mozilla/firefox',
                'brave': f'{home}/.config/BraveSoftware/Brave-Browser/Default/Login Data'
            }
            
            db_path = paths.get(browser)
            if not db_path or not os.path.exists(db_path):
                return 0
            
            if browser == 'firefox':
                return self._clear_firefox_passwords(db_path)
            else:
                return self._clear_chromium_passwords(db_path)
                
        except Exception as e:
            print(f"⚠️  Error clearing {browser}: {e}")
            return 0
    
    def _clear_chromium_passwords(self, db_path: str) -> int:
        """Clear passwords from Chromium-based browsers"""
        try:
            # Copy database (might be locked)
            import shutil
            temp_db = db_path + '.tmp'
            shutil.copy2(db_path, temp_db)
            
            # Clear logins table
            conn = sqlite3.connect(temp_db)
            cursor = conn.cursor()
            cursor.execute("DELETE FROM logins")
            conn.commit()
            conn.close()
            
            # Replace original
            shutil.move(temp_db, db_path)
            
            print(f"✅ Cleared Chromium passwords: {db_path}")
            return 1
            
        except Exception as e:
            print(f"⚠️  Could not clear chromium passwords: {e}")
            return 0
    
    def _clear_firefox_passwords(self, profile_dir: str) -> int:
        """Clear Firefox passwords"""
        try:
            cleared = 0
            
            # Find profile directories
            if os.path.isdir(profile_dir):
                for profile in os.listdir(profile_dir):
                    profile_path = os.path.join(profile_dir, profile)
                    if not os.path.isdir(profile_path):
                        continue
                    
                    # Remove key4.db and logins.json
                    key_db = os.path.join(profile_path, 'key4.db')
                    logins_json = os.path.join(profile_path, 'logins.json')
                    
                    if os.path.exists(key_db):
                        os.remove(key_db)
                        cleared += 1
                    
                    if os.path.exists(logins_json):
                        os.remove(logins_json)
                        cleared += 1
            
            print(f"✅ Cleared Firefox credential files: {cleared}")
            return 1 if cleared > 0 else 0
            
        except Exception as e:
            print(f"⚠️  Could not clear Firefox passwords: {e}")
            return 0
    
    def clear_windows_credential_manager(self) -> bool:
        """Clear Windows Credential Manager"""
        if not self.is_windows:
            print("⚠️  Windows Credential Manager only on Windows")
            return False
        
        try:
            # Use cmdkey to list and delete credentials
            result = subprocess.run(['cmdkey', '/list'], 
                                   capture_output=True, text=True)
            
            # Parse targets
            targets = []
            for line in result.stdout.split('\n'):
                if 'Target:' in line:
                    target = line.split('Target:')[1].strip()
                    targets.append(target)
            
            # Delete each credential
            for target in targets:
                subprocess.run(['cmdkey', f'/delete:{target}'], 
                              capture_output=True)
            
            print(f"✅ Cleared {len(targets)} Windows credentials")
            return True
            
        except Exception as e:
            print(f"❌ Failed to clear Windows credentials: {e}")
            return False
    
    def clear_ssh_artifacts(self) -> int:
        """Clear SSH keys and known_hosts"""
        try:
            home = os.path.expanduser('~')
            ssh_dir = os.path.join(home, '.ssh')
            
            if not os.path.exists(ssh_dir):
                print("⚠️  No .ssh directory found")
                return 0
            
            cleared = 0
            
            # Clear known_hosts
            known_hosts = os.path.join(ssh_dir, 'known_hosts')
            if os.path.exists(known_hosts):
                with open(known_hosts, 'w') as f:
                    f.write('')
                print("✅ Cleared known_hosts")
                cleared += 1
            
            # Optionally remove private keys (commented for safety)
            # for key_file in ['id_rsa', 'id_dsa', 'id_ecdsa', 'id_ed25519']:
            #     key_path = os.path.join(ssh_dir, key_file)
            #     if os.path.exists(key_path):
            #         os.remove(key_path)
            #         cleared += 1
            
            return cleared
            
        except Exception as e:
            print(f"❌ Failed to clear SSH artifacts: {e}")
            return 0
    
    def dump_linux_passwords(self) -> List[Dict]:
        """
        Attempt to dump current user passwords from memory (mimipenguin-style)
        Requires root privileges
        """
        if not self.is_linux:
            print("⚠️  Linux password dumping only on Linux")
            return []
        
        if os.geteuid() != 0:
            print("⚠️  Root privileges required for password dumping")
            return []
        
        try:
            passwords = []
            
            # Check common processes that may contain passwords
            targets = ['gnome-keyring', 'gdm-password', 'lightdm', 'vsftpd']
            
            for proc in psutil.process_iter(['name', 'pid']):
                if proc.info['name'] in targets:
                    # Read process memory (simplified)
                    pid = proc.info['pid']
                    mem_path = f'/proc/{pid}/mem'
                    maps_path = f'/proc/{pid}/maps'
                    
                    print(f"🔍 Found target process: {proc.info['name']} (PID: {pid})")
                    passwords.append({
                        'process': proc.info['name'],
                        'pid': pid,
                        'note': 'Memory dump would occur here (requires root)'
                    })
            
            return passwords
            
        except Exception as e:
            print(f"❌ Password dumping failed: {e}")
            return []
    
    def clear_windows_sam_backup(self) -> bool:
        """
        Clear SAM backup files (Windows)
        Requires admin privileges
        """
        if not self.is_windows:
            print("⚠️  SAM clearing only on Windows")
            return False
        
        try:
            sam_locations = [
                'C:\\Windows\\repair\\SAM',
                'C:\\Windows\\System32\\config\\RegBack\\SAM'
            ]
            
            cleared = 0
            for sam_path in sam_locations:
                if os.path.exists(sam_path):
                    try:
                        os.remove(sam_path)
                        cleared += 1
                        print(f"✅ Removed SAM backup: {sam_path}")
                    except PermissionError:
                        print(f"⚠️  Permission denied: {sam_path}")
            
            return cleared > 0
            
        except Exception as e:
            print(f"❌ Failed to clear SAM backups: {e}")
            return False
    
    def extract_browser_cookies(self, browser: str = "chrome") -> List[Dict]:
        """
        Extract cookies from browser (for demonstration)
        """
        try:
            if self.is_windows:
                username = os.getenv('USERNAME')
                cookie_paths = {
                    'chrome': f'C:\\Users\\{username}\\AppData\\Local\\Google\\Chrome\\User Data\\Default\\Cookies',
                    'edge': f'C:\\Users\\{username}\\AppData\\Local\\Microsoft\\Edge\\User Data\\Default\\Cookies'
                }
            else:
                home = os.path.expanduser('~')
                cookie_paths = {
                    'chrome': f'{home}/.config/google-chrome/Default/Cookies'
                }
            
            cookie_db = cookie_paths.get(browser)
            if not cookie_db or not os.path.exists(cookie_db):
                print(f"⚠️  Cookie database not found for {browser}")
                return []
            
            # Copy and read (simplified - actual decryption needed for real data)
            import shutil
            temp_db = cookie_db + '.tmp'
            shutil.copy2(cookie_db, temp_db)
            
            conn = sqlite3.connect(temp_db)
            cursor = conn.cursor()
            cursor.execute("SELECT host_key, name, encrypted_value FROM cookies LIMIT 10")
            cookies = cursor.fetchall()
            conn.close()
            
            os.remove(temp_db)
            
            print(f"✅ Extracted {len(cookies)} cookies (encrypted)")
            return [{'host': c[0], 'name': c[1]} for c in cookies]
            
        except Exception as e:
            print(f"❌ Cookie extraction failed: {e}")
            return []
    
    def clear_all_credentials(self) -> Dict[str, int]:
        """Clear all credential artifacts"""
        results = {}
        
        print("🧹 Clearing all credential artifacts...")
        
        # Browser passwords
        results['browsers'] = self.clear_browser_passwords("all")
        
        # SSH artifacts
        results['ssh'] = self.clear_ssh_artifacts()
        
        # Windows-specific
        if self.is_windows:
            results['windows_creds'] = 1 if self.clear_windows_credential_manager() else 0
            results['sam_backups'] = 1 if self.clear_windows_sam_backup() else 0
        
        print("\n✅ Credential clearing complete")
        return results
    
    def get_report(self) -> List[Dict]:
        """Get report of extracted credentials"""
        return self.extracted_creds.copy()


if __name__ == "__main__":
    phantom = CredentialPhantom()
    print("🔑 Credential Phantom - Credential Management Module")
    print("=" * 60)
