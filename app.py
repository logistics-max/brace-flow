from flask import Flask, render_template, request
import gspread
from google.oauth2.service_account import Credentials
from datetime import datetime

app = Flask(__name__)

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
        # Get data from the form
        clinic = request.form.get('clinic_name')
        brace = request.form.get('brace_type')
        size = request.form.get('brace_size')
        qty = request.form.get('quantity')
        
        # Create timestamp
        now = datetime.now()
        date_str = now.strftime("%Y-%m-%d %H:%M:%S")

        # Send to Google Sheet
        sheet = get_google_sheet()
        sheet.append_row([date_str, clinic, brace, size, qty])
        
        return "<h1>Success! Data recorded.</h1><a href='/'>Submit another order</a>"
    except Exception as e:
        return f"<h1>Error: {e}</h1>"

if __name__ == "__main__":
    app.run()
