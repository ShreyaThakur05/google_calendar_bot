from datetime import datetime
from dateparser.search import search_dates

def parse_user_request(message: str):
    date_results = search_dates(
        message,
        settings={
            "PREFER_DATES_FROM": "future",
            "RETURN_AS_TIMEZONE_AWARE": False,
            "TIMEZONE": "Asia/Kolkata"
        }
    )
    if not date_results:
        raise ValueError("I couldn’t find a future date/time in that message.")

    matched_text, dt = date_results[0]
    if dt < datetime.now():
        raise ValueError("I can't book an appointment in the past. Please pick a future time.")

    # Extract title if using " - title" format
    parts = message.split(" - ")
    title = parts[1].strip() if len(parts) > 1 else "Meeting"

    return matched_text, dt.strftime("%Y-%m-%dT%H:%M:%S"), title
