#!/usr/bin/env python3
# Copyright (C) 2026 Ayush - PhantomTrace Project
# Licensed under GPL-3.0 - See LICENSE file for details

# PhantomTrace Config

"""
Configuration settings
"""

import os
from pathlib import Path

# Base directories
BASE_DIR = Path(__file__).parent.parent
OUTPUT_DIR = BASE_DIR / 'output'
TEMP_DIR = BASE_DIR / 'temp'
LOGS_DIR = BASE_DIR / 'logs'

# Make sure they exist
OUTPUT_DIR.mkdir(exist_ok=True)
TEMP_DIR.mkdir(exist_ok=True)
LOGS_DIR.mkdir(exist_ok=True)

# Quantum Decay settings
QUANTUM_DECAY = {
    'default_passes': 7,
    'verify_writes': True,
    'secure_rename': True,
    'chunk_size': 1024 * 1024,  # 1MB
}

# Temporal Fog settings
TEMPORAL_FOG = {
    'default_days_offset': -30,
    'randomize_by_default': True,
    'break_correlation_by_default': True,
    'microsecond_entropy': True,
}

# Shadow Clone settings
SHADOW_CLONE = {
    'default_output_dir': str(OUTPUT_DIR / 'decoys'),
    'default_count': 50,
    'default_time_range_days': 90,
    'generate_realistic_content': True,
}

# Memory Whisper settings
MEMORY_WHISPER = {
    'secure_wipe_passes': 3,
    'enable_memory_lock': True,
    'anti_dump_protection': False,  # Requires admin
}

# Data Camouflage settings
DATA_CAMOUFLAGE = {
    'default_technique': 'adaptive_lsb',
    'polymorphic_encryption': True,
    'compression_before_hiding': True,
}

# Log Smoke settings
LOG_SMOKE = {
    'default_entries': 50,
    'preserve_format': True,
    'create_backups': True,
    'backup_suffix': '.backup',
}

# Entropy Injection settings
ENTROPY_INJECTION = {
    'default_cluster_size': 4096,
    'random_padding_max': 1024,
    'break_signatures': False,  # May break files
}

# Network Ghost settings
NETWORK_GHOST = {
    'default_delay_ms': 100,
    'jitter_enabled': True,
    'protocol_mimicry': 'http',
}

# Logging
LOGGING = {
    'enabled': True,
    'level': 'INFO',
    'log_file': str(LOGS_DIR / 'phantomtrace.log'),
    'max_size_mb': 10,
}

# Security
SECURITY = {
    'wipe_temp_on_exit': True,
    'secure_memory_wiping': True,
    'check_debugger': True,
}

# Performance
PERFORMANCE = {
    'use_multiprocessing': False,
    'max_workers': 4,
    'buffer_size': 8192,
}
