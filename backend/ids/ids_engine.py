#!/usr/bin/env python3
"""
NexusIDS — VMware Single-VM Edition
Auto-detects the network interface.
Target = localhost (127.0.0.1)
Attacker = also localhost (same machine, different terminal)
"""

from scapy.all import sniff, IP, TCP, UDP, ICMP, conf, get_if_list
from flask import Flask, jsonify
from flask_cors import CORS
import threading, time, subprocess
from datetime import datetime
from collections import defaultdict, deque

conf.verb = 0

app  = Flask(__name__)
CORS(app)
LOCK = threading.Lock()

# ─────────────────────────────────────────
#  Auto-detect network interface
# ─────────────────────────────────────────
def get_interface():
    """Pick the best interface to sniff on."""
    try:
        result = subprocess.check_output(
            "ip route | grep default | awk '{print $5}'",
            shell=True).decode().strip().split('\n')[0]
        if result:
            return result
    except:
        pass

    # Fallback: try common VMware interface names
    for name in ["ens33", "ens32", "eth0", "enp0s3", "enp0s8"]:
        if name in get_if_list():
            return name

    return get_if_list()[0]  # last resort: first available

IFACE = get_interface()

# ─────────────────────────────────────────
#  Shared State
# ─────────────────────────────────────────
alerts          = deque(maxlen=300)
alert_id        = [0]
traffic_stats   = {"total":0,"tcp":0,"udp":0,"icmp":0,"other":0,"bytes":0}
traffic_timeline = deque(maxlen=60)

syn_tracker  = defaultdict(lambda: deque(maxlen=5000))
icmp_tracker = defaultdict(lambda: deque(maxlen=5000))
udp_tracker  = defaultdict(lambda: deque(maxlen=5000))
ssh_tracker  = defaultdict(lambda: deque(maxlen=500))
port_tracker = defaultdict(lambda: {"ports": set(), "first_seen": 0.0})

cooldown = {}
COOLDOWN_SEC = 10

# ─────────────────────────────────────────
#  Thresholds
# ─────────────────────────────────────────
TH_PORT_SCAN   = 30    # unique ports in 3s
TH_SYN_FLOOD   = 300   # SYN/sec
TH_ICMP_FLOOD  = 200   # ICMP echo/sec
TH_UDP_FLOOD   = 300   # UDP/sec
TH_BRUTE_FORCE = 15    # SSH attempts / 30s

# ─────────────────────────────────────────
#  Alert Helper
# ─────────────────────────────────────────
def fire(atype, src, dst, severity, details, proto="TCP"):
    key = (src, atype)
    now = time.time()
    if now - cooldown.get(key, 0) < COOLDOWN_SEC:
        return
    cooldown[key] = now

    with LOCK:
        alert_id[0] += 1
        alerts.appendleft({
            "id":        alert_id[0],
            "type":      atype,
            "src_ip":    src,
            "dst_ip":    dst,
            "protocol":  proto,
            "severity":  severity,
            "details":   details,
            "timestamp": datetime.now().strftime("%H:%M:%S"),
        })
    sev_colors = {
        "CRITICAL": "\033[91m",
        "HIGH":     "\033[93m",
        "MEDIUM":   "\033[33m",
        "LOW":      "\033[36m",
    }
    color = sev_colors.get(severity, "")
    reset = "\033[0m"
    print(f"{color}[{severity}]{reset} {atype} | {src} → {dst} | {details}")

# ─────────────────────────────────────────
#  Detection Rules
# ─────────────────────────────────────────
def detect_port_scan(src, dst, dport):
    now = time.time()
    t = port_tracker[src]
    if t["first_seen"] == 0:
        t["first_seen"] = now
    t["ports"].add(dport)
    if now - t["first_seen"] > 3:
        t["ports"]      = {dport}
        t["first_seen"] = now
        return
    if len(t["ports"]) >= TH_PORT_SCAN:
        fire("Port Scan", src, dst, "HIGH",
             f"{len(t['ports'])} unique ports in 3s", "TCP")
        t["ports"]      = set()
        t["first_seen"] = now


def detect_syn_flood(src, dst):
    now = time.time()
    syn_tracker[src].append(now)
    pps = sum(1 for t in syn_tracker[src] if now - t <= 1.0)
    if pps >= TH_SYN_FLOOD:
        fire("SYN Flood", src, dst, "CRITICAL",
             f"{pps} SYN pkts/sec — half-open flood", "TCP")


def detect_icmp_flood(src, dst):
    now = time.time()
    icmp_tracker[src].append(now)
    pps = sum(1 for t in icmp_tracker[src] if now - t <= 1.0)
    if pps >= TH_ICMP_FLOOD:
        fire("ICMP Flood", src, dst, "HIGH",
             f"{pps} ICMP echo requests/sec", "ICMP")


