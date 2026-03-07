#!/usr/bin/env python3
# Copyright (C) 2026 Ayush - PhantomTrace Project
# Licensed under GPL-3.0 - See LICENSE file for details
"""
Log Smoke - Add fake entries to log files

Injects realistic-looking log entries to create confusion.
Tries to match the format so it doesn't look tampered with.
"""

import secrets
import re
from datetime import datetime, timedelta
from pathlib import Path
from typing import List, Dict


class LogSmoke:
    """Inject fake log entries that look real."""
    
    LOG_TYPES = {
        'apache': r'(\d+\.\d+\.\d+\.\d+) - - \[(.*?)\] "(.*?)" (\d+) (\d+)',
        'nginx': r'(\d+\.\d+\.\d+\.\d+) - - \[(.*?)\] "(.*?)" (\d+) (\d+) "(.*?)" "(.*?)"',
        'syslog': r'(\w+\s+\d+ \d+:\d+:\d+) (\w+) (.*?): (.*)',
        'windows': r'(\d+/\d+/\d+ \d+:\d+:\d+ [AP]M), (.*?), (.*?), (.*)',
    }
    
    def __init__(self):
        self.modifications = []
        self.original_backups = {}
    
    def inject_noise(self, log_file, num_entries=50, preserve_format=True):
        """Add fake log entries to a log file."""
        try:
            log_path = Path(log_file)
            
            self._backup_file(log_path)  # backup first
            log_type = self._detect_log_type(log_path)
            
            # Read current logs
            with open(log_path, 'r', encoding='utf-8', errors='ignore') as f:
                existing_logs = f.readlines()
            
            # Make fake entries
            fake_entries = self._generate_fake_entries(log_type, num_entries, existing_logs)
            merged_logs = self._merge_logs(existing_logs, fake_entries)
            
            # Write it back
            with open(log_path, 'w', encoding='utf-8') as f:
                f.writelines(merged_logs)
            
            self.modifications.append({
                'file': str(log_path),
                'type': 'noise_injection',
                'entries_added': num_entries,
                'timestamp': datetime.now().isoformat()
            })
            
            return True
            
        except Exception as e:
            print(f"Error injecting log noise: {e}")
            return False
    
    def _detect_log_type(self, log_path: Path) -> str:
        """Detect log file format."""
        with open(log_path, 'r', encoding='utf-8', errors='ignore') as f:
            sample = f.read(1024)
        
        for log_type, pattern in self.LOG_TYPES.items():
            if re.search(pattern, sample):
                return log_type
        
        return 'generic'
    
    def _generate_fake_entries(
        self,
        log_type: str,
        count: int,
        existing_logs: List[str]
    ) -> List[str]:
        """Generate believable fake log entries."""
        fake_entries = []
        
        # Analyze existing patterns
        time_pattern = self._extract_time_pattern(existing_logs)
        
        for _ in range(count):
            if log_type == 'apache' or log_type == 'nginx':
                entry = self._generate_web_log_entry(log_type, time_pattern)
            elif log_type == 'syslog':
                entry = self._generate_syslog_entry(time_pattern)
            elif log_type == 'windows':
                entry = self._generate_windows_log_entry(time_pattern)
            else:
                entry = self._generate_generic_log_entry(time_pattern)
            
            fake_entries.append(entry)
        
        return fake_entries
    
    def _extract_time_pattern(self, logs: List[str]) -> Dict:
        """Extract temporal patterns from existing logs."""
        # Simplified - would analyze actual time distributions
        return {
            'start_time': datetime.now() - timedelta(days=30),
            'end_time': datetime.now(),
            'peak_hours': [9, 10, 11, 14, 15, 16]  # Business hours
        }
    
    def _generate_web_log_entry(self, log_type: str, time_pattern: Dict) -> str:
        """Generate fake web server log entry."""
        # Random IP
        ip = f"{secrets.randbelow(256)}.{secrets.randbelow(256)}.{secrets.randbelow(256)}.{secrets.randbelow(256)}"
        
        # Random timestamp within pattern
        timestamp = self._random_timestamp(time_pattern)
        timestamp_str = timestamp.strftime('%d/%b/%Y:%H:%M:%S +0000')
        
        # Random request
        methods = ['GET', 'POST', 'HEAD']
        paths = ['/index.html', '/api/data', '/images/logo.png', '/css/style.css', '/about']
        method = secrets.choice(methods)
        path = secrets.choice(paths)
        protocol = 'HTTP/1.1'
        
        # Random status codes (weighted towards success)
        status_codes = [200] * 70 + [404] * 15 + [301] * 10 + [500] * 5
        status = secrets.choice(status_codes)
        
        # Random size
        size = secrets.randbelow(50000) + 100
        
        if log_type == 'apache':
            return f'{ip} - - [{timestamp_str}] "{method} {path} {protocol}" {status} {size}\n'
        else:  # nginx
            user_agents = [
                'Mozilla/5.0 (Windows NT 10.0; Win64; x64)',
                'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)',
                'Mozilla/5.0 (X11; Linux x86_64)'
            ]
            ua = secrets.choice(user_agents)
            referer = secrets.choice(['-', 'https://www.google.com', 'https://www.example.com'])
            return f'{ip} - - [{timestamp_str}] "{method} {path} {protocol}" {status} {size} "{referer}" "{ua}"\n'
    
    def _generate_syslog_entry(self, time_pattern: Dict) -> str:
        """Generate fake syslog entry."""
        timestamp = self._random_timestamp(time_pattern)
        timestamp_str = timestamp.strftime('%b %d %H:%M:%S')
        
        hostname = 'localhost'
        
        processes = ['sshd', 'systemd', 'kernel', 'cron', 'postfix']
        process = secrets.choice(processes)
        
        messages = [
            'Connection accepted',
            'Service started',
            'Process completed successfully',
            'Configuration reloaded',
            'Task executed'
        ]
        message = secrets.choice(messages)
        
        return f'{timestamp_str} {hostname} {process}: {message}\n'
    
    def _generate_windows_log_entry(self, time_pattern: Dict) -> str:
        """Generate fake Windows event log entry."""
        timestamp = self._random_timestamp(time_pattern)
        timestamp_str = timestamp.strftime('%m/%d/%Y %I:%M:%S %p')
        
        types = ['Information', 'Warning', 'Error']
        log_type = secrets.choice(types)
        
        sources = ['Service Control Manager', 'System', 'Application', 'Security']
        source = secrets.choice(sources)
        
        event_ids = [1000, 1001, 7036, 7040, 4624, 4625]
        event_id = secrets.choice(event_ids)
        
        return f'{timestamp_str}, {log_type}, {source}, {event_id}\n'
    
    def _generate_generic_log_entry(self, time_pattern: Dict) -> str:
        """Generate generic log entry."""
        timestamp = self._random_timestamp(time_pattern)
        timestamp_str = timestamp.strftime('%Y-%m-%d %H:%M:%S')
        
        levels = ['INFO', 'DEBUG', 'WARNING', 'ERROR']
        level = secrets.choice(levels)
        
        messages = [
            'Operation completed',
            'Request processed',
            'Task executed',
            'Event triggered',
            'Action performed'
        ]
        message = secrets.choice(messages)
        
        return f'[{timestamp_str}] {level}: {message}\n'
    
    def _random_timestamp(self, time_pattern: Dict) -> datetime:
        """Generate random timestamp following pattern."""
        start = time_pattern['start_time']
        end = time_pattern['end_time']
        
        delta = end - start
        random_seconds = secrets.randbelow(int(delta.total_seconds()))
        
        timestamp = start + timedelta(seconds=random_seconds)
        
        # Prefer peak hours
        if secrets.randbelow(100) < 70:  # 70% chance
            peak_hour = secrets.choice(time_pattern['peak_hours'])
            timestamp = timestamp.replace(hour=peak_hour)
        
        return timestamp
    
    def _merge_logs(self, existing: List[str], fake: List[str]) -> List[str]:
        """Merge fake entries with existing logs maintaining chronological order."""
        all_logs = existing + fake
        
        # Try to sort by timestamp (simplified)
        # In production, would parse timestamps more carefully
        return all_logs
    
    def _backup_file(self, filepath: Path):
        """Create backup of original file."""
        backup_path = filepath.with_suffix(filepath.suffix + '.backup')
        
        with open(filepath, 'rb') as src:
            with open(backup_path, 'wb') as dst:
                dst.write(src.read())
        
        self.original_backups[str(filepath)] = str(backup_path)
    
    def poison_pattern_detection(self, log_file: str) -> bool:
        """
        Add entries specifically designed to poison machine learning
        and pattern detection tools.
        
        Args:
            log_file: Path to log file
        
        Returns:
            True if successful
        """
        try:
            # Add adversarial examples that look normal but poison ML models
            # This would implement adversarial machine learning techniques
            pass
            
        except Exception as e:
            print(f"Error poisoning pattern detection: {e}")
            return False
    
    def restore_backup(self, log_file: str) -> bool:
        """Restore original log file from backup."""
        try:
            if log_file in self.original_backups:
                backup = Path(self.original_backups[log_file])
                original = Path(log_file)
                
                with open(backup, 'rb') as src:
                    with open(original, 'wb') as dst:
                        dst.write(src.read())
                
                return True
            else:
                print("No backup found for this file")
                return False
                
        except Exception as e:
            print(f"Error restoring backup: {e}")
            return False
