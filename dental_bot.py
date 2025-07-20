import os
import requests
from flask import current_app as app

# Load Airtable creds
AIRTABLE_BASE_ID = os.environ["AIRTABLE_BASE_ID"]
AIRTABLE_API_KEY = os.environ["AIRTABLE_API_KEY"]

def push_to_airtable(name, dob, phone, email, treatment):
    url = f"https://api.airtable.com/v0/{AIRTABLE_BASE_ID}/Bookings"
    headers = {
        "Authorization": f"Bearer {AIRTABLE_API_KEY}",
        "Content-Type": "application/json",
    }
    payload = {
        "fields": {
            "Name":        name,
            "DOB":         dob,
            "PhoneNumber": phone,
            "Issues":      email,
            "Treatment":   treatment,
            "Status":      "True"
        }
    }

    # —— DEBUG via Flask logger —— 
    app.logger.info(f"[AIRTABLE DEBUG] POST → {url}")
    app.logger.info(f"[AIRTABLE DEBUG] Payload: {payload}")

    resp = requests.post(url, json=payload, headers=headers)

    app.logger.info(f"[AIRTABLE DEBUG] Status: {resp.status_code}")
    app.logger.info(f"[AIRTABLE DEBUG] Body:   {resp.text}")
    # — end debug —

    return resp.status_code == 200