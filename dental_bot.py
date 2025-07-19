# dental_bot.py

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

AIRTABLE_URL = "https://api.airtable.com/v0/appGrimhgiQjWqdxu/Table%201"
AIRTABLE_KEY = "YOUR_AIRTABLE_API_KEY"  # <- Replace this before deploy

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

def push_to_airtable(name: str, dob: str, phone: str, treatment: str) -> bool:
    headers = {
        "Authorization": f"Bearer {AIRTABLE_KEY}",
        "Content-Type": "application/json"
    }
    data = {
        "records": [
            {
                "fields": {
                    "Name": name,
                    "DOB": dob,
                    "PhoneNumber": phone,
                    "Treatment": treatment,
                    "Status": "False",
                }
            }
        ]
    }
    r = requests.post(AIRTABLE_URL, headers=headers, json=data, timeout=10)
    return r.status_code == 200

class DentalBot:
    def __init__(self):
        self.name = None
        self.dob = None
        self.phone = None
        self.treatment = None

    def match_intent(self, text):
        return match_intent(text)

    def reset(self):
        self.name = self.dob = self.phone = self.treatment = None
