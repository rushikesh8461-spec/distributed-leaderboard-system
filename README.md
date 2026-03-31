# Distributed Leaderboard System using Secure Socket Programming

## Project Overview
This project is a secure multi-client Distributed Leaderboard System developed using Python socket programming. It follows a client-server architecture where multiple clients can connect to a central server, join the leaderboard, update scores, and retrieve the sorted leaderboard.

The communication between the client and server is secured using SSL/TLS.

## Features
- Multi-client client-server architecture
- Secure communication using SSL/TLS
- Commands supported:
  - JOIN username
  - UPDATE username score
  - GET
  - TOP n
  - SAVE
  - EXIT
- Leaderboard sorted by:
  - Highest score first
  - Alphabetical order if scores are equal
- Case-insensitive username handling
- Duplicate user prevention
- Persistent storage using `leaderboard.json`

## Technologies Used
- Python
- Socket Programming
- TCP Protocol
- SSL/TLS (`ssl` module)
- Threading
- JSON file storage

## Files
- `server.py` → Main server program
- `client.py` → Client program
- `server.crt` → SSL certificate file (optional)

## How to Run

### 1. Start the server
```bash
python server.py
