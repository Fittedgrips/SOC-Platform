import os
import shutil
import hashlib
from datetime import datetime

# ==========================
# CONFIG
# ==========================
TARGET_FOLDER = "scan_folder"
OUTPUT_FOLDER = "organized"

SUSPICIOUS_EXTENSIONS = [".exe", ".bat", ".sh", ".cmd", ".scr"]

CATEGORIES = {
    "images": [".jpg", ".jpeg", ".png", ".gif"],
    "documents": [".pdf", ".docx", ".txt"],
    "scripts": [".py", ".js", ".php"],
}

report_data = []

# ==========================
# HASH FUNCTION
# ==========================
def get_file_hash(file_path):
    sha256 = hashlib.sha256()
    try:
        with open(file_path, "rb") as f:
            while chunk := f.read(4096):
                sha256.update(chunk)
        return sha256.hexdigest()
    except:
        return "ERROR"

# ==========================
# FILE CLASSIFIER
# ==========================
def classify_file(file_name):
    ext = os.path.splitext(file_name)[1].lower()

    for category, extensions in CATEGORIES.items():
        if ext in extensions:
            return category

    if ext in SUSPICIOUS_EXTENSIONS:
        return "suspicious"

    return "others"

# ==========================
# ORGANIZER
# ==========================
def organize_file(file_path):
    file_name = os.path.basename(file_path)
    category = classify_file(file_name)

    dest_folder = os.path.join(OUTPUT_FOLDER, category)
    os.makedirs(dest_folder, exist_ok=True)

    try:
        shutil.copy2(file_path, dest_folder)
    except:
        pass

    file_hash = get_file_hash(file_path)

    report_data.append({
        "file": file_name,
        "category": category,
        "hash": file_hash
    })

# ==========================
# SCANNER
# ==========================
def scan_folder(folder):
    for root, _, files in os.walk(folder):
        for file in files:
            full_path = os.path.join(root, file)
            organize_file(full_path)

# ==========================
# REPORT GENERATOR
# ==========================
def generate_report():
    report_file = os.path.join(OUTPUT_FOLDER, "report.txt")

    with open(report_file, "w") as f:
        f.write("SECURITY SCAN REPORT\n")
        f.write("=====================\n")
        f.write(f"Date: {datetime.now()}\n\n")

        for item in report_data:
            f.write(f"File: {item['file']}\n")
            f.write(f"Category: {item['category']}\n")
            f.write(f"SHA256: {item['hash']}\n")
            f.write("---------------------\n")

# ==========================
# MAIN
# ==========================
if __name__ == "__main__":
    print("[+] Starting Security Scan...")

    # ✅ Ensure base output folder exists FIRST
    os.makedirs(OUTPUT_FOLDER, exist_ok=True)

    scan_folder(TARGET_FOLDER)
    generate_report()

    print("[+] Scan Complete!")
    print("[+] Check 'organized/' folder for results")
