import os
import uuid
from flask import Flask, render_template, request, redirect, url_for
import gspread
from google.oauth2.service_account import Credentials
from datetime import datetime

app = Flask(__name__)

# --- CONFIGURATION ---
SHEET_NAME = "Brace_Logistics_Database"

def get_sheet():
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    # Ensure credentials.json is uploaded to your GitHub main folder
    creds = Credentials.from_service_account_file('credentials.json', scopes=scope)
    client = gspread.authorize(creds)
    return client.open(SHEET_NAME).sheet1

# --- ROUTES ---

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit():
    try:
        sheet = get_sheet()
        data = [
            datetime.now().strftime("%Y-%m-%d %H:%M"),
            request.form.get('clinic_name'),
            request.form.get('brace_type'),
            request.form.get('brace_size'),
            request.form.get('quantity'),
            "Pending Approval", # Initial Status
            ""                  # Receipt ID placeholder
        ]
        sheet.append_row(data)
        return "<h1>✔ Request Submitted!</h1><script>setTimeout(()=>{window.location.href='/';}, 2000);</script>"
    except Exception as e:
        return f"<h1>Error</h1><p>{str(e)}</p><a href='/'>Back</a>"

@app.route('/portal/<role>')
def portal(role):
    sheet = get_sheet()
    rows = sheet.get_all_records()
    
    # Calculate Live Inventory Balances (+1 for Store, -1 for Dispatch)
    balances = {}
    for r in rows:
        clinic = r['Clinic']
        qty = int(r.get('Qty', 0) or 0)
        status = r['Status']
        
        if clinic not in balances:
            balances[clinic] = 0
            
        if status == "In Store":
            balances[clinic] += qty
        elif status == "Dispatched":
            balances[clinic] -= qty

    # Filter orders based on the Department Role
    if role == "coordinator":
        orders = [r for r in rows if r['Status'] in ["Pending Approval", "Dist. Requested"]]
    elif role == "workshop":
        orders = [r for r in rows if r['Status'] == "In Production"]
    elif role == "store":
        orders = [r for r in rows if r['Status'] in ["Produced", "In Store", "Dist. Approved"]]
    else:
        orders = []
