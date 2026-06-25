import os
import time
import hashlib
from datetime import datetime

print("==============================")
print("     MINI SOC MONITOR")
print("==============================")

file = input("Enter file to monitor: ")

def get_hash(filename):
    with open(filename, "rb") as f:
        return hashlib.sha256(f.read()).hexdigest()

if os.path.exists(file):

    old_hash = get_hash(file)

    print()
    print("Monitoring started...")
    print("Press CTRL + C to stop")
    print()

    try:
        while True:

            new_hash = get_hash(file)

            if new_hash != old_hash:

                log = open("soc_alerts.log", "a")

                log.write("==============================\n")
                log.write("ALERT TIME: " + str(datetime.now()) + "\n")
                log.write("FILE CHANGED: " + file + "\n")
                log.write("==============================\n\n")

                log.close()

                print("⚠️ ALERT: File changed!")

                old_hash = new_hash

            time.sleep(5)

    except KeyboardInterrupt:
        print()
        print("Monitoring stopped")

else:
    print("File not found ❌")
