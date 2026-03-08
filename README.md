# PhantomTrace - Advanced Anti-Forensics Toolkit

![License](https://img.shields.io/badge/license-GPL--3.0-red.svg)
![Python](https://img.shields.io/badge/python-3.8+-green.svg)
![Version](https://img.shields.io/badge/version-0.3.0-blue.svg)
![Copyright](https://img.shields.io/badge/copyright-2026%20Ayush-blue.svg)

**Copyright (C) 2026 Ayush@Velqore (Original Creator)**

An open-source, modular anti-forensics toolkit featuring innovative techniques for privacy protection, security research, and penetration testing. Now with **homomorphic encryption** and **advanced authenticated encryption**.

## 🔒 Copyright & License

**This project is protected under GPL-3.0 License.**

- **Original Author**: Ayush|@Velqore
- **Year**: 2026
- **License**: GNU General Public License v3.0

**IMPORTANT**: This software is licensed under GPL-3.0, which means:
- ✅ You CAN use, study, and modify this software
- ✅ You MUST provide attribution to the original author (Ayush|@Velqore)
- ✅ Any derivative works MUST be released under GPL-3.0
- ❌ You CANNOT make this software proprietary/closed-source
- ❌ You CANNOT remove copyright notices or attribution

Anyone found violating the GPL-3.0 license terms will face legal consequences. See [LICENSE](LICENSE) for full details.

## ⚠️ Disclaimer

This tool is designed for:
- Educational purposes
- Security research
- Privacy protection
- Authorized penetration testing
- Digital rights advocacy

**Users are solely responsible for compliance with applicable laws. Unauthorized use may be illegal.**

## 🚀 Features

### Core Anti-Forensics Modules

**1. Quantum Decay**
Time-based multi-pass secure deletion with unpredictable patterns and quantum-inspired randomization.

**2. Temporal Fog**
Sophisticated timestamp manipulation across multiple sources (filesystem, EXIF, registry, logs) with entropy injection.

**3. Shadow Clones**
Generate forensically-convincing decoy files and activities that consume investigator resources.

**4. Memory Whisper**
RAM-only operations with secure memory wiping using cryptographic techniques—data never touches disk.

**5. Data Camouflage**
Multi-layer steganography combined with polymorphic encoding to hide data in images and other media.

**6. Log Smoke**
Sophisticated log manipulation with format-preserving transformation and noise injection.

**7. Network Ghost**
Traffic pattern obfuscation and protocol manipulation to evade DPI and network forensics.

**8. Entropy Injection**
Add cryptographically strong randomness to forensic artifacts and slack space for signature disruption.

### Advanced Encryption (v0.2.0+)

**9. Advanced Encryption**
- **AES-256-GCM**: Authenticated encryption with hardware acceleration
- **ChaCha20-Poly1305**: Stream cipher with built-in authentication
- **Sealed Boxes**: Combine EC key exchange with ChaCha20-Poly1305 for hybrid encryption
- **Argon2 KDF**: Memory-hard key derivation from passphrases

**10. Homomorphic Encryption**
- **Additive Homomorphic**: Perform computations on encrypted data without decryption
- **Secret Sharing**: Shamir-style threshold cryptography for distributed trust
- **Secure Multi-Party Computation**: Enable collaborative encrypted calculations
- **Statistics on Encrypted Data**: Compute sums, averages on ciphertexts

### Phantom Modules (v0.3.0+) - NEW! 🔥

**11. Metadata Phantom**
- Strip EXIF data from images (JPG, PNG, TIFF, etc.)
- Remove PDF metadata (author, creator, timestamps)
- Clean Office document metadata (DOCX, XLSX, PPTX)
- Strip media file metadata (MP3, MP4, etc.)
- Manipulate NTFS timestamps with nanosecond precision
- Inject fake metadata for misdirection
- Batch process entire directories

**12. Process Phantom**
- In-memory code execution without disk artifacts
- Process name spoofing (Linux)
- Parent PID spoofing (Windows)
- Detect hidden processes
- Anti-debugging checks (IsDebuggerPresent, TracerPid)
- Detect analysis tools (IDA, x64dbg, Wireshark, etc.)
- Process hollowing techniques
- Shellcode injection capabilities

**13. Credential Phantom**
- Clear browser saved passwords (Chrome, Firefox, Edge, Brave)
- Wipe Windows Credential Manager
- Clear SSH keys and known_hosts
- Remove browser cookies and autofill data
- Clear SAM backup files (Windows)
- Dump Linux passwords from memory (mimipenguin-style)
- Extract browser cookies for analysis
- Comprehensive credential wiping

**14. Event Phantom**
- Clear Windows event logs (Application, Security, System)
- Clear PowerShell command history
- Clear Bash history (Linux)
- Remove RDP connection logs
- Clear Sysmon logs
- Disable event logging temporarily
- Clear specific event IDs
- Configure log size limits

**15. AV Phantom**
- Detect running AV/EDR products (Defender, CrowdStrike, Carbon Black, etc.)
- Sandbox environment detection
- Virtual machine detection
- Debugger detection
- Sleep acceleration detection
- Check for analysis tools
- Process masquerading techniques
- Polymorphic signature generation

**16. USB Phantom**
- Real-time USB device monitoring
- USB kill switch (tripwire)
- Emergency system shutdown on USB change
- Device whitelisting
- BusKill-style protection
- RAM wipe on disconnect
- USB activity logging
- Callback system for custom actions

**17. Disk Phantom**
- Multi-pass secure file deletion (Gutmann, DoD standards)
- LUKS header destruction (Linux)
- Emergency LUKS nuke for multiple devices
- Free space wiping
- Slack space wiping
- MBR/GPT destruction
- Fill disk with random data
- Shred integration (Linux)

**18. Registry Phantom** (Windows)
- Clear recent documents registry
- Remove Run/Search MRU lists
- Clear UserAssist (program execution tracking)
- Remove typed URLs/paths
- Clear shellbags (folder view history)
- Delete Jump Lists
- Clear Windows Timeline/Activity History
- Disable prefetch tracking
- Comprehensive registry anti-forensics

**19. Browser Phantom**
- Clear browsing history (all major browsers)
- Delete cookies from all browsers
- Remove cache data
- Clear download history
- Remove local storage
- Delete IndexedDB
- Support for Chrome, Firefox, Edge, Brave
- Cross-platform compatibility

**20. Panic Button** 🚨
- **Level 1**: Quick cleanup (browser, logs, credentials)
- **Level 2**: Aggressive cleanup (Level 1 + registry, event logs)
- **Level 3**: Nuclear option (Level 2 + secure deletion, RAM wipe, shutdown)
- USB-triggered emergency cleanup
- Keyboard hotkey activation (Ctrl+Shift+Alt+P)
- Network-based panic broadcast support
- Standalone panic script generation
- Customizable destruction sequences

## 📦 Installation

### Automated Installation (Recommended)

```bash
# Clone the repository
git clone https://github.com/Velqore/phantomtrace.git
cd phantomtrace

# Run automatic installer (handles venv, dependencies, verification)
python install.py
```

The installer will:
- Create an isolated Python virtual environment
- Install all required dependencies
- Verify all modules load correctly
- Provide next steps for usage

### Manual Installation

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate.ps1

# Install from source
pip install -e .

# Or install with optional features
pip install -e ".[he,network,dev]"  # homomorphic encryption, networking, dev tools
```

### Optional Dependencies

- **Network Module**: `pip install scapy` (for traffic manipulation)
- **Homomorphic Encryption**: `pip install tenseal` (for advanced FHE)
- **Development**: `pip install pytest black flake8` (for development)

## 🎯 Quick Start

### Core Modules

```python
from phantomtrace import QuantumDecay, TemporalFog, ShadowClone
from phantomtrace import AdvancedEncryption, HomomorphicEncryption

# Secure file deletion
qd = QuantumDecay()
qd.quantum_delete("sensitive_file.txt", passes=7)

# Timestamp manipulation
tf = TemporalFog()
tf.apply_fog("document.pdf", days_offset=-30)

# Generate decoys
sc = ShadowClone()
sc.create_believable_decoys(activity_type="browsing", count=50)

# Advanced encryption
ae = AdvancedEncryption()
encrypted_data, nonce, tag = ae.encrypt_aes_gcm(b"secret", "password")
decrypted = ae.decrypt_aes_gcm(encrypted_data, nonce, tag, "password")

# Homomorphic encryption (compute on encrypted data)
he = HomomorphicEncryption()
c1 = he.encrypt_additive(5)
c2 = he.encrypt_additive(10)
c_sum = he.add_encrypted(c1, c2)
result = he.decrypt_additive(c_sum)  # Returns 15, never decrypts intermediate values
```

### Phantom Modules (v0.3.0+)

```python
from phantomtrace import (
    MetadataPhantom, ProcessPhantom, CredentialPhantom,
    EventPhantom, AVPhantom, USBPhantom, DiskPhantom,
    RegistryPhantom, BrowserPhantom, PanicButton
)

# Metadata manipulation
mp = MetadataPhantom()
mp.strip_all_metadata("photo.jpg")  # Remove EXIF
mp.manipulate_timestamps("document.pdf", randomize=True)

# Process operations
pp = ProcessPhantom()
checks = pp.anti_debug_checks()  # Detect debuggers
pp.execute_in_memory("print('No disk artifacts!')")

# Credential cleaning
cp = CredentialPhantom()
cp.clear_all_credentials()  # Wipe all credential caches
cp.clear_browser_passwords("all")

# Event log manipulation
ep = EventPhantom()
ep.clear_all_logs()  # Clear Windows event logs
ep.clear_powershell_history()

# AV/EDR evasion
ap = AVPhantom()
av_detected = ap.detect_av_products()
is_vm = ap.detect_virtual_machine()
is_sandbox = ap.detect_sandbox()

# USB security
up = USBPhantom()
up.setup_kill_switch(action="shutdown")  # Kill switch on USB change

# Secure disk operations
dp = DiskPhantom()
dp.secure_delete_file("secret.txt", passes=7)
dp.wipe_free_space("C:\\")

# Registry cleaning (Windows)
rp = RegistryPhantom()
rp.comprehensive_registry_clean()

# Browser forensics cleaning
bp = BrowserPhantom()
bp.clear_all_browser_data("all")

# Emergency panic button
pb = PanicButton()
pb.panic_level_1()  # Quick cleanup
pb.panic_level_2()  # Aggressive cleanup
pb.panic_level_3()  # Nuclear option (includes shutdown)
pb.setup_usb_panic_trigger(level=2)  # USB-triggered
```

### CLI Commands

```bash
# Core modules
phantomtrace quantum-delete sensitive.txt --passes 7
phantomtrace temporal-fog document.pdf --randomize
phantomtrace shadow-clone --type mixed --count 100
phantomtrace encrypt-aes secret.txt -p mypassword

# Phantom modules (NEW in v0.3.0)
phantomtrace metadata-strip photo.jpg
phantomtrace metadata-timestamps document.pdf --randomize
phantomtrace process-list --hidden
phantomtrace process-check
phantomtrace clear-credentials --target all
phantomtrace clear-logs --type all
phantomtrace av-detect
phantomtrace usb-monitor --interval 1.0
phantomtrace usb-killswitch --action shutdown
phantomtrace secure-delete secret_folder/ --passes 3
phantomtrace registry-clean
phantomtrace browser-clean --browser all --type all
phantomtrace panic --level 2 --trigger manual
```

## 🏗️ Architecture

```
phantomtrace/
├── modules/
│   # Core Modules
│   ├── quantum_decay.py           # Multi-pass secure deletion
│   ├── temporal_fog.py            # Timestamp manipulation  
│   ├── shadow_clones.py           # Decoy file generation
│   ├── memory_whisper.py          # RAM-only operations
│   ├── data_camouflage.py         # Steganography & encoding
│   ├── log_smoke.py               # Log manipulation
│   ├── network_ghost.py           # Traffic obfuscation
│   ├── entropy_injection.py       # Forensic artifact randomization
│   ├── advanced_encryption.py     # AES-GCM, ChaCha20, sealed boxes
│   ├── homomorphic_encryption.py  # FHE, secret sharing, MPC
│   # Phantom Modules (v0.3.0+)
│   ├── metadata_phantom.py        # Metadata stripping & manipulation
│   ├── process_phantom.py         # Process hiding & injection
│   ├── credential_phantom.py      # Credential extraction & clearing
│   ├── event_phantom.py           # Event log manipulation
│   ├── av_phantom.py              # AV/EDR/Sandbox detection
│   ├── usb_phantom.py             # USB monitoring & kill switch
│   ├── disk_phantom.py            # Disk wiping & LUKS destruction
│   ├── registry_phantom.py        # Windows registry cleaning
│   ├── browser_phantom.py         # Browser artifact cleaning
│   └── panic_button.py            # Emergency data destruction
├── utils/                         # Helper utilities
├── core/                          # Core anti-forensics engine
├── cli.py                         # Command-line interface
├── install.py                     # Automated installer
└── __init__.py                    # Module exports
```

## 🛠️ Key Highlights

- **Zero Investment**: Built entirely with free, open-source technologies
- **Modular Design**: Mix and match techniques as needed
- **Cross-Platform**: Works on Windows, Linux, and macOS
- **Extensible**: Plugin architecture for custom modules
- **Cryptographically Sound**: NIST-approved algorithms (AES-256, ChaCha20)
- **Advanced Privacy**: Homomorphic encryption for private computation
- **Easy Installation**: Automatic environment setup with `install.py`
- **Active Development**: Regular updates with new research

### Version 0.3.0 Release - COMPREHENSIVE FEATURE EXPANSION 🚀

✨ **MASSIVE UPDATE - 10 New Phantom Modules:**
- **Metadata Phantom**: EXIF/metadata stripping and manipulation
- **Process Phantom**: Process hiding, injection, anti-debugging
- **Credential Phantom**: Comprehensive credential wiping
- **Event Phantom**: Event log and history manipulation
- **AV Phantom**: AV/EDR/sandbox/VM detection
- **USB Phantom**: USB monitoring and kill switch (BusKill-style)
- **Disk Phantom**: Secure wiping, LUKS destruction
- **Registry Phantom**: Windows registry anti-forensics
- **Browser Phantom**: Multi-browser forensics cleaning
- **Panic Button**: Emergency multi-level data destruction system

🎯 **Feature Highlights:**
- 150+ original anti-forensic techniques implemented by Ayush
- USB kill switch with tripwire support
- Three-level panic button (quick, aggressive, nuclear)
- Comprehensive metadata manipulation
- Process memory operations
- Complete browser artifact cleaning
- Windows registry anti-forensics
- Cross-platform support (Windows/Linux)

### Version 0.2.0 Release

✨ **Major Additions:**
- Advanced Encryption module with Argon2 key derivation
- Homomorphic encryption for computation on encrypted data
- Automatic installer with virtual environment setup
- Enhanced CLI with encryption commands
- Production-ready package configuration

## 📚 Documentation

- [Installation Guide](docs/installation.md)
- [User Manual](docs/user_manual.md)
- [Module Reference](docs/modules.md)
- [Development Guide](docs/development.md)
- [Research Papers](docs/research.md)

## 🤝 Contributing

Contributions are welcome! Please read [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

## Acknowledgments

PhantomTrace is completely original work by Ayush, created from the ground up with novel anti-forensics methodologies and implementations.

## 📄 License

GNU General Public License v3.0 (GPL-3.0) - see [LICENSE](LICENSE) file for details.

## 🔬 Research

This project implements novel anti-forensics techniques based on:
- Quantum uncertainty principles applied to data deletion
- Temporal entropy in forensic timelines
- Adversarial machine learning for decoy generation
- Memory-resident computing patterns

## ⭐ Roadmap

### Completed (v0.2.0)
- [x] 8 core anti-forensics modules
- [x] Advanced AES-256-GCM and ChaCha20-Poly1305 encryption
- [x] Homomorphic encryption with secret sharing
- [x] Automatic installation system
- [x] Production-ready package structure

### Planned
- [ ] Fully Homomorphic Encryption (FHE) integration with TenSEAL
- [ ] AI-assisted decoy pattern generation
- [ ] Distributed anti-forensics coordination
- [ ] Hardware acceleration (GPU support)
- [ ] Mobile platform support (Android)
- [ ] Zero-knowledge proof modules

## 📧 Contact

For research collaboration or security inquiries: [Your Contact]

---

**Remember**: With great power comes great responsibility. Use ethically.
