
import socket
import ssl
import threading
import json
import os
import time

LEADERBOARD_FILE = "leaderboard.json"
leaderboard = {}
lock = threading.Lock()


def load_leaderboard():
    global leaderboard
    if os.path.exists(LEADERBOARD_FILE):
        try:
            with open(LEADERBOARD_FILE, "r") as f:
                leaderboard = json.load(f)
                # Ensure scores are integers
                leaderboard = {k: int(v) for k, v in leaderboard.items()}
        except:
            leaderboard = {}
    else:
        leaderboard = {}


def save_leaderboard():
    with open(LEADERBOARD_FILE, "w") as f:
        json.dump(leaderboard, f)


def get_sorted_board():
    return sorted(leaderboard.items(), key=lambda x: (-x[1], x[0]))


def handle_client(conn):
    while True:
        try:
            data = conn.recv(1024).decode().strip()
            if not data:
                break

            parts = data.split()
            if not parts:
                conn.send(b"Invalid command\n")
                continue

            command = parts[0].upper()

            if command == "JOIN":
                if len(parts) != 2:
                    conn.send(b"Invalid JOIN format. Use: JOIN username\n")
                    continue

                username = parts[1].upper()

                with lock:
                    if username not in leaderboard:
                        leaderboard[username] = 0
                        save_leaderboard()
                        conn.send(b"User joined\n")
                    else:
                        conn.send(b"User already exists\n")

            elif command == "UPDATE":
                if len(parts) != 3:
                    conn.send(b"Invalid UPDATE format. Use: UPDATE username score\n")
                    continue

                username = parts[1].upper()

                try:
                    score = int(parts[2])
                except ValueError:
                    conn.send(b"Score must be a number\n")
                    continue

                with lock:
                    if username in leaderboard:
                        leaderboard[username] = score
                        save_leaderboard()
                        conn.send(b"Score updated\n")
                    else:
                        conn.send(b"User not found. Please JOIN first\n")

            elif command == "GET":
                with lock:
                    sorted_board = get_sorted_board()

                    if not sorted_board:
                        conn.send(b"Leaderboard is empty\n")
                    else:
                        board = "\n".join([f"{u}:{s}" for u, s in sorted_board])
                        conn.send(board.encode())

            elif command == "TOP":
                if len(parts) != 2:
                    conn.send(b"Invalid TOP format. Use: TOP n\n")
                    continue

                try:
                    n = int(parts[1])
                except ValueError:
                    conn.send(b"TOP value must be a number\n")
                    continue

                with lock:
                    sorted_board = get_sorted_board()[:n]

                    if not sorted_board:
                        conn.send(b"Leaderboard is empty\n")
                    else:
                        board = "\n".join([f"{u}:{s}" for u, s in sorted_board])
                        conn.send(board.encode())

            elif command == "SAVE":
                with lock:
                    save_leaderboard()
                conn.send(b"Leaderboard saved\n")

            else:
                conn.send(b"Invalid command\n")

        except (ConnectionResetError, BrokenPipeError, ssl.SSLError):
            break
        except:
            break

    try:
        conn.close()
    except:
        pass


load_leaderboard()

context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
context.load_cert_chain(certfile="server.crt", keyfile="server.key")

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind(("localhost", 5000))
server.listen(10)

print("Server started...")

while True:
    try:
        client, addr = server.accept()
        secure_client = context.wrap_socket(client, server_side=True)
        threading.Thread(target=handle_client, args=(secure_client,), daemon=True).start()
    except ssl.SSLError:
        print("SSL handshake failed")
    except KeyboardInterrupt:
        print("\nServer shutting down...")
        break
    except:
        continue

server.close()