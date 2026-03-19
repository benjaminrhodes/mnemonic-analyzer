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
    """Estimate time to crack based on entropy.
    
    Uses realistic BIP-39 cracking rates:
    - GPU cluster (high-end): ~10^5-10^6 guesses/sec for scrypt/argon2
    - Single high-end GPU: ~10^4 guesses/sec
    - CPU: ~10^2-10^3 guesses/sec
    
    We use conservative estimate assuming dedicated cracking hardware.
    """
    # Conservative: 100,000 guesses per second (good GPU cluster on KDF)
    guesses_per_second = 1e5

    total_guesses = 2**entropy_bits
    seconds = total_guesses / guesses_per_second
    
    # Convert to human-readable time units
    minutes = seconds / 60
    hours = minutes / 60
    days = hours / 24
    years = days / 365
    centuries = years / 100

    return {
        "entropy_bits": entropy_bits,
        "guesses": total_guesses,
        "guesses_per_second": guesses_per_second,
        "seconds": seconds,
        "minutes": minutes,
        "hours": hours,
        "days": days,
        "years": years,
        "centuries": centuries,
    }
