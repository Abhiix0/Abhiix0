from datetime import datetime
import requests

USERNAME = "Abhiix0"
README_FILE = "README.md"

# -----------------------------
# Get latest commit date
# -----------------------------
url = f"https://api.github.com/users/{USERNAME}/events"

response = requests.get(url)
events = response.json()

latest_commit = "unknown"
push_events = 0

for event in events:
    if event["type"] == "PushEvent":
        push_events += 1

        if latest_commit == "unknown":
            latest_commit = event["created_at"][:10]

# Format date
if latest_commit != "unknown":
    dt = datetime.strptime(latest_commit, "%Y-%m-%d")
    latest_commit = dt.strftime("%Y.%m.%d")

# -----------------------------
# Activity Heat Logic
# -----------------------------
if push_events >= 15:
    activity_heat = "INSANE"
elif push_events >= 8:
    activity_heat = "HIGH"
elif push_events >= 3:
    activity_heat = "STABLE"
elif push_events >= 1:
    activity_heat = "LOW"
else:
    activity_heat = "RECHARGING"

# -----------------------------
# Build Status Block
# -----------------------------
status_block = f"""<!-- SYSTEM_STATUS_START -->

## system.status

```txt
+ curiosity        : online
+ sleep_schedule   : unstable
+ current_project  : AI-Data-Analyst
+ latest_commit    : {latest_commit}
+ activity_heat    : {activity_heat}
