import uuid
from flask import Flask, render_template, request, redirect
import gspread
from google.oauth2.service_account import Credentials
from datetime import datetime

app = Flask(__name__)
SHEET_NAME = "Brace_Logistics_Database"

def get_sheet():
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    creds = Credentials.from_service_account_file('credentials.json', scopes=scope)
    client = gspread.authorize(creds)
    return client.open(SHEET_NAME).sheet1

@app.route('/')
def index():
    return render_template('index.html')

# 1. PRODUCTION REQUEST
@app.route('/submit', methods=['POST'])
def submit():
    try:
        data = [datetime.now().strftime("%Y-%m-%d %H:%M"), request.form.get('clinic_name'), 
                request.form.get('brace_type'), request.form.get('brace_size'), 
                request.form.get('quantity'), "Pending Approval", ""]
        get_sheet().append_row(data)
        return "<h1>Success! Request Sent.</h1><script>setTimeout(()=> {window.location.href='/';}, 2000);</script>"
    except Exception as e: return str(e)

# 2. DEPARTMENT PORTALS
@app.route('/portal/<role>')
def portal(role):
    sheet = get_sheet()
    rows = sheet.get_all_records()
    
    # Logic: +1 for "In Store", -1 for "Dispatched"
    balances = {}
    for r in rows:
        c = r['Clinic']
        q = int(r.get('Qty', 0))
        if c not in balances: balances[c] = 0
        if r['Status'] == "In Store": balances[c] += q
        if r['Status'] == "Dispatched": balances[c] -= q

    # Filter orders based on the "Lock" status
    if role == "coordinator":
        orders = [r for r in rows if r['Status'] in ["Pending Approval", "Dist. Requested"]]
    elif role == "workshop":
        orders = [r for r in rows if r['Status'] == "In Production"]
    elif role == "store":
        orders = [r for r in rows if r['Status'] in ["Produced", "Dist. Approved", "In Store"]]
    else: orders = []

    return render_template('workflow.html', role=role, orders=orders, balances=balances)

# 3. THE APPROVAL LOCK & TRANSITION
@app.route('/transition/<int:row_idx>/<next_status>')
def transition(row_idx, next_status):
    sheet = get_sheet()
    actual_row = row_idx + 2
    if next_status == "Dispatched":
        sheet.update_cell(actual_row, 7, f"M19-{uuid.uuid4().hex[:6].upper()}")
    sheet.update_cell(actual_row, 6, next_status)
    return redirect(request.referrer)

if __name__ == "__main__":
    app.run()
