#!/usr/bin/env python3
# Copyright (C) 2026 Ayush - PhantomTrace Project
# Licensed under GPL-3.0 - See LICENSE file for details
"""
Browser Phantom - Browser forensics artifact cleaning
Inspired by tools: BleachBit, CCleaner, browser forensics tools
"""

import os
import sys
import sqlite3
import shutil
from pathlib import Path
from typing import List, Dict

class BrowserPhantom:
    """
    Browser anti-forensics:
    - Clear browsing history
    - Delete cookies
    - Remove cache
    - Clear download history
    - Delete saved passwords
    - Remove autofill data
    - Clear local storage
    - Delete IndexedDB
    - Remove extensions artifacts
    """
    
    def __init__(self):
        self.is_windows = sys.platform.startswith('win')
        self.cleaned_items = []
        
    def get_browser_data_paths(self, browser: str) -> Dict[str, str]:
        """Get paths to browser data directories"""
        if self.is_windows:
            username = os.getenv('USERNAME')
            base = f'C:\\Users\\{username}\\AppData\\Local'
            roaming = f'C:\\Users\\{username}\\AppData\\Roaming'
            
            paths = {
                'chrome': {
                    'base': f'{base}\\Google\\Chrome\\User Data\\Default',
                    'history': 'History',
                    'cookies': 'Cookies',
                    'cache': f'{base}\\Google\\Chrome\\User Data\\Default\\Cache',
                    'passwords': 'Login Data'
                },
                'edge': {
                    'base': f'{base}\\Microsoft\\Edge\\User Data\\Default',
                    'history': 'History',
                    'cookies': 'Cookies',
                    'cache': f'{base}\\Microsoft\\Edge\\User Data\\Default\\Cache',
                    'passwords': 'Login Data'
                },
                'firefox': {
                    'base': f'{roaming}\\Mozilla\\Firefox\\Profiles',
                    'history': 'places.sqlite',
                    'cookies': 'cookies.sqlite',
                    'passwords': 'logins.json'
                },
                'brave': {
                    'base': f'{base}\\BraveSoftware\\Brave-Browser\\User Data\\Default',
                    'history': 'History',
                    'cookies': 'Cookies',
                    'cache': f'{base}\\BraveSoftware\\Brave-Browser\\User Data\\Default\\Cache'
                }
            }
        else:
            home = os.path.expanduser('~')
            paths = {
                'chrome': {
                    'base': f'{home}/.config/google-chrome/Default',
                    'history': 'History',
                    'cookies': 'Cookies',
                    'cache': f'{home}/.cache/google-chrome/Default',
                    'passwords': 'Login Data'
                },
                'firefox': {
                    'base': f'{home}/.mozilla/firefox',
                    'history': 'places.sqlite',
                    'cookies': 'cookies.sqlite',
                    'passwords': 'logins.json'
                },
                'brave': {
                    'base': f'{home}/.config/BraveSoftware/Brave-Browser/Default',
                    'history': 'History',
                    'cookies': 'Cookies'
                }
            }
        
        return paths.get(browser, {})
    
    def clear_browser_history(self, browser: str = "all") -> int:
        """Clear browser history"""
        browsers = ['chrome', 'firefox', 'edge', 'brave'] if browser == "all" else [browser]
        cleared = 0
        
        for br in browsers:
            paths = self.get_browser_data_paths(br)
            if not paths:
                continue
            
            if br == 'firefox':
                cleared += self._clear_firefox_history(paths)
            else:
                cleared += self._clear_chromium_history(paths, br)
        
        print(f"✅ Cleared history from {cleared} browser(s)")
        return cleared
    
    def _clear_chromium_history(self, paths: Dict, browser_name: str) -> int:
        """Clear history for Chromium-based browsers"""
        try:
            history_path = os.path.join(paths['base'], paths['history'])
            
            if not os.path.exists(history_path):
                return 0
            
            # Copy database
            temp_db = history_path + '.tmp'
            shutil.copy2(history_path, temp_db)
            
            # Clear history tables
            conn = sqlite3.connect(temp_db)
            cursor = conn.cursor()
            
            tables_to_clear = ['urls', 'visits', 'visit_source', 'keyword_search_terms']
            for table in tables_to_clear:
                try:
                    cursor.execute(f"DELETE FROM {table}")
                except:
                    pass
            
            conn.commit()
            conn.close()
            
            # Replace original
            shutil.move(temp_db, history_path)
            
            self.cleaned_items.append(f"{browser_name}_history")
            print(f"✅ Cleared {browser_name} history")
            return 1
            
        except Exception as e:
            print(f"⚠️  Error clearing {browser_name} history: {e}")
            return 0
    
    def _clear_firefox_history(self, paths: Dict) -> int:
        """Clear Firefox history"""
        try:
            base_path = paths['base']
            
            if not os.path.exists(base_path):
                return 0
            
            cleared = 0
            
            # Find profile directories
            for profile in os.listdir(base_path):
                profile_path = os.path.join(base_path, profile)
                if not os.path.isdir(profile_path):
                    continue
                
                places_db = os.path.join(profile_path, paths['history'])
                
                if os.path.exists(places_db):
                    temp_db = places_db + '.tmp'
                    shutil.copy2(places_db, temp_db)
                    
                    conn = sqlite3.connect(temp_db)
                    cursor = conn.cursor()
                    
                    # Clear history tables
                    tables = ['moz_places', 'moz_historyvisits', 'moz_inputhistory']
                    for table in tables:
                        try:
                            cursor.execute(f"DELETE FROM {table}")
                        except:
                            pass
                    
                    conn.commit()
                    conn.close()
                    
                    shutil.move(temp_db, places_db)
                    cleared += 1
            
            if cleared > 0:
                self.cleaned_items.append("firefox_history")
                print(f"✅ Cleared Firefox history")
            
            return 1 if cleared > 0 else 0
            
        except Exception as e:
            print(f"⚠️  Error clearing Firefox history: {e}")
            return 0
    
    def clear_browser_cookies(self, browser: str = "all") -> int:
        """Clear browser cookies"""
        browsers = ['chrome', 'firefox', 'edge', 'brave'] if browser == "all" else [browser]
        cleared = 0
        
        for br in browsers:
            paths = self.get_browser_data_paths(br)
            if not paths:
                continue
            
            cookie_path = os.path.join(paths['base'], paths.get('cookies', 'Cookies'))
            
            if os.path.exists(cookie_path):
                try:
                    temp_db = cookie_path + '.tmp'
                    shutil.copy2(cookie_path, temp_db)
                    
                    conn = sqlite3.connect(temp_db)
                    cursor = conn.cursor()
                    cursor.execute("DELETE FROM cookies")
                    conn.commit()
                    conn.close()
                    
                    shutil.move(temp_db, cookie_path)
                    
                    self.cleaned_items.append(f"{br}_cookies")
                    print(f"✅ Cleared {br} cookies")
                    cleared += 1
                except Exception as e:
                    print(f"⚠️  Error clearing {br} cookies: {e}")
        
        return cleared
    
    def clear_browser_cache(self, browser: str = "all") -> int:
        """Clear browser cache"""
        browsers = ['chrome', 'firefox', 'edge', 'brave'] if browser == "all" else [browser]
        cleared = 0
        
        for br in browsers:
            paths = self.get_browser_data_paths(br)
            if not paths or 'cache' not in paths:
                continue
            
            cache_path = paths['cache']
            
            if os.path.exists(cache_path):
                try:
                    shutil.rmtree(cache_path)
                    os.makedirs(cache_path, exist_ok=True)
                    
                    self.cleaned_items.append(f"{br}_cache")
                    print(f"✅ Cleared {br} cache")
                    cleared += 1
                except Exception as e:
                    print(f"⚠️  Error clearing {br} cache: {e}")
        
        return cleared
    
    def clear_download_history(self, browser: str = "all") -> int:
        """Clear download history"""
        browsers = ['chrome', 'firefox', 'edge', 'brave'] if browser == "all" else [browser]
        cleared = 0
        
        for br in browsers:
            paths = self.get_browser_data_paths(br)
            if not paths:
                continue
            
            if br == 'firefox':
                # Firefox stores downloads in places.sqlite
                base_path = paths['base']
                if os.path.exists(base_path):
                    for profile in os.listdir(base_path):
                        profile_path = os.path.join(base_path, profile)
                        places_db = os.path.join(profile_path,  'places.sqlite')
                        
                        if os.path.exists(places_db):
                            try:
                                temp_db = places_db + '.tmp'
                                shutil.copy2(places_db, temp_db)
                                
                                conn = sqlite3.connect(temp_db)
                                cursor = conn.cursor()
                                cursor.execute("DELETE FROM moz_annos WHERE anno_attribute_id IN (SELECT id FROM moz_anno_attributes WHERE name = 'downloads/destinationFileURI')")
                                conn.commit()
                                conn.close()
                                
                                shutil.move(temp_db, places_db)
                                cleared += 1
                            except:
                                pass
            else:
                # Chromium-based browsers
                history_path = os.path.join(paths['base'], paths['history'])
                
                if os.path.exists(history_path):
                    try:
                        temp_db = history_path + '.tmp'
                        shutil.copy2(history_path, temp_db)
                        
                        conn = sqlite3.connect(temp_db)
                        cursor = conn.cursor()
                        cursor.execute("DELETE FROM downloads")
                        cursor.execute("DELETE FROM downloads_url_chains")
                        conn.commit()
                        conn.close()
                        
                        shutil.move(temp_db, history_path)
                        cleared += 1
                    except:
                        pass
        
        if cleared > 0:
            print(f"✅ Cleared download history from {cleared} browser(s)")
        
        return cleared
    
    def clear_all_browser_data(self, browser: str = "all") -> Dict[str, int]:
        """Clear all browser forensic artifacts"""
        print(f"🧹 Clearing all data from: {browser}")
        
        results = {
            'history': self.clear_browser_history(browser),
            'cookies': self.clear_browser_cookies(browser),
            'cache': self.clear_browser_cache(browser),
            'downloads': self.clear_download_history(browser)
        }
        
        print(f"\n✅ Browser cleaning complete")
        return results
    
    def get_report(self) -> List[str]:
        """Get report of cleaned items"""
        return self.cleaned_items.copy()


if __name__ == "__main__":
    phantom = BrowserPhantom()
    print("🌐 Browser Phantom - Browser Forensics Cleaning")
    print("=" * 60)
