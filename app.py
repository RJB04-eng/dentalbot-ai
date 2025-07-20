# app.py

import os
from flask import Flask, request, jsonify
from dental_bot import DentalBot, push_to_airtable
import logging

AIRTABLE_API_KEY = os.environ["AIRTABLE_API_KEY"]
AIRTABLE_BASE_ID = os.environ["AIRTABLE_BASE_ID"]

app = Flask(__name__)
logging.basicConfig(level=logging.INFO)

sessions = {}

def get_bot(session_id: str) -> DentalBot:
    if session_id not in sessions:
        sessions[session_id] = DentalBot()
    return sessions[session_id]

@app.route("/", methods=["GET"])
def health():
    return "DentalBot API is running 🦷", 200

@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json(force=True)
    session_id = data.get("session_id", "default")
    user_text = data.get("user", "")

    bot = get_bot(session_id)
    intent = bot.match_intent(user_text)

    if intent == "Book a appointment":
        return jsonify({"reply": "Sure! You can book via the /book endpoint.", "intent": intent})
    if intent in ("Services.", "FAQs"):
        from dental_bot import CLINIC_INFO
        return jsonify({"reply": CLINIC_INFO, "intent": intent})
    if intent == "Real Human":
        return jsonify({"reply": "Connecting you to a receptionist…", "intent": intent})
    return jsonify({"reply": "👂 I didn’t get that. Try again or use /book.", "intent": "None"})

@app.route("/book", methods=["POST"])
def book():
    data = request.get_json(force=True)
    app.logger.info(f"[BOOK] Received payload: {data}")
    try:
        ok = push_to_airtable(
            ok = push_to_airtable(
    data["name"],
    data["dob"],
    data["phone"],
    data["email"],
    data["treatment"]
)

        )
        app.logger.info(f"[BOOK] push_to_airtable returned: {ok}")
        return jsonify({"success": ok}), 200
    except Exception as e:
        app.logger.exception("[BOOK] Exception during booking:")
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    # Get the PORT Render assigns (default to 5000 locally)
    port = int(os.environ.get("PORT", 5000))
    # Enable debug locally, bind to all interfaces so Render can reach it
    app.run(debug=True, host="0.0.0.0", port=port)

