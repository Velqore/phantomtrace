#!/usr/bin/env python3
# Copyright (C) 2026 Ayush - PhantomTrace Project
# Licensed under GPL-3.0 - See LICENSE file for details
"""
Command-line interface for PhantomTrace
"""

import argparse
import sys
import io
from pathlib import Path

# Fix Unicode output on Windows
if sys.platform.startswith('win'):
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')


def print_banner():
    """Print PhantomTrace banner."""
    banner = """
    ╔═══════════════════════════════════════════════════════════╗
    ║                                                           ║
    ║              ██████╗ ██╗  ██╗ █████╗ ███╗   ██╗         ║
    ║              ██╔══██╗██║  ██║██╔══██╗████╗  ██║         ║
    ║              ██████╔╝███████║███████║██╔██╗ ██║         ║
    ║              ██╔═══╝ ██╔══██║██╔══██║██║╚██╗██║         ║
    ║              ██║     ██║  ██║██║  ██║██║ ╚████║         ║
    ║              ╚═╝     ╚═╝  ╚═╝╚═╝  ╚═╝╚═╝  ╚═══╝         ║
    ║                                                           ║
    ║          ████████╗██████╗  █████╗  ██████╗███████╗      ║
    ║          ╚══██╔══╝██╔══██╗██╔══██╗██╔════╝██╔════╝      ║
    ║             ██║   ██████╔╝███████║██║     █████╗        ║
    ║             ██║   ██╔══██╗██╔══██║██║     ██╔══╝        ║
    ║             ██║   ██║  ██║██║  ██║╚██████╗███████╗      ║
    ║             ╚═╝   ╚═╝  ╚═╝╚═╝  ╚═╝ ╚═════╝╚══════╝      ║
    ║                                                           ║
    ║              Advanced Anti-Forensics Toolkit             ║
    ║                      Version 0.3.0                       ║
    ║                                                           ║
    ╚═══════════════════════════════════════════════════════════╝
    """
    print(banner)
    print("    🔒 Open Source • 🆓 No Investment • 🚀 Novel Concepts\n")


from phantomtrace import (
    QuantumDecay,
    TemporalFog,
    ShadowClone,
    MemoryWhisper,
    DataCamouflage,
    LogSmoke,
    EntropyInjector,
    AdvancedEncryption,
    HomomorphicEncryption,
    # New phantom modules
    MetadataPhantom,
    ProcessPhantom,
    CredentialPhantom,
    EventPhantom,
    AVPhantom,
    USBPhantom,
    DiskPhantom,
    RegistryPhantom,
    BrowserPhantom,
    PanicButton
)


