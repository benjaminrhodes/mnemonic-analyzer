"""CLI interface for mnemonic analyzer."""

from __future__ import annotations

import json
import sys
import os
from typing import Any, Optional

# Add parent to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import click

from src.entropy import calculate_entropy, validate_wordlist, detect_language
from src.scorer import (
    classify_strength,
    get_kdf_recommendations,
    get_strength_description,
    calculate_cracking_time,
)
from src.wordlists import get_wordlist_set


def analyze_phrase(phrase: str, verbose: bool = False) -> dict[str, Any]:
    """Analyze a mnemonic phrase.
    
    Args:
        phrase: Space-separated mnemonic words
        verbose: Include detailed breakdown
    
    Returns:
        Analysis results dictionary
    """
    words = phrase.strip().split()
    word_count = len(words)

    result = {"word_count": word_count}

    # Validate word count
    if word_count not in [12, 15, 18, 21, 24]:
        result["error"] = f"Invalid word count: {word_count}. Use 12, 15, 18, 21, or 24."
        return result

    # Calculate entropy
    entropy_info = calculate_entropy(word_count)
    result.update(entropy_info)

    # Detect language
    language = detect_language(words)
    result["language"] = language

    # Validate against BIP-39 wordlist
    wordlist = get_wordlist_set("en")
    validation = validate_wordlist(words, wordlist)
    result["wordlist_valid"] = validation["valid"]
    if not validation["valid"]:
        result["invalid_words"] = validation["invalid_words"]

    # Classify strength
    strength = classify_strength(entropy_info["entropy_bits"])
    result["strength"] = strength
    result["strength_description"] = get_strength_description(strength)

    # Calculate cracking time
    cracking = calculate_cracking_time(entropy_info["entropy_bits"])
    result["cracking_time_years"] = cracking["years"]
    
    if verbose:
        result["cracking_time_detailed"] = {
            "seconds": cracking["seconds"],
            "minutes": cracking["minutes"],
            "hours": cracking["hours"],
            "days": cracking["days"],
            "centuries": cracking["centuries"],
        }

    # KDF recommendations
    result["kdf_recommendations"] = get_kdf_recommendations(entropy_info["entropy_bits"])

    return result


@click.group()
def cli():
    """Mnemonic phrase entropy analyzer for BIP-39 wallets."""
    pass


@cli.command()
@click.argument("phrase")
@click.option("--json", "json_output", is_flag=True, help="Output as JSON")
@click.option("--verbose", "-v", is_flag=True, help="Include detailed breakdown")
def analyze(phrase: str, json_output: bool, verbose: bool):
    """Analyze a BIP-39 mnemonic phrase for entropy and strength.
    
    PHRASE: Space-separated mnemonic words (12, 15, 18, 21, or 24 words)
    
    Examples:
    
        mnemonic-analyzer analyze "abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon about"
    
        mnemonic-analyzer analyze "word1 word2 ... word12" --verbose
    """
    result = analyze_phrase(phrase, verbose=verbose)

    if "error" in result:
        click.echo(f"Error: {result['error']}", err=True)
        sys.exit(1)

    if json_output:
        # Remove non-serializable items for JSON output
        json_result = result.copy()
        if "kdf_recommendations" in json_result:
            # Convert KDF recommendations to JSON-serializable format
            kdf = json_result["kdf_recommendations"]
            json_result["kdf_recommendations"] = {
                key: {k: v for k, v in val.items() if k != "description"}
                for key, val in kdf.items() if isinstance(val, dict)
            }
        click.echo(json.dumps(json_result, indent=2))
        return

    # Human-readable output
    print(f"\n🔐 Mnemonic Strength Analysis")
    print(f"{'=' * 45}")
    print(f"  Word Count:     {result['word_count']}")
    print(f"  Language:       {result['language'].upper()}")
    print(f"  Wordlist Valid: {'✅ Yes' if result['wordlist_valid'] else '❌ No'}")
    
    if not result.get("wordlist_valid", True):
        print(f"  Invalid Words:  {', '.join(result.get('invalid_words', []))}")
    
    print(f"\n  Entropy:")
    print(f"    Bits:         {result['entropy_bits']}")
    print(f"    Checksum:      {result['checksum_bits']} bits")
    print(f"    Total:         {result['total_bits']} bits")
    
    print(f"\n  Strength:       {result['strength'].upper()}")
    print(f"    {result['strength_description']}")
    
    print(f"\n  Cracking Time (estimated):")
    print(f"    {result['cracking_time_years']:.2e} years")
    
    if verbose and "cracking_time_detailed" in result:
        dt = result["cracking_time_detailed"]
        print(f"\n  Detailed Time Estimates:")
        if dt["centuries"] > 1:
            print(f"    {dt['centuries']:.2e} centuries")
        elif dt["years"] > 1:
            print(f"    {dt['years']:.2e} years")
        elif dt["days"] > 1:
            print(f"    {dt['days']:.2f} days")
        elif dt["hours"] > 1:
            print(f"    {dt['hours']:.2f} hours")
        elif dt["minutes"] > 1:
            print(f"    {dt['minutes']:.2f} minutes")
        else:
            print(f"    {dt['seconds']:.2f} seconds")
    
    print(f"\n  KDF Recommendations:")
    for kdf, params in result["kdf_recommendations"].items():
        if kdf == "notes":
            print(f"    ⚠️  {params}")
        elif isinstance(params, dict):
            print(f"    {kdf.upper()}:")
            print(f"      {params.get('description', '')}")


@cli.command()
def wordlist():
    """Show supported BIP-39 wordlists."""
    click.echo("Supported languages:")
    click.echo("  - en (English)")
    click.echo("\nMore languages coming soon!")


if __name__ == "__main__":
    cli()
