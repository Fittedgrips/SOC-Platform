import os
import shutil
import hashlib
from datetime import datetime

# ==========================
# CONFIG
# ==========================
TARGET_FOLDER = "scan_folder"
OUTPUT_FOLDER = "organized"
QUARANTINE_FOLDER = os.path.join(OUTPUT_FOLDER, "quarantine")

SUSPICIOUS_EXTENSIONS = [".exe", ".bat", ".sh", ".cmd", ".scr", ".apk"]

CATEGORIES = {
    "images": [".jpg", ".jpeg", ".png", ".gif"],
    "documents": [".pdf", ".docx", ".txt"],
    "scripts": [".py", ".js", ".php"],
}

log_data = []

# ==========================
# HASH FUNCTION
# ==========================
def get_hash(path):
    sha256 = hashlib.sha256()
    try:
        with open(path, "rb") as f:
            while chunk := f.read(4096):
                sha256.update(chunk)
        return sha256.hexdigest()
    except:
        return "ERROR"

# ==========================
# RISK ENGINE (NEW)
# ==========================
def assess_risk(file_path, file_name):
    ext = os.path.splitext(file_name)[1].lower()
    size = os.path.getsize(file_path)

    risk_score = 0

    # rule 1: suspicious extension
    if ext in SUSPICIOUS_EXTENSIONS:
        risk_score += 70

    # rule 2: unknown file type
    if ext == "":
        risk_score += 40

    # rule 3: large file anomaly
    if size > 5 * 1024 * 1024:  # 5MB
        risk_score += 20

    # classify
    if risk_score >= 70:
        return "HIGH"
    elif risk_score >= 30:
        return "MEDIUM"
    else:
        return "LOW"

# ==========================
# CLASSIFIER
# ==========================
def classify(file_name):
    ext = os.path.splitext(file_name)[1].lower()

    for cat, exts in CATEGORIES.items():
        if ext in exts:
            return cat

    if ext in SUSPICIOUS_EXTENSIONS:
        return "suspicious"

    return "others"

# ==========================
# HANDLER
# ==========================
def process_file(file_path):
    file_name = os.path.basename(file_path)

    category = classify(file_name)
    risk = assess_risk(file_path, file_name)
    file_hash = get_hash(file_path)

    # Decide destination
    if risk == "HIGH":
        dest = QUARANTINE_FOLDER
    else:
        dest = os.path.join(OUTPUT_FOLDER, category)

    os.makedirs(dest, exist_ok=True)

    try:
        shutil.copy2(file_path, dest)
    except:
        pass

    log_data.append({
        "file": file_name,
        "category": category,
        "risk": risk,
        "hash": file_hash
    })

# ==========================
# SCANNER
# ==========================
def scan(folder):
    for root, _, files in os.walk(folder):
        for file in files:
            full_path = os.path.join(root, file)
            process_file(full_path)

# ==========================
# REPORT SYSTEM
# ==========================
def generate_report():
    os.makedirs(OUTPUT_FOLDER, exist_ok=True)

    report_file = os.path.join(OUTPUT_FOLDER, "soc_report.txt")

    with open(report_file, "w") as f:
        f.write("=== SOC SECURITY REPORT ===\n")
        f.write(f"Time: {datetime.now()}\n\n")

        for item in log_data:
            f.write(f"File: {item['file']}\n")
            f.write(f"Category: {item['category']}\n")
            f.write(f"Risk Level: {item['risk']}\n")
            f.write(f"SHA256: {item['hash']}\n")
            f.write("------------------------\n")

# ==========================
# MAIN
# ==========================
if __name__ == "__main__":
    print("[+] SOC Scanner Starting...")

    os.makedirs(TARGET_FOLDER, exist_ok=True)
    os.makedirs(OUTPUT_FOLDER, exist_ok=True)
    os.makedirs(QUARANTINE_FOLDER, exist_ok=True)

    scan(TARGET_FOLDER)
    generate_report()

    print("[+] Scan Complete!")
    print("[+] Check 'organized/' and 'quarantine/' folders")
