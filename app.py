from flask import Flask, render_template, request, redirect
import gspread
from google.oauth2.service_account import Credentials
from datetime import datetime

app = Flask(__name__)

# IMPORTANT: Make sure this name matches your Google Sheet EXACTLY
SHEET_NAME = "Brace_Logistics_Database"

def get_google_sheet():
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    # Ensure credentials.json is uploaded to your GitHub main folder
    creds = Credentials.from_service_account_file('credentials.json', scopes=scope)
    client = gspread.authorize(creds)
    return client.open(SHEET_NAME).sheet1

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit():
    try:
        # Get data from the form
        clinic = request.form.get('clinic_name')
        brace = request.form.get('brace_type')
        size = request.form.get('brace_size')
        qty = request.form.get('quantity')
        date_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # Send to Google Sheet
        sheet = get_google_sheet()
        sheet.append_row([date_str, clinic, brace, size, qty])
        
        # This sends you back to the form so you can enter more data immediately
        return "<h1>Success! Order Added to Google Sheet.</h1><br><a href='/'>Click here to enter another order</a>"
    except Exception as e:
        return f"<h1>Error Connection: {e}</h1><p>Check if your Google Sheet is named: {SHEET_NAME}</p>"

@app.route('/balancing')
def balancing():
    data = {'program': 20000, 'workshop': 15000, 'store': 8000, 'gap_workshop': 5000, 'gap_store': 7000}
    return render_template('dashboard.html', data=data)

if __name__ == "__main__":
    app.run()
