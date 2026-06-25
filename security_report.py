import os
import platform
import socket
import getpass
from datetime import datetime

report = open("security_report.txt", "w")

report.write("==============================\n")
report.write("     SECURITY REPORT\n")
report.write("==============================\n\n")

# Date and time
report.write("Report Time:\n")
report.write(str(datetime.now()))
report.write("\n\n")

# User
report.write("User:\n")
report.write(getpass.getuser())
report.write("\n\n")

# Operating system
report.write("Operating System:\n")
report.write(platform.system())
report.write("\n\n")

# Computer name
report.write("Computer Name:\n")
report.write(socket.gethostname())
report.write("\n\n")

# Current directory
report.write("Current Directory:\n")
report.write(os.getcwd())
report.write("\n\n")

report.write("==============================\n")
report.write("REPORT COMPLETE\n")
report.write("==============================\n")

report.close()

print("Security report created successfully ✅")
print("Saved as: security_report.txt")
