#!/usr/bin/env python3
"""
Attack 4: SSH Brute Force — VMware Edition
Tries real TCP connections to port 22 (SSH) on localhost.
The IDS detects the repeated connection attempts.
"""
import socket
import time

TARGET = "127.0.0.1"
PORT   = 22

USERNAMES = ["admin", "root", "labuser", "ubuntu", "user", "pi"]
PASSWORDS = [
    "password", "123456", "admin", "letmein", "qwerty",
    "abc123", "root", "toor", "pass", "test",
    "hello", "welcome", "master", "dragon", "monkey",
    "password1", "1234", "12345", "123123", "shadow",
]

print(f"""
╔══════════════════════════════════════╗
║        SSH BRUTE FORCE ATTACK        ║
║  Target : {TARGET}:{PORT:<21}║
║  Combos : {len(USERNAMES)*len(PASSWORDS):<27}║
╚══════════════════════════════════════╝
""")

attempt = 0
for user in USERNAMES:
    for passwd in PASSWORDS:
        attempt += 1
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(1)
            s.connect((TARGET, PORT))
            banner = s.recv(128).decode("utf-8", errors="ignore").strip()
            print(f"  [{attempt:>3}] {user}:{passwd:<12} → connected | {banner[:35]}")
            s.close()
        except Exception:
            print(f"  [{attempt:>3}] {user}:{passwd:<12} → failed")
        time.sleep(0.05)

print(f"\n  Brute force complete — {attempt} attempts made.\n")
