import csv
import json
import requests
import os
import time

DOMO_WEBHOOK_URL = os.environ["DOMO_WEBHOOK_URL"]
CSV_FILE = "2015_16_Districtwise.csv"

def csv_to_json(filepath):
    rows = []
    with open(filepath, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            rows.append(dict(row))
    return rows

def send_in_chunks(data, chunk_size=10):  # Reduced default to 10
    for i in range(0, len(data), chunk_size):
        chunk = data[i:i + chunk_size]
        
        # Serialize and calculate the payload size in Kilobytes
        json_payload = json.dumps(chunk)
        payload_kb = len(json_payload.encode('utf-8')) / 1024
        
        print(f"Chunk {i//chunk_size + 1}: Sending {len(chunk)} rows ({payload_kb:.2f} KB)...")
        
        response = requests.post(
            DOMO_WEBHOOK_URL,
            headers={"Content-Type": "application/json"},
            data=json_payload,
            timeout=30
        )
        print(f"Status: {response.status_code} - {response.text}")  # change this line
        if response.status_code not in (200, 204):
            raise Exception(f"Failed at chunk {i//chunk_size + 1}: Status {response.status_code} - {response.text}")
        
        # Short pause to ensure you don't hit Domo's 25 requests/sec rate limit
        time.sleep(0.1)

data = csv_to_json(CSV_FILE)
# Explicitly call it with a safe chunk size of 10 rows
send_in_chunks(data, chunk_size=10)
