#!/usr/bin/env python3
# Copyright (C) 2026 Ayush - PhantomTrace Project
# Licensed under GPL-3.0 - See LICENSE file for details
"""
PhantomTrace - Automatic Installer
Handles venv setup and dependency installation
"""

import os
import sys
import subprocess
import platform
from pathlib import Path


class PhantomTraceInstaller:
    def __init__(self):
        self.project_root = Path(__file__).parent
        self.venv_path = self.project_root / '.venv'
        self.python_bin = self._get_python_cmd()
        self.is_windows = platform.system() == 'Windows'
        
    def _get_python_cmd(self):
        """Get python executable based on OS"""
        if platform.system() == 'Windows':
            return str(self.venv_path / 'Scripts' / 'python.exe')
        else:
            return str(self.venv_path / 'bin' / 'python')
    
    def print_header(self, text):
        """Print formatted header"""
        print(f"\n{'='*60}")
        print(f"  {text}")
        print(f"{'='*60}\n")
    
    def create_venv(self):
        """Create virtual environment"""
        self.print_header("Creating Virtual Environment")
        
        if self.venv_path.exists():
            print(f"✓ Virtual environment already exists at {self.venv_path}")
            return True
        
        try:
            subprocess.check_call([sys.executable, '-m', 'venv', str(self.venv_path)])
            print(f"✓ Virtual environment created successfully")
            return True
        except Exception as e:
            print(f"✗ Failed to create virtual environment: {e}")
            return False
    
    def upgrade_pip(self):
        """Upgrade pip"""
        self.print_header("Upgrading pip")
        
        try:
            subprocess.check_call([
                self.python_bin, '-m', 'pip', 'install', 
                '--upgrade', 'pip', 'setuptools', 'wheel'
            ])
            print("✓ pip upgraded successfully")
            return True
        except Exception as e:
            print(f"✗ Failed to upgrade pip: {e}")
            return False
    
    def install_requirements(self):
        """Install all requirements"""
        self.print_header("Installing Dependencies")
        
        requirements_file = self.project_root / 'requirements.txt'
        
        if not requirements_file.exists():
            print("✗ requirements.txt not found")
            return False
        
        try:
            subprocess.check_call([
                self.python_bin, '-m', 'pip', 'install', 
                '-r', str(requirements_file)
            ])
            print("✓ Dependencies installed successfully")
            return True
        except Exception as e:
            print(f"✗ Failed to install dependencies: {e}")
            return False
    
    def install_package(self):
        """Install PhantomTrace in development mode"""
        self.print_header("Installing PhantomTrace")
        
        try:
            subprocess.check_call([
                self.python_bin, '-m', 'pip', 'install', '-e', '.'
            ], cwd=str(self.project_root))
            print("✓ PhantomTrace installed successfully")
            return True
        except Exception as e:
            print(f"✗ Failed to install PhantomTrace: {e}")
            return False
    
    def test_installation(self):
        """Test if installation was successful"""
        self.print_header("Testing Installation")
        
        test_code = "from phantomtrace import QuantumDecay, TemporalFog, ShadowClone; print('✓ All modules working!')"
        
        try:
            subprocess.check_call([
                self.python_bin, '-c', test_code
            ])
            return True
        except Exception as e:
            print(f"✗ Installation test failed: {e}")
            return False
    
    def print_next_steps(self):
        """Print next steps"""
        self.print_header("Installation Complete!")
        
        if self.is_windows:
            activate_cmd = f"{self.venv_path / 'Scripts' / 'activate.bat'}"
        else:
            activate_cmd = f"source {self.venv_path / 'bin' / 'activate'}"
        
        print(f"To activate the virtual environment, run:")
        print(f"  {activate_cmd}")
        print(f"\nThen you can use PhantomTrace:")
        print(f"  phantomtrace --help")
        print(f"\nOr import it in Python:")
        print(f"  python -c 'from phantomtrace import QuantumDecay'")
        print()
    
    def install(self):
        """Run full installation"""
        print("\n")
        print(r"""
          ╔═══════════════════════════════════════════════╗
          ║      PhantomTrace - Installation Wizard       ║
          ╚═══════════════════════════════════════════════╝
        """)
        
        steps = [
            ("Virtual Environment", self.create_venv),
            ("pip Upgrade", self.upgrade_pip),
            ("Dependencies", self.install_requirements),
            ("PhantomTrace", self.install_package),
            ("Verification", self.test_installation),
        ]
        
        for name, step in steps:
            if not step():
                print(f"\n✗ Installation failed at: {name}")
                return False
        
        self.print_next_steps()
        return True


def main():
    installer = PhantomTraceInstaller()
    
    try:
        success = installer.install()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n\n✗ Installation cancelled by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n✗ Unexpected error: {e}")
        sys.exit(1)


if __name__ == '__main__':
    main()
