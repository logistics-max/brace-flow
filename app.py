import os
import uuid
from flask import Flask, render_template, request, redirect
import gspread
from google.oauth2.service_account import Credentials
from datetime import datetime

app = Flask(__name__)

def get_sheet():
    try:
        scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
        # Make sure credentials.json is actually in your GitHub!
        creds = Credentials.from_service_account_file('credentials.json', scopes=scope)
        client = gspread.authorize(creds)
        return client.open("Brace_Logistics_Database").sheet1
    except Exception as e:
        print(f"Google Sheet Connection Error: {e}")
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
            request.form.get('clinic_name', 'Unknown'),
            request.form.get('brace_type', 'AFO'),
            request.form.get('brace_size', '4'),
            request.form.get('quantity', '1'),
            "Pending Approval",
            ""
        ]
        sheet.append_row(data)
        return "<h1>✔ Success!</h1><a href='/'>Go Back</a>"
    except Exception as e:
        return f"Error: {e}"

# Simple Dashboard logic to prevent crashes
@app.route('/dashboard')
def dashboard():
    sheet = get_sheet()
    if not sheet: return "Database Connection Error"
    rows = sheet.get_all_records()
    
    # Defaults
    balances = {}
    total_in_store = 0
    
    for r in rows:
        # Use .get() to prevent 'KeyError' (Red Screen)
        c = r.get('Clinic', 'Unknown')
        q = int(r.get('Qty', 0) or 0)
        s = r.get('Status', '')
        
        if c not in balances: balances[c] = 0
        if s == "In Store": 
            balances[c] += q
            total_in_store += q
        elif s == "Dispatched":
            balances[c] -= q
            
    return render_template('dashboard.html', balances=balances, total_in_store=total_in_store)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
