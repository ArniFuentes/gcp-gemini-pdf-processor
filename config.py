import os
import google.auth
from dotenv import load_dotenv
from googleapiclient.discovery import build
from google.oauth2 import service_account

# Load .env only if it exists (Local)
load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")
SPREADSHEET_ID = os.getenv("SPREADSHEET_ID")
FOLDER_ID = os.getenv("FOLDER_ID")

SCOPES = [
    'https://www.googleapis.com/auth/drive',
    'https://www.googleapis.com/auth/spreadsheets'
]


def get_credentials():
    key_path = 'credentials.json'

    # If the file exists, it is local.
    if os.path.exists(key_path):
        return service_account.Credentials.from_service_account_file(
            key_path, scopes=SCOPES)
    # Use Application Default Credentials (GCP)
    else:
        creds, _ = google.auth.default(scopes=SCOPES)
        return creds

creds = get_credentials()
drive_service = build('drive', 'v3', credentials=creds)
