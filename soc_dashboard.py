import os
import hashlib
import time
from datetime import datetime

print("==============================")
print("       SOC DASHBOARD")
print("==============================")

files = input("Enter files to monitor (separate with spaces): ").split()

hashes = {}

for file in files:
    if os.path.exists(file):
        with open(file, "rb") as f:
            hashes[file] = hashlib.sha256(f.read()).hexdigest()
    else:
        print("File not found:", file)

print()
print("Monitoring started...")
print("Press CTRL + C to stop")
print()

try:
    while True:

        for file in hashes:

            with open(file, "rb") as f:
                new_hash = hashlib.sha256(f.read()).hexdigest()

            if new_hash != hashes[file]:

                alert = open("soc_history.log", "a")

                alert.write("==============================\n")
                alert.write("TIME: " + str(datetime.now()) + "\n")
                alert.write("ALERT: " + file + " changed\n")
                alert.write("==============================\n\n")

                alert.close()

                print("⚠️ ALERT:", file, "changed")

                hashes[file] = new_hash

        time.sleep(5)

except KeyboardInterrupt:
    print()
    print("SOC Monitoring stopped")
