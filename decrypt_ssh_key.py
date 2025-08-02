# decrypt_ssh_key.py

import argparse
from mnemonic import Mnemonic
from hashlib import sha256
from Crypto.Cipher import AES
import os

def unpad_pkcs7(data):
    pad_len = data[-1]
    return data[:-pad_len]

def main():
    parser = argparse.ArgumentParser(description="Descifra una clave SSH privada desde una frase BIP-39.")
    parser.add_argument("--input", default="id_ed25519.enc", help="Archivo cifrado de entrada")
    parser.add_argument("--output", default="id_ed25519", help="Archivo restaurado de salida (clave privada SSH)")
    args = parser.parse_args()

    seed_phrase = input("🧠 Ingresa tu frase BIP-39: ").strip()
    mnemo = Mnemonic("english")

    try:
        entropy = mnemo.to_entropy(seed_phrase)
    except Exception:
        print("❌ Frase inválida. Asegúrate de que sea una frase BIP-39 válida.")
        return

    key = sha256(entropy).digest()

    with open(args.input, "rb") as f:
        encrypted = f.read()

    cipher = AES.new(key, AES.MODE_CBC, iv=b"\x00" * 16)
    padded = cipher.decrypt(encrypted)
    private_key = unpad_pkcs7(padded)

    with open(args.output, "wb") as f:
        f.write(private_key)

    os.chmod(args.output, 0o600)
    print(f"\n✅ Clave SSH restaurada en: {args.output}")

if __name__ == "__main__":
    main()

