"""Tests for strength scoring."""

import pytest
from scorer import (
    classify_strength,
    get_strength_description,
    get_kdf_recommendations,
    calculate_cracking_time,
)


def test_weak_strength():
    """Test classification of weak entropy."""
    assert classify_strength(64) == "weak"
    assert classify_strength(100) == "weak"


def test_moderate_strength():
    """Test classification of moderate entropy."""
    assert classify_strength(128) == "moderate"
    assert classify_strength(200) == "moderate"


def test_strong_strength():
    """Test classification of strong entropy."""
    assert classify_strength(256) == "strong"
    assert classify_strength(512) == "strong"


def test_strength_description():
    """Test strength description retrieval."""
    desc = get_strength_description("weak")
    assert "Vulnerable" in desc


def test_kdf_recommendations():
    """Test KDF recommendations."""
    recs = get_kdf_recommendations(128)
    assert "scrypt" in recs
    assert "argon2" in recs


def test_cracking_time():
    """Test cracking time estimation."""
    result = calculate_cracking_time(128)
    assert result["entropy_bits"] == 128
    assert result["years"] > 0
