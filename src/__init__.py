"""Mnemonic Analyzer package."""

import os
import sys

# Ensure src is in path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.entropy import calculate_entropy
from src.scorer import classify_strength, get_kdf_recommendations

__all__ = ["calculate_entropy", "classify_strength", "get_kdf_recommendations"]
