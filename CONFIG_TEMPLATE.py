# Configuration File for Google Sheets Integration
# Copy the values from your Google Cloud Console and Google Sheets

# Your Google Sheet ID (from the URL)
# https://docs.google.com/spreadsheets/d/{SHEET_ID}/edit
GOOGLE_SHEETS_ID = "your-google-sheet-id-here"

# Your Google API Key (from Google Cloud Console)
GOOGLE_SHEETS_API_KEY = "your-google-api-key-here"

# The name of the sheet in your workbook (default: "Sheet1")
SHEET_NAME = "Sheet1"

# Flask Configuration
FLASK_SECRET_KEY = "your_secret_key_here_change_this"

# Agent Credentials (Update these for security)
VALID_CREDENTIALS = {
    'admin': 'password123',
    'agent': 'agent123'
}

# N8N Webhook URL (for sending messages to N8N)
N8N_WEBHOOK_URL = "https://vikramautomation.app.n8n.cloud/webhook/vedantu-chat"

# Server Configuration
HOST = "0.0.0.0"
PORT = 5000
DEBUG = True

# Polling Configuration
POLL_INTERVAL = 2000  # milliseconds
DASHBOARD_REFRESH = 10000  # milliseconds
SHEETS_CACHE_EXPIRE = 300  # seconds (5 minutes)
