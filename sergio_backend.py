
from flask import Flask, request, jsonify
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime

app = Flask(__name__)

# Google Sheets setup
scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name('YOUR_CREDENTIALS_FILE.json', scope)
client = gspread.authorize(creds)
sheet = client.open("Sergio on time?").sheet1

@app.route('/submit_bet', methods=['POST'])
def submit_bet():
    data = request.get_json()
    name = data.get("name")
    pick = data.get("pick")
    date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    line = "+3:40"

    if name and pick:
        sheet.append_row([name, pick, date, line])
        return jsonify({"status": "success"}), 200
    else:
        return jsonify({"status": "error", "message": "Missing name or pick"}), 400

if __name__ == '__main__':
    app.run(debug=True)
