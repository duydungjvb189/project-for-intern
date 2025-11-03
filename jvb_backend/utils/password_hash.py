"""Password hashing utilities.

This module wraps Passlib's CryptContext to provide a simple API for
hashing and verifying passwords. The project is configured to use the
Argon2 algorithm by default (configured in `pwd_context`).

Security note: Do NOT log or print plaintext passwords in production.
"""

from passlib.context import CryptContext

# CryptContext configured to use Argon2. Adjust schemes here if you need
# to support other hash algorithms or migration strategies.
pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")


def hash_password(password: str) -> str:
    """Hash a plaintext password using the configured hashing algorithm.

    Args:
        password: Plaintext password provided by the user.

    Returns:
        A hashed password string suitable for storage in the database.
    """
    # Avoid printing or logging the plaintext password.
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a plaintext password against a stored hash.

    Args:
        plain_password: The plaintext password to verify.
        hashed_password: The hashed password retrieved from storage.

    Returns:
        True if the plaintext password matches the hashed password,
        otherwise False.
    """
    return pwd_context.verify(plain_password, hashed_password)