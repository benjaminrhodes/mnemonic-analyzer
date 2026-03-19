# Mnemonic Strength Analyzer

A security tool that analyzes BIP-39 mnemonic phrases for entropy strength and provides KDF recommendations.

## Purpose

This tool calculates the entropy of BIP-39 mnemonic phrases and rates their cryptographic strength. It helps developers and security engineers validate that wallet seed phrases meet industry standards for entropy and provides recommendations for key derivation functions (KDFs).

## Features

- **Entropy calculation** — Accurate BIP-39 entropy (128/256 bits for 12/24 words)
- **Strength classification** — weak / moderate / strong with descriptions
- **Cracking time estimates** — Realistic GPU cluster attack scenarios
- **KDF recommendations** — scrypt, argon2, pbkdf2 parameters
- **BIP-39 validation** — Validates words against official 2048-word English wordlist
- **Language detection** — Auto-detects mnemonic language
- **CLI interface** — Human-readable or JSON output for automation

## Installation

```bash
# From PyPI
pip install mnemonic-analyzer

# Or install from source
git clone https://github.com/benjaminrhodes/mnemonic-analyzer.git
cd mnemonic-analyzer
pip install -e .
```

## Usage

### Analyze a mnemonic phrase

```bash
mnemonic-analyzer analyze "abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon about"
```

Output:
```
🔐 Mnemonic Strength Analysis
=============================================
  Word Count:     12
  Language:       EN
  Wordlist Valid: ✅ Yes

  Entropy:
    Bits:         128
    Checksum:      4 bits
    Total:         132 bits

  Strength:       MODERATE
    Acceptable for most use cases. Consider 24 words for higher security.

  Cracking Time (estimated):
    1.08e+26 years
```

### Verbose mode (detailed breakdown)

```bash
mnemonic-analyzer analyze "abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon about" --verbose
```

### JSON output (for scripting)

```bash
mnemonic-analyzer analyze "abandon ... about" --json
```

```json
{
  "word_count": 12,
  "entropy_bits": 128,
  "checksum_bits": 4,
  "total_bits": 132,
  "language": "en",
  "wordlist_valid": true,
  "strength": "moderate",
  "cracking_time_years": 1.08e+26,
  "kdf_recommendations": {
    "scrypt": { "n": 262144, "r": 8, "p": 1 },
    "argon2": { "type": "id", "m": 65536, "t": 3, "p": 4 }
  }
}
```

## Understanding the Output

### Entropy Bits

| Words | Entropy | Checksum | Total |
|-------|---------|----------|-------|
| 12    | 128     | 4        | 132   |
| 15    | 160     | 5        | 165   |
| 18    | 192     | 6        | 198   |
| 21    | 224     | 7        | 231   |
| 24    | 256     | 8        | 264   |

### Strength Classification

- **weak** (<128 bits): Vulnerable to brute-force. Not recommended.
- **moderate** (128 bits): Acceptable for most use cases. 24 words recommended for higher security.
- **strong** (≥256 bits): Industry standard. Resistant to current brute-force capabilities.

### Cracking Time

Estimates assume a dedicated GPU cluster performing 100,000 guesses/second against a properly configured KDF (scrypt/argon2). This is conservative — many real-world attacks are slower due to memory-hard functions.

## Development

```bash
# Clone and install with dev dependencies
git clone https://github.com/benjaminrhodes/mnemonic-analyzer.git
cd mnemonic-analyzer
pip install -e ".[dev]"

# Run tests
pytest tests/ -v

# Lint
ruff check src/
```

## Security

- **Uses synthetic seeds only** for testing
- **Does not store or transmit** any sensitive data
- **Local computation only** — no network requests
- **For educational purposes** — cryptographically secure random generation requires dedicated libraries (e.g., `secrets`, `os.urandom`)

## License

MIT
