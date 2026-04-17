import os
import uuid
from flask import Flask, render_template, request, redirect, url_for
import gspread
from google.oauth2.service_account import Credentials
from datetime import datetime

app = Flask(__name__)

# CONFIGURATION
SHEET_NAME = "Brace_Logistics_Database"

def get_sheet():
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    # credentials.json must be in your main GitHub folder
    creds = Credentials.from_service_account_file('credentials.json', scopes=scope)
    client = gspread.authorize(creds)
    return client.open(SHEET_NAME).sheet1

@app.route('/')
def index():
    return render_template('index.html')

# THIS IS THE PART THAT HANDLES THE BUTTON
@app.route('/submit_request', methods=['POST'])
def submit_request():
    try:
        sheet = get_sheet()
        
        # Pulling data from the form
        clinic = request.form.get('clinic_name')
        b_type = request.form.get('brace_type')
        size = request.form.get('brace_size')
        qty = request.form.get('quantity')
        ts = datetime.now().strftime("%Y-%m-%d %H:%M")

        # Adding to Google Sheet
        # Columns: Timestamp, Clinic, Type, Size, Qty, Status, ReceiptID
        sheet.append_row([ts, clinic, b_type, size, qty, "Pending Approval", ""])
        
        # Success Redirect
        return "<h1>✔ Order Sent to Coordinator!</h1><script>setTimeout(()=>{window.location.href='/';}, 2000);</script>"
    
    except Exception as e:
        return f"<h1>Submit Failed</h1><p>Error: {str(e)}</p><a href='/'>Try again</a>"

# PORTALS AND DASHBOARD... (keep your existing portal/transition/dashboard code here)

if __name__ == "__main__":
    app.run(debug=True)
