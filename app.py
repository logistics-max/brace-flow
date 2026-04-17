from flask import Flask, render_template, request
import gspread
from google.oauth2.service_account import Credentials
from datetime import datetime

app = Flask(__name__)

# --- GOOGLE SHEETS CONFIG ---
SHEET_NAME = "Brace_Logistics_Database"

def get_google_sheet():
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    creds = Credentials.from_service_account_file('credentials.json', scopes=scope)
    client = gspread.authorize(creds)
    return client.open(SHEET_NAME).sheet1

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit():
    try:
        clinic = request.form.get('clinic_name')
        brace = request.form.get('brace_type')
        qty = request.form.get('quantity')
        
        now = datetime.now()
        date_str = now.strftime("%Y-%m-%d %H:%M:%S")
        day_str = now.strftime("%A")
        month_str = now.strftime("%B")

        sheet = get_google_sheet()
        sheet.append_row([date_str, day_str, month_str, clinic, brace, qty])
        return "<h1>Success! Data sent to Google Sheets.</h1><a href='/'>Back to Form</a>"
    except Exception as e:
        return f"<h1>Error: {e}</h1>"

if __name__ == "__main__":
    app.run()
