# 🤖 Google Calendar Booking Assistant

A chatbot-style assistant that allows users to schedule Google Calendar events via natural language using **FastAPI** + **Streamlit**.  
It features real-time availability checks, prevents scheduling in the past, and provides clickable links to the created events.

---

## 📸 Demo

![Assistant](assets/Screenshot_calendarbot.png)

![Calendar](assets/Screenshot_calendar.png)

---

## 📦 Features

✅ **Book events via natural language**  
`Example: schedule on 10 July 2025 3 PM - meeting with team`

🕒 **Prevents booking in the past**

🚫 **Detects and blocks time slot conflicts**

📎 **Provides clickable event link to Google Calendar**

🎨 **Stylish and responsive chatbot UI**

🔒 **Uses Google Calendar API with service account authentication**

---

## 🧰 Tech Stack

| Frontend  | Backend | Others |
|-----------|---------|--------|
| Streamlit | FastAPI | Google Calendar API |
| HTML/CSS  | Python 3.11 | `python-dotenv`, `pytz` |
|           |          | `google-auth`, `requests` |

---

## ⚙️ Setup Instructions

### 1️⃣ Clone the Repository

```bash
git clone https://github.com/ShreyaThakur05/google_calendar_bot.git
cd google_calendar_bot
```

### 2️⃣ Start Backend (FastAPI)

```bash
cd backend
uvicorn main:app --reload
```

### 3️⃣ Start Frontend (Streamlit)

```bash
cd frontend
streamlit run app.py
```

---

## 🔐 Authentication

This project uses a **Google Service Account** with the Calendar API enabled.  
👉 **Important:** You must create a `service_account.json` from your **Google Cloud Console** and place it in your project root or the backend directory.  
Make sure it has permission to access and manage your Google Calendar.


---
