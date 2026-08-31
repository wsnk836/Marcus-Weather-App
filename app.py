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
