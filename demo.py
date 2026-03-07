1#!/usr/bin/env python3
# Copyright (C) 2026 Ayush - PhantomTrace Project
# Licensed under GPL-3.0 - See LICENSE file for details
"""
PhantomTrace - Interactive Demo

An interactive demonstration of PhantomTrace capabilities.
"""

import sys
from pathlib import Path


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
    ║                      Version 0.1.0                       ║
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
    print("  [1] Quantum Decay - Secure File Deletion")
    print("  [2] Temporal Fog - Timestamp Manipulation")
    print("  [3] Shadow Clones - Decoy Generation")
    print("  [4] Memory Whisper - RAM-Only Operations")
    print("  [5] Data Camouflage - Steganography")
    print("  [6] Log Smoke - Log Manipulation")
    print("  [7] Entropy Injection - Pattern Breaking")
    print("  [8] Complete Workflow - Run All Techniques")
    print()
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
    print("📜 License: MIT (Open Source)")
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
            choice = input("Select option [0-9]: ").strip()
            
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
