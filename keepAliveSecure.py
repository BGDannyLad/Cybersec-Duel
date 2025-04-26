import socket
import threading
import time

HOST = '0.0.0.0'
PORT = 8888

# Global counters for tracking
connection_count = 0
command_count = 0
start_time = time.time()

def log_event(msg):
    with open("keepalive.log", "a") as f:
        f.write(f"[LOG] {time.ctime()} - {msg}\n")

def vulnerable_copy(user_input):
    """
    Simulated vulnerable function: copies user input into a small fixed-size buffer.
    """
    buffer_size = 32  # Small fixed buffer (like C-style)
    buffer = bytearray(buffer_size)

    for i in range(len(user_input)):
        # NO bounds checking here - classic overflow style
        buffer[i] = user_input[i]

    return buffer

def handle_client(conn, addr):
    global command_count
    print(f"[+] Connection from {addr}")
    log_event(f"Connected from {addr}")
    try:
        while True:
            conn.sendall(b"alive\n")
            data = conn.recv(1024)  # Wait for data from the client
            if not data:
                break

            # Vulnerable part: copy the raw bytes into a fixed buffer
            vulnerable_copy(data)  # <-- Simulates overflow

            command = data.decode().strip()
            command_count += 1  # Increment command count

            if command == "ping":
                conn.sendall(b"pong\n")
            elif command == "status":
                conn.sendall(b"OK\n")
            elif command == "exit":
                break
            else:
                conn.sendall(b"Unknown command\n")

            # Flushing not needed — remove conn.flush()

    except Exception as e:
        log_event(f"Error: {e}")
    finally:
        conn.close()
        log_event(f"Disconnected from {addr}")
        print(f"[-] Disconnected {addr}")

def main():
    global connection_count
    print("[*] KeepAlive Secure Service Started")
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen(5)

    while True:
        conn, addr = server.accept()
        connection_count += 1
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()

        if connection_count % 100 == 0:
            elapsed_time = time.time() - start_time
            print(f"[+] Connections: {connection_count}, Commands Processed: {command_count}, Time Elapsed: {elapsed_time:.2f}s")
            log_event(f"Connections: {connection_count}, Commands Processed: {command_count}, Time Elapsed: {elapsed_time:.2f}s")

if __name__ == "__main__":
    main()