def main():
    print_banner()
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
    
    # NEW PHANTOM MODULES (v0.3.0+)
    
    # Metadata Phantom commands
    meta_parser = subparsers.add_parser('metadata-strip', help='Strip all metadata from file')
    meta_parser.add_argument('file', help='File to clean')
    
    meta_ts_parser = subparsers.add_parser('metadata-timestamps', help='Manipulate file timestamps')
    meta_ts_parser.add_argument('file', help='File to modify')
    meta_ts_parser.add_argument('--randomize', action='store_true', help='Random timestamps')
    
    # Process Phantom commands
    proc_list_parser = subparsers.add_parser('process-list', help='List all processes')
    proc_list_parser.add_argument('--hidden', action='store_true', help='Detect hidden processes')
    
    proc_check_parser = subparsers.add_parser('process-check', help='Anti-debug/AV checks')
    
    # Credential Phantom commands
    cred_clear_parser = subparsers.add_parser('clear-credentials', help='Clear credential caches')
    cred_clear_parser.add_argument('--target', choices=['browser', 'ssh', 'windows', 'all'], default='all')
    
    # Event Phantom commands
    event_clear_parser = subparsers.add_parser('clear-logs', help='Clear event/system logs')
    event_clear_parser.add_argument('--type', choices=['event', 'powershell', 'bash', 'all'], default='all')
    
    # AV Phantom commands
    av_detect_parser = subparsers.add_parser('av-detect', help='Detect AV/EDR/Sandbox/VM')
    
    # USB Phantom commands
    usb_monitor_parser = subparsers.add_parser('usb-monitor', help='Monitor USB devices')
    usb_monitor_parser.add_argument('--interval', type=float, default=1.0, help='Check interval')
    
    usb_kill_parser = subparsers.add_parser('usb-killswitch', help='Arm USB kill switch')
    usb_kill_parser.add_argument('--action', choices=['shutdown', 'lock', 'wipe'], default='shutdown')
    
    # Disk Phantom commands
    disk_wipe_parser = subparsers.add_parser('secure-delete', help='Securely delete file/directory')
    disk_wipe_parser.add_argument('path', help='Path to delete')
    disk_wipe_parser.add_argument('--passes', type=int, default=3, help='Wipe passes')
    
    # Registry Phantom commands
    reg_clean_parser = subparsers.add_parser('registry-clean', help='Clean Windows registry artifacts')
    
    # Browser Phantom commands
    browser_clean_parser = subparsers.add_parser('browser-clean', help='Clean browser artifacts')
    browser_clean_parser.add_argument('--browser', choices=['chrome', 'firefox', 'edge', 'brave', 'all'], default='all')
    browser_clean_parser.add_argument('--type', choices=['history', 'cookies', 'cache', 'all'], default='all')
    
    # Panic Button commands
    panic_parser = subparsers.add_parser('panic', help='Emergency cleanup')
    panic_parser.add_argument('--level', type=int, choices=[1, 2, 3], default=2, help='Cleanup level (1=quick, 2=aggressive, 3=nuclear)')
    panic_parser.add_argument('--trigger', choices=['manual', 'usb', 'hotkey'], default='manual')
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return 1
    
    try:
        # Original commands
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
        
        # NEW PHANTOM MODULE COMMANDS
        
        elif args.command == 'metadata-strip':
            mp = MetadataPhantom()
            if mp.strip_all_metadata(args.file):
                print(f"✓ Metadata stripped from {args.file}")
                return 0
            return 1
        
        elif args.command == 'metadata-timestamps':
            mp = MetadataPhantom()
            if mp.manipulate_timestamps(args.file, randomize=args.randomize):
                print(f"✓ Timestamps manipulated for {args.file}")
                return 0
            return 1
        
        elif args.command == 'process-list':
            pp = ProcessPhantom()
            processes = pp.list_all_processes(include_hidden=args.hidden)
            print(f"✓ Found {len(processes)} processes")
            for proc in processes[:20]:  # Show first 20
                print(f"  PID {proc['pid']}: {proc['name']}")
            return 0
        
        elif args.command == 'process-check':
            pp = ProcessPhantom()
            checks = pp.anti_debug_checks()
            print("✓ Anti-debug checks:")
            for check, result in checks.items():
                print(f"  {check}: {result}")
            return 0
        
        elif args.command == 'clear-credentials':
            cp = CredentialPhantom()
            if args.target == 'all':
                results = cp.clear_all_credentials()
                print(f"✓ Cleared credentials: {results}")
            elif args.target == 'browser':
                cp.clear_browser_passwords("all")
            elif args.target == 'ssh':
                cp.clear_ssh_artifacts()
            elif args.target == 'windows':
                cp.clear_windows_credential_manager()
            return 0
        
        elif args.command == 'clear-logs':
            ep = EventPhantom()
            if args.type == 'all':
                results = ep.anti_forensic_cleanup()
                print(f"✓ Cleared logs: {results}")
            elif args.type == 'event':
                ep.clear_all_logs()
            elif args.type == 'powershell':
                ep.clear_powershell_history()
            elif args.type == 'bash':
                ep.clear_bash_history()
            return 0
        
        elif args.command == 'av-detect':
            ap = AVPhantom()
            results = ap.comprehensive_evasion_check()
            print("✓ Evasion check complete")
            return 0
        
        elif args.command == 'usb-monitor':
            up = USBPhantom()
            print("Starting USB monitoring...")
            up.start_monitoring(interval=args.interval)
            return 0
        
        elif args.command == 'usb-killswitch':
            up = USBPhantom()
            print(f"Arming USB kill switch (action: {args.action})...")
            thread = up.setup_kill_switch(action=args.action)
            if thread:
                thread.join()  # Wait for monitoring
            return 0
        
        elif args.command == 'secure-delete':
            dp = DiskPhantom()
            import os
            from pathlib import Path
            if os.path.isdir(args.path):
                count = dp.secure_delete_directory(args.path, passes=args.passes)
                print(f"✓ Securely deleted {count} files from directory")
            else:
                if dp.secure_delete_file(args.path, passes=args.passes):
                    print(f"✓ Securely deleted {args.path}")
                    return 0
                return 1
            return 0
        
        elif args.command == 'registry-clean':
            rp = RegistryPhantom()
            results = rp.comprehensive_registry_clean()
            print(f"✓ Registry cleaned: {results}")
            return 0
        
        elif args.command == 'browser-clean':
            bp = BrowserPhantom()
            if args.type == 'all':
                results = bp.clear_all_browser_data(args.browser)
                print(f"✓ Browser data cleared: {results}")
            elif args.type == 'history':
                bp.clear_browser_history(args.browser)
            elif args.type == 'cookies':
                bp.clear_browser_cookies(args.browser)
            elif args.type == 'cache':
                bp.clear_browser_cache(args.browser)
            return 0
        
        elif args.command == 'panic':
            pb = PanicButton()
            if args.trigger == 'manual':
                if args.level == 1:
                    pb.panic_level_1()
                elif args.level == 2:
                    pb.panic_level_2()
                elif args.level == 3:
                    pb.panic_level_3()
            elif args.trigger == 'usb':
                pb.setup_usb_panic_trigger(level=args.level)
            elif args.trigger == 'hotkey':
                pb.hotkey_panic(level=args.level)
            return 0
    
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
        return 1
    
    return 0


if __name__ == '__main__':
    sys.exit(main())
