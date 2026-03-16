import os
import secrets
import shutil
import zipfile
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.backends import default_backend

def derive_key(password, salt):
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000,
        backend=default_backend()
    )
    return kdf.derive(password.encode())

def encrypt_file(path, password):
    salt = secrets.token_bytes(16)
    nonce = secrets.token_bytes(12)
    key = derive_key(password, salt)
    aesgcm = AESGCM(key)

    with open(path, 'rb') as f:
        data = f.read()

    encrypted = aesgcm.encrypt(nonce, data, None)

    out = path + ".enc"
    with open(out, 'wb') as f:
        f.write(salt + nonce + encrypted)

    return out

def decrypt_file(path, password):
    with open(path, 'rb') as f:
        salt = f.read(16)
        nonce = f.read(12)
        ciphertext = f.read()

    key = derive_key(password, salt)
    aesgcm = AESGCM(key)
    data = aesgcm.decrypt(nonce, ciphertext, None)

    out = path.replace(".enc", "")
    with open(out, 'wb') as f:
        f.write(data)

    return out

def zip_folder(folder):
    shutil.make_archive(folder, 'zip', folder)
    return folder + ".zip"

def encrypt_folder(folder, password):
    zip_path = zip_folder(folder)
    enc = encrypt_file(zip_path, password)
    os.remove(zip_path)
    return enc

def decrypt_folder(enc_path, password):
    zip_path = decrypt_file(enc_path, password)
    out_dir = zip_path.replace(".zip", "")
    with zipfile.ZipFile(zip_path, 'r') as z:
        z.extractall(out_dir)
    os.remove(zip_path)
    return out_dir
