# 📦 requirements
* python==3.12.4
* mnemonic==0.20
* pycryptodome==3.20.0
* gpg==2.4.4
* ligbcrypt 1.10.3

## Python installation via asdf (optional)
* homebrew==4.5.13
* asdf==0.18.0
* ubuntu=24.04

[homebrew installation](https://brew.sh/)

[asdf installation](https://asdf-vm.com/guide/getting-started.html#_1-install-asdf)

[asdf python plugin](https://github.com/asdf-community/asdf-python)

# SSH
## ▶️ Cómo usar
### 🔐 Crear y cifrar clave SSH

```bash
ssh-keygen -t ed25519 -f id_ed25519 -C "tu@email.com"
python encrypt_ssh_key.py --input id_ed25519 --output id_ed25519.enc
```

🔐 Guarda la seed phrase que imprime.
Puedes borrar id_ed25519 después si deseas seguridad.

### 🔓 Restaurar clave SSH privada

```bash
python decrypt_ssh_key.py --input id_ed25519.enc --output id_ed25519
```
Esto restaurará la clave privada id_ed25519 (ya lista para usar con ssh o git).

# GPG

## ▶️ Cómo usar
### 🔐 Cifrado
```bash
python encrypt_gpg_key.py --key-id 0x1234ABCD --output mi_backup_cifrado.gpgenc
```


* Imprimirá la seed BIP-39
* Guardará tu clave GPG cifrada como mi_backup_cifrado.gpgenc

### 🔓 Descifrado + Importación
```bash
python decrypt_and_import_gpg_key.py --input mi_backup_cifrado.gpgenc --output restaurada.key
```

* Te pedirá la frase BIP-39
* Restaurará e importará la clave en GPG


