1#!/usr/bin/env python3
# Copyright (C) 2026 Ayush - PhantomTrace Project
# Licensed under GPL-3.0 - See LICENSE file for details
"""
PhantomTrace - Interactive Demo

An interactive demonstration of PhantomTrace capabilities.
"""

import sys
import io
from pathlib import Path

# Fix Unicode output on Windows
if sys.platform.startswith('win'):
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')


def print_banner():
    """Print welcome banner."""
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
    print("\n    🔒 Open Source • 🆓 No Investment • 🚀 Novel Concepts\n")


def show_menu():
    """Display main menu."""
    print("\n" + "="*60)
    print("                    MAIN MENU")
    print("="*60)
    print()
    print("  CORE MODULES (v0.1-0.2):")
    print("  [1] Quantum Decay - Secure File Deletion")
    print("  [2] Temporal Fog - Timestamp Manipulation")
    print("  [3] Shadow Clones - Decoy Generation")
    print("  [4] Memory Whisper - RAM-Only Operations")
    print("  [5] Data Camouflage - Steganography")
    print("  [6] Log Smoke - Log Manipulation")
    print("  [7] Entropy Injection - Pattern Breaking")
    print()
    print("  PHANTOM MODULES (v0.3.0 - NEW!):")
    print("  [A] Metadata Phantom - Metadata Stripping")
    print("  [B] Process Phantom - Process Hiding/Injection")
    print("  [C] Credential Phantom - Credential Management")
    print("  [D] Event Phantom - Event Log Manipulation")
    print("  [E] AV Phantom - AV/EDR Detection & Evasion")
    print("  [F] USB Phantom - USB Kill Switch")
    print("  [G] Disk Phantom - Secure Disk Operations")
    print("  [H] Registry Phantom - Windows Registry Cleaning")
    print("  [I] Browser Phantom - Browser Forensics Cleaning")
    print("  [J] Panic Button - Emergency Data Destruction")
    print()
    print("  [8] Complete Workflow - Run All Techniques")
    print("  [9] About PhantomTrace")
    print("  [0] Exit")
    print()
    print("="*60)


def demo_quantum_decay():
    """Demo Quantum Decay."""
    print("\n📌 QUANTUM DECAY - Secure File Deletion")
    print("-" * 60)
    print("Novel approach using quantum-inspired uncertainty patterns")
    print("for secure file deletion that resists forensic recovery.\n")
    
    print("Features:")
    print("  ✓ Non-deterministic pass patterns")
    print("  ✓ Cryptographic randomness")
    print("  ✓ Hardware-aware optimization")
    print("  ✓ Secure file renaming")
    print("\nSee: examples/quantum_decay_example.py")


def demo_temporal_fog():
    """Demo Temporal Fog."""
    print("\n📌 TEMPORAL FOG - Timestamp Manipulation")
    print("-" * 60)
    print("Break temporal correlation across multiple forensic sources")
    print("with sophisticated timestamp manipulation techniques.\n")
    
    print("Features:")
    print("  ✓ Multi-source correlation breaking")
    print("  ✓ Entropy-injected time deltas")
    print("  ✓ Impossible temporal sequences")
    print("  ✓ Microsecond precision manipulation")
    print("\nSee: examples/temporal_fog_example.py")


def demo_shadow_clones():
    """Demo Shadow Clones."""
    print("\n📌 SHADOW CLONES - Decoy Generation")
    print("-" * 60)
    print("Generate forensically-convincing decoys that create")
    print("reasonable doubt and consume investigator resources.\n")
    
    print("Features:")
    print("  ✓ AI-inspired pattern generation")
    print("  ✓ Realistic document content")
    print("  ✓ Believable browsing history")
    print("  ✓ Polymorphic generation (unique each time)")
    print("\nSee: examples/shadow_clone_example.py")


def demo_memory_whisper():
    """Demo Memory Whisper."""
    print("\n📌 MEMORY WHISPER - RAM-Only Operations")
    print("-" * 60)
    print("Process data entirely in RAM with secure memory wiping")
    print("and anti-forensics memory management techniques.\n")
    
    print("Features:")
    print("  ✓ Memory-only data processing")
    print("  ✓ Hardware-accelerated wiping")
    print("  ✓ Anti-memory dump protection")
    print("  ✓ Secure memory allocation")


def demo_data_camouflage():
    """Demo Data Camouflage."""
    print("\n📌 DATA CAMOUFLAGE - Steganography")
    print("-" * 60)
    print("Multi-layer steganography with polymorphic encoding")
    print("to hide data in plain sight.\n")
    
    print("Features:")
    print("  ✓ Adaptive LSB steganography")
    print("  ✓ Polymorphic encryption")
    print("  ✓ Multi-layer plausible deniability")
    print("  ✓ Statistical normalization")


