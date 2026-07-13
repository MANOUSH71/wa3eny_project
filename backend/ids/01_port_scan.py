#!/usr/bin/env python3
"""
Attack 1: Port Scanner — VMware Edition
Target: 127.0.0.1 (localhost) or change TARGET to your VM's IP
"""
from scapy.all import IP, TCP, sr1, conf
import time

conf.verb = 0

TARGET     = "127.0.0.1"
START_PORT = 1
END_PORT   = 500   # scan first 500 ports

print(f"""
╔══════════════════════════════════════╗
║         PORT SCANNER ATTACK          ║
║  Target : {TARGET:<27}║
║  Ports  : {START_PORT} - {END_PORT:<26}║
╚══════════════════════════════════════╝
""")

open_ports = []
start = time.time()

for port in range(START_PORT, END_PORT + 1):
    pkt  = IP(dst=TARGET) / TCP(dport=port, flags="S")
    resp = sr1(pkt, timeout=0.2)

    if resp and resp.haslayer(TCP):
        if resp[TCP].flags == 0x12:   # SYN-ACK = OPEN
            open_ports.append(port)
            print(f"  Port {port:>5} : OPEN ✓")
            # send RST to close cleanly
            sr1(IP(dst=TARGET)/TCP(dport=port, flags="R"), timeout=0.1)
        # RST = closed, ignore

    if port % 100 == 0:
        print(f"  ... scanned up to port {port}")

print(f"""
  Scan done in {time.time()-start:.1f}s
  Open ports: {open_ports}
""")
