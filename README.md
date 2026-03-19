# Crypto Security 101: Learn by Building

> Build tools that actually teach you how crypto works under the hood.

## Why This Course?

You use cryptocurrency every day — but how much do you actually understand about what's happening under the hood?

This is a hands-on course for developers who want to:
- **Understand** how crypto wallets actually work
- **Build** real security tools (not just use them)
- **Learn** by doing — every project solves a real problem

## What You'll Build

| Project | Concepts Learned |
|---------|------------------|
| **1. Mnemonic Analyzer** | Entropy, BIP-39, randomness, seed phrases |
| **2. Key Derivation Engine** | KDFs (scrypt, argon2, pbkdf2), password hashing |
| **3. Wallet Validator** | Address formats, checksum validation, network prefixes |
| **4. Transaction Signing Demo** | Elliptic curves, digital signatures, ECDSA |

By the end, you'll understand why "12 random words" isn't enough — and how to build systems that are actually secure.

## Project 1: Mnemonic Analyzer

Your first tool analyzes BIP-39 seed phrases (those 12-24 word lists your wallet gives you).

### What is BIP-39?

When you create a crypto wallet, it generates a **mnemonic phrase** — a list of words that represents your private key. Here's how it works:

```
Random bytes (128-256 bits) → BIP-39 wordlist → Your seed phrase
```

**Example:**
```
abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon about
```

That string of words represents 128 bits of entropy. But here's the thing — most people don't understand what that actually means.

### What This Tool Does

```bash
# Analyze any mnemonic phrase
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
    Total:        132 bits

  Strength:       MODERATE
    Acceptable for most use cases. Consider 24 words for higher security.

  Cracking Time (estimated):
    1.08e+26 years
```

### What You'll Learn

1. **Entropy** — Why more words = more security
2. **BIP-39** — The standard that makes wallet recovery possible
3. **Checksums** — How the last word validates the rest
4. **Strength classification** — What "128 bits" actually means

## Installation

```bash
git clone https://github.com/benjaminrhodes/mnemonic-analyzer.git
cd mnemonic-analyzer
pip install -e .

# Run the analyzer
mnemonic-analyzer analyze "abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon about"
```

## Course Roadmap

### Phase 1: Foundations (Complete)
- [x] Entropy & randomness
- [x] BIP-39 wordlists
- [x] CLI tool basics

### Phase 2: Key Derivation (In Progress)
- [ ] Understanding KDFs
- [ ] scrypt vs argon2 vs pbkdf2
- [ ] Building a key derivation engine

### Phase 3: Advanced
- [ ] HD wallets (BIP-32)
- [ ] Address generation
- [ ] Transaction signing basics

## Who Is This For?

- **Developers** who use crypto but want to understand it
- **Security professionals** who need to audit wallet implementations
- **Curious engineers** who learn by building

## Prerequisites

- Basic Python knowledge
- Familiarity with the command line
- Curiosity about how things work

## Contributing

This is a learning project. Found a bug? Have a suggestion? PRs welcome.

## Disclaimer

⚠️ **Educational purposes only.** This code helps you learn about crypto security — don't use it to generate real wallets or handle actual cryptocurrency without understanding the full security implications.

## License

MIT

---

**Next:** [Project 2: Building a Key Derivation Engine →](./projects/02-key-derivation.md)

---

Built by [Benjamin Rhodes](https://github.com/benjaminrhodes) | [Follow @basicbeny](https://twitter.com/basicbeny)
