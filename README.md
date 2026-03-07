# PhantomTrace - Advanced Anti-Forensics Toolkit

![License](https://img.shields.io/badge/license-GPL--3.0-red.svg)
![Python](https://img.shields.io/badge/python-3.8+-green.svg)
![Version](https://img.shields.io/badge/version-0.2.0-blue.svg)
![Copyright](https://img.shields.io/badge/copyright-2026%20Ayush-blue.svg)

**Copyright (C) 2026 Ayush (Original Creator)**

An open-source, modular anti-forensics toolkit featuring innovative techniques for privacy protection, security research, and penetration testing. Now with **homomorphic encryption** and **advanced authenticated encryption**.

## 🔒 Copyright & License

**This project is protected under GPL-3.0 License.**

- **Original Author**: Ayush
- **Year**: 2026
- **License**: GNU General Public License v3.0

**IMPORTANT**: This software is licensed under GPL-3.0, which means:
- ✅ You CAN use, study, and modify this software
- ✅ You MUST provide attribution to the original author (Ayush)
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

## 📦 Installation

### Automated Installation (Recommended)

```bash
# Clone the repository
git clone https://github.com/yourusername/phantomtrace.git
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
source venv/bin/activate  # Windows: venv\Scripts\activate

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

## 🏗️ Architecture

```
phantomtrace/
├── modules/
│   ├── quantum_decay.py           # Multi-pass secure deletion
│   ├── temporal_fog.py            # Timestamp manipulation  
│   ├── shadow_clones.py           # Decoy file generation
│   ├── memory_whisper.py          # RAM-only operations
│   ├── data_camouflage.py         # Steganography & encoding
│   ├── log_smoke.py               # Log manipulation
│   ├── network_ghost.py           # Traffic obfuscation
│   ├── entropy_injection.py       # Forensic artifact randomization
│   ├── advanced_encryption.py     # AES-GCM, ChaCha20, sealed boxes
│   └── homomorphic_encryption.py  # FHE, secret sharing, MPC
├── utils/                          # Helper utilities
├── core/                           # Core anti-forensics engine
├── cli.py                          # Command-line interface
├── install.py                      # Automated installer
└── __init__.py                     # Module exports
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

## 📄 License

MIT License - see [LICENSE](LICENSE) file for details.

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
