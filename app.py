from flask import Flask, render_template, request, jsonify
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import base64
import json
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'
encoded_creds = os.environ['GOOGLE_SHEETS'].strip()


cred_json = json.loads(base64.b64decode(encoded_creds).decode('utf-8'))


# Set up Google Sheets credentials
scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_dict(cred_json, scope)
client = gspread.authorize(creds)

# Open the Google Sheet (replace with your sheet ID)
sheet = client.open_by_key('1OeqE0y0_YCOyHFxdDgNbN7DgiwFTIXuKFrJkge39HoU').sheet1

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit_email', methods=['POST'])
def submit_email():
    email = request.json['email']
    try:
        sheet.append_row([email])
        return jsonify({"success": True, "message": "Email submitted successfully!"})
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500

if __name__ == "__main__":
    app.run(debug = True)
