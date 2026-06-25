from datetime import datetime

print("==============================")
print("       SOC ALERT SYSTEM")
print("==============================")

event = input("Enter security event: ")

severity = "LOW"

if "FAILED" in event.upper():
    severity = "MEDIUM"

if "ATTACK" in event.upper() or "MALWARE" in event.upper():
    severity = "HIGH"

time = datetime.now()

report = open("incident_report.log", "a")

report.write("==============================\n")
report.write("TIME: " + str(time) + "\n")
report.write("EVENT: " + event + "\n")
report.write("SEVERITY: " + severity + "\n")
report.write("==============================\n\n")

report.close()

print()
print("Alert Created ✅")
print("Severity:", severity)
print("Saved to: incident_report.log")
