import os
import re
import json
from datetime import datetime
from typing import Dict, List
import requests
from flask import current_app as app
from rapidfuzz import fuzz, process

# Load Airtable credentials from environment
AIRTABLE_BASE_ID = os.environ["AIRTABLE_BASE_ID"]
AIRTABLE_API_KEY = os.environ["AIRTABLE_API_KEY"]

print(f"[ENV CHECK] token prefix={AIRTABLE_API_KEY[:6]}… len={len(AIRTABLE_API_KEY)}")

# Clinic constants and intents omitted for brevity
GREETING = (
    "Hey there, this is Cedar House Dental how can we help you today? 🏡"
)

# ... other constants ...

# Intent matching
INTENTS = {
    "Book an appointment": [
        "book", "i want to book", "schedule", "appointment", "reserve", "plan a visit"
    ],
    # ... other intents ...
}

def match_intent(text: str) -> str:
    text = text.lower()
    best, score = process.extractOne(text, list(INTENTS.keys()))
    return best if score > 60 else "None"

# Function to push booking data into Airtable
def push_to_airtable(name, dob, phone, email, treatment, date):
    url = "https://api.airtable.com/v0/appGrimhgiQjWqdxu/Table%201"
    headers = {
        "Authorization": Bearer {AIRTABLE_API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "fields": {
            "Name":        name,
            "DOB":         dob,
            "PhoneNumber": phone,
            "Issues":      email,
            "Treatment":   treatment,
            "Status":      date
        }
    }

    # Debug logging
    app.logger.info(f"[AIRTABLE DEBUG] POST → {url}")
    app.logger.info(f"[AIRTABLE DEBUG] Payload: {payload}")

    resp = requests.post(url, json=payload, headers=headers)

    app.logger.info(f"[AIRTABLE DEBUG] Status: {resp.status_code}")
    app.logger.info(f"[AIRTABLE DEBUG] Body: {resp.text}")

    return resp.status_code == 200

# DentalBot class managing session state
class DentalBot:
    def __init__(self):
        self.name = None
        self.dob = None
        self.phone = None
        self.treatment = None

    def match_intent(self, text: str) -> str:
        return match_intent(text)

    def reset(self):
        self.name = self.dob = self.phone = self.treatment = None
