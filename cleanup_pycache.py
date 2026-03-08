#!/usr/bin/env python3
# Copyright (C) 2026 Ayush - PhantomTrace Project
# Licensed under GPL-3.0 - See LICENSE file for details
"""
PhantomTrace - Python Cache Cleanup Script

Removes all __pycache__ directories and .pyc/.pyo files from the project.
Useful for keeping the repository clean and reducing fingerprints.
"""

import os
import shutil
from pathlib import Path

def cleanup_pycache(root_dir=None, exclude_venv=True):
    if root_dir is None:
        root_dir = Path(__file__).parent
    else:
        root_dir = Path(root_dir)
    
    removed_dirs = 0
    removed_files = 0
    total_size = 0
    
    print("="*70)
    print("🧹 PhantomTrace - Python Cache Cleanup")
    print("="*70)
    print(f"Scanning: {root_dir}\n")
    
    # Patterns to clean
    cache_patterns = {
        '__pycache__': 'Python cache directories',
        '.pytest_cache': 'Pytest cache',
    }
    
    egg_info_pattern = '*.egg-info'
    pyc_patterns = ['*.pyc', '*.pyo', '*.pyd']
    
    # Remove __pycache__ and .pytest_cache directories
    print("Removing directories:")
    for item in root_dir.rglob('*'):
        if exclude_venv and '.venv' in item.parts:
            continue
        if exclude_venv and 'venv' in item.parts:
            continue
        
        # Check cache directories
        if item.is_dir():
            for pattern, desc in cache_patterns.items():
                if item.name == pattern:
                    try:
                        size = sum(f.stat().st_size for f in item.rglob('*') if f.is_file())
                        shutil.rmtree(item)
                        print(f"  ✓ {item.relative_to(root_dir)} ({desc})")
                        removed_dirs += 1
                        total_size += size
                    except Exception as e:
                        print(f"  ✗ {item.relative_to(root_dir)}: {e}")
            
            # Check .egg-info directories
            if item.name.endswith('.egg-info'):
                try:
                    size = sum(f.stat().st_size for f in item.rglob('*') if f.is_file())
                    shutil.rmtree(item)
                    print(f"  ✓ {item.relative_to(root_dir)} (Egg info)")
                    removed_dirs += 1
                    total_size += size
                except Exception as e:
                    print(f"  ✗ {item.relative_to(root_dir)}: {e}")
    
    # Remove compiled Python files
    print("\nRemoving files:")
    for pattern in pyc_patterns:
        for item in root_dir.rglob(pattern):
            if exclude_venv and '.venv' in item.parts:
                continue
            if exclude_venv and 'venv' in item.parts:
                continue
            try:
                size = item.stat().st_size
                item.unlink()
                print(f"  ✓ {item.relative_to(root_dir)} ({pattern})")
                removed_files += 1
                total_size += size
            except Exception as e:
                print(f"  ✗ {item.relative_to(root_dir)}: {e}")
    
    # Summary
    print("\n" + "="*70)
    print(f"✅ Cleanup Complete!")
    print(f"   • Directories removed: {removed_dirs}")
    print(f"   • Files removed: {removed_files}")
    print(f"   • Space freed: {total_size / 1024:.2f} KB")
    print("="*70)
    print("\n💡 Prevention Tips:")
    print("   • Your .gitignore is already configured")
    print("   • Run: git rm -r --cached __pycache__ (if tracked)")
    print("   • Run this script before committing changes\n")
    
    return removed_dirs, removed_files, total_size

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(
        description="Clean Python cache files from PhantomTrace project"
    )
    parser.add_argument(
        '--include-venv',
        action='store_true',
        help='Also clean cache from virtual environment (not recommended)'
    )
    parser.add_argument(
        '--path',
        type=str,
        default=None,
        help='Custom path to clean (default: current project directory)'
    )
    
    args = parser.parse_args()
    
    cleanup_pycache(
        root_dir=args.path,
        exclude_venv=not args.include_venv
    )
