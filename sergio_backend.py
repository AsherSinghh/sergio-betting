from flask import Flask, request, jsonify
from flask_cors import CORS
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime

app = Flask(__name__)
CORS(app)

# Auth setup
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name("credentials.json", scope)
client = gspread.authorize(creds)

@app.route("/bet", methods=["POST"])
def bet():
    try:
        sheet = client.open("Sergio Bets").sheet1
        data = request.get_json()
        name = data["name"]
        pick = data["pick"]
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        line = "+3:40"
        sheet.append_row([name, pick, now, line])
        return jsonify({"status": "success"})
    except Exception as e:
        print(e)
        return jsonify({"status": "error", "message": str(e)}), 500

# NEW ROUTE
@app.route("/line", methods=["GET"])
def get_line():
    try:
        sheet = client.open("Sergio on time?").sheet1
        records = sheet.get_all_records()
        lateness_list = [float(r["Minutes Late"]) for r in records if r["Minutes Late"] != ""]
        mean = sum(lateness_list) / len(lateness_list)
        std_dev = (sum([(x - mean)**2 for x in lateness_list]) / len(lateness_list))**0.5
        next_line = mean + 0.1 * std_dev

        minutes = int(next_line)
        seconds = int((next_line - minutes) * 60)
        line_str = f"{minutes}:{seconds:02d}"

        return jsonify({"line": line_str})
    except Exception as e:
        print(e)
        return jsonify({"status": "error", "message": str(e)}), 500

# Run the Flask app
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
