# PhantomTrace - Quick Start Guide

Welcome to PhantomTrace! This guide will help you get started quickly.

## Installation

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)

### Install Steps

```bash
# Navigate to the project directory
cd Anti-forensics

# Install the package
pip install -r requirements.txt
pip install -e .
```

## First Steps

### 1. Test Installation

```bash
# Run a simple test
python -c "from phantomtrace import QuantumDecay; print('✓ PhantomTrace installed successfully!')"
```

### 2. Run Your First Example

```bash
# Run the complete workflow example
python examples/complete_workflow.py
```

This will demonstrate all major features in action.

## Basic Usage

### Command Line Interface

PhantomTrace includes a CLI for quick operations:

```bash
# Secure file deletion
phantomtrace quantum-delete sensitive_file.txt --passes 7

# Timestamp manipulation
phantomtrace temporal-fog document.pdf --days-offset -30 --randomize

# Generate decoys
phantomtrace shadow-clone --type mixed --count 50

# Log manipulation
phantomtrace log-smoke system.log --entries 50

# Inject entropy
phantomtrace entropy-inject file.dat --type slack
```

### Python API

Use PhantomTrace programmatically:

```python
from phantomtrace import QuantumDecay, TemporalFog, ShadowClone

# Secure file deletion
qd = QuantumDecay()
qd.quantum_delete("sensitive.txt", passes=7)

# Timestamp manipulation
tf = TemporalFog()
tf.apply_fog("document.pdf", days_offset=-30, randomize=True)

# Generate decoys
sc = ShadowClone()
decoys = sc.create_believable_decoys(count=50)
```

## Module Overview

### 1. Quantum Decay
**Purpose:** Secure file deletion with non-deterministic patterns

```python
from phantomtrace import QuantumDecay

qd = QuantumDecay(verify=True, secure_rename=True)
qd.quantum_delete("file.txt", passes=7)
print(qd.get_stats())
```

### 2. Temporal Fog
**Purpose:** Sophisticated timestamp manipulation

```python
from phantomtrace import TemporalFog

tf = TemporalFog()
tf.apply_fog("file.txt", days_offset=-30, break_correlation=True)
```

### 3. Shadow Clones
**Purpose:** Generate believable decoy files and activities

```python
from phantomtrace import ShadowClone

sc = ShadowClone(output_dir="./decoys")
decoys = sc.create_believable_decoys(activity_type='mixed', count=50)
```

### 4. Memory Whisper
**Purpose:** RAM-only operations with secure memory wiping

```python
from phantomtrace import MemoryWhisper

mw = MemoryWhisper()
addr = mw.allocate_secure_memory(1024 * 1024)  # 1MB
# ... use memory ...
mw.secure_wipe_memory(addr, 1024 * 1024)
```

### 5. Data Camouflage
**Purpose:** Multi-layer steganography with polymorphic encoding

```python
from phantomtrace import DataCamouflage

dc = DataCamouflage()
dc.hide_in_image(
    secret_data=b"secret message",
    cover_image_path="cover.png",
    output_path="stego.png"
)
```

### 6. Log Smoke
**Purpose:** Log manipulation and noise injection

```python
from phantomtrace import LogSmoke

ls = LogSmoke()
ls.inject_noise("system.log", num_entries=50)
```

### 7. Entropy Injector
**Purpose:** Inject randomness to break pattern analysis

```python
from phantomtrace import EntropyInjector

ei = EntropyInjector()
ei.inject_file_slack("file.dat")
ei.poison_file_carver("./directory", num_files=100)
```

## Common Workflows

### Privacy Protection Workflow

```python
from phantomtrace import QuantumDecay, TemporalFog, EntropyInjector

# 1. Modify timestamps before deletion
tf = TemporalFog()
tf.apply_fog("sensitive.txt", randomize=True)

# 2. Inject entropy
ei = EntropyInjector()
ei.inject_file_slack("sensitive.txt")

# 3. Securely delete
qd = QuantumDecay()
qd.quantum_delete("sensitive.txt", passes=7)
```

### Decoy Generation Workflow

```python
from phantomtrace import ShadowClone, TemporalFog

# 1. Create decoys
sc = ShadowClone()
decoys = sc.create_believable_decoys(count=100)

# 2. Apply realistic timestamps
tf = TemporalFog()
for decoy in decoys:
    tf.apply_fog(decoy, randomize=True)
```

## Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=phantomtrace

# Run specific test file
pytest tests/test_modules.py -v
```

## Best Practices

1. **Always backup important data** before using destructive operations
2. **Test in isolated environments** first
3. **Understand the legal implications** in your jurisdiction
4. **Use appropriate pass counts** for your threat model
5. **Combine multiple techniques** for better results

## Troubleshooting

### Import Errors

```bash
# Make sure PhantomTrace is installed
pip install -e .

# Check Python version
python --version  # Should be 3.8+
```

### Permission Errors

Some operations require elevated privileges:

```bash
# Windows (Run as Administrator)
# Right-click Command Prompt → Run as Administrator

# Linux/Mac
sudo python script.py
```

### Module Not Found

```bash
# Install missing dependencies
pip install -r requirements.txt

# For optional features
pip install scapy  # Network features
pip install pillow  # Image steganography
```

## Next Steps

1. **Explore Examples:** Check the `examples/` directory
2. **Read Documentation:** See `docs/` for detailed information
3. **Read Research:** Check `docs/research.md` for academic background
4. **Contribute:** See `CONTRIBUTING.md` to contribute

## Getting Help

- **Issues:** Open an issue on GitHub
- **Questions:** Start a discussion
- **Security:** Report privately

## Disclaimer

⚠️ **Important:** This tool is for educational, research, and authorized security testing only. Users are responsible for ensuring their use complies with applicable laws.

---

**Happy researching! Use PhantomTrace responsibly.**
