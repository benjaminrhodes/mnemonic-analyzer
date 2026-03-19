"""Core entropy calculation for mnemonic phrases."""

import math
from typing import Optional

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.wordlists import get_wordlist, get_wordlist_set


def calculate_entropy(word_count: int) -> dict:
    """Calculate entropy based on word count.

    BIP-39 uses 11 bits per word, with checksum varying by word count.
    12 words = 128 bits entropy + 4 bits checksum
    24 words = 256 bits entropy + 8 bits checksum
    """
    if word_count not in [12, 15, 18, 21, 24]:
        raise ValueError(f"Invalid BIP-39 word count: {word_count}")

    entropy_bits = (word_count // 3) * 32
    checksum_bits = word_count // 3
    total_bits = word_count * 11

    return {
        "word_count": word_count,
        "entropy_bits": entropy_bits,
        "checksum_bits": checksum_bits,
        "total_bits": total_bits,
    }


def validate_wordlist(words: list[str], wordlist: Optional[set[str]] = None) -> dict:
    """Validate that words are in the BIP-39 wordlist.
    
    Args:
        words: List of mnemonic words to validate
        wordlist: Optional custom wordlist. If not provided, uses English BIP-39.
    
    Returns:
        Dict with validation results
    """
    if wordlist is None:
        wordlist = get_wordlist_set("en")
    
    invalid_words = [w for w in words if w.lower() not in wordlist]

    return {
        "valid": len(invalid_words) == 0,
        "invalid_words": invalid_words,
        "word_count": len(words),
    }


def detect_language(words: list[str]) -> Optional[str]:
    """Detect the language of a mnemonic phrase.
    
    Args:
        words: List of mnemonic words
    
    Returns:
        Language code (en, es, fr, it, ja, ko, pt, zh) or None
    """
    if not words:
        return None
    
    first_word = words[0].lower()
    
    # Language indicators based on first word of each BIP-39 wordlist
    language_indicators = {
        "en": ["abandon", "ability", "able", "about"],
        "es": ["ábaco", "abdomen", "abeja", "abrir"],
        "fr": ["abaisser", "abandon", "abattre", "abriter"],
        "it": ["abbandonare", "abbinare", "abitare", "abrogare"],
        "pt": ["abaixo", "abandonar", "abater", "aberto"],
        "ja": ["あいこう", "あいこく", "あいする", "あいて"],
        "ko": ["가격", "가까이", "가계", "가정"],
        "zh": ["的", "一", "不", "人"],
    }
    
    for lang, indicators in language_indicators.items():
        if first_word in indicators:
            return lang
    
    return "en"  # Default to English
