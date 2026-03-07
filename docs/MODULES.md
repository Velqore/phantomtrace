# Module Reference - PhantomTrace v0.2.0

Complete API documentation for all PhantomTrace modules.

## Table of Contents
1. [Quantum Decay](#quantum-decay)
2. [Temporal Fog](#temporal-fog)
3. [Shadow Clones](#shadow-clones)
4. [Memory Whisper](#memory-whisper)
5. [Data Camouflage](#data-camouflage)
6. [Log Smoke](#log-smoke)
7. [Network Ghost](#network-ghost)
8. [Entropy Injection](#entropy-injection)
9. [Advanced Encryption](#advanced-encryption)
10. [Homomorphic Encryption](#homomorphic-encryption)

---

## Quantum Decay

**Secure file deletion with quantum-inspired randomization patterns.**

```python
from phantomtrace import QuantumDecay

qd = QuantumDecay()

# Multi-pass deletion with unpredictable patterns
qd.quantum_delete(filepath, passes=7)

# Generate quantum noise (for other modules)
noise = qd.generate_quantum_noise(size_bytes=1024)
```

### Parameters
- `filepath` (str): Path to file for deletion
- `passes` (int, default=7): Number of overwrite passes (more = slower but more secure)

### Returns
- None (file deleted)
- Noise pattern matches quantum decoherence principles

---

## Temporal Fog

**Manipulate timestamps across multiple sources with entropy injection.**

```python
from phantomtrace import TemporalFog

tf = TemporalFog()

# Apply timestamp manipulation
tf.apply_fog(filepath, days_offset=-30)

# Get fogged timestamp
new_time = tf.get_fogged_time(days_offset=-15)
```

### Parameters
- `filepath` (str): Target file path
- `days_offset` (int): Days to shift timestamp (negative = past, positive = future)

### Methods
- `apply_fog(filepath, days_offset)`: Modify file times
- `get_fogged_time(days_offset)`: Generate offset timestamp without modifying file
- `inject_entropy()`: Add randomness to break pattern analysis

---

## Shadow Clones

**Generate realistic decoy files and activities.**

```python
from phantomtrace import ShadowClone

sc = ShadowClone()

# Create believable decoys
sc.create_believable_decoys(activity_type="browsing", count=50)

# Types: "browsing", "documents", "media", "development"
```

### Parameters
- `activity_type` (str): Type of decoy activity
- `count` (int): Number of decoys to create

### Supported Types
- `browsing`: Cache files, history, cookies
- `documents`: Office files, PDFs, text
- `media`: Images, videos, music metadata
- `development`: Code files, logs, config

---

## Memory Whisper

**RAM-only operations with secure memory wiping.**

```python
from phantomtrace import MemoryWhisper

mw = MemoryWhisper()

# Process data in memory only
data = mw.process_in_memory(sensitive_data)

# Secure memory wipe
mw.secure_wipe()
```

### Methods
- `process_in_memory(data)`: Keep data in RAM only
- `secure_wipe()`: Cryptographically wipe memory buffers
- `encrypt_in_ram(data)`: Encrypt before any disk swapping

---

## Data Camouflage

**Steganography with polymorphic encoding.**

```python
from phantomtrace import DataCamouflage

dc = DataCamouflage()

# Hide data in image
dc.hide_in_image("secret_message", "cover_image.jpg", "output.jpg")

# Extract hidden data
extracted = dc.extract_from_image("output.jpg")
```

### Methods
- `hide_in_image(data, cover_image, output_path)`: LSB steganography
- `extract_from_image(image_path)`: Recover hidden data
- `polymorphic_encode(data)`: Multiple encoding schemes

### Supported Formats
- JPEG, PNG, BMP (images)
- Capacity: ~25% of image size depending on format

---

## Log Smoke

**Sophisticated log manipulation and poisoning.**

```python
from phantomtrace import LogSmoke

ls = LogSmoke()

# Manipulate log entries
ls.inject_noise(logfile_path, noise_ratio=0.3)

# Format-preserving transformation
ls.obfuscate_entries(logfile_path, mode="timestamp")
```

### Methods
- `inject_noise(logpath, noise_ratio)`: Add realistic but false entries
- `obfuscate_entries(logpath, mode)`: Transform entries while maintaining log format
- `fragment_logs(logpath)`: Split logs to break temporal patterns

### Modes
- `timestamp`: Randomize entry times
- `user`: Obfuscate usernames
- `action`: Randomize action codes
- `all`: Apply all transformations

---

## Network Ghost

**Traffic pattern obfuscation and DPI evasion.**

```python
from phantomtrace import NetworkGhost

ng = NetworkGhost()

# Obfuscate traffic patterns
ng.obfuscate_traffic(interface="eth0", duration_seconds=60)

# Generate dummy traffic
ng.generate_decoy_traffic(destination="8.8.8.8", packets=1000)
```

### Methods
- `obfuscate_traffic(interface, duration_seconds)`: Randomize packet patterns
- `generate_decoy_traffic(destination, packets)`: Create dummy network flow
- `inject_jitter(min_ms, max_ms)`: Add random delays between packets

### Requirements
- Root/Admin privileges for packet capture/injection
- Optional: `scapy` library for advanced manipulation

---

## Entropy Injection

**Add randomness to break forensic signature analysis.**

```python
from phantomtrace import EntropyInjector

ei = EntropyInjector()

# Inject entropy into slack space
ei.inject_slack_space(volume_path, entropy_type="quantum")

# Randomize file carving signatures
ei.randomize_file_signatures(directory_path)
```

### Methods
- `inject_slack_space(volume, entropy_type)`: Fill slack with randomness
- `randomize_file_signatures(path)`: Alter file header magic bytes
- `disrupt_patterns(path)`: Break recognizable byte patterns

### Entropy Types
- `quantum`: Quantum noise patterns
- `cryptographic`: /dev/urandom patterns
- `algorithmic`: Pseudorandom sequences

---

## Advanced Encryption

**NIST-approved authenticated encryption schemes.**

```python
from phantomtrace import AdvancedEncryption

ae = AdvancedEncryption()

# AES-256-GCM
ciphertext, nonce, tag = ae.encrypt_aes_gcm(plaintext, password)
plaintext = ae.decrypt_aes_gcm(ciphertext, nonce, tag, password)

# ChaCha20-Poly1305
ciphertext, nonce, tag = ae.encrypt_chacha20_poly1305(plaintext, password)
plaintext = ae.decrypt_chacha20_poly1305(ciphertext, nonce, tag, password)

# Sealed Box (EC-based)
pub, priv = ae.generate_key_pair()
sealed = ae.create_sealed_box(pub)
ciphertext = sealed.encrypt(plaintext)
plaintext = sealed.decrypt(ciphertext)
```

### Methods
- `encrypt_aes_gcm(plaintext, password) -> (ciphertext, nonce, tag)`
- `decrypt_aes_gcm(ciphertext, nonce, tag, password) -> plaintext`
- `encrypt_chacha20_poly1305(plaintext, password) -> (ciphertext, nonce, tag)`
- `decrypt_chacha20_poly1305(ciphertext, nonce, tag, password) -> plaintext`
- `generate_key_pair() -> (public_key, private_key)`
- `create_sealed_box(key) -> SealedBox` instance

### Parameters
- `plaintext` (bytes): Data to encrypt
- `password` (str): Passphrase (16+ characters recommended)
- `key` (bytes): Public or private key for sealed boxes

### Returns
- Authenticated encryption with GCM/Poly1305 authentication tags
- Nonce ensures no IV reuse (even with same password)

---

## Homomorphic Encryption

**Computation on encrypted data without decryption.**

```python
from phantomtrace import HomomorphicEncryption

he = HomomorphicEncryption()
he.generate_keys()

# Additive scheme
c1 = he.encrypt_additive(5)
c2 = he.encrypt_additive(10)
c_sum = c1 + c2  # or he.add_encrypted(c1, c2)
result = he.decrypt_additive(c_sum)  # 15

# Secret sharing
shares = he.secret_sharing(secret=987654, num_shares=5, threshold=3)
recovered = he.recover_secret(shares[:3])

# Statistics
scores = [85, 92, 78, 88]
enc_scores = [he.encrypt_additive(s) for s in scores]
sum_enc = sum(enc_scores)
total = he.decrypt_additive(sum_enc)
```

### Methods
- `generate_keys()`: Initialize encryption scheme
- `encrypt_additive(value)`: Encrypt integer for addition
- `decrypt_additive(ciphertext)`: Recover plaintext integer
- `add_encrypted(c1, c2)`: Add two ciphertexts (result can be further added)
- `multiply_encrypted(ciphertext, scalar)`: Multiply ciphertext by plaintext scalar
- `secret_sharing(secret, num_shares, threshold)`: Create threshold shares
- `recover_secret(shares)`: Recover from any threshold-number shares
- `compute_statistics_encrypted(ciphertexts)`: Sum/average without decrypting

### Parameters
- `value` (int): Integer plaintext to encrypt
- `num_shares` (int): Total shares to create
- `threshold` (int): Minimum shares needed to recover
- `ciphertexts` (list): List of encrypted values

### Returns
- Integer ciphertexts (can be used in arithmetic)
- Threshold shares as integers
- Recovered secret after averaging recovered shares

### Limitations
- Additive HE: Only addition and multiplication by constants
- Secret sharing: Must decrypt all shares to recover (or average multiple recoveries)
- Noise growth: With many operations, precision may degrade
- Performance: Slower than plaintext (10-100x depending on value size)

---

## Common Patterns

### Encrypting Files
```python
from phantomtrace import AdvancedEncryption

ae = AdvancedEncryption()

# Read file
with open("data.txt", "rb") as f:
    plaintext = f.read()

# Encrypt
ct, nonce, tag = ae.encrypt_aes_gcm(plaintext, "mypassword")

# Write encrypted
with open("data.enc", "wb") as f:
    f.write(nonce + tag + ct)

# Later, read and decrypt
with open("data.enc", "rb") as f:
    data = f.read()
    nonce_read = data[:12]
    tag_read = data[12:28]
    ct_read = data[28:]
    plaintext_recovered = ae.decrypt_aes_gcm(ct_read, nonce_read, tag_read, "mypassword")
```

### Batch Operations
```python
from phantomtrace import QuantumDecay, TemporalFog
import os

qd = QuantumDecay()
tf = TemporalFog()

# Secure delete multiple files with timestamp manipulation
for filepath in os.listdir("."):
    if filepath.endswith(".tmp"):
        tf.apply_fog(filepath, days_offset=-60)
        qd.quantum_delete(filepath, passes=5)
```

### Error Handling
```python
from phantomtrace import AdvancedEncryption

ae = AdvancedEncryption()

try:
    plaintext = ae.decrypt_aes_gcm(ct, nonce, tag, password)
except ValueError as e:
    print(f"Decryption failed - authentication tag mismatch: {e}")
    # Data may be corrupted or tampered with
except Exception as e:
    print(f"Unexpected error: {e}")
```

---

## Version Compatibility

| Version | Release Date | Highlights |
|---------|--------------|-----------|
| 0.2.0 | Current | Advanced Encryption, Homomorphic Encryption, Auto-installer |
| 0.1.0 | Initial | 8 core anti-forensics modules |

---

## See Also
- [Advanced Usage Guide](ADVANCED_USAGE.md)
- [Installation Guide](installation.md)
- [Security Considerations](ADVANCED_USAGE.md#security-considerations)
