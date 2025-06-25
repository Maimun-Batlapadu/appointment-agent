from fastapi import FastAPI
from pydantic import BaseModel
from google.oauth2 import service_account
from googleapiclient.discovery import build
from datetime import datetime, timedelta

app = FastAPI()

# A simple test route
@app.get("/")
def read_root():
    return {"status": "Backend is working"}
# --------------------------------------------------
# STEP: Connect to Google Calendar
# --------------------------------------------------
SERVICE_ACCOUNT_FILE = "appointment-agent-sa.json"  # <-- Name of your JSON file
SCOPES = ["https://www.googleapis.com/auth/calendar"]

# Create Credentials
creds = service_account.Credentials.from_service_account_file(
    SERVICE_ACCOUNT_FILE, scopes=SCOPES
)

# Build the Service
calendar_service = build("calendar", "v3", credentials=creds)

CALENDAR_ID = "maimunbatlapadu123@gmail.com"  # Replace with your actual calendar email
from typing import List

# Route to List Upcoming Events
@app.get("/events")
def list_events():
    now = datetime.utcnow().isoformat() + "Z"  # Current time in UTC
    events_result = calendar_service.events().list(
        calendarId=CALENDAR_ID,
        timeMin=now,
        maxResults=5,
        singleEvents=True,
        orderBy="startTime",
    ).execute()
    events = events_result.get("items", [])

    results = []
    for event in events:
        results.append({
            "summary": event.get("summary", "No title"),
            "start": event["start"].get("dateTime", event["start"].get("date")),
            "end": event["end"].get("dateTime", event["end"].get("date")),
        })
    return results
from fastapi import Request

@app.post("/book")
def book_event(data: dict):
    summary = data.get("summary")
    start_time = data.get("start")
    end_time = data.get("end")

    event = {
        "summary": summary,
        "start": {"dateTime": start_time, "timeZone": "Asia/Kolkata"},
        "end": {"dateTime": end_time, "timeZone": "Asia/Kolkata"},
    }

    created_event = calendar_service.events().insert(
        calendarId=CALENDAR_ID, body=event
    ).execute()

    return {"status": "Booked", "eventId": created_event.get("id")}
