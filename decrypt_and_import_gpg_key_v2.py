# decrypt_and_import_gpg_key.py

import argparse
from mnemonic import Mnemonic
from hashlib import sha256
from Crypto.Cipher import AES
import subprocess
import sys

def unpad_pkcs7(data):
    pad_len = data[-1]
    return data[:-pad_len]

def main():
    parser = argparse.ArgumentParser(description="Descifra e importa una clave GPG desde un archivo cifrado con frase BIP-39.")
    parser.add_argument("--input", default="secret.key.enc", help="Archivo cifrado de entrada (default: secret.key.enc)")
    parser.add_argument("--output", default="restored_secret.key", help="Archivo de salida con la clave restaurada")
    args = parser.parse_args()

    seed_phrase = input("🧠 Ingresa tu frase BIP-39: ").strip()
    mnemo = Mnemonic("english")

    try:
        entropy = mnemo.to_entropy(seed_phrase)
    except Exception:
        print("❌ Frase inválida. Asegúrate de que sea una frase BIP-39 válida.")
        sys.exit(1)

    key = sha256(entropy).digest()
    iv = b"\x00" * 16

    # Leer archivo cifrado
    with open(args.input, "rb") as f:
        ciphertext = f.read()

    cipher = AES.new(key, AES.MODE_CBC, iv)
    padded = cipher.decrypt(ciphertext)
    plaintext = unpad_pkcs7(padded)

    # Guardar archivo restaurado
    with open(args.output, "wb") as f:
        f.write(plaintext)

    print(f"\n✅ Clave restaurada y guardada en: {args.output}")

    # Importar en GPG (opcional)
    subprocess.run(["gpg", "--import", args.output])

if __name__ == "__main__":
    main()

