# Advanced Usage Guide - PhantomTrace v0.2.0

## Table of Contents
1. [Advanced Encryption](#advanced-encryption)
2. [Homomorphic Encryption](#homomorphic-encryption)
3. [Production Patterns](#production-patterns)
4. [Security Considerations](#security-considerations)

---

## Advanced Encryption

The `AdvancedEncryption` module provides NIST-approved, authenticated encryption schemes suitable for sensitive data protection.

### AES-256-GCM Encryption

**Authenticated Encryption with Associated Data (AEAD)**

```python
from phantomtrace import AdvancedEncryption

ae = AdvancedEncryption()

# Encrypt with AES-256-GCM
plaintext = b"Sensitive document content"
password = "strong_passphrase_123"
ciphertext, nonce, tag = ae.encrypt_aes_gcm(plaintext, password)

# Store or transmit ciphertext + nonce + tag
# Later, decrypt with the same password
decrypted = ae.decrypt_aes_gcm(ciphertext, nonce, tag, password)
assert decrypted == plaintext
```

**Features:**
- 256-bit AES encryption via NIST-approved algorithm
- Argon2 key derivation (memory-hard, GPU-resistant)
- GCM mode provides authentication tag (detects tampering)
- Random 96-bit nonce per encryption (prevents IV reuse)
- Safe for high-security applications

### ChaCha20-Poly1305 Stream Cipher

**Modern stream cipher alternative to AES (faster on some systems)**

```python
# ChaCha20 is faster than AES on systems without hardware acceleration
ciphertext, nonce, tag = ae.encrypt_chacha20_poly1305(plaintext, password)
decrypted = ae.decrypt_chacha20_poly1305(ciphertext, nonce, tag, password)
```

**When to use:**
- Systems without AES-NI hardware support
- Mobile or embedded systems
- When throughput > security margin needed
- RFC 7539 compliance

### Sealed Boxes (Hybrid Encryption)

**Elliptic Curve Diffie-Hellman + ChaCha20-Poly1305**

```python
# Generate EC key pair (NIST P-256 curve)
public_key, private_key = ae.generate_key_pair()

# Sender: encrypt using recipient's public key
sealed_box = ae.create_sealed_box(public_key)
ciphertext = sealed_box.encrypt(b"Message for recipient")

# Recipient: decrypt using their private key  
sealed_box_recipient = ae.create_sealed_box(private_key)
plaintext = sealed_box_recipient.decrypt(ciphertext)
```

**Use cases:**
- End-to-end encrypted messaging
- Key exchange with forward secrecy
- Asymmetric encryption without RSA overhead
- Mobile authentication tokens

---

## Homomorphic Encryption

**Perform computations on encrypted data without decryption.**

### Additive Homomorphic Encryption

Encrypt numbers and add them without ever decrypting intermediate values.

```python
from phantomtrace import HomomorphicEncryption

he = HomomorphicEncryption()

# Generate encryption keys
he.generate_keys()

# Encrypt sensitive numbers
salary_1 = he.encrypt_additive(45000)
salary_2 = he.encrypt_additive(52000)  
salary_3 = he.encrypt_additive(48000)

# Compute sum without decrypting individual values
total_encrypted = salary_1 + salary_2 + salary_3  # or use add_encrypted()
total_sum = he.decrypt_additive(total_encrypted)

print(f"Total payroll (never decrypted): {total_sum}")  # 145000
```

**Practical applications:**
- Privacy-preserving analytics
- Medical data aggregation (HIPAA compliance)
- Financial reporting without exposing individual records
- Census data analysis

### Multiply Encrypted Values

```python
# Encryption supports addition AND limited multiplication
encrypted_value = he.encrypt_additive(10)
encrypted_result = he.multiply_encrypted(encrypted_value, 5)  # 10 * 5
result = he.decrypt_additive(encrypted_result)  # 50
```

### Secret Sharing (Threshold Cryptography)

**Shamir-like scheme: distribute trust across N parties, any M can recover**

```python
# Split secret into 5 shares, require 3 to recover
secret = 987654
shares = he.secret_sharing(secret, num_shares=5, threshold=3)

# Any 3 shares can recover the secret
recovered = he.recover_secret(shares[:3])
assert recovered == secret

# But only 2 shares cannot recover (outputs garbage)
fake_recovery = he.recover_secret(shares[:2])
assert fake_recovery != secret
```

**Use cases:**
- Distributed key management (3-of-5)
- Insurance/legal document control
- Blockchain validator quorums
- Multi-signature authorization

### Statistics on Encrypted Data

```python
# Compute statistics without decrypting individual values
scores = [85, 92, 78, 88, 95, 81, 89]
encrypted_scores = [he.encrypt_additive(s) for s in scores]

# Encrypted sum
sum_enc = sum(encrypted_scores)
total = he.decrypt_additive(sum_enc)
avg = total / len(scores)  # 87.7
```

### Secure Multi-Party Computation Pattern

```python
# Pattern for collaborative computation
# Three organizations want to compute average salary without sharing data

# Each encrypts their sum and count
org_a_sum = he.encrypt_additive(150000)  # 3 employees
org_a_count = he.encrypt_additive(3)

org_b_sum = he.encrypt_additive(200000)  # 4 employees  
org_b_count = he.encrypt_additive(4)

# Combine encrypted values
total_sum_enc = org_a_sum + org_b_sum
total_count_enc = org_a_count + org_b_count

# Decrypt only the aggregates (not individual company data)
total_sum = he.decrypt_additive(total_sum_enc)       # 350000
total_count = he.decrypt_additive(total_count_enc)   # 7
average = total_sum / total_count  # 50000

# Individual organization data never exposed
```

---

## Production Patterns

### Pattern 1: Secure Configuration Storage

```python
from phantomtrace import AdvancedEncryption
import json

ae = AdvancedEncryption()

config = {
    "api_key": "sk_live_abc123xyz",
    "db_password": "super_secret_pwd",
    "webhook_secret": "whsec_123456"
}

# Encrypt entire config
encrypted, nonce, tag = ae.encrypt_aes_gcm(
    json.dumps(config).encode(),
    password="master_key_from_env"
)

# Store compressed
with open("config.encrypted", "wb") as f:
    f.write(nonce + tag + encrypted)

# Later, decrypt on startup
with open("config.encrypted", "rb") as f:
    data = f.read()
    nonce = data[:12]
    tag = data[12:28]
    ciphertext = data[28:]
    
decrypted = ae.decrypt_aes_gcm(ciphertext, nonce, tag, "master_key_from_env")
config = json.loads(decrypted)
```

### Pattern 2: End-to-End Message Encryption

```python
from phantomtrace import AdvancedEncryption
import json

ae = AdvancedEncryption()

# Setup: Alice generates her key pair and publishes public key
alice_pub, alice_priv = ae.generate_key_pair()
# alice_pub goes in directory/registry

# Bob wants to send Alice a message
bob_pub, bob_priv = ae.generate_key_pair()
message = {"content": "Secret meeting 3pm", "priority": "high"}

# Bob encrypts for Alice (using her public key)
sealed = ae.create_sealed_box(alice_pub)
ciphertext = sealed.encrypt(json.dumps(message).encode())

# Message transmitted over any channel (stored in database, etc)
# Only Alice can decrypt with her private key
sealed_alice = ae.create_sealed_box(alice_priv)
decrypted_msg = sealed_alice.decrypt(ciphertext)
msg_data = json.loads(decrypted_msg)
```

### Pattern 3: Privacy-Preserving Analytics

```python
from phantomtrace import HomomorphicEncryption

he = HomomorphicEncryption()
he.generate_keys()

# Multiple users encrypt their data and send to analytics server
user_ages = []
for age in [25, 34, 28, 31, 29]:  # 5 users' ages
    user_ages.append(he.encrypt_additive(age))

# Server computes without decrypting
sum_ages = sum(user_ages)
count_users = 5

# Only the aggregate is revealed
avg_age = he.decrypt_additive(sum_ages) / count_users  # 29.4
print(f"Average age (privacy preserved): {avg_age}")

# Individual ages never exposed to server
```

### Pattern 4: Distributed Trust Secret Storage

```python
from phantomtrace import HomomorphicEncryption

he = HomomorphicEncryption()

# Master database password
db_password = 789456123

# Split among 7 IT staff, require 4 to recover
shares = he.secret_sharing(db_password, num_shares=7, threshold=4)

# Store shares in different locations/with different people
locations = ["vault_a", "vault_b", "vault_c", "vault_d", "vault_e", "vault_f", "vault_g"]
for i, share in enumerate(shares):
    print(f"Share {i+1} stored at {locations[i]}: {share}")

# In emergency: any 4 people bring shares to recover password
recovered = he.recover_secret(shares[0:4])
assert recovered == db_password
```

---

## Security Considerations

### Key Management

1. **Password Strength**: Always use 16+ character random passwords for AES/ChaCha20
   ```python
   # ❌ Don't do this
   password = "password123"
   
   # ✅ Do this
   import secrets
   password = secrets.token_urlsafe(32)  # 43+ characters
   ```

2. **Key Derivation**: Argon2 is used internally but ensure parameters suit your threat model
   - Default: 1 second computation time (2^17 memory)
   - Adjust via `AdvancedEncryption.derive_key()` parameters

3. **Key Storage**: Never hardcode encryption keys
   ```python
   # ❌ Never hardcode
   KEY = "my_secret_123"
   
   # ✅ Use environment variables
   import os
   KEY = os.environ["ENCRYPTION_KEY"]
   ```

### Nonce/IV Management

- ✅ Each encryption generates a random nonce (automatically handled)
- ❌ Never reuse the same nonce with the same key (leads to plaintext recovery)
- Store nonce alongside ciphertext (recommended: front 12 bytes + tag + ciphertext)

### Authentication Tags

- Always verify authentication tags to detect tampering
- GCM and ChaCha20-Poly1305 provide authenticated encryption
- Tags prevent silent corruption/forgery

### Homomorphic Encryption Limitations

- **No exact arithmetic**: XOR-based schemes provide addition/limited multiplication
- **Noise growth**: Operations grow ciphertext size and noise
- **Performance**: Slower than plaintext operations (10-1000x depending on algorithm)
- **Use case dependent**: Better for aggregation, worse for complex computations

### Avoid Common Mistakes

```python
# ❌ WRONG: Reusing password for every encryption
password = "fixed_password"
for file in files:
    ae.encrypt_aes_gcm(file_content, password)  # UNSAFE

# ✅ RIGHT: Unique password or KDF salt per encryption
import secrets
for file in files:
    salt = secrets.token_bytes(16)
    ae.encrypt_aes_gcm(file_content, password)  # Each creates new nonce internally

# ❌ WRONG: Ignoring authentication failures
try:
    plaintext = ae.decrypt_aes_gcm(ct, nonce, tag, pwd)
except:
    plaintext = b""  # UNSAFE: accepts corrupted data

# ✅ RIGHT: Handle authentication failures explicitly
try:
    plaintext = ae.decrypt_aes_gcm(ct, nonce, tag, pwd)
except Exception as e:
    print(f"Authentication failed - data compromised: {e}")
    sys.exit(1)
```

---

## Performance Characteristics

| Operation | Time | Notes |
|-----------|------|-------|
| AES-256-GCM encrypt 1MB | ~10ms | With AES-NI hardware |
| ChaCha20-Poly1305 1MB | ~15ms | Stream cipher speed |
| Argon2 key derive | ~1000ms | Intentionally slow (memory-hard) |
| Secret sharing (5-of-3) | <1ms | XOR-based, very fast |
| HE add 100 values | ~50ms | Per-value cost increases |

---

## Next Steps

- See [modules.md](modules.md) for complete API reference
- Check [installation.md](installation.md) for setup
- Review [CONTRIBUTING.md](../CONTRIBUTING.md) to add new algorithms
