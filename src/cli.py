"""CLI interface for mnemonic analyzer."""

from __future__ import annotations

import sys
from typing import Any, Optional

from entropy import calculate_entropy
from scorer import (
    classify_strength,
    get_kdf_recommendations,
    get_strength_description,
    calculate_cracking_time,
)


def load_wordlist(lang: str = "en") -> set[str]:
    """Load BIP-39 wordlist for specified language."""
    wordlists = {
        "en": {
            "abandon",
            "ability",
            "able",
            "about",
            "above",
            "absent",
            "absorb",
            "abstract",
            "absurd",
            "abuse",
            "access",
            "accident",
            "account",
            "accuse",
            "achieve",
            "acid",
            "acoustic",
            "acquire",
            "across",
            "act",
            "action",
            "actor",
            "actress",
            "actual",
            "adapt",
            "add",
            "addict",
            "address",
            "adjust",
            "admit",
            "adult",
            "advance",
            "advice",
            "aerobic",
            "affair",
            "afford",
            "afraid",
            "again",
            "age",
            "agent",
            "agree",
            "ahead",
            "aim",
            "air",
            "airport",
            "aisle",
            "alarm",
            "album",
        },
    }
    return wordlists.get(lang, wordlists["en"])


def analyze_phrase(phrase: str) -> dict[str, Any]:
    """Analyze a mnemonic phrase."""
    words = phrase.strip().split()
    word_count = len(words)

    result = {"word_count": word_count}

    if word_count not in [12, 15, 18, 21, 24]:
        result["error"] = f"Invalid word count: {word_count}. Use 12, 15, 18, 21, or 24."
        return result

    entropy_info = calculate_entropy(word_count)
    result.update(entropy_info)

    strength = classify_strength(entropy_info["entropy_bits"])
    result["strength"] = strength
    result["strength_description"] = get_strength_description(strength)

    cracking = calculate_cracking_time(entropy_info["entropy_bits"])
    result["cracking_time_years"] = cracking["years"]

    result["kdf_recommendations"] = get_kdf_recommendations(entropy_info["entropy_bits"])

    return result


def main():
    """Main CLI entry point."""
    if len(sys.argv) < 2 or sys.argv[1] != "analyze":
        print("Usage: python -m src.cli analyze <mnemonic_phrase>")
        print("\nExample:")
        print(
            '  python -m src.cli analyze "abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon about"'
        )
        sys.exit(1)

    phrase = " ".join(sys.argv[2:])
    result = analyze_phrase(phrase)

    if "error" in result:
        print(f"Error: {result['error']}")
        sys.exit(1)

    print(f"\nMnemonic Strength Analysis")
    print(f"{'=' * 40}")
    print(f"Word Count: {result['word_count']}")
    print(f"Entropy Bits: {result['entropy_bits']}")
    print(f"Strength: {result['strength'].upper()}")
    print(f"  {result['strength_description']}")
    print(f"\nEstimated Cracking Time: {result['cracking_time_years']:.2e} years")
    print(f"\nKDF Recommendations:")
    for kdf, params in result["kdf_recommendations"].items():
        if kdf == "notes":
            print(f"  Notes: {params}")
        else:
            print(f"  {kdf}: {params.get('description', '')}")


if __name__ == "__main__":
    main()
