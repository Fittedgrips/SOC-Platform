from flask import Flask, render_template_string
import json
import os


app = Flask(__name__)

LOG_FILE = "soc_log.json"


HTML = """
<!DOCTYPE html>
<html>
<head>
<title>SOC Dashboard</title>

<style>
body {
    font-family: Arial;
    background: #111;
    color: white;
    padding: 20px;
}

.card {
    background: #222;
    padding: 20px;
    margin: 10px;
    border-radius: 10px;
}

.high {
    color: red;
}

.medium {
    color: orange;
}

.low {
    color: green;
}
</style>

</head>


<body>

<h1>🛡️ SOC SECURITY DASHBOARD</h1>


<div class="card">
<h2>Status</h2>
<p>System: ONLINE</p>
</div>


<div class="card">

<h2>Threat Statistics</h2>

<p>Total Events: {{total}}</p>

<p class="high">
HIGH: {{high}}
</p>

<p class="medium">
MEDIUM: {{medium}}
</p>

<p class="low">
LOW: {{low}}
</p>

</div>



<div class="card">

<h2>Recent Events</h2>

{% for event in events %}

<p>
{{event}}
</p>

{% endfor %}


</div>


</body>
</html>
"""


def load_logs():

    events=[]

    if os.path.exists(LOG_FILE):

        with open(LOG_FILE) as f:

            for line in f:
                events.append(line.strip())


    return events



@app.route("/")
def dashboard():

    events = load_logs()

    high = 0
    medium = 0
    low = 0


    for e in events:

        if "HIGH" in e:
            high += 1

        elif "MEDIUM" in e:
            medium += 1

        elif "LOW" in e:
            low += 1


    return render_template_string(
        HTML,
        total=len(events),
        high=high,
        medium=medium,
        low=low,
        events=events[-10:]
    )



if __name__ == "__main__":

    print("[+] SOC Da
