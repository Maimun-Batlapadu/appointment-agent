# Appointment Agent Project

This project allows you to book appointments by submitting a summary, date, and time. It has two parts:
- **Backend**: A FastAPI app that handles appointment booking.
- **Frontend**: A Streamlit app that collects input and displays results.

---

## Install Requirements
```bash
pip install -r requirements.txt
Run the Backend
bash
Copy
Edit
uvicorn backend.app:app --reload
Run the Frontend
bash
Copy
Edit
streamlit run frontend/app.py
Directory Structure
Copy
Edit
appointment-agent/
├─ backend/
│  └─ app.py
├─ frontend/
│  └─ app.py
├─ README.md
├─ requirements.txt