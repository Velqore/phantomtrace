# Installation Guide - PhantomTrace v0.2.0

## Quick Start (Recommended)

The easiest way to install PhantomTrace with all dependencies:

```bash
# Clone repository
git clone https://github.com/yourusername/phantomtrace.git
cd phantomtrace

# Run automatic installer
python install.py
```

The installer will:
- Create a Python virtual environment (`venv/`)
- Upgrade pip and setuptools
- Install all required dependencies
- Install PhantomTrace in development mode
- Verify all modules load correctly
- Display next steps

**That's it!** PhantomTrace is ready to use.

---

## Manual Installation

If you prefer more control over the installation process:

### Step 1: Create Virtual Environment

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/macOS
python3 -m venv venv
source venv/bin/activate
```

### Step 2: Install Dependencies

```bash
# Core dependencies
pip install -r requirements.txt

# Or with optional features
pip install -e ".[network,dev]"
```

### Step 3: Verify Installation

```bash
python -c "from phantomtrace import QuantumDecay; print('PhantomTrace installed successfully!')"
```

---

## Installation Variants

### Minimal Installation (Core modules only)

```bash
pip install -e .
```

**Includes:** All 10 core modules
**Size:** ~50 MB

### Network Support (Include scapy)

```bash
pip install -e ".[network]"
```

**Adds:** Network traffic obfuscation, packet manipulation
**Requires:** Scapy library

### Homomorphic Encryption Support

```bash
pip install -e ".[he]"
```

**Adds:** TenSEAL for fully homomorphic encryption
**Requires:** C++ build tools (may take extra time to build)

### Development Installation (All features + testing)

```bash
pip install -e ".[network,he,dev]"
```

**Includes:** All modules + pytest, black, flake8
**Best for:** Contributing to PhantomTrace

---

## System Requirements

### Minimum Requirements
- **Python:** 3.8 or higher
- **OS:** Windows 10+, Ubuntu 18.04+, macOS 10.14+
- **Disk Space:** 500 MB (with dependencies)
- **RAM:** 2 GB minimum, 4 GB recommended

### For Full Features
- **C++ Compiler:** Visual Studio Build Tools (Windows) or GCC (Linux)
- **Admin/Root Access:** For network modules and some encryption operations
- **OpenSSL:** Installed separately on some systems

### Platform-Specific

**Windows:**
- Python 3.8+ (from python.org)
- Visual Studio Build Tools (or Microsoft C++ Build Tools)
- Admin privilege for network operations

**Linux:**
- Python 3.8+ (via apt/yum)
- Build tools: `sudo apt install build-essential python3-dev`
- For network module: `sudo` access

**macOS:**
- Python 3.8+ (via Homebrew: `brew install python3`)
- Xcode Command Line Tools: `xcode-select --install`
- Intel/Apple Silicon both supported

---

## Troubleshooting

### "Python not found" Error

**Windows:**
```powershell
# Try with python3
python3 install.py

# Or full path
C:\Python311\python.exe install.py
```

**Linux/macOS:**
```bash
# Try with python3
python3 install.py

# Or check Python path
which python3
/usr/bin/python3 install.py
```

### pip Install Failures

**Permission Denied:**
```bash
# Use user-level installation instead of sudo
pip install --user -r requirements.txt
```

**SSL Certificate Error:**
```bash
# Upgrade pip and setuptools
python -m pip install --upgrade pip setuptools
pip install --cert /path/to/cert -r requirements.txt
```

**Module Not Found After Install:**
```bash
# Verify virtual environment is activated
which python  # Should show venv path
python -m pip list  # Should show all packages
```

### Virtual Environment Issues

**"venv not recognized" (Windows):**
```powershell
# Use full path
venv\Scripts\python.exe -m pip list

# Or activate properly
.\venv\Scripts\Activate.ps1
```

**"command not found: python" (Linux/macOS):**
```bash
# Check python3 location
python3 --version

