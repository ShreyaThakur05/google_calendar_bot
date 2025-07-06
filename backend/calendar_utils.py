from google.oauth2 import service_account
from googleapiclient.discovery import build
from datetime import datetime, timedelta
import pytz
import os
from dotenv import load_dotenv

load_dotenv()

SCOPES = ['https://www.googleapis.com/auth/calendar']
SERVICE_ACCOUNT_FILE = 'service_account.json'
CALENDAR_ID = os.getenv("CALENDAR_ID", "primary")

credentials = service_account.Credentials.from_service_account_file(
    SERVICE_ACCOUNT_FILE, scopes=SCOPES
)
service = build('calendar', 'v3', credentials=credentials)

def check_availability(start_dt: datetime, duration_minutes: int) -> bool:
    end_dt = start_dt + timedelta(minutes=duration_minutes)
    events = service.events().list(
        calendarId=CALENDAR_ID,
        timeMin=start_dt.isoformat(),
        timeMax=end_dt.isoformat(),
        singleEvents=True,
        orderBy='startTime'
    ).execute().get('items', [])
    return len(events) == 0

def create_event(summary: str, description: str, start_dt: datetime, duration_minutes: int):
    end_dt = start_dt + timedelta(minutes=duration_minutes)
    event = {
        'summary': summary,
        'description': description,
        'start': {
            'dateTime': start_dt.isoformat(),
            'timeZone': 'Asia/Kolkata'
        },
        'end': {
            'dateTime': end_dt.isoformat(),
            'timeZone': 'Asia/Kolkata'
        }
    }
    return service.events().insert(calendarId=CALENDAR_ID, body=event).execute()
