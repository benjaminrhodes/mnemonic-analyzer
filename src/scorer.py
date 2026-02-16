"""Strength classification and KDF recommendations."""


def classify_strength(entropy_bits: int) -> str:
    """Classify entropy strength."""
    if entropy_bits < 128:
        return "weak"
    elif entropy_bits < 256:
        return "moderate"
    return "strong"


def get_strength_description(strength: str) -> str:
    """Get human-readable strength description."""
    descriptions = {
        "weak": "Vulnerable to brute-force attacks. Not recommended for production.",
        "moderate": "Acceptable for most use cases. Consider 24 words for higher security.",
        "strong": "Industry standard. Resistant to current brute-force capabilities.",
    }
    return descriptions.get(strength, "Unknown")


def get_kdf_recommendations(entropy_bits: int) -> dict:
    """Get KDF recommendations based on entropy."""
    recommendations: dict = {
        "scrypt": {
            "n": 2**18,
            "r": 8,
            "p": 1,
            "description": "Memory-hard function, recommended for key derivation",
        },
        "argon2": {
            "type": "id",
            "m": 65536,
            "t": 3,
            "p": 4,
            "description": "Winner of Password Hashing Competition",
        },
        "pbkdf2": {
            "iterations": 600000,
            "hash": "sha256",
            "description": "Widely supported, NIST approved",
        },
    }

    if entropy_bits < 128:
        recommendations["notes"] = "Consider using stronger KDF parameters"  # type: ignore

    return recommendations


def calculate_cracking_time(entropy_bits: int) -> dict:
    """Estimate time to crack based on entropy."""
    guesses_per_second = 1e10

    total_guesses = 2**entropy_bits
    seconds = total_guesses / guesses_per_second

    return {
        "entropy_bits": entropy_bits,
        "guesses": total_guesses,
        "seconds": seconds,
        "years": seconds / (365 * 24 * 3600),
    }
