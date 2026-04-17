import os
from flask import Flask, render_template, request, redirect, url_for
import gspread
from google.oauth2.service_account import Credentials
from datetime import datetime

app = Flask(__name__)

# --- GOOGLE SHEETS CONFIG ---
# Make sure your Google Sheet is named exactly this:
SHEET_NAME = "Brace_Logistics_Database"

def get_google_sheet():
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    # This looks for the credentials.json file you uploaded to GitHub
    creds = Credentials.from_service_account_file('credentials.json', scopes=scope)
    client = gspread.authorize(creds)
    return client.open(SHEET_NAME).sheet1

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit():
    clinic_name = request.form.get('clinic_name')
    brace_type = request.form.get('brace_type')
    quantity = request.form.get('quantity')
    
    # Get current date and time
    now = datetime.now()
    date_str = now.strftime("%Y-%m-%d %H:%M:%S")
    day_str = now.strftime("%A")
    month_str = now.strftime("%B")

    try:
        sheet = get_google_sheet()
        # Add a new row to the Google Sheet
        sheet.append_row([date_str, day_str, month_str, clinic_name, brace_type, quantity])
        return "<h1>Success! Data sent to Google Sheets.</h1><a href='/'>Back to Form</a>"
    except Exception as e:
        return f"<h1>Error: {e}</h1><p>Check if the sheet is shared with your service account email.</p>"

if __name__ == "__main__":
    # Standard startup block with NO 'with' and correct indentation
    app.run(debug=True)
