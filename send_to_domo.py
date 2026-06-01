import csv
import json
import requests
import os

DOMO_WEBHOOK_URL = os.environ["DOMO_WEBHOOK_URL"]  # set as GitHub secret
CSV_FILE = "2015_16_Districtwise.csv"  # path to your CSV in repo

def csv_to_json(filepath):
    rows = []
    with open(filepath, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            rows.append(dict(row))
    return rows

data = csv_to_json(CSV_FILE)

response = requests.post(
    DOMO_WEBHOOK_URL,
    headers={"Content-Type": "application/json"},
    data=json.dumps(data)
)

print(f"Status: {response.status_code}")
if response.status_code not in (200, 204):
    raise Exception(f"Failed to send data: {response.text}")
