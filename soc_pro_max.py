import os
import time
import shutil
import hashlib
from datetime import datetime
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# ==========================
# CONFIG
# ==========================
WATCH_FOLDER = "scan_folder"
OUTPUT_FOLDER = "organized"
QUARANTINE_FOLDER = os.path.join(OUTPUT_FOLDER, "quarantine")
LOG_FILE = "soc_history.log"

SUSPICIOUS_EXTENSIONS = [".exe", ".bat", ".sh", ".cmd", ".scr", ".apk"]

CATEGORIES = {
    "images": [".jpg", ".jpeg", ".png", ".gif"],
    "documents": [".pdf", ".docx", ".txt"],
    "scripts": [".py", ".js", ".php"],
}

# ==========================
# STATE
# ==========================
stats = {"scanned": 0, "low": 0, "medium": 0, "high": 0}
running = True

# ==========================
# SETUP
# ==========================
os.makedirs(WATCH_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)
os.makedirs(QUARANTINE_FOLDER, exist_ok=True)

# ==========================
# HASH
# ==========================
def file_hash(path):
    sha = hashlib.sha256()
    try:
        with open(path, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                sha.update(chunk)
        return sha.hexdigest()
    except:
        return "ERROR"

# ==========================
# RISK ENGINE
# ==========================
def risk(file_path):
    ext = os.path.splitext(file_path)[1].lower()
    size = os.path.getsize(file_path)

    score = 0
    if ext in SUSPICIOUS_EXTENSIONS:
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

    return "others"

# ==========================
# LOGGING (PERSISTENT)
# ==========================
def log_event(text):
    with open(LOG_FILE, "a") as f:
        f.write(f"{datetime.now()} | {text}\n")

# ==========================
# ALERT SYSTEM
# ==========================
def alert(message):
    print("\a")  # terminal beep (if supported)
    print("[!!! ALERT !!!]", message)

# ==========================
# PROCESS FILE
# ==========================
def process(path):
    time.sleep(1)

    name = os.path.basename(path)
    cat = classify(name)
    r = risk(path)
    h = file_hash(path)

    stats["scanned"] += 1

    if r == "LOW":
        stats["low"] += 1
        dest = os.path.join(OUTPUT_FOLDER, cat)

    elif r == "MEDIUM":
        stats["medium"] += 1
        dest = os.path.join(OUTPUT_FOLDER, cat)

    else:
        stats["high"] += 1
        dest = QUARANTINE_FOLDER
        alert(f"HIGH RISK FILE DETECTED: {name}")

    os.makedirs(dest, exist_ok=True)

    try:
        shutil.copy2(path, dest)
    except:
        pass

    event = f"{name} | {r} | {cat} | {h[:10]}"
    log_event(event)

    print(event)

# ==========================
# MONITOR HANDLER
# ==========================
class Handler(FileSystemEventHandler):
    def on_created(self, event):
        if not event.is_directory:
            process(event.src_path)

# ==========================
# STATUS
# ==========================
def status():
    print("\n===== SOC STATUS =====")
    print(f"Scanned: {stats['scanned']}")
    print(f"LOW: {stats['low']}")
    print(f"MEDIUM: {stats['medium']}")
    print(f"HIGH: {stats['high']}")
    print("======================\n")

# ==========================
# MAIN CONTROL
# ==========================
def start():
    global running

    print("[+] SOC PRO MAX STARTED")
    print("[+] Commands: status | stop")

    observer = Observer()
    observer.schedule(Handler(), WATCH_FOLDER, recursive=True)
    observer.start()

    try:
        while running:
            cmd = input()
            if cmd == "status":
                status()
            elif cmd == "stop":
                running = False
                break
    except KeyboardInterrupt:
        pass

    observer.stop()
    observer.join()
    print("[+] SOC STOPPED")

# ==========================
# RUN
# ==========================
if __name__ == "__main__":
    start()
