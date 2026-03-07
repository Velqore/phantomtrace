#!/usr/bin/env python3
# Copyright (C) 2026 Ayush - PhantomTrace Project
# Licensed under GPL-3.0 - See LICENSE file for details
"""
PhantomTrace Setup Script
"""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="phantomtrace",
    version="0.2.0",
    author="Ayush",
    author_email="ayush@phantomtrace.dev",
    description="Advanced anti-forensics toolkit with homomorphic encryption",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ayushsecurity/phantomtrace",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Security Researchers",
        "Topic :: Security",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    python_requires=">=3.8",
    install_requires=[
        "cryptography>=41.0.0",
        "numpy>=1.24.0",
        "psutil>=5.9.0",
        "pillow>=10.0.0",
        "pycryptodome>=3.18.0",
        "libnacl>=1.9.2",
    ],
    extras_require={
        "dev": [
            "pytest>=7.4.0",
            "black>=23.7.0",
            "flake8>=6.1.0",
        ],
        "network": [
            "scapy>=2.5.0",
        ],
        "he": [
            "tenseal>=0.3.10",
        ],
    },
    entry_points={
        "console_scripts": [
            "phantomtrace=phantomtrace.cli:main",
        ],
    },
)
