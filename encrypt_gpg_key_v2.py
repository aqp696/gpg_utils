# encrypt_gpg_key.py

import argparse
import subprocess
from mnemonic import Mnemonic
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from hashlib import sha256

def pad_pkcs7(data):
    pad_len = 16 - (len(data) % 16)
    return data + bytes([pad_len] * pad_len)

def main():
    parser = argparse.ArgumentParser(description="Cifra una clave GPG secreta usando una frase BIP-39.")
    parser.add_argument("--key-id", required=True, help="KEY ID de la clave GPG secreta")
    parser.add_argument("--output", default="secret.key.enc", help="Nombre del archivo de salida cifrado (default: secret.key.enc)")
    args = parser.parse_args()

    # 1. Generar frase BIP-39
    mnemo = Mnemonic("english")
    entropy = get_random_bytes(32)  # 256 bits
    seed_words = mnemo.to_mnemonic(entropy)
    key = sha256(entropy).digest()

    # 2. Exportar clave GPG secreta
    try:
        secret = subprocess.check_output(["gpg", "--export-secret-key", args.key_id])
    except subprocess.CalledProcessError as e:
        print("❌ Error al exportar clave GPG:", e)
        return

    # 3. Cifrar con AES-256-CBC
    iv = b"\x00" * 16  # Fijo para simplificar (puedes cambiarlo si lo guardas)
    cipher = AES.new(key, AES.MODE_CBC, iv)
    ciphertext = cipher.encrypt(pad_pkcs7(secret))

    # 4. Guardar archivo
    with open(args.output, "wb") as f:
        f.write(ciphertext)

    print(f"\n✅ Clave GPG cifrada guardada en: {args.output}")
    print("\n🧠 Frase BIP-39 de recuperación:\n")
    print(seed_words)
    print("\n⚠️ Guarda esta frase en un lugar seguro. Es la única forma de descifrar el archivo.")

if __name__ == "__main__":
    main()

