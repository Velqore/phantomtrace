#!/usr/bin/env python3
# Copyright (C) 2026 Ayush - PhantomTrace Project
# Licensed under GPL-3.0 - See LICENSE file for details
"""
PhantomTrace Protection Verification Script

Verifies that all code protection measures are properly implemented.
"""

import sys
from pathlib import Path

def check_license_file():
    """Check if LICENSE file exists and contains GPL-3.0"""
    license_path = Path(__file__).parent / "LICENSE"
    
    if not license_path.exists():
        return False, "LICENSE file not found"
    
    content = license_path.read_text(encoding='utf-8')
    
    checks = {
        "GNU GENERAL PUBLIC LICENSE": "GPL-3.0 text",
        "Version 3": "GPL version 3",
        "Ayush": "Author attribution",
        "PhantomTrace": "Project name"
    }
    
    missing = []
    for text, desc in checks.items():
        if text not in content:
            missing.append(desc)
    
    if missing:
        return False, f"Missing in LICENSE: {', '.join(missing)}"
    
    return True, "LICENSE file valid"

def check_copyright_headers():
    """Check if all Python files have copyright headers"""
    project_root = Path(__file__).parent
    python_files = list(project_root.rglob("*.py"))
    
    # Exclude virtual environment
    python_files = [f for f in python_files if '.venv' not in str(f) and 'venv' not in str(f)]
    
    files_without_header = []
    for file in python_files:
        content = file.read_text(encoding='utf-8', errors='ignore')
        
        if "Copyright (C) 2026 Ayush" not in content:
            files_without_header.append(str(file.relative_to(project_root)))
    
    if files_without_header:
        return False, f"{len(files_without_header)} files missing headers: {files_without_header[:3]}"
    
    return True, f"All {len(python_files)} Python files have copyright headers"

def check_license_guard():
    """Check if license guard module exists and is imported"""
    guard_path = Path(__file__).parent / "phantomtrace" / "license_guard.py"
    
    if not guard_path.exists():
        return False, "license_guard.py not found"
    
    init_path = Path(__file__).parent / "phantomtrace" / "__init__.py"
    init_content = init_path.read_text(encoding='utf-8')
    
    if "from .license_guard import" not in init_content:
        return False, "license_guard not imported in __init__.py"
    
    return True, "License guard active"

def check_package_metadata():
    """Check package metadata"""
    sys.path.insert(0, str(Path(__file__).parent))
    
    try:
        import phantomtrace
        
        checks = {
            "__license__": ("GPL-3.0", phantomtrace.__license__),
            "__author__": ("Ayush", phantomtrace.__author__),
        }
        
        for attr, (expected, actual) in checks.items():
            if expected not in actual:
                return False, f"{attr} does not contain '{expected}'"
        
        return True, f"Package metadata correct (v{phantomtrace.__version__})"
    except Exception as e:
        return False, f"Failed to import: {e}"

def check_readme():
    """Check README has GPL-3.0 and ownership info"""
    readme_path = Path(__file__).parent / "README.md"
    
    if not readme_path.exists():
        return False, "README.md not found"
    
    content = readme_path.read_text(encoding='utf-8')
    
    checks = {
        "GPL-3.0": "GPL-3.0 license mention",
        "Ayush": "Author name",
        "Copyright": "Copyright notice",
    }
    
    missing = []
    for text, desc in checks.items():
        if text not in content:
            missing.append(desc)
    
    if missing:
        return False, f"Missing in README: {', '.join(missing)}"
    
    return True, "README has ownership info"

def check_gitignore():
    """Check .gitignore blocks __pycache__"""
    gitignore_path = Path(__file__).parent / ".gitignore"
    
    if not gitignore_path.exists():
        return False, ".gitignore not found"
    
    content = gitignore_path.read_text(encoding='utf-8')
    
    if "__pycache__" not in content:
        return False, "__pycache__ not in .gitignore"
    
    return True, ".gitignore blocks cache files"

def main():
    print("="*70)
    print("PhantomTrace - Code Protection Verification")
    print("="*70)
    print()
    
    checks = [
        ("LICENSE File", check_license_file),
        ("Copyright Headers", check_copyright_headers),
        ("License Guard", check_license_guard),
        ("Package Metadata", check_package_metadata),
        ("README Documentation", check_readme),
        (".gitignore", check_gitignore),
    ]
    
    results = []
    for name, check_func in checks:
        try:
            passed, message = check_func()
            results.append((name, passed, message))
        except Exception as e:
            results.append((name, False, f"Error: {e}"))
    
    # Print results
    for name, passed, message in results:
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"{status} | {name}")
        print(f"       {message}")
        print()
    
    # Summary
    passed_count = sum(1 for _, p, _ in results if p)
    total_count = len(results)
    
    print("="*70)
    if passed_count == total_count:
        print(f"🎉 ALL CHECKS PASSED ({passed_count}/{total_count})")
        print()
        print("Your code is fully protected:")
        print("  • GPL-3.0 license enforced")
        print("  • Copyright headers on all files")
        print("  • License verification active")
        print("  • Ownership clearly documented")
        print()
        print("Nobody can steal your code without violating GPL-3.0!")
    else:
        print(f"⚠️  SOME CHECKS FAILED ({passed_count}/{total_count} passed)")
        print()
        print("Please fix the failed checks to ensure full protection.")
    print("="*70)
    
    return 0 if passed_count == total_count else 1

if __name__ == "__main__":
    sys.exit(main())
