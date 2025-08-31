# encrypt_ssh_key.py

import argparse
from mnemonic import Mnemonic
from hashlib import sha256
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes

def pad_pkcs7(data):
    pad_len = 16 - len(data) % 16
    return data + bytes([pad_len] * pad_len)

def encrypt_file(file_path, seed):
    key = sha256(seed.encode()).digest()
    with open(file_path, "rb") as f:
        data = f.read()
    cipher = AES.new(key, AES.MODE_CBC, iv=b"\x00"*16)
    encrypted = cipher.encrypt(pad_pkcs7(data))
    out_file = file_path + ".enc"
    with open(out_file, "wb") as f:
        f.write(encrypted)
    return out_file

def main():
    parser = argparse.ArgumentParser(description="Cifra clave SSH privada usando frase BIP-39.")
    parser.add_argument("--input", required=True, help="Clave SSH privada (ej: id_ed25519)")
    parser.add_argument("--output", default="id_ed25519.enc", help="Archivo cifrado de salida")
    args = parser.parse_args()

    # Generar frase
    mnemo = Mnemonic("english")
    entropy = get_random_bytes(32)
    seed_words = mnemo.to_mnemonic(entropy)
    key = sha256(entropy).digest()

    with open(args.input, "rb") as f:
        private_key = f.read()

    cipher = AES.new(key, AES.MODE_CBC, iv=b"\x00" * 16)
    encrypted = cipher.encrypt(pad_pkcs7(private_key))

    with open(args.output, "wb") as f:
        f.write(encrypted)

    print(f"\n✅ Clave SSH cifrada guardada en: {args.output}")
    print("\n🧠 Frase BIP-39 de recuperación:\n")
    print(seed_words)
    print("\n⚠️ Guarda esta frase en un lugar seguro. Es tu única forma de restaurar la clave.")

if __name__ == "__main__":
    main()

