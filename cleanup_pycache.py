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
    print("PhantomTrace - Python Cache Cleanup")
    print("="*70)
    print(f"Scanning directory: {root_dir}")
    print()
    
    for root, dirs, files in os.walk(root_dir):
        # Skip virtual environment if requested
        if exclude_venv and '.venv' in root:
            continue
        if exclude_venv and 'venv' in root:
            continue
        if exclude_venv and 'env' in root:
            continue
            
        # Remove __pycache__ directories
        if '__pycache__' in dirs:
            pycache_path = Path(root) / '__pycache__'
            try:
                # Calculate size before removal
                for item in pycache_path.rglob('*'):
                    if item.is_file():
                        total_size += item.stat().st_size
                
                shutil.rmtree(pycache_path)
                removed_dirs += 1
                print(f"✓ Removed: {pycache_path}")
            except Exception as e:
                print(f"✗ Failed to remove {pycache_path}: {e}")
        
        # Remove .pyc and .pyo files
        for file in files:
            if file.endswith(('.pyc', '.pyo')):
                file_path = Path(root) / file
                try:
                    file_size = file_path.stat().st_size
                    total_size += file_size
                    file_path.unlink()
                    removed_files += 1
                    print(f"✓ Removed: {file_path}")
                except Exception as e:
                    print(f"✗ Failed to remove {file_path}: {e}")
    
    print()
    print("="*70)
    print("Cleanup Complete")
    print("="*70)
    print(f"Directories removed: {removed_dirs}")
    print(f"Files removed: {removed_files}")
    print(f"Space freed: {total_size / 1024:.2f} KB")
    print("="*70)
    
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
