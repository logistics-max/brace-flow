from flask import Flask, render_template, request
import gspread
from google.oauth2.service_account import Credentials
from datetime import datetime

app = Flask(__name__)

# Replace with your actual Google Sheet name
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
        size = request.form.get('brace_size')
        qty = request.form.get('quantity')
        date_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        sheet = get_google_sheet().sheet1
        sheet.append_row([date_str, clinic, "Brace", size, qty])
        return "<h1>Success!</h1><a href='/'>Back</a>"
    except Exception as e:
        return f"<h1>Error: {e}</h1>"

@app.route('/balancing')
def balancing():
    # Example logic using numbers from your "Balancing" diagram
    # Program: 20,000 | Workshop: 15,000 | Store: 8,000
    pipeline_data = {
        'program': 20000,
        'workshop': 15000,
        'store': 8000,
        'distributed': 8000,
        'gap_workshop': 5000, # Program - Workshop
        'gap_store': 7000     # Workshop - Store
    }
    return render_template('dashboard.html', data=pipeline_data)

# Dummy routes for other sections
@app.route('/workshop')
@app.route('/program')
@app.route('/store')
def placeholder():
    return "<h1>Section coming soon</h1><a href='/'>Back Home</a>"

if __name__ == "__main__":
    app.run()
