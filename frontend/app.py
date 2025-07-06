import streamlit as st
import requests
from datetime import datetime
import pytz

st.set_page_config(page_title="Google Calendar Booking Assistant", layout="centered")

#Custom CSS 
st.markdown("""
    <style>
        html, body {
            background: #0D0D0D;
        }
        .fixed-header {
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            background-color: #333333; /* Dark grey header */
            color: #ffffff;
            padding: 1.2rem 0;
            text-align: center;
            z-index: 1000;
            box-shadow: 0 4px 12px rgba(0,0,0,0.3);
        }
        .fixed-header h2 {
            margin: 0;
            font-size: 1.8rem;
            letter-spacing: 0.5px;
        }
        .fixed-header::after {
            content: "";
            display: block;
            height: 3px;
            background-color: #FFD600; /* Yellow accent strip */
            margin-top: 0.5rem;
            width: 80%;
            margin-left: auto;
            margin-right: auto;
            border-radius: 2px;
        }
        .spacer {
            height: 110px;
        }
        .chat-bubble.user {
            background-color: #008080; /* Teal user bubble */
            color: white;
            padding: 0.75rem;
            border-radius: 1rem;
            margin: 0.5rem 0;
            text-align: right;
        }
        .chat-bubble.bot {
            background-color: #368DD9; /* Bright blue bot bubble */
            color: white;
            padding: 0.75rem;
            border-radius: 1rem;
            margin: 0.5rem 0;
            text-align: left;
        }
        a {
            color: #00FF7F; /* Mint green link */
            font-weight: bold;
            text-decoration: underline;
        }
    </style>
""", unsafe_allow_html=True)

# Header
st.markdown("""
<div class="fixed-header">
    <h2>🤖 Google Calendar Booking Assistant</h2>
</div>
<div class="spacer"></div>
""", unsafe_allow_html=True)

# Chat State
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display messages 
for msg in st.session_state.messages:
    role = msg["role"]
    content = msg["content"]
    bubble_class = "user" if role == "user" else "bot"
    st.markdown(f"<div class='chat-bubble {bubble_class}'>{content}</div>", unsafe_allow_html=True)

# Input field 
user_input = st.chat_input("Schedule something...")

if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})

    try:
        if "schedule" in user_input.lower():
            text = user_input.lower().split("schedule on")[-1].strip()
            date_time_part, _, message = text.partition("-")
            date_time_obj = datetime.strptime(date_time_part.strip(), "%d %B %Y %I %p")

            # Convert to UTC
            india_tz = pytz.timezone("Asia/Kolkata")
            localized_dt = india_tz.localize(date_time_obj)
            start_time_utc = localized_dt.astimezone(pytz.utc).isoformat()

            payload = {
                "summary": "Scheduled Event",
                "description": message.strip(),
                "start_time": start_time_utc,
                "duration_minutes": 30,
                "message": user_input
            }

            res = requests.post("http://localhost:8000/create-event/", json=payload)

            if res.status_code == 200:
                event_link = res.json().get("htmlLink")
                reply = f'✅ Scheduled successfully! <a href="{event_link}" target="_blank">Click here</a> to view it now.'

            else:
                reply = f"❌ {res.json().get('detail', 'Something went wrong')}"

        else:
            reply = "🤖 I can help you schedule a meeting. Try:\n\n`schedule on 10 July 2025 3 PM - team sync`"

    except Exception as e:
        reply = "❌ Something went wrong while parsing your message. Please use the format:\n\n`schedule on 10 July 2025 3 PM - meeting`"

    st.session_state.messages.append({"role": "bot", "content": reply})
    st.rerun()
