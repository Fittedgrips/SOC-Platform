from datetime import datetime

print("==============================")
print("   SECURITY LOG GENERATOR")
print("==============================")

event = input("Enter security event: ")

time = datetime.now()

log = open("security_events.log", "a")

log.write("==============================\n")
log.write("Time: " + str(time) + "\n")
log.write("Event: " + event + "\n")
log.write("==============================\n\n")

log.close()

print()
print("Event saved successfully ✅")
print("Log file: security_events.log")


