#!/usr/bin/env python3
"""
NexusIDS — Attack Menu (VMware Edition)
Run from: sudo python3 run_attacks.py
"""
import subprocess, sys, time, os

BASE = os.path.dirname(os.path.abspath(__file__))

ATTACKS = {
    "1": ("Port Scan     (ports 1-500)",  "01_port_scan.py",  "HIGH"),
    "2": ("SYN Flood     (port 80)",      "02_syn_flood.py",  "CRITICAL"),
    "3": ("ICMP Flood    (ping flood)",   "03_icmp_flood.py", "HIGH"),
    "4": ("SSH Brute     (port 22)",      "04_brute_force.py","MEDIUM"),
    "5": ("UDP Flood     (random ports)", "05_udp_flood.py",  "CRITICAL"),
    "6": ("Run ALL attacks in sequence",  None,               "---"),
}

SEV_COLOR = {
    "CRITICAL": "\033[91m", "HIGH": "\033[93m",
    "MEDIUM":   "\033[33m", "---":  "\033[36m",
}
RESET = "\033[0m"
CYAN  = "\033[96m"

def menu():
    print(f"""
{CYAN}╔══════════════════════════════════════════╗
║      NEXUSIDS — ATTACK MENU (VMware)     ║
║  Target    : 127.0.0.1                  ║
║  Dashboard : http://localhost:5000       ║
╠══════════════════════════════════════════╣{RESET}""")
    for k, (name, _, sev) in ATTACKS.items():
        c = SEV_COLOR.get(sev, "")
        print(f"  [{k}] {name:<34} {c}[{sev}]{RESET}")
    print("  [0] Exit\n")

def run(script):
    path = os.path.join(BASE, script)
    subprocess.run([sys.executable, path])

while True:
    menu()
    choice = input("  Select attack: ").strip()
    if choice == "0":
        break
    elif choice in ATTACKS:
        name, script, _ = ATTACKS[choice]
        if choice == "6":
            for k,(n,s,_) in ATTACKS.items():
                if s:
                    print(f"\n  >>> {n}")
                    time.sleep(1)
                    run(s)
                    print("  >>> Waiting 5s...\n")
                    time.sleep(5)
        else:
            print(f"\n  >>> Launching: {name}\n")
            run(script)
    else:
        print("  Invalid choice.\n")
