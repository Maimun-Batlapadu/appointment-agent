from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# 1️⃣ SCOPES and SERVICE_ACCOUNT setup
SCOPES = ["https://www.googleapis.com/auth/calendar.events"]
SERVICE_ACCOUNT_FILE = "appointment-agent-sa.json"

# 2️⃣ Create the credentials and service
credentials = service_account.Credentials.from_service_account_file(
    SERVICE_ACCOUNT_FILE, scopes=SCOPES
)

calendar_service = build("calendar", "v3", credentials=credentials)

# 3️⃣ Initialize your app
app = FastAPI()
@app.get("/")
def root():
    return {"message": "Hello, your Calendar app is running!"}



# 4️⃣ EventRequest Model
class EventRequest(BaseModel):
    summary: str
    start: str
    end: str


# 5️⃣ Route for booking
@app.post("/book")
def book_event(event: EventRequest):
    """Books an event in the connected Google Calendar."""
    try:
        event_body = {
            "summary": event.summary,
            "start": {"dateTime": event.start, "timeZone": "UTC"},
            "end": {"dateTime": event.end, "timeZone": "UTC"}
        }

        created_event = calendar_service.events().insert(
            calendarId='primary',
            body=event_body
        ).execute()

        return {
            "status": "ok",
            "eventId": created_event.get("id"),
            "htmlLink": created_event.get("htmlLink")
        }

    except HttpError as http_err:
        raise HTTPException(status_code=500, detail=f"Google Calendar error: {http_err}")

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")


# 6️⃣ Other Routes (optional)
@app.get("/")
def root():
    return {"message": "Hello, your Calendar app is running!"}
