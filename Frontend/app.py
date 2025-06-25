import streamlit as st
import requests
from datetime import datetime
import streamlit as st
import requests
import json
st.title("Book an Event")

with st.form("event_form"):
    summary = st.text_input("Summary of the Event")
    date = st.date_input("Date of the Event", value=datetime.today())
    start_time = st.time_input("Start Time", value=datetime.now().time())
    end_time = st.time_input("End Time", value=datetime.now().time())
    submitted = st.form_submit_button("Book Event")
if submitted:
    start_dt = datetime.combine(date, start_time).isoformat()
    end_dt = datetime.combine(date, end_time).isoformat()

    url = "http://127.0.0.1:8000/book"
    payload = {
        "summary": summary,
        "start": start_dt,
        "end": end_dt
    }

    response = requests.post(url, json=payload)

    if response.status_code == 200:
        data = response.json()
        st.success(f"✅ Event Booked!\nEvent ID: {data.get('eventId')}\nStatus: {data.get('status')}")
    else:
        st.error(f"❌ Failed to book the event. Status Code: {response.status_code}")
        st.write(response.json())

st.title("📅 Appointment Booking Chat")

user_message = st.text_input("You:", "")

if user_message:
    if "book" in user_message.lower() or "schedule" in user_message.lower():
        st.write("🤔 Extracting date and time... (you can upgrade this later!)")

        # Demo example: Book fixed date/time
        payload = {
            "summary": "Meeting with Maimun",
            "start": "2025-06-25T15:00:00",
            "end": "2025-06-25T15:30:00"
        }

        response = requests.post("http://127.0.0.1:8000/book",
                                 headers={"Content-Type": "application/json"},
                                 data=json.dumps(payload))
        if response.status_code == 200:
            result = response.json()
            st.success(f"✅ Booked! Event ID: {result.get('eventId')}")
        else:
            st.error(f"Error: {response.content}")

    else:
        st.write("👋 Try typing something like: 'Book a call tomorrow at 3 PM'.")
