import os
import uuid
from flask import Flask, render_template, request, redirect
import gspread
from google.oauth2.service_account import Credentials
from datetime import datetime

app = Flask(__name__)

# This function connects to your Google Sheet
def get_sheet():
    try:
        scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
        # IMPORTANT: credentials.json must be uploaded to your GitHub!
        creds = Credentials.from_service_account_file('credentials.json', scopes=scope)
        client = gspread.authorize(creds)
        return client.open("Brace_Logistics_Database").sheet1
    except Exception as e:
        print(f"Connection Error: {e}")
        return None

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit_request', methods=['POST'])
def submit_request():
    sheet = get_sheet()
    if not sheet: return "Database Connection Error"
    
    try:
        data = [
            datetime.now().strftime("%Y-%m-%d %H:%M"),
            request.form.get('clinic_name'),
            request.form.get('brace_type'),
            request.form.get('brace_size'),
            request.form.get('quantity'),
            "Pending Approval",  # Initial Status for Coordinator
            ""                   # Empty ReceiptID for now
        ]
        sheet.append_row(data)
        return "<h1>✔ Success! Sent to Coordinator.</h1><a href='/'>Back</a>"
    except Exception as e:
        return f"Error: {e}"

@app.route('/dashboard')
def dashboard():
    sheet = get_sheet()
    if not sheet: return "Database Error"
    rows = sheet.get_all_records()
    
    balances = {}
    for r in rows:
        c = r.get('Clinic')
        q = int(r.get('Qty', 0) or 0)
        s = r.get('Status')
        
        if c not in balances: balances[c] = 0
        # Math for your concept (+1 for store, -1 for dispatch)
        if s == "In Store": balances[c] += q
        elif s == "Dispatched": balances[c] -= q
            
    return render_template('dashboard.html', balances=balances)

if __name__ == "__main__":
    # This port setting is required for Render
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
