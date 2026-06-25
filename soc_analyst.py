import os
import time
import json
import shutil
import hashlib
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from collections import defaultdict
from datetime import datetime

# ==========================
# CONFIG
# ==========================
WATCH_FOLDER = "scan_folder"
OUTPUT_FOLDER = "organized"
QUARANTINE = os.path.join(OUTPUT_FOLDER, "quarantine")
LOG_FILE = "soc_incidents.json"

SUSPICIOUS_EXT = [".exe", ".bat", ".sh", ".cmd", ".scr", ".apk"]

CATEGORIES = {
    "images": [".jpg", ".jpeg", ".png"],
    "docs": [".pdf", ".txt", ".docx"],
    "scripts": [".py", ".js", ".php"]
}

# ==========================
# STATE / INTELLIGENCE
# ==========================
running = False
observer = None

stats = {"scanned": 0, "low": 0, "medium": 0, "high": 0}

# track repeated files (basic behavior intelligence)
file_counter = defaultdict(int)

# ==========================
# SETUP
# ==========================
os.makedirs(WATCH_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)
os.makedirs(QUARANTINE, exist_ok=True)

# ==========================
# HASH ENGINE
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
# THREAT SCORE ENGINE (NEW CORE)
# ==========================
def threat_score(path, name):
    ext = os.path.splitext(name)[1].lower()
    size = os.path.getsize(path)

    score = 0

    # rule 1: dangerous extension
    if ext in SUSPICIOUS_EXT:
        score += 50

    # rule 2: unknown extension
    if ext == "":
        score += 30

    # rule 3: large file anomaly
    if size > 5 * 1024 * 1024:
        score += 10

    # rule 4: repeated file behavior (IMPORTANT SOC CONCEPT)
    file_counter[name] += 1
    if file_counter[name] > 2:
        score += 20

    # classification
    if score >= 80:
        level = "CRITICAL"
    elif score >= 60:
        level = "HIGH"
    elif score >= 30:
        level = "MEDIUM"
    else:
        level = "LOW"

    return score, level

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
# INCIDENT LOGGING
# ==========================
def log_incident(data):
    try:
        with open(LOG_FILE, "a") as f:
            f.write(json.dumps(data) + "\n")
    except:
        pass

# ==========================
# ALERT ENGINE
# ==========================
def alert(level, name, score):
    if level in ["HIGH", "CRITICAL"]:
        print("\n🚨 ALERT:", level, "FILE DETECTED:", name, "SCORE:", score, "\n")

# ==========================
# PROCESS FILE
# ==========================
def process_file(path):
    time.sleep(1)

    name = os.path.basename(path)
    cat = classify(name)
    score, level = threat_score(path, name)
    h = hash_file(path)

    stats["scanned"] += 1
    stats[level.lower()] += 1

    # decision engine
    if level in ["HIGH", "CRITICAL"]:
        dest = QUARANTINE
    else:
        dest = os.path.join(OUTPUT_FOLDER, cat)

    os.makedirs(dest, exist_ok=True)

    try:
        shutil.copy2(path, dest)
    except:
        pass

    alert(level, name, score)

    incident = {
        "time": str(datetime.now()),
        "file": name,
        "category": cat,
        "threat_score": score,
        "level": level,
        "hash": h[:12]
    }

    log_incident(incident)

    print(f"[{level}] {name} | score={score} | {cat}")

# ==========================
# WATCHER
# ==========================
class Handler(FileSystemEventHandler):
    def on_created(self, event):
        if not event.is_directory:
            process_file(event.src_path)

# ==========================
# STATUS REPORT
# ==========================
def status():
    print("\n===== SOC ANALYST REPORT =====")
    print(f"Scanned : {stats['scanned']}")
    print(f"LOW     : {stats['low']}")
    print(f"MEDIUM  : {stats['medium']}")
    print(f"HIGH    : {stats['high']}")
    print("==============================\n")

# ==========================
# ENGINE
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
# CLI
# ==========================
def cli():
    global running

    print("\nSOC ANALYST MODE")
    print("Commands:")
    print("  start")
    print("  status")
    print("  exit\n")

    while True:
        cmd = input("soc> ").strip().lower()

        if cmd == "start":
            if not running:
                running = True
                import threading
                threading.Thread(target=run_engine, daemon=True).start()
                print("[+] ANALYST MODE STARTED")

        elif cmd == "status":
            status()

        elif cmd == "exit":
            running = False
            print("[+] EXITING SOC ANALYST")
            break

        else:
            print("Unknown command")

# ==========================
# MAIN
# ==========================
if __name__ == "__main__":
    running = True
    run_engine()
