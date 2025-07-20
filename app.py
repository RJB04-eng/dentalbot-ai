import os
import logging
from flask import Flask, request, jsonify
from dental_bot import push_to_airtable

# Load from env
AIRTABLE_API_KEY = os.environ["AIRTABLE_API_KEY"]
AIRTABLE_BASE_ID = os.environ["AIRTABLE_BASE_ID"]

app = Flask(__name__)
logging.basicConfig(level=logging.INFO)

@app.route("/", methods=["GET"])
def health():
    return "DentalBot API is running 🦷", 200

@app.route("/book", methods=["POST"])
def book():
    data = request.get_json(force=True)
    app.logger.info(f"[BOOK] Received payload: {data}")

    ok = push_to_airtable(
        data.get("name"),
        data.get("dob"),
        data.get("phone"),
        data.get("email"),
        data.get("treatment")
    )

    app.logger.info(f"[BOOK] push_to_airtable returned: {ok}")
    status_code = 200 if ok else 400
    return jsonify({"success": ok}), status_code

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=True, host="0.0.0.0", port=port)