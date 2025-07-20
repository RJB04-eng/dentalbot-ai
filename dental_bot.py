# dental_bot.py
import os
import requests
from flask import current_app as app

# Load credentials
AIRTABLE_BASE_ID = os.environ["AIRTABLE_BASE_ID"]
AIRTABLE_API_KEY = os.environ["AIRTABLE_API_KEY"]

# Function to push to Airtable
def push_to_airtable(name, dob, phone, email, treatment):
    url = f"https://api.airtable.com/v0/{AIRTABLE_BASE_ID}/Bookings"
    headers = {
        "Authorization": f"Bearer {AIRTABLE_API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "fields": {
            "Name": name,
            "DOB": dob,
            "PhoneNumber": phone,
            "Issues": email,
            "Treatment": treatment,
            "Status": True
        }
    }

    # Debug logs
    print(f"[AIRTABLE DEBUG] POST → {url}")
    print(f"[AIRTABLE DEBUG] Payload: {payload}")

    resp = requests.post(url, json=payload, headers=headers)

    print(f"[AIRTABLE DEBUG] Status: {resp.status_code}")
    print(f"[AIRTABLE DEBUG] Body: {resp.text}")

    return resp.status_code == 200

# Minimal bot class
class DentalBot:
    pass