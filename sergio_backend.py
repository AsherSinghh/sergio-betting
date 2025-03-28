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

# Route to submit a bet
@app.route("/bet", methods=["POST"])
def bet():
    try:
        sheet = client.open("Sergio Bets").sheet1
        data = request.get_json()
        name = data["name"]
        pick = data["pick"]
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        line = "+3:40"  # You can update this to be dynamic if needed
        sheet.append_row([name, pick, now, line])
        return jsonify({"status": "success"})
    except Exception as e:
        print("Error in /bet:", e)
        return jsonify({"status": "error", "message": str(e)}), 500

# Route to get the current betting line
@app.route("/line", methods=["GET"])
def get_line():
    try:
        sheet = client.open("Sergio on time?").sheet1
        records = sheet.get_all_records()
        print("Fetched records:", records)

        if not records:
            print("No records found.")
            return jsonify({"line": "N/A"})

        lateness_list = []
        for row in records:
            value = row.get("Decimal Minutes Late")  # <-- Fixed here
            if value:
                try:
                    lateness_list.append(float(value))
                except ValueError:
                    print(f"Skipping non-numeric value: {value}")

        if not lateness_list:
            print("No valid 'Decimal Minutes Late' values found.")
            return jsonify({"line": "N/A"})

        mean = sum(lateness_list) / len(lateness_list)
        std_dev = (sum([(x - mean)**2 for x in lateness_list]) / len(lateness_list))**0.5
        next_line = mean + 0.1 * std_dev

        minutes = int(next_line)
        seconds = int((next_line - minutes) * 60)
        line_str = f"{minutes}:{seconds:02d}"

        print("Calculated betting line:", line_str)
        return jsonify({"line": line_str})
    except Exception as e:
        print("Error in /line:", e)
        return jsonify({"status": "error", "message": str(e)}), 500

# Run the Flask app
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
