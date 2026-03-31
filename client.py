import socket
import ssl

context = ssl.create_default_context()
context.check_hostname = False
context.verify_mode = ssl.CERT_NONE

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
secure_sock = context.wrap_socket(sock, server_hostname="localhost")

secure_sock.connect(("localhost", 5000))

print("Connected to secure leaderboard server.")
print("Commands:")
print("JOIN username")
print("UPDATE username score")
print("GET")
print("TOP n")
print("SAVE")
print("Type EXIT to quit")

while True:
    msg = input("Enter command: ").strip()

    if msg.upper() == "EXIT":
        print("Client exiting...")
        break

    secure_sock.send(msg.encode())

    data = secure_sock.recv(4096).decode()
    print(data)

secure_sock.close()