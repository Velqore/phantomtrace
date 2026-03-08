#!/usr/bin/env python3
# Copyright (C) 2026 Ayush - PhantomTrace Project
# This file is part of PhantomTrace.
# 
# PhantomTrace is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
"""
PhantomTrace - Advanced Anti-Forensics Toolkit
"""

__version__ = "0.3.0"
__author__ = "Ayush (Original Creator)"
__license__ = "GPL-3.0"

# License verification and anti-tampering
from .license_guard import get_license_status, get_project_fingerprint

# Import main modules
from .modules.quantum_decay import QuantumDecay
from .modules.temporal_fog import TemporalFog
from .modules.shadow_clones import ShadowClone
from .modules.memory_whisper import MemoryWhisper
from .modules.data_camouflage import DataCamouflage
from .modules.log_smoke import LogSmoke
from .modules.entropy_injection import EntropyInjector
from .modules.network_ghost import NetworkGhost
from .modules.advanced_encryption import AdvancedEncryption
from .modules.homomorphic_encryption import HomomorphicEncryption

# Import new phantom modules (v0.3.0+)
from .modules.metadata_phantom import MetadataPhantom
from .modules.process_phantom import ProcessPhantom
from .modules.credential_phantom import CredentialPhantom
from .modules.event_phantom import EventPhantom
from .modules.av_phantom import AVPhantom
from .modules.usb_phantom import USBPhantom
from .modules.disk_phantom import DiskPhantom
from .modules.registry_phantom import RegistryPhantom
from .modules.browser_phantom import BrowserPhantom
from .modules.panic_button import PanicButton

__all__ = [
    # Core modules
    'QuantumDecay',
    'TemporalFog',
    'ShadowClone',
    'MemoryWhisper',
    'DataCamouflage',
    'LogSmoke',
    'EntropyInjector',
    'NetworkGhost',
    'AdvancedEncryption',
    'HomomorphicEncryption',
    # Phantom modules
    'MetadataPhantom',
    'ProcessPhantom',
    'CredentialPhantom',
    'EventPhantom',
    'AVPhantom',
    'USBPhantom',
    'DiskPhantom',
    'RegistryPhantom',
    'BrowserPhantom',
    'PanicButton',
]
