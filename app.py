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

# --- HOME / DATA ENTRY ---
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
        
        now = datetime.now()
        date_str = now.strftime("%Y-%m-%d %H:%M:%S")

        sheet = get_google_sheet()
        sheet.append_row([date_str, clinic, brace, size, qty])
        
        return "<h1>Success! Data recorded.</h1><a href='/'>Back to Data Entry</a>"
    except Exception as e:
        return f"<h1>Error: {e}</h1>"

# --- NEW SECTIONS ---
@app.route('/workshop')
def workshop():
    return "<h1>Workshop Program Dashboard</h1><p>We will build the logic to view workshop data here next.</p><br><a href='/'>Back to Home</a>"

@app.route('/program')
def program():
    return "<h1>Program Analytics</h1><p>We will build the logic to view program data here next.</p><br><a href='/'>Back to Home</a>"

@app.route('/store')
def store():
    return "<h1>Store Logistics</h1><p>We will build the logic to view inventory levels here next.</p><br><a href='/'>Back to Home</a>"

@app.route('/balancing')
def balancing():
    return "<h1>Balancing System</h1><p>We will build the logic to balance stock between clinics here next.</p><br><a href='/'>Back to Home</a>"

@app.route('/distribution')
def distribution():
    return "<h1>Distribution Center</h1><p>We will build the logic to manage shipping/distribution here next.</p><br><a href='/'>Back to Home</a>"

if __name__ == "__main__":
    app.run()
