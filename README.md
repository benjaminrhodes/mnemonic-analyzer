# Mnemonic Strength Analyzer

A security tool that analyzes cryptocurrency mnemonic phrases for entropy strength and provides KDF recommendations.

## Purpose

This tool calculates the entropy of BIP-39 mnemonic phrases and rates their cryptographic strength. It helps developers and security engineers validate that wallet seed phrases meet industry standards for entropy and provides recommendations for key derivation functions (KDFs).

## Features

- Entropy calculation for BIP-39 wordlists
- Strength classification (weak/moderate/strong)
- KDF recommendations (scrypt, argon2)
- BIP-39 wordlist validation
- CLI interface for easy integration

## Installation

```bash
pip install mnemonic-analyzer
```

## Usage

```bash
python -m src.cli analyze "abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon about"
```

## Testing

```bash
pytest tests/ -v
```

## Security

- Uses synthetic seeds only for testing
- Does not store or transmit any sensitive data
- Local computation only

## License

MIT
