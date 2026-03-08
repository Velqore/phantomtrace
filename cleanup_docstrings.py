#!/usr/bin/env python3
import re
from pathlib import Path

modules = ['metadata_phantom.py', 'process_phantom.py', 'credential_phantom.py', 
           'event_phantom.py', 'av_phantom.py', 'usb_phantom.py', 'disk_phantom.py',
           'registry_phantom.py', 'browser_phantom.py', 'panic_button.py']

base = Path('phantomtrace/modules')

for mod in modules:
    filepath = base / mod
    if filepath.exists():
        with open(filepath, 'r') as f:
            content = f.read()
        
        content = re.sub(r'(def \w+\([^)]*\)[^:]*(?:\->[^:]*)?):\s*\n\s+"""[^"]*"""', 
                        r'\1:', content, flags=re.MULTILINE | re.DOTALL)
        
        with open(filepath, 'w') as f:
            f.write(content)
        print(f"✅ {mod}")
    else:
        print(f"⚠️  {mod} not found")

print("\n✅ All modules refactored!")
