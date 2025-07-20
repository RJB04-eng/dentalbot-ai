# app.py
from flask import Flask, request, jsonify
from dental_bot import push_to_airtable

app = Flask(__name__)

@app.route("/book", methods=["POST"])
def book():
    data = request.get_json(force=True)
    ok = push_to_airtable(
        data.get("name"),
        data.get("dob"),
        data.get("phone"),
        data.get("email"),
        data.get("treatment")
    )
    return jsonify({"success": ok}), (200 if ok else 400)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
