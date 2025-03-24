import base64
import json
import os
from datetime import datetime
from enum import Enum
from typing import Any

from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from passlib.context import CryptContext

from app.core.settings import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


## External Function ##
def encrypt_data(data: Any) -> str:
    data = _convert_data_to_string(data)
    json_data = json.dumps(data).encode('utf-8')
    iv = os.urandom(16)
    padder = padding.PKCS7(128).padder()
    padded_data = padder.update(json_data) + padder.finalize()
    cipher = Cipher(algorithms.AES(_decode_key(settings.CRYPTO_SECRET)), modes.CBC(iv), backend=default_backend())
    encryptor = cipher.encryptor()
    encrypted_content = encryptor.update(padded_data) + encryptor.finalize()
    encrypted_data = iv + encrypted_content
    return encrypted_data.hex()


def decrypt_data(encrypted_data: str) -> str:
    encrypted_data_bytes = bytes.fromhex(encrypted_data)
    iv = encrypted_data_bytes[:16]
    encrypted_content = encrypted_data_bytes[16:]
    cipher = Cipher(algorithms.AES(_decode_key(settings.CRYPTO_SECRET)), modes.CBC(iv), backend=default_backend())
    decryptor = cipher.decryptor()
    padded_data = decryptor.update(encrypted_content) + decryptor.finalize()
    unpadder = padding.PKCS7(128).unpadder()
    data = unpadder.update(padded_data) + unpadder.finalize()
    return data.decode('utf-8')


def hash_data(data: Any) -> str:
    data = _convert_data_to_string(data)
    return pwd_context.hash(data)


def verify_data(data: Any, hashed_data: str) -> bool:
    data = _convert_data_to_string(data)
    return pwd_context.verify(data, hashed_data)


## Internal Function ##
def _decode_key(key_aes: str)-> bytes:
    base64_key = base64.b64decode(key_aes)
    return base64_key


def _convert_data_to_string(data: Any) -> Any:
    if isinstance(data, dict):
        return {k: _convert_data_to_string(v) for k, v in data.items()}
    elif isinstance(data, datetime):
        return data.isoformat()
    elif isinstance(data, Enum):
        return data.value
    elif isinstance(data, list):
        return [_convert_data_to_string(i) for i in data]
    else:
        return data
