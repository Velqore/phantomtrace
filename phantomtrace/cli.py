#!/usr/bin/env python3
# Copyright (C) 2026 Ayush - PhantomTrace Project
# Licensed under GPL-3.0 - See LICENSE file for details
"""
Command-line interface for PhantomTrace
"""

import argparse
import sys
from pathlib import Path

from phantomtrace import (
    QuantumDecay,
    TemporalFog,
    ShadowClone,
    MemoryWhisper,
    DataCamouflage,
    LogSmoke,
    EntropyInjector,
    AdvancedEncryption,
    HomomorphicEncryption
)


def main():
    parser = argparse.ArgumentParser(
        description='PhantomTrace - Anti-Forensics Toolkit',
        epilog='Educational use only!'
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # Quantum Decay command
    qd_parser = subparsers.add_parser('quantum-delete', help='Secure file deletion')
    qd_parser.add_argument('file', help='File to delete')
    qd_parser.add_argument('--passes', type=int, default=7, help='Number of overwrite passes')
    
    # Temporal Fog command
    tf_parser = subparsers.add_parser('temporal-fog', help='Timestamp manipulation')
    tf_parser.add_argument('path', help='File or directory path')
    tf_parser.add_argument('--days-offset', type=int, help='Days to offset timestamps')
    tf_parser.add_argument('--randomize', action='store_true', help='Add random entropy')
    
    # Shadow Clone command
    sc_parser = subparsers.add_parser('shadow-clone', help='Generate decoys')
    sc_parser.add_argument('--type', choices=['browsing', 'documents', 'mixed'], default='mixed')
    sc_parser.add_argument('--count', type=int, default=50, help='Number of decoys')
    sc_parser.add_argument('--output', default='./decoys', help='Output directory')
    
    # Log Smoke command
    ls_parser = subparsers.add_parser('log-smoke', help='Log manipulation')
    ls_parser.add_argument('logfile', help='Log file to manipulate')
    ls_parser.add_argument('--entries', type=int, default=50, help='Fake entries to inject')
    
    # Entropy Injection command
    ei_parser = subparsers.add_parser('entropy-inject', help='Inject entropy')
    ei_parser.add_argument('file', help='File to inject entropy into')
    ei_parser.add_argument('--type', choices=['slack', 'metadata', 'structure'], default='slack')
    
    # Advanced Encryption commands
    enc_aes_parser = subparsers.add_parser('encrypt-aes', help='AES-256-GCM encryption')
    enc_aes_parser.add_argument('input', help='Input file to encrypt')
    enc_aes_parser.add_argument('-p', '--password', help='Encryption password (prompted if not provided)')
    enc_aes_parser.add_argument('-o', '--output', help='Output file (default: input.enc)')
    
    dec_aes_parser = subparsers.add_parser('decrypt-aes', help='AES-256-GCM decryption')
    dec_aes_parser.add_argument('input', help='Encrypted file to decrypt')
    dec_aes_parser.add_argument('-p', '--password', help='Decryption password (prompted if not provided)')
    dec_aes_parser.add_argument('-o', '--output', help='Output file (default: input.dec)')
    
    enc_chacha_parser = subparsers.add_parser('encrypt-chacha', help='ChaCha20-Poly1305 encryption')
    enc_chacha_parser.add_argument('input', help='Input file to encrypt')
    enc_chacha_parser.add_argument('-p', '--password', help='Encryption password')
    enc_chacha_parser.add_argument('-o', '--output', help='Output file')
    
    dec_chacha_parser = subparsers.add_parser('decrypt-chacha', help='ChaCha20-Poly1305 decryption')
    dec_chacha_parser.add_argument('input', help='Encrypted file')
    dec_chacha_parser.add_argument('-p', '--password', help='Decryption password')
    dec_chacha_parser.add_argument('-o', '--output', help='Output file')
    
    # Homomorphic Encryption command
    he_parser = subparsers.add_parser('secret-share', help='Secret sharing (threshold cryptography)')
    he_parser.add_argument('secret', type=int, help='Secret to share')
    he_parser.add_argument('--shares', type=int, default=5, help='Total shares to create')
    he_parser.add_argument('--threshold', type=int, default=3, help='Shares needed to recover')
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return 1
    
    try:
        if args.command == 'quantum-delete':
            qd = QuantumDecay()
            if qd.quantum_delete(args.file, passes=args.passes):
                print(f"✓ Successfully deleted {args.file}")
                return 0
            else:
                print(f"✗ Failed to delete {args.file}")
                return 1
        
        elif args.command == 'temporal-fog':
            tf = TemporalFog()
            if tf.apply_fog(args.path, days_offset=args.days_offset, randomize=args.randomize):
                print(f"✓ Applied temporal fog to {args.path}")
                return 0
            else:
                print(f"✗ Failed to apply fog")
                return 1
        
        elif args.command == 'shadow-clone':
            sc = ShadowClone(output_dir=args.output)
            files = sc.create_believable_decoys(activity_type=args.type, count=args.count)
            print(f"✓ Created {len(files)} decoy files in {args.output}")
            return 0
        
        elif args.command == 'log-smoke':
            ls = LogSmoke()
            if ls.inject_noise(args.logfile, num_entries=args.entries):
                print(f"✓ Injected {args.entries} fake entries into {args.logfile}")
                return 0
            else:
                print(f"✗ Failed to inject log noise")
                return 1
        
        elif args.command == 'entropy-inject':
            ei = EntropyInjector()
            success = False
            
            if args.type == 'slack':
                success = ei.inject_file_slack(args.file)
            elif args.type == 'metadata':
                success = ei.inject_metadata_entropy(args.file)
            elif args.type == 'structure':
                success = ei.randomize_file_structure(args.file)
            
            if success:
                print(f"✓ Injected entropy into {args.file}")
                return 0
            else:
                print(f"✗ Failed to inject entropy")
                return 1
        
        elif args.command == 'encrypt-aes':
            import getpass
            ae = AdvancedEncryption()
            password = args.password or getpass.getpass("Enter encryption password: ")
            
            with open(args.input, 'rb') as f:
                plaintext = f.read()
            
            encrypted = ae.encrypt_aes_gcm(plaintext, password)
            output_file = args.output or f"{args.input}.enc"
            
            with open(output_file, 'wb') as f:
                f.write(encrypted)
            
            print(f"✓ Encrypted {args.input} -> {output_file}")
            return 0
        
        elif args.command == 'decrypt-aes':
            import getpass
            ae = AdvancedEncryption()
            password = args.password or getpass.getpass("Enter decryption password: ")
            
            with open(args.input, 'rb') as f:
                encrypted = f.read()
            
            plaintext = ae.decrypt_aes_gcm(encrypted, password)
            output_file = args.output or f"{args.input}.dec"
            
            with open(output_file, 'wb') as f:
                f.write(plaintext)
            
            print(f"✓ Decrypted {args.input} -> {output_file}")
            return 0
        
        elif args.command == 'encrypt-chacha':
            import getpass
            ae = AdvancedEncryption()
            password = args.password or getpass.getpass("Enter encryption password: ")
            
            with open(args.input, 'rb') as f:
                plaintext = f.read()
            
            encrypted = ae.encrypt_chacha20_poly1305(plaintext, password)
            output_file = args.output or f"{args.input}.enc"
            
            with open(output_file, 'wb') as f:
                f.write(encrypted)
            
            print(f"✓ Encrypted {args.input} -> {output_file} (ChaCha20-Poly1305)")
            return 0
        
        elif args.command == 'decrypt-chacha':
            import getpass
            ae = AdvancedEncryption()
            password = args.password or getpass.getpass("Enter decryption password: ")
            
            with open(args.input, 'rb') as f:
                encrypted = f.read()
            
            plaintext = ae.decrypt_chacha20_poly1305(encrypted, password)
            output_file = args.output or f"{args.input}.dec"
            
            with open(output_file, 'wb') as f:
                f.write(plaintext)
            
            print(f"✓ Decrypted {args.input} -> {output_file}")
            return 0
        
        elif args.command == 'secret-share':
            he = HomomorphicEncryption()
            shares = he.secret_sharing(args.secret, num_shares=args.shares, threshold=args.threshold)
            
            print(f"✓ Secret {args.secret} split into {args.shares} shares ({args.threshold} needed):")
            for i, share in enumerate(shares, 1):
                print(f"  Share {i}: {share}")
            
            return 0
    
    except Exception as e:
        print(f"Error: {e}")
        return 1
    
    return 0


if __name__ == '__main__':
    sys.exit(main())
