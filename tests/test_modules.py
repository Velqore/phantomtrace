#!/usr/bin/env python3
# Copyright (C) 2026 Ayush - PhantomTrace Project
# Licensed under GPL-3.0 - See LICENSE file for details
"""
Unit tests for PhantomTrace modules
"""

import pytest
import tempfile
from pathlib import Path

from phantomtrace import (
    QuantumDecay,
    TemporalFog,
    ShadowClone,
    EntropyInjector,
)


class TestQuantumDecay:
    """Test Quantum Decay module."""
    
    def test_quantum_delete_creates_passes(self):
        """Test that quantum delete performs multiple passes."""
        qd = QuantumDecay()
        
        # Create temp file
        with tempfile.NamedTemporaryFile(mode='w', delete=False) as f:
            f.write("test data" * 100)
            temp_file = f.name
        
        # Delete
        result = qd.quantum_delete(temp_file, passes=3)
        
        assert result is True
        assert not Path(temp_file).exists()
        assert qd.stats['files_deleted'] == 1
        assert qd.stats['total_passes'] >= 3
    
    def test_quantum_delete_nonexistent_file(self):
        """Test deleting non-existent file raises error."""
        qd = QuantumDecay()
        
        with pytest.raises(FileNotFoundError):
            qd.quantum_delete("/nonexistent/file.txt")


class TestTemporalFog:
    """Test Temporal Fog module."""
    
    def test_apply_fog_modifies_timestamp(self):
        """Test that temporal fog modifies timestamps."""
        tf = TemporalFog()
        
        # Create temp file
        with tempfile.NamedTemporaryFile(mode='w', delete=False) as f:
            f.write("test")
            temp_file = f.name
        
        # Get original timestamp
        original_mtime = Path(temp_file).stat().st_mtime
        
        # Apply fog
        result = tf.apply_fog(temp_file, days_offset=-30)
        
        # Get new timestamp
        new_mtime = Path(temp_file).stat().st_mtime
        
        assert result is True
        assert new_mtime != original_mtime
        assert len(tf.modifications) == 1
        
        # Cleanup
        Path(temp_file).unlink()
    
    def test_apply_fog_nonexistent_file(self):
        """Test applying fog to non-existent file raises error."""
        tf = TemporalFog()
        
        with pytest.raises(FileNotFoundError):
            tf.apply_fog("/nonexistent/file.txt")


class TestShadowClone:
    """Test Shadow Clone module."""
    
    def test_create_believable_decoys(self):
        """Test decoy creation."""
        with tempfile.TemporaryDirectory() as temp_dir:
            sc = ShadowClone(output_dir=temp_dir)
            
            decoys = sc.create_believable_decoys(
                activity_type='mixed',
                count=10,
                time_range_days=30
            )
            
            assert len(decoys) == 10
            assert all(Path(d).exists() for d in decoys)
            assert len(sc.get_generated_decoys()) == 10


class TestEntropyInjector:
    """Test Entropy Injection module."""
    
    def test_create_entropy_file(self):
        """Test entropy file creation."""
        ei = EntropyInjector()
        
        with tempfile.NamedTemporaryFile(delete=False) as f:
            temp_file = f.name
        
        # Remove the file first
        Path(temp_file).unlink()
        
        # Create entropy file
        result = ei.create_entropy_file(temp_file, size_mb=1)
        
        assert result is True
        assert Path(temp_file).exists()
        assert Path(temp_file).stat().st_size >= 1024 * 1024
        
        # Cleanup
        Path(temp_file).unlink()
    
    def test_poison_file_carver(self):
        """Test poison file creation."""
        ei = EntropyInjector()
        
        with tempfile.TemporaryDirectory() as temp_dir:
            count = ei.poison_file_carver(temp_dir, num_files=5)
            
            assert count == 5
            files = list(Path(temp_dir).glob('*.dat'))
            assert len(files) == 5


def test_module_imports():
    """Test that all modules can be imported."""
    from phantomtrace import (
        QuantumDecay,
        TemporalFog,
        ShadowClone,
        MemoryWhisper,
        DataCamouflage,
        LogSmoke,
        EntropyInjector,
    )
    
    # Verify all classes exist
    assert QuantumDecay is not None
    assert TemporalFog is not None
    assert ShadowClone is not None
    assert MemoryWhisper is not None
    assert DataCamouflage is not None
    assert LogSmoke is not None
    assert EntropyInjector is not None


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
