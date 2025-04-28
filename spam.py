import socket
import threading

TARGET_IP = '192.161.1.2'
TARGET_PORT = 8888

def fast_spam():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((TARGET_IP, TARGET_PORT))
        for _ in range(1000):
            s.sendall(b"ping\n")
            print(s.recv(1024).decode(), end="")
        s.close()
    except Exception as e:
        print(f"[!] Error: {e}")

# Launch multiple threads
for _ in range(50):
    threading.Thread(target=fast_spam).start()
