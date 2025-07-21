import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "vendor"))

from flask import Flask, request, jsonify
from dental_bot import push_to_airtable
import logging

AIRTABLE_API_KEY = os.environ["AIRTABLE_API_KEY"]
AIRTABLE_BASE_ID = os.environ["AIRTABLE_BASE_ID"]

app = Flask(__name__)
logging.basicConfig(level=logging.INFO)

def json_resp(body: dict, code: int):
    return jsonify(body), code

@app.route("/", methods=["GET"])
def health():
    return "DentalBot API is running 🦷", 200

@app.route("/book", methods=["POST"])
def book():
    try:
        data = request.get_json(force=True)
        app.logger.info(f"[BOOK] Received payload: {data}")

        
        for field in ("name","dob","phone","email","treatment"):
            if not data.get(field):
                return json_resp(
                    {"success": False, "error": f"Missing '{field}'"}, 400
                )

        ok = push_to_airtable(
            data["name"],
            data["dob"],
            data["phone"],
            data["email"],
            data["treatment"],
        )

        app.logger.info(f"[BOOK] push_to_airtable returned: {ok}")
        return json_resp({"success": ok}, 200 if ok else 400)

    except Exception as e:
        app.logger.exception("[BOOK] uncaught exception:")
        return json_resp({"success": False, "error": str(e)}, 500)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=True, host="0.0.0.0", port=port)