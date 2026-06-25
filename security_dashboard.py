import os
import platform
import socket
import getpass
from datetime import datetime

print("==============================")
print("   SECURITY DASHBOARD TOOL")
print("==============================")

report = open("dashboard_report.txt", "w")

report.write("SECURITY DASHBOARD REPORT\n")
report.write("==============================\n\n")

report.write("Time:\n")
report.write(str(datetime.now()))
report.write("\n\n")

report.write("User:\n")
report.write(getpass.getuser())
report.write("\n\n")

report.write("System:\n")
report.write(platform.system())
report.write("\n\n")

report.write("Machine Name:\n")
report.write(socket.gethostname())
report.write("\n\n")

report.write("IP Address:\n")
report.write(socket.gethostbyname(socket.gethostname()))
report.write("\n\n")

report.write("Current Folder:\n")
report.write(os.getcwd())
report.write("\n\n")

report.write("==============================\n")
report.write("REPORT FINISHED\n")

report.close()

print("Dashboard complete ✅")
print("Report saved as dashboard_report.txt")
