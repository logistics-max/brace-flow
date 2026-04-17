from flask import Flask, render_template, request
import gspread
from google.oauth2.service_account import Credentials
from datetime import datetime

app = Flask(__name__)

# Use your exact Google Sheet name
SHEET_NAME = "Brace_Logistics_Database"

def get_google_sheet():
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    creds = Credentials.from_service_account_file('credentials.json', scopes=scope)
    client = gspread.authorize(creds)
    return client.open(SHEET_NAME)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit():
    try:
        clinic = request.form.get('clinic_name')
        brace = request.form.get('brace_type')
        size = request.form.get('brace_size')
        qty = request.form.get('quantity')
        date_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        sheet = get_google_sheet().sheet1
        sheet.append_row([date_str, clinic, brace, size, qty])
        return "<h1>Success! Data Sent to Sheet.</h1><a href='/'>Back to Entry</a>"
    except Exception as e:
        return f"<h1>Error: {e}</h1>"

@app.route('/balancing')
def balancing():
    # Math from your handwritten drawing: Program(20k) -> Workshop(15k) -> Store(8k)
    data = {
        'program': 20000,
        'workshop': 15000,
        'store': 8000,
        'gap_workshop': 5000,
        'gap_store': 7000
    }
    return render_template('dashboard.html', data=data)

@app.route('/workshop')
def workshop():
    return "<h1>Workshop Production Page</h1><p>Status: Active</p><a href='/'>Home</a>"

@app.route('/program')
def program():
    return "<h1>Program Goals Page</h1><p>Target: 20,000 Braces</p><a href='/'>Home</a>"

@app.route('/store')
def store():
    return "<h1>Store Logistics</h1><p>Current Stock: 8,000</p><a href='/'>Home</a>"

@app.route('/distribution')
def distribution():
    return "<h1>Distribution Center</h1><p>Clinic Deliveries in Progress</p><a href='/'>Home</a>"

if __name__ == "__main__":
    app.run()
