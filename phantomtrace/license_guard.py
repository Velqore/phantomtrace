#!/usr/bin/env python3
# Copyright (C) 2026 Ayush - PhantomTrace Project
# Licensed under GPL-3.0 - See LICENSE file for details

import hashlib
import sys
from pathlib import Path

PROJECT_FINGERPRINT = "PhantomTrace-GPL3-2026-Ayush"
LICENSE_HASH = "f3b9a8c2d7e1a6b5c4d3e2f1a0b9c8d7e6f5a4b3c2d1e0f9a8b7c6d5e4f3a2b1"

class LicenseGuard:
    
    def __init__(self):
        self.project_root = Path(__file__).parent.parent
        self.license_file = self.project_root / "LICENSE"
        self.verified = False
        
    def verify_license(self):
        if not self.license_file.exists():
            self._license_violation("LICENSE file not found")
            return False
            
        try:
            content = self.license_file.read_text(encoding='utf-8')
            if "GNU GENERAL PUBLIC LICENSE" not in content:
                self._license_violation("Invalid license detected")
                return False
            if "PhantomTrace" not in content:
                self._license_violation("Project attribution removed")
                return False
            if "Ayush" not in content:
                self._license_violation("Author attribution removed")
                return False
                
            self.verified = True
            return True
        except Exception:
            return False
    
    def get_code_fingerprint(self):
        return hashlib.sha256(PROJECT_FINGERPRINT.encode()).hexdigest()[:16]
    
    def _license_violation(self, reason):
        print(f"\n{'='*70}", file=sys.stderr)
        print("LICENSE VIOLATION DETECTED", file=sys.stderr)
        print(f"{'='*70}", file=sys.stderr)
        print(f"Reason: {reason}", file=sys.stderr)
        print("\nThis software is licensed under GPL-3.0", file=sys.stderr)
        print("Original Author: Ayush", file=sys.stderr)
        print("Project: PhantomTrace", file=sys.stderr)
        print("\nYou must:", file=sys.stderr)
        print("1. Keep the original LICENSE file intact", file=sys.stderr)
        print("2. Provide attribution to the original author", file=sys.stderr)
        print("3. License any derivative works under GPL-3.0", file=sys.stderr)
        print(f"{'='*70}\n", file=sys.stderr)
    
    def enforce_attribution(self):
        if not self.verify_license():
            print("\nWARNING: License verification failed", file=sys.stderr)
            print("This project is GPL-3.0 licensed by Ayush", file=sys.stderr)

_guard = LicenseGuard()
_guard.enforce_attribution()

def get_license_status():
    return _guard.verified

def get_project_fingerprint():
    return _guard.get_code_fingerprint()

__all__ = ['get_license_status', 'get_project_fingerprint', 'LicenseGuard']
