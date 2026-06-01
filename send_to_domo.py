import csv
import json
import requests
import os

DOMO_WEBHOOK_URL = os.environ["DOMO_WEBHOOK_URL"]
CSV_FILE = "2015_16_Districtwise.csv"

def csv_to_json(filepath):
    rows = []
    with open(filepath, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            rows.append(dict(row))
    return rows

def send_in_chunks(data, chunk_size=500):
    for i in range(0, len(data), chunk_size):
        chunk = data[i:i + chunk_size]
        response = requests.post(
            DOMO_WEBHOOK_URL,
            headers={"Content-Type": "application/json"},
            data=json.dumps(chunk)
        )
        print(f"Chunk {i//chunk_size + 1}: Status {response.status_code}")
        if response.status_code not in (200, 204):
            raise Exception(f"Failed: {response.text}")

data = csv_to_json(CSV_FILE)
send_in_chunks(data, chunk_size=500)
