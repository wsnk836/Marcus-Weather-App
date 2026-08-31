import streamlit as st
import requests

# Page Configuration
st.set_page_config(page_title="Weather & Radio Dashboard", layout="wide")
st.title("📻 Weather & Radio Dashboard")

# 1. Fetch Live Weather Data
st.header("🌦️ Current Weather Data (Chicago)")
weather_url = "https://api.open-meteo.com/v1/forecast?latitude=41.85&longitude=-87.65&current_weather=true"

try:
    response = requests.get(weather_url).json()
    current = response.get("current_weather", {})
    
    col1, col2, col3 = st.columns(3)
    col1.metric("Temperature", f"{current.get('temperature', '--')} °C")
    col2.metric("Wind Speed", f"{current.get('windspeed', '--')} km/h")
    col3.metric("Wind Direction", f"{current.get('winddirection', '--')}°")
except Exception as e:
    st.error(f"Could not fetch weather data. Error: {e}")

st.markdown("---")

# 2. Embed a Live Radio Stream
st.header("📡 Live Radio Stream")
st.write("Currently playing: BBC World Service (Testing Stream)")

# This is a REAL, working streaming URL so you can hear audio
real_stream_url = "https://stream.live.vc.bbcmedia.co.uk/bbc_world_service" 

st.audio(real_stream_url, format="audio/mp3")

st.markdown("---")

# ==========================================
# --- NEW COMMUNITY ANNOUNCEMENTS SECTION ---
# ==========================================
st.header("📢 Community Announcements")
st.write("Browse current announcements or submit a new notice below.")

if "community_announcements" not in st.session_state:
    st.session_state.community_announcements = [
        {
            "author": "Dashboard Admin",
            "title": "Welcome to the Community Board",
            "text": "Feel free to post local notices and announcements using the submission form below.",
            "time": "Active"
        }
    ]

# Display existing announcements
for ann in st.session_state.community_announcements:
    st.markdown(
        f"""
        <div style="background: #1e1e24; border: 1px solid #3f3f46; border-left: 4px solid #38bdf8; border-radius: 8px; padding: 14px; margin-bottom: 10px;">
            <strong style="font-size: 1.05rem; color: #f4f4f5;">{ann['title']}</strong><br/>
            <span style="font-size: 0.9rem; color: #d4d4d8; display: block; margin-top: 4px;">{ann['text']}</span>
            <span style="font-size: 0.75rem; color: #a1a1aa; display: block; margin-top: 8px; font-style: italic;">Posted by: {ann['author']}</span>
        </div>
        """,
        unsafe_allow_html=True,
    )

# Form to add a new announcement
with st.form("community_announcement_form"):
    st.subheader("Post a New Announcement")
    ann_author = st.text_input("Your Name / Organization *", placeholder="e.g., Neighborhood Watch")
    ann_title = st.text_input("Announcement Title *", placeholder="e.g., Community Cleanup Event")
    ann_text = st.text_area("Announcement Details *", placeholder="Enter the details of your announcement here...")
    
    ann_submitted = st.form_submit_button("Publish Announcement", use_container_width=True)
    
    if ann_submitted:
        if not ann_author.strip() or not ann_title.strip() or not ann_text.strip():
            st.error("Please fill in all required fields before publishing.")
        else:
            st.session_state.community_announcements.insert(
                0,
                {
                    "author": ann_author.strip(),
                    "title": ann_title.strip(),
                    "text": ann_text.strip(),
                    "time": "Just now"
                }
            )
            st.success("Announcement published successfully!")
            st.rerun()