# Use python3 instead
python3 -m venv venv
```

**"ImportError: No module named...":**
```bash
# Ensure venv is activated
source venv/bin/activate  # Linux/macOS
venv\Scripts\activate      # Windows

# Reinstall requirements
pip install -r requirements.txt
```

### Encryption Module Issues

**"cryptography not installed":**
```bash
pip install cryptography>=41.0.0
```

**"libnacl import error":**
```bash
# Linux: Install libsodium
sudo apt install libsodium-dev

# macOS: Install via Homebrew
brew install libsodium

# Windows: Requires Visual C++ runtime
# Download from: https://support.microsoft.com/en-us/help/2977003
```

**"tenseal not available":**
- TenSEAL requires C++ compiler and can take 5-10 minutes to build
- Only needed for advanced FHE features
- Optional: `pip install -e ".[he]"` (with build tools)

### Network Module Issues

**"scapy not installed":**
```bash
pip install scapy>=2.5.0

# Or with network support
pip install -e ".[network]"
```

**"No module named 'scapy'":**
```bash
# Verify venv activated
source venv/bin/activate

# Reinstall scapy specifically
pip install scapy
```

---

## Verify Installation

After installation, verify everything works:

```bash
# Test 1: Import all modules
python -c "from phantomtrace import *; print('All modules imported successfully')"

# Test 2: Run CLI help
phantomtrace --help

# Test 3: Test Quantum Decay
python -c "
from phantomtrace import QuantumDecay
qd = QuantumDecay()
noise = qd.generate_quantum_noise(100)
print(f'Generated quantum noise: {len(noise)} bytes')
"

# Test 4: Test Encryption
python -c "
from phantomtrace import AdvancedEncryption
ae = AdvancedEncryption()
ct, n, t = ae.encrypt_aes_gcm(b'test', 'password123')
print(f'Encryption successful: {len(ct)} byte ciphertext')
"
```

---

## Post-Installation Setup

### Set Environment Variables

For production use, configure these environment variables:

**Linux/macOS:**
```bash
# In ~/.bashrc or ~/.zshrc
export PHANTOMTRACE_WORK_DIR="/tmp/phantomtrace_work"
export PHANTOMTRACE_LOG_LEVEL="INFO"

# Reload shell
source ~/.bashrc
```

**Windows PowerShell:**
```powershell
# Permanent setup
[Environment]::SetEnvironmentVariable("PHANTOMTRACE_WORK_DIR", "C:\Temp\phantomtrace_work", "User")
[Environment]::SetEnvironmentVariable("PHANTOMTRACE_LOG_LEVEL", "INFO", "User")

# Temporary (current session only)
$env:PHANTOMTRACE_WORK_DIR = "C:\Temp\phantomtrace_work"
```

### Configure CLI

Test the command-line interface:

```bash
# List all commands
phantomtrace --help

# Test specific command help
phantomtrace quantum-delete --help
phantomtrace encrypt-aes --help
phantomtrace secret-share --help
```

---

## Uninstall

To completely remove PhantomTrace:

```bash
# Deactivate virtual environment
deactivate

# Remove venv directory
rm -rf venv          # Linux/macOS
rmdir /s venv        # Windows

# If installed globally (not recommended)
pip uninstall phantomtrace
```

---

## Getting Help

If you encounter issues:

1. **CheckREADME.md** - General overview and quick start
2. **See [docs/](../docs/)** - Full documentation
3. **Search Issues** - GitHub issues may have solutions
4. **File a Bug Report** - Include Python version, OS, and full error message

```bash
# Collect system info for bug reports
python -c "import sys, platform; print(f'{platform.system()} {platform.release()}\nPython {sys.version}')"
pip list
```

---

## Next Steps

After installation:

1. **Read** [ADVANCED_USAGE.md](ADVANCED_USAGE.md) for encryption examples
2. **Explore** [MODULES.md](MODULES.md) for complete API reference
3. **Try** CLI commands: `phantomtrace quantum-delete --help`
4. **Join** the community and contribute!

Happy hacking! 🚀