def demo_log_smoke():
    """Demo Log Smoke."""
    print("\n📌 LOG SMOKE - Log Manipulation")
    print("-" * 60)
    print("Sophisticated log injection and manipulation that")
    print("introduces forensic noise without obvious tampering.\n")
    
    print("Features:")
    print("  ✓ Statistically plausible injection")
    print("  ✓ Format-preserving modifications")
    print("  ✓ Anti-pattern detection evasion")
    print("  ✓ Timeline gap creation")


def demo_entropy_injection():
    """Demo Entropy Injection."""
    print("\n📌 ENTROPY INJECTION - Pattern Breaking")
    print("-" * 60)
    print("Inject cryptographic entropy into forensic artifacts")
    print("to break pattern analysis and signature detection.\n")
    
    print("Features:")
    print("  ✓ Slack space manipulation")
    print("  ✓ File structure randomization")
    print("  ✓ Signature breaking")
    print("  ✓ File carver poisoning")


def demo_metadata_phantom():
    """Demo Metadata Phantom."""
    print("\n📌 METADATA PHANTOM - Metadata Stripping (v0.3.0+)")
    print("-" * 60)
    print("Comprehensive metadata manipulation and removal")
    print("for images, PDFs, and office documents.\n")
    
    print("Features:")
    print("  ✓ EXIF data stripping")
    print("  ✓ PDF metadata removal")
    print("  ✓ Office document cleaning")
    print("  ✓ NTFS timestamp manipulation (nanosecond precision)")
    print("  ✓ Fake metadata injection for misdirection")


def demo_process_phantom():
    """Demo Process Phantom."""
    print("\n📌 PROCESS PHANTOM - Process Hiding/Injection (v0.3.0+)")
    print("-" * 60)
    print("Advanced process manipulation and anti-debugging")
    print("techniques for evading forensic detection.\n")
    
    print("Features:")
    print("  ✓ In-memory code execution")
    print("  ✓ Process name spoofing")
    print("  ✓ Anti-debugging checks")
    print("  ✓ Shellcode injection")
    print("  ✓ Hidden process detection")


def demo_credential_phantom():
    """Demo Credential Phantom."""
    print("\n📌 CREDENTIAL PHANTOM - Credential Management (v0.3.0+)")
    print("-" * 60)
    print("Comprehensive credential wiping and extraction")
    print("across multiple browsers and systems.\n")
    
    print("Features:")
    print("  ✓ Browser password clearing")
    print("  ✓ Windows Credential Manager wipe")
    print("  ✓ SSH key removal")
    print("  ✓ SAM backup deletion")
    print("  ✓ Complete credential destruction")


def demo_event_phantom():
    """Demo Event Phantom."""
    print("\n📌 EVENT PHANTOM - Event Log Manipulation (v0.3.0+)")
    print("-" * 60)
    print("Sophisticated event log and history manipulation")
    print("for Windows and Linux systems.\n")
    
    print("Features:")
    print("  ✓ Windows event log clearing")
    print("  ✓ PowerShell history removal")
    print("  ✓ Bash history clearing")
    print("  ✓ RDP log deletion")
    print("  ✓ System logging disabling")


def demo_av_phantom():
    """Demo AV Phantom."""
    print("\n📌 AV PHANTOM - AV/EDR/Sandbox Detection (v0.3.0+)")
    print("-" * 60)
    print("Detect and evade antivirus, EDR, sandboxes")
    print("and virtual machine environments.\n")
    
    print("Features:")
    print("  ✓ AV/EDR product detection")
    print("  ✓ Sandbox environment detection")
    print("  ✓ Virtual machine detection")
    print("  ✓ Debugger detection")
    print("  ✓ Analysis tool detection")


def demo_usb_phantom():
    """Demo USB Phantom."""
    print("\n📌 USB PHANTOM - USB Kill Switch (v0.3.0+)")
    print("-" * 60)
    print("Real-time USB monitoring with emergency")
    print("shutdown/data destruction capabilities.\n")
    
    print("Features:")
    print("  ✓ USB device monitoring")
    print("  ✓ BusKill-style kill switch")
    print("  ✓ Tripwire assassination")
    print("  ✓ Emergency RAM wipe")
    print("  ✓ System shutdown trigger")


def demo_disk_phantom():
    """Demo Disk Phantom."""
    print("\n📌 DISK PHANTOM - Secure Disk Operations (v0.3.0+)")
    print("-" * 60)
    print("Multi-pass secure deletion and disk wiping")
    print("with LUKS header destruction support.\n")
    
    print("Features:")
    print("  ✓ Multi-pass file deletion")
    print("  ✓ LUKS header destruction")
    print("  ✓ Free space wiping")
    print("  ✓ MBR/GPT destruction")
    print("  ✓ Slack space wiping")


def demo_registry_phantom():
    """Demo Registry Phantom."""
    print("\n📌 REGISTRY PHANTOM - Windows Registry Cleaning (v0.3.0+)")
    print("-" * 60)
    print("Comprehensive Windows registry anti-forensics")
    print("and artifact cleaning.\n")
    
    print("Features:")
    print("  ✓ Recent documents clearing")
    print("  ✓ Run/MRU list removal")
    print("  ✓ UserAssist clearing")
    print("  ✓ Shellbags deletion")
    print("  ✓ Jump Lists removal")


