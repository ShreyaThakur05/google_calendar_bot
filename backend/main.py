from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from calendar_utils import check_availability, create_event
from dateutil.parser import isoparse
from datetime import datetime, timezone  # ✅ This was missing

app = FastAPI()

class EventRequest(BaseModel):
    summary: str
    description: str
    start_time: str
    duration_minutes: int
    message: str

@app.post("/create-event/")
def create_calendar_event(req: EventRequest):
    start_dt = isoparse(req.start_time).astimezone(timezone.utc)
    now_utc = datetime.now(timezone.utc)

    if start_dt < now_utc:
        raise HTTPException(status_code=400, detail="⚠️ Cannot schedule an event in the past.")

    if not check_availability(start_dt, req.duration_minutes):
        raise HTTPException(status_code=409, detail="⚠️ Oops! That time is already booked. Try a different slot!")

    event = create_event(
        summary=req.summary,
        description=req.description,
        start_dt=start_dt,
        duration_minutes=req.duration_minutes
    )
    return {"htmlLink": event.get("htmlLink")}
