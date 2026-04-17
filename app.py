import os
from flask import Flask, render_template, request
import gspread
from google.oauth2.service_account import Credentials
from datetime import datetime

app = Flask(__name__)

# CONFIGURATION
SHEET_NAME = "Brace_Logistics_Database"

def get_sheet():
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    # Ensure credentials.json is in your main GitHub folder
    creds = Credentials.from_service_account_file('credentials.json', scopes=scope)
    client = gspread.authorize(creds)
    return client.open(SHEET_NAME).sheet1

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit():
    try:
        # Capture Form Data
        clinic = request.form.get('clinic_name')
        brace = request.form.get('brace_type')
        size = request.form.get('brace_size')
        qty = request.form.get('quantity')
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # Write to Google Sheet
        sheet = get_sheet()
        sheet.append_row([timestamp, clinic, brace, size, qty])
        
        return f"""
        <div style="text-align:center; padding:50px; font-family:sans-serif;">
            <h1 style="color:green;">✔ Order Received!</h1>
            <p>Sent to Sheet: {clinic} - {brace} (Size {size}) x{qty}</p>
            <a href="/" style="padding:10px 20px; background:#1a73e8; color:white; text-decoration:none; border-radius:5px;">Enter Another Order</a>
        </div>
        """
    except Exception as e:
        return f"<h1 style='color:red;'>Error!</h1><p>{str(e)}</p><a href='/'>Try Again</a>"

@app.route('/balancing')
def balancing():
    # Numbers from your handwritten drawing
    stats = {'prog': 20000, 'work': 15000, 'store': 8000, 'gap1': 5000, 'gap2': 7000}
    return render_template('dashboard.html', data=stats)

if __name__ == "__main__":
    app.run(debug=True)
