from flask import Flask, jsonify, request
import pandas as pd
import gspread
from google.oauth2.service_account import Credentials
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Google Sheets API setup
SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]
creds = Credentials.from_service_account_file("credentials.json", scopes=SCOPES)
client = gspread.authorize(creds)

SHEET_ID = "1dTDd8Xwg3wv7MRHG2WAX_vXZKlEFne_rDMeemcHSD3s"

# Fetch the latest data from Google Sheets
def fetch_data():
    """Fetches the latest data from Google Sheets into a DataFrame"""
    sheet = client.open_by_key(SHEET_ID).sheet1
    data = sheet.get_all_records()
    return pd.DataFrame(data)

# Route: Fetch all residents with optional filtering
@app.route("/get_residents", methods=["GET"])
def get_residents():
    """Returns all residents' data directly from Google Sheets with optional filtering"""
    try:
        df = fetch_data()
        
        # Apply filters based on query parameters
        for key, value in request.args.items():
            if key in df.columns:
                df = df[df[key] == value]
        
        return jsonify(df.to_dict(orient='records'))
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Route: Fetch WhatsApp numbers
@app.route("/get_whatsapp_numbers", methods=["GET"])
def get_whatsapp_numbers():
    """Returns list of WhatsApp numbers directly from Google Sheets"""
    try:
        df = fetch_data()

        # Ensure all values are strings before using .str operations
        df["Would you like to receive important WhatsApp alerts?"] = df["Would you like to receive important WhatsApp alerts?"].fillna('').astype(str).str.lower()
        
        # Filter only users who want WhatsApp alerts
        whatsapp_users = df[df["Would you like to receive important WhatsApp alerts?"] == "yes"]
        
        # Extract WhatsApp numbers
        numbers = whatsapp_users["Phone Number for WhatsApp Communication (Include Area Code e.g \"1\" for U.S. Numbers)"].tolist()
        
        return jsonify({"whatsapp_numbers": numbers})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
