"""Core entropy calculation for mnemonic phrases."""

import math
from typing import Optional


def calculate_entropy(word_count: int) -> dict:
    """Calculate entropy based on word count.

    BIP-39 uses 11 bits per word, with checksum varying by word count.
    12 words = 128 bits entropy + 4 bits checksum
    24 words = 256 bits entropy + 8 bits checksum
    """
    if word_count not in [12, 15, 18, 21, 24]:
        raise ValueError(f"Invalid BIP-39 word count: {word_count}")

    entropy_bits = (word_count // 3) * 32
    checksum_bits = word_count // 33
    total_bits = word_count * 11

    return {
        "word_count": word_count,
        "entropy_bits": entropy_bits,
        "checksum_bits": checksum_bits,
        "total_bits": total_bits,
    }


def validate_wordlist(words: list[str], wordlist: set[str]) -> dict:
    """Validate that words are in the all BIP-39 wordlist."""
    invalid_words = [w for w in words if w.lower() not in wordlist]

    return {
        "valid": len(invalid_words) == 0,
        "invalid_words": invalid_words,
        "word_count": len(words),
    }


def detect_language(wordlist: set[str]) -> Optional[str]:
    """Detect the language of a wordlist based on common words."""
    common_words = {
        "abandon": "en",
        "about": "en",
        "above": "en",
        "abandon": "zh",
        "ba": "zh",
        "bei": "zh",
    }
    return common_words.get(next(iter(wordlist), ""), "en")