def demo_browser_phantom():
    """Demo Browser Phantom."""
    print("\n📌 BROWSER PHANTOM - Browser Forensics Cleaning (v0.3.0+)")
    print("-" * 60)
    print("Multi-browser forensic artifact cleaning")
    print("across Chrome, Firefox, Edge, and Brave.\n")
    
    print("Features:")
    print("  ✓ Browsing history clearing")
    print("  ✓ Cookie deletion")
    print("  ✓ Cache removal")
    print("  ✓ Download history deletion")
    print("  ✓ Cross-browser support")


def demo_panic_button():
    """Demo Panic Button."""
    print("\n📌 PANIC BUTTON - Emergency Data Destruction (v0.3.0+)")
    print("-" * 60)
    print("Emergency multi-level cleanup system with")
    print("USB-triggered and hotkey-activated modes.\n")
    
    print("Panic Levels:")
    print("  🟢 Level 1: Quick cleanup (browser, logs, creds)")
    print("  🟡 Level 2: Aggressive (Level 1 + registry, events)")
    print("  🔴 Level 3: Nuclear (Level 2 + secure delete, shutdown)")
    print("\nTrigger Modes:")
    print("  • Manual activation")
    print("  • USB kill switch")
    print("  • Keyboard hotkey (Ctrl+Shift+Alt+P)")


def demo_complete_workflow():
    """Demo complete workflow."""
    print("\n📌 COMPLETE WORKFLOW - All Techniques")
    print("-" * 60)
    print("Demonstration of combining multiple PhantomTrace")
    print("modules for comprehensive anti-forensics coverage.\n")
    
    print("Workflow Steps:")
    print("  1. Generate shadow clone decoys")
    print("  2. Apply temporal fog to timestamps")
    print("  3. Inject entropy into files")
    print("  4. Manipulate system logs")
    print("  5. Secure deletion of originals")
    print("\nRun: python examples/complete_workflow.py")


def show_about():
    """Show about information."""
    print("\n📖 ABOUT PHANTOMTRACE")
    print("="*60)
    print()
    print("PhantomTrace is an open-source anti-forensics toolkit")
    print("featuring completely novel concepts, built with zero")
    print("investment using free and open-source technologies.")
    print()
    print("🎯 Purpose:")
    print("  • Educational research")
    print("  • Privacy protection")
    print("  • Security testing")
    print("  • Digital rights advocacy")
    print()
    print("🔬 Novel Concepts:")
    print("  1. Quantum-inspired secure deletion")
    print("  2. Multi-source temporal correlation breaking")
    print("  3. AI-inspired decoy generation")
    print("  4. Polymorphic steganography")
    print("  5. Statistical anti-forensics normalization")
    print()
    print("📜 License: GPL-3.0 (Open Source)")
    print("🐍 Built with: Python 3.8+")
    print("💰 Cost: $0 (Free Forever)")
    print()
    print("⚠️  Use Responsibly: Educational & Legal Purposes Only")
    print()
    print("="*60)


def main():
    """Main interactive demo."""
    print_banner()
    
    while True:
        show_menu()
        
        try:
            choice = input("Select option [0-9, A-J]: ").strip().upper()
            
            if choice == '0':
                print("\n👋 Thank you for using PhantomTrace!")
                print("   Remember: Use responsibly and legally.\n")
                sys.exit(0)
            
            elif choice == '1':
                demo_quantum_decay()
            
            elif choice == '2':
                demo_temporal_fog()
            
            elif choice == '3':
                demo_shadow_clones()
            
            elif choice == '4':
                demo_memory_whisper()
            
            elif choice == '5':
                demo_data_camouflage()
            
            elif choice == '6':
                demo_log_smoke()
            
            elif choice == '7':
                demo_entropy_injection()
            
            elif choice == 'A':
                demo_metadata_phantom()
            
            elif choice == 'B':
                demo_process_phantom()
            
            elif choice == 'C':
                demo_credential_phantom()
            
            elif choice == 'D':
                demo_event_phantom()
            
            elif choice == 'E':
                demo_av_phantom()
            
            elif choice == 'F':
                demo_usb_phantom()
            
            elif choice == 'G':
                demo_disk_phantom()
            
            elif choice == 'H':
                demo_registry_phantom()
            
            elif choice == 'I':
                demo_browser_phantom()
            
            elif choice == 'J':
                demo_panic_button()
            
            elif choice == '8':
                demo_complete_workflow()
            
            elif choice == '9':
                show_about()
            
            else:
                print("\n❌ Invalid option. Please try again.")
            
            input("\nPress Enter to continue...")
            
        except KeyboardInterrupt:
            print("\n\n👋 Goodbye!")
            sys.exit(0)
        except Exception as e:
            print(f"\n❌ Error: {e}")
            input("\nPress Enter to continue...")


if __name__ == '__main__':
    main()