def detect_udp_flood(src, dst):
    now = time.time()
    udp_tracker[src].append(now)
    pps = sum(1 for t in udp_tracker[src] if now - t <= 1.0)
    if pps >= TH_UDP_FLOOD:
        fire("UDP Flood", src, dst, "CRITICAL",
             f"{pps} UDP pkts/sec", "UDP")


def detect_brute_force(src, dst, dport):
    if dport != 22:
        return
    now = time.time()
    ssh_tracker[src].append(now)
    count = sum(1 for t in ssh_tracker[src] if now - t <= 30.0)
    if count >= TH_BRUTE_FORCE:
        fire("SSH Brute Force", src, dst, "MEDIUM",
             f"{count} SSH attempts in 30s", "TCP")

# ─────────────────────────────────────────
#  Packet Handler
# ─────────────────────────────────────────
def handle_packet(pkt):
    if not pkt.haslayer(IP):
        return

    src  = pkt[IP].src
    dst  = pkt[IP].dst
    size = len(pkt)

    with LOCK:
        traffic_stats["total"] += 1
        traffic_stats["bytes"] += size

    if pkt.haslayer(TCP):
        with LOCK:
            traffic_stats["tcp"] += 1
        flags = pkt[TCP].flags
        dport = pkt[TCP].dport
        detect_port_scan(src, dst, dport)
        if (flags & 0x02) and not (flags & 0x10):  # SYN without ACK
            detect_syn_flood(src, dst)
            detect_brute_force(src, dst, dport)

    elif pkt.haslayer(UDP):
        with LOCK:
            traffic_stats["udp"] += 1
        detect_udp_flood(src, dst)

    elif pkt.haslayer(ICMP):
        with LOCK:
            traffic_stats["icmp"] += 1
        if pkt[ICMP].type == 8:
            detect_icmp_flood(src, dst)

    else:
        with LOCK:
            traffic_stats["other"] += 1

# ─────────────────────────────────────────
#  Timeline Thread
# ─────────────────────────────────────────
def timeline_recorder():
    last = 0
    while True:
        time.sleep(1)
        with LOCK:
            cur = traffic_stats["total"]
        traffic_timeline.append({
            "time":    datetime.now().strftime("%H:%M:%S"),
            "packets": cur - last,
        })
        last = cur

# ─────────────────────────────────────────
#  Flask API
# ─────────────────────────────────────────
@app.route("/api/stats")
def api_stats():
    with LOCK:
        st = dict(traffic_stats)
    total = st["total"] or 1
    return jsonify({
        "traffic": st,
        "protocol_distribution": {
            "TCP":   round(st["tcp"]   / total * 100, 1),
            "UDP":   round(st["udp"]   / total * 100, 1),
            "ICMP":  round(st["icmp"]  / total * 100, 1),
            "Other": round(st["other"] / total * 100, 1),
        },
        "alert_count":    len(alerts),
        "critical_count": sum(1 for a in alerts if a["severity"] == "CRITICAL"),
    })

@app.route("/api/alerts")
def api_alerts():
    with LOCK:
        return jsonify(list(alerts)[:50])

@app.route("/api/timeline")
def api_timeline():
    with LOCK:
        return jsonify(list(traffic_timeline)[-30:])

@app.route("/api/clear", methods=["POST"])
def api_clear():
    with LOCK:
        alerts.clear()
    return jsonify({"status": "cleared"})

@app.route("/api/health")
def api_health():
    return jsonify({"status": "running", "interface": IFACE})

# ─────────────────────────────────────────
#  Main
# ─────────────────────────────────────────
if __name__ == "__main__":
    print(f"""
╔══════════════════════════════════════╗
║         NEXUSIDS — VMware Lab        ║
║  Interface : {IFACE:<23}║
║  Dashboard : http://localhost:5000   ║
╚══════════════════════════════════════╝
""")

    threading.Thread(target=timeline_recorder, daemon=True).start()

    threading.Thread(
        target=lambda: sniff(
            iface=IFACE,
            filter="ip",
            prn=handle_packet,
            store=False
        ),
        daemon=True
    ).start()

    print(f"[IDS] Sniffing on: {IFACE}")
    print(f"[IDS] Thresholds → PortScan:{TH_PORT_SCAN}p | "
          f"SYN:{TH_SYN_FLOOD}/s | ICMP:{TH_ICMP_FLOOD}/s | "
          f"UDP:{TH_UDP_FLOOD}/s | SSH:{TH_BRUTE_FORCE}/30s\n")

    app.run(host="0.0.0.0", port=5000, debug=False, threaded=True)
