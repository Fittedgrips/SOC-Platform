import json
import os
from datetime import datetime


LOG_FILE = "soc_log.json"
REPORT_FILE = "incident_report.txt"


def load_events():

    events = []

    if os.path.exists(LOG_FILE):

        with open(LOG_FILE, "r") as f:

            for line in f:
                try:
                    events.append(json.loads(line))
                except:
                    pass

    return events



def generate_report():

    events = load_events()

    if not events:
        print("No incidents found")
        return


    high = 0
    medium = 0
    low = 0


    with open(REPORT_FILE, "w") as report:

        report.write("==============================\n")
        report.write("SOC INCIDENT REPORT\n")
        report.write("==============================\n\n")

        report.write(
            f"Generated: {datetime.now()}\n\n"
        )


        for number, event in enumerate(events, start=1):

            level = event.get("level","UNKNOWN")

            if level in ["HIGH","CRITICAL"]:
                high += 1

            elif level == "MEDIUM":
                medium += 1

            else:
                low += 1


            report.write(
                f"Incident ID: INC-{number:04}\n"
            )

            report.write(
                f"File: {event.get('file')}\n"
            )

            report.write(
                f"Threat Score: {event.get('threat_score')}\n"
            )

            report.write(
                f"Level: {level}\n"
            )

            report.write(
                f"Hash: {event.get('hash')}\n"
            )

            report.write(
                "Status: INVESTIGATING\n"
            )

            report.write(
                "------------------------------\n"
            )


        report.write("\nSUMMARY\n")
        report.write("------------------------------\n")
        report.write(f"HIGH: {high}\n")
        report.write(f"MEDIUM: {medium}\n")
        report.write(f"LOW: {low}\n")


    print("[+] Incident report created")
    print("[+] File:", REPORT_FILE)



if __name__ == "__main__":

    generate_report()
