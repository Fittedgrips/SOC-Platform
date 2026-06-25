import os
import subprocess
import time


running = False


def start_monitor():

    global running

    if running:
        print("[!] SOC Monitor already running")
        return

    running = True

    print("[+] Starting SOC Monitor...")

    subprocess.Popen(
        ["python3", "soc_analyst.py"]
    )

    print("[+] Detection engine started")


def status():

    print("\n==============================")
    print("        SOC STATUS")
    print("==============================")

    if running:
        print("System: ONLINE 🟢")
    else:
        print("System: OFFLINE 🔴")

    print("==============================\n")


def generate_report():

    print("[+] Generating incident report...")

    os.system(
        "python3 incident_response.py"
    )



def dashboard():

    print("""
==============================
SOC WEB DASHBOARD

Start dashboard with:

python3 soc_web_dashboard.py

Open browser:

http://127.0.0.1:5000
==============================
""")


def cli():

    while True:

        print("""
==============================
       SOC PLATFORM
==============================

1. Start Monitoring
2. Status
3. Generate Report
4. Dashboard
5. Exit

""")

        choice = input("soc> ")


        if choice == "1":
            start_monitor()


        elif choice == "2":
            status()


        elif choice == "3":
            generate_report()


        elif choice == "4":
            dashboard()


        elif choice == "5":

            print("[+] Closing SOC Platform")
            break


        else:
            print("Invalid option")


if __name__ == "__main__":
    cli()
