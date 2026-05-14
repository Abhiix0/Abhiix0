from datetime import datetime
import requests
import sys

USERNAME = "Abhiix0"
README_FILE = "README.md"

# -----------------------------
# Get latest commit date
# -----------------------------
url = f"https://api.github.com/users/{USERNAME}/events"
headers = {"Accept": "application/vnd.github+json"}

response = requests.get(url, headers=headers)

if response.status_code != 200:
    print(f"GitHub API error: {response.status_code} - {response.text}")
    sys.exit(1)

events = response.json()

if not isinstance(events, list):
    print(f"Unexpected API response: {events}")
    sys.exit(1)

latest_commit = "unknown"
push_events = 0

for event in events:
    if event.get("type") == "PushEvent":
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
status_block = (
    "<!-- SYSTEM_STATUS_START -->\n\n"
    "## system.status\n\n"
    "```txt\n"
    "+ curiosity        : online\n"
    "+ sleep_schedule   : unstable\n"
    f"+ current_project  : AI-Data-Analyst\n"
    f"+ latest_commit    : {latest_commit}\n"
    f"+ activity_heat    : {activity_heat}\n"
    "```\n\n"
    "<!-- SYSTEM_STATUS_END -->"
)

# -----------------------------
# Replace in README
# -----------------------------
import re

with open(README_FILE, "r", encoding="utf-8") as f:
    readme = f.read()

updated_readme = re.sub(
    r"<!-- SYSTEM_STATUS_START -->.*?<!-- SYSTEM_STATUS_END -->",
    status_block,
    readme,
    flags=re.DOTALL
)

with open(README_FILE, "w", encoding="utf-8") as f:
    f.write(updated_readme)

print(f"README updated — latest_commit: {latest_commit}, activity_heat: {activity_heat}")
