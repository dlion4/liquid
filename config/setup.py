import os
from datetime import datetime
from datetime import timedelta
from pathlib import Path

import jwt
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa

from .settings.base import env

BASE_DIR = Path(__file__).resolve().parent.parent
PRIVATE_KEY_PATH = os.path.join(BASE_DIR, "keys", "private.pem")
PUBLIC_KEY_PATH = os.path.join(BASE_DIR, "keys", "public.pem")

password = env("RSA_ENCRYPTION_PASSWORD").encode()

def generate_keys():
    """
    Generate RSA private and public keys if they do not exist.
    """
    if not os.path.exists(PRIVATE_KEY_PATH) or not os.path.exists(PUBLIC_KEY_PATH):
        private_key = rsa.generate_private_key(
        public_exponent=65537, key_size=2048, backend=default_backend(),
    )

        # Save the private key with an encryption algorithm (e.g., PBKDF2)
        encryption_algorithm = serialization.BestAvailableEncryption(password)
        with open(PRIVATE_KEY_PATH, "wb") as f:
            f.write(
                private_key.private_bytes(
                    encoding=serialization.Encoding.PEM,
                    format=serialization.PrivateFormat.TraditionalOpenSSL,
                    encryption_algorithm=encryption_algorithm,
                ),
            )

        # Generate and save the public key
        public_key = private_key.public_key()
        with open(PUBLIC_KEY_PATH, "wb") as f:
            f.write(
                public_key.public_bytes(
                    encoding=serialization.Encoding.PEM,
                    format=serialization.PublicFormat.SubjectPublicKeyInfo,
                ),
            )


def load_keys():
    """
    Load the RSA private and public keys from the file system.
    """
    generate_keys()
    if not os.path.exists(PRIVATE_KEY_PATH):
        return None, None

    with open(PRIVATE_KEY_PATH, "rb") as f:
        private_key_data = f.read()
        try:
            private_key = serialization.load_pem_private_key(
                private_key_data,password=password,backend=default_backend())
        except ValueError:
            raise

    if not os.path.exists(PUBLIC_KEY_PATH):
        return private_key, None

    with open(PUBLIC_KEY_PATH, "rb") as f:
        public_key_data = f.read()
        public_key = serialization.load_pem_public_key(
            public_key_data, backend=default_backend())

    return private_key, public_key


load_keys()


def encode_jwt(payload, exp_minutes=60):
    """
    Encode a JWT token using RSA private key.
    """
    # Ensure keys are generated and loaded

    private_key, _ = load_keys()
    payload["exp"] = datetime.utcnow() + timedelta(minutes=exp_minutes)
    token = jwt.encode(payload, private_key, algorithm="RS256")
    return token


def decode_jwt(token):
    """
    Decode a JWT token using RSA public key.
    """
    _, public_key = load_keys()
    try:
        payload = jwt.decode(token, public_key, algorithms=["RS256"])
        return payload
    except jwt.ExpiredSignatureError:
        return {"error": "Token has expired"}
    except jwt.InvalidTokenError:
        return {"error": "Invalid token"}
