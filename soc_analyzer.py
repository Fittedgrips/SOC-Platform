print("==============================")
print("       SOC LOG ANALYZER")
print("==============================")

log_file = input("Enter log file name: ")

failed = 0
success = 0
alerts = 0

try:
    with open(log_file, "r") as log:

        for line in log:

            if "FAILED" in line:
                failed += 1

            if "SUCCESS" in line:
                success += 1

            if "ALERT" in line:
                alerts += 1


    print()
    print("========= INCIDENT REPORT =========")
    print("Successful events:", success)
    print("Failed events:", failed)
    print("Alerts found:", alerts)

    print()

    if failed >= 3:
        print("⚠️ HIGH RISK: Multiple failed attempts detected")

    elif failed > 0:
        print("⚠️ LOW RISK: Some failed attempts detected")

    else:
        print("✅ No suspicious activity detected")

except:
    print("Log file not found ❌")

print()
print("Analysis complete")
