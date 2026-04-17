import os
from flask import Flask, render_template, request, redirect, url_for
import gspread
from google.oauth2.service_account import Credentials
from datetime import datetime

app = Flask(__name__)

# This part stops the "get_inv" error you are seeing
@app.context_processor
def utility_processor():
    def get_inv(category, item_name):
        return "0"  # This is a placeholder so the page loads
    return dict(get_inv=get_inv)

# --- GOOGLE SHEETS CONFIG ---
SHEET_NAME = "Brace_Logistics_Database"

def get_google_sheet():
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    creds = Credentials.from_service_account_file('credentials.json', scopes=scope)
    client = gspread.authorize(creds)
    return client.open(SHEET_NAME).sheet1

@app.route('/')
def index():
    # We pass an empty 's' variable because your HTML is looking for it
    return render_template('index.html', s={})

@app.route('/submit', methods=['POST'])
def submit():
    clinic_name = request.form.get('clinic_name')
    brace_type = request.form.get('brace_type')
    quantity = request.form.get('quantity')
    
    now = datetime.now()
    date_str = now.strftime("%Y-%m-%d %H:%M:%S")
    day_str = now.strftime("%A")
    month_str = now.strftime("%B")

    try:
        sheet = get_google_sheet()
        sheet.append_row([date_str, day_str, month_str, clinic_name, brace_type, quantity])
        return "<h1>Success! Data sent to Google Sheets.</h1><a href='/'>Back to Form</a>"
    except Exception as e:
        return f"<h1>Error: {e}</h1>"

if __name__ == "__main__":
    app.run(debug=True)
