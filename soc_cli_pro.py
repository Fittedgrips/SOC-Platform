import os
import time
import json
import threading
import shutil
import hashlib
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# ==========================
# CONFIG
# ==========================
WATCH_FOLDER = "scan_folder"
OUTPUT_FOLDER = "organized"
QUARANTINE = os.path.join(OUTPUT_FOLDER, "quarantine")
LOG_FILE = "soc_log.json"

SUSPICIOUS_EXT = [".exe", ".bat", ".sh", ".cmd", ".scr", ".apk"]

CATEGORIES = {
    "images": [".jpg", ".jpeg", ".png"],
    "docs": [".pdf", ".txt", ".docx"],
    "scripts": [".py", ".js", ".php"]
}

# ==========================
# STATE
# ==========================
running = False
observer = None

stats = {
    "scanned": 0,
    "low": 0,
    "medium": 0,
    "high": 0
}

# ==========================
# SETUP
# ==========================
os.makedirs(WATCH_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)
os.makedirs(QUARANTINE, exist_ok=True)

# ==========================
# HASH
# ==========================
def hash_file(path):
    h = hashlib.sha256()
    try:
        with open(path, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                h.update(chunk)
        return h.hexdigest()
    except:
        return "ERROR"

# ==========================
# RISK ENGINE
# ==========================
def risk_level(path):
    ext = os.path.splitext(path)[1].lower()
    size = os.path.getsize(path)

    score = 0

    if ext in SUSPICIOUS_EXT:
        score += 70
    if ext == "":
        score += 40
    if size > 5 * 1024 * 1024:
        score += 20

    if score >= 70:
        return "HIGH"
    elif score >= 30:
        return "MEDIUM"
    return "LOW"

# ==========================
# CLASSIFY
# ==========================
def classify(name):
    ext = os.path.splitext(name)[1].lower()

    for cat, exts in CATEGORIES.items():
        if ext in exts:
            return cat

    return "other"

# ==========================
# LOG (JSON STYLE)
# ==========================
def log_event(data):
    try:
        with open(LOG_FILE, "a") as f:
            f.write(json.dumps(data) + "\n")
    except:
        pass

# ==========================
# PROCESS FILE
# ==========================
def process_file(path):
    time.sleep(1)

    name = os.path.basename(path)
    cat = classify(name)
    risk = risk_level(path)
    h = hash_file(path)

    stats["scanned"] += 1
    stats[risk.lower()] += 1

    if risk == "HIGH":
        dest = QUARANTINE
    else:
        dest = os.path.join(OUTPUT_FOLDER, cat)

    os.makedirs(dest, exist_ok=True)

    try:
        shutil.copy2(path, dest)
    except:
        pass

    event = {
        "file": name,
        "category": cat,
        "risk": risk,
        "hash": h[:12],
        "time": str(time.ctime())
    }

    log_event(event)

    print(f"[{risk}] {name} -> {cat}")

# ==========================
# WATCHER
# ==========================
class Handler(FileSystemEventHandler):
    def on_created(self, event):
        if not event.is_directory:
            process_file(event.src_path)

# ==========================
# DASHBOARD
# ==========================
def show_status():
    print("\n===== SOC STATUS =====")
    print(f"Scanned : {stats['scanned']}")
    print(f"LOW     : {stats['low']}")
    print(f"MEDIUM  : {stats['medium']}")
    print(f"HIGH    : {stats['high']}")
    print("======================\n")

# ==========================
# CORE ENGINE
# ==========================
def run_engine():
    global observer

    observer = Observer()
    observer.schedule(Handler(), WATCH_FOLDER, recursive=True)
    observer.start()

    while running:
        time.sleep(1)

    observer.stop()
    observer.join()

# ==========================
# CLI SYSTEM
# ==========================
def cli():
    global running

    print("\nSOC CLI SYSTEM")
    print("Commands:")
    print("  start  - start monitoring")
    print("  status - show stats")
    print("  stop   - stop system")
    print("  exit   - quit CLI\n")

    while True:
        cmd = input("soc> ").strip().lower()

        if cmd == "start":
            if not running:
                running = True
                threading.Thread(target=run_engine, daemon=True).start()
                print("[+] SOC MONITOR STARTED")
            else:
                print("[!] Already running")

        elif cmd == "status":
            show_status()

        elif cmd == "stop":
            running = False
            print("[+] SOC STOPPED")

        elif cmd == "exit":
            running = False
            print("[+] EXITING...")
            break

        else:
            print("Unknown command")

# ==========================
# MAIN
# ==========================
if __name__ == "__main__":
    cli()
