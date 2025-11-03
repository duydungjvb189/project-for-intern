from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")

# Hash a plain-text password using bcrypt.
def hash_password(password: str) -> str:
    print("DEBUG password:", password, "| type:", type(password))
    return pwd_context.hash(password)

# Verify a plain-text password against its hashed version.
def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)