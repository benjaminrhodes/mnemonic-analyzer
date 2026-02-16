"""Tests for entropy calculation."""

import pytest
from entropy import calculate_entropy, validate_wordlist


def test_entropy_12_words():
    """Test entropy calculation for 12 words."""
    result = calculate_entropy(12)
    assert result["word_count"] == 12
    assert result["entropy_bits"] == 128


def test_entropy_24_words():
    """Test entropy calculation for 24 words."""
    result = calculate_entropy(24)
    assert result["word_count"] == 24
    assert result["entropy_bits"] == 256


def test_invalid_word_count():
    """Test error for invalid word count."""
    with pytest.raises(ValueError):
        calculate_entropy(10)


def test_validate_wordlist_valid():
    """Test wordlist validation with valid words."""
    wordlist = {"abandon", "about", "above"}
    words = ["abandon", "about"]
    result = validate_wordlist(words, wordlist)
    assert result["valid"] is True
    assert len(result["invalid_words"]) == 0


def test_validate_wordlist_invalid():
    """Test wordlist validation with invalid words."""
    wordlist = {"abandon", "about", "above"}
    words = ["abandon", "invalidword"]
    result = validate_wordlist(words, wordlist)
    assert result["valid"] is False
    assert "invalidword" in result["invalid_words"]
