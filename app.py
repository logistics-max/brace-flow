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
        creds = Credentials.from_service_account_file('credentials.json', scopes=scope)
        client = gspread.authorize(creds)
        return client.open("Brace_Logistics_Database").sheet1
    except:
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
            "Pending Approval",
            ""
        ]
        sheet.append_row(data)
        return "<h1>✔ Success! Sent to Coordinator.</h1><a href='/'>Back</a>"
    except Exception as e:
        return f"Error: {e}"

@app.route('/portal/<role>')
def portal(role):
    sheet = get_sheet()
    if not sheet: return "Database Error"
    rows = sheet.get_all_records()
    
    # Inventory Balance Logic (+1 / -1)
    balances = {}
    for r in rows:
        c = r.get('Clinic')
        q = int(r.get('Qty', 0) or 0)
        s = r.get('Status')
        if c not in balances: balances[c] = 0
        if s == "In Store": balances[c] += q
        elif s == "Dispatched": balances[c] -= q

    # Filter by Role
    if role == "coordinator":
        orders = [r for r in rows if r['Status'] in ["Pending Approval", "Dist. Requested"]]
    elif role == "store":
        orders = [r for r in rows if r['Status'] in ["Produced", "In Store", "Dist. Approved"]]
    else: orders = []

    return render_template('workflow.html', role=role, orders=orders, balances=balances)

@app.route('/transition/<int:row_idx>/<next_status>')
def transition(row_idx, next_status):
    sheet = get_sheet()
    actual_row = row_idx + 2
    if next_status == "Dispatched":
        sheet.update_cell(actual_row, 7, f"M19-{uuid.uuid4().hex[:6].upper()}")
    sheet.update_cell(actual_row, 6, next_status)
    return redirect(request.referrer)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
