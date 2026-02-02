from passlib.context import CryptContext
import logging

# To ignore a warning due to an unhandled bcrypt exception
logging.getLogger("passlib").setLevel(logging.ERROR)

# Helper instance allowing secure hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    """Takes a string password and creates a hashed version of it."""
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Checks a plain password and verifies it against its corresponding
    hashed password.
    """
    return pwd_context.verify(plain_password, hashed_password)
