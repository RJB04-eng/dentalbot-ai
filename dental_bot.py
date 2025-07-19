# dental_bot.py

from flask import current_app as app

import os
import re
import json
from datetime import datetime
from typing import Dict, List
import requests
from rapidfuzz import fuzz, process

GREETING = (
    "Hey there, this is Cedar House Dental how can we help you today? 🏡"
)
NO_MATCH = "Sorry, I didn’t get that. Please try again."

CLINIC_INFO = """
Clinic Name: Cedar House Dental
Location: 18 Orchard Road, Cardiff
Phone: 029 2019 48
Email: info@cedarhousedental
Opening Hours: Monday–Friday 9:00am–5:00pm, Sat–Sun Closed
Parking: Free parking behind the clinic

Services & Prices
- Check-up: £55
- Hygienist Clean: £75
- Teeth Whitening: £299
- Composite Bonding: £150 per tooth
- Invisalign: from £2,500
- Emergency Appointment: £85 (same-day slots)

FAQs
- Accepting new PRIVATE patients (no NHS)
- Emergency appointments available same-day
- Payment: all major cards, Apple Pay
"""

ALLOWED_TREATMENTS = [
    "Check Ups",
    "Hygienist Clean",
    "Teeth Whitening",
    "Composite Bonding",
    "Invisalign",
    "Emergency Appointment",
]

AIRTABLE_BASE_ID  = os.environ["AIRTABLE_BASE_ID"]
AIRTABLE_API_KEY = os.environ["AIRTABLE_API_KEY"]

INTENTS = {
    "Book a appointment": [
        "book", "i want to book", "schedule", "appointment", "reserve", "plan a visit"
    ],
    "Services.": [
        "services", "treatments", "what do you offer", "prices", "cost"
    ],
    "FAQs": [
        "faq", "frequently asked", "what is asked", "not sure what to ask"
    ],
    "Real Human": [
        "real human", "receptionist", "live person", "human", "speak to someone"
    ],
    "Yes": ["yes", "yep", "sure", "ok", "correct"],
    "No": ["no", "nope", "nah", "not at all"],
}

def match_intent(text: str) -> str:
    text = text.lower()
    best, score = process.extractOne(text, [k for k in INTENTS])
    return best if score > 60 else "None"

def push_to_airtable(name, dob, phone, email, treatment, date):
    url = f"https://api.airtable.com/v0/{AIRTABLE_BASE_ID}/Bookings"
    headers = {
        "Authorization": f"Bearer {AIRTABLE_API_KEY}",
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

    # DEBUG: log the outgoing request via Flask’s logger
    app.logger.info(f"[AIRTABLE DEBUG] POST → {url}")
    app.logger.info(f"[AIRTABLE DEBUG] Payload: {payload}")

    # Actually send to Airtable
    resp = requests.post(url, json=payload, headers=headers)

    # DEBUG: log the response via Flask’s logger
    app.logger.info(f"[AIRTABLE DEBUG] Status: {resp.status_code}")
    app.logger.info(f"[AIRTABLE DEBUG] Body: {resp.text}")

    return resp.status_code == 200
