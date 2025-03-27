from flask import Flask, request, jsonify
from flask_cors import CORS
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import datetime

app = Flask(__name__)
CORS(app)


# Auth setup
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name("credentials.json", scope)
client = gspread.authorize(creds)

@app.route("/bet", methods=["POST"])
def bet():
    try:
        # Move sheet access here
        sheet = client.open("Sergio Bets").sheet1

        data = request.get_json()
        name = data["name"]
        pick = data["pick"]
        from datetime import datetime
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        line = "+3:40"

        sheet.append_row([name, pick, now, line])

        return jsonify({"status": "success"})
    except Exception as e:
        print(e)
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)