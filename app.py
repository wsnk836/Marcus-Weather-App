import streamlit as st
import streamlit.components.v1 as requests_comp
import requests
import time
from datetime import datetime
from zoneinfo import ZoneInfo

# Page Configuration
st.set_page_config(
    page_title="Weather Command", 
    page_icon="📡",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- AUTOMATIC MOBILE & BROWSER NAMING ---
requests_comp.html("""
<script>
    window.parent.document.title = "Weather Command";
    let metaApple = window.parent.document.createElement('meta');
    metaApple.name = "apple-mobile-web-app-title";
    metaApple.content = "Weather Radar";
    window.parent.document.head.appendChild(metaApple);

    let metaApp = window.parent.document.createElement('meta');
    metaApp.name = "application-name";
    metaApp.content = "Weather Radar";
    window.parent.document.head.appendChild(metaApp);
</script>
""", height=0, width=0)

# --- TACTICAL CRIMSON & CARBON CSS ---
st.markdown("""
<style>
    .stApp {
        background-color: #0c0d10;
        color: #f4f4f5;
        font-family: system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
    }
    .hero-banner {
        background: linear-gradient(145deg, #18191f 0%, #0e0f12 100%);
        border: 1px solid #27272a;
        border-top: 3px solid #ef4444;
        border-radius: 14px;
        padding: 22px 28px;
        margin-bottom: 16px;
        box-shadow: 0 10px 25px -10px rgba(0, 0, 0, 0.7);
    }
    .hero-title {
        font-size: 2rem;
        font-weight: 800;
        color: #f87171;
        margin: 0;
        display: flex;
        align-items: center;
        gap: 12px;
        letter-spacing: -0.02em;
    }
    .hero-subtitle {
        color: #a1a1aa;
        font-size: 0.92rem;
        margin-top: 6px;
        letter-spacing: 0.04em;
        text-transform: uppercase;
        font-weight: 500;
    }
    .command-card {
        background: #121316;
        border: 1px solid #27272a;
        border-radius: 12px;
        padding: 16px 20px;
        margin-bottom: 16px;
        color: #e4e4e7;
        font-size: 0.96rem;
        line-height: 1.5;
    }
    .welcome-card { border-left: 4px solid #ef4444; }
    .alert-card-severe {
        background: rgba(239, 68, 68, 0.12);
        border: 1px solid rgba(239, 68, 68, 0.3);
        border-left: 4px solid #ef4444;
        border-radius: 10px;
        padding: 14px 18px;
        margin-bottom: 12px;
    }
    .alert-card-clear {
        background: rgba(16, 185, 129, 0.08);
        border: 1px solid rgba(16, 185, 129, 0.25);
        border-left: 4px solid #10b981;
        border-radius: 10px;
        padding: 14px 18px;
        margin-bottom: 12px;
        color: #d1fae5;
    }
    .radar-wrapper {
        position: relative;
        width: 100%;
        background: #121316;
        border-radius: 10px;
        overflow: hidden;
        border: 1px solid #27272a;
    }
    .radar-img {
        width: 100%;
        display: block;
    }
    .user-pin-container {
        position: absolute;
        top: 50%;
        left: 50%;
        transform: translate(-50%, -50%);
        display: flex;
        flex-direction: column;
        align-items: center;
        pointer-events: none;
    }
    .user-dot {
        width: 12px;
        height: 12px;
        background-color: #38bdf8;
        border: 2px solid #ffffff;
        border-radius: 50%;
        box-shadow: 0 0 10px #38bdf8, 0 0 20px #38bdf8;
        animation: pulse-dot 2s infinite;
    }
    .user-label {
        background: rgba(12, 13, 16, 0.85);
        color: #38bdf8;
        font-size: 0.7rem;
        font-weight: 700;
        padding: 2px 6px;
        border-radius: 4px;
        border: 1px solid rgba(56, 189, 248, 0.4);
        margin-top: 3px;
        white-space: nowrap;
        letter-spacing: 0.03em;
    }
    @keyframes pulse-dot {
        0% { transform: scale(0.95); box-shadow: 0 0 0 0 rgba(56, 189, 248, 0.7); }
        70% { transform: scale(1); box-shadow: 0 0 0 8px rgba(56, 189, 248, 0); }
        100% { transform: scale(0.95); box-shadow: 0 0 0 0 rgba(56, 189, 248, 0); }
    }
    [data-testid="stMetric"] {
        background: #121316;
        border: 1px solid #27272a;
        border-radius: 12px;
        padding: 14px 18px;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
    }
    [data-testid="stMetricLabel"] {
        font-size: 0.85rem !important;
        color: #a1a1aa !important;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }
    [data-testid="stMetricValue"] {
        font-size: 1.6rem !important;
        font-weight: 700 !important;
        color: #fafafa !important;
    }
    .stTabs [data-baseweb="tab-list"] { gap: 8px; background-color: transparent; }
    .stTabs [data-baseweb="tab"] {
        border-radius: 8px;
        padding: 4px 12px;
        background-color: #121316;
        border: 1px solid #27272a;
        color: #a1a1aa;
        font-weight: 600;
        font-size: 0.85rem;
    }
    .stTabs [aria-selected="true"] {
        background: #ef4444 !important;
        color: #0c0d10 !important;
        border-color: #ef4444 !important;
        font-weight: 700 !important;
    }
</style>
""", unsafe_allow_html=True)

# --- HERO HEADER ---
st.markdown("""
<div class="hero-banner">
    <div class="hero-title">📡 Weather Command</div>
    <div class="hero-subtitle">Real-time NWS Telemetry & Live Device Geolocation</div>
</div>
""", unsafe_allow_html=True)

# --- GEOLOCATION JAVASCRIPT BRIDGE ---
requests_comp.html("""
<script>
    function fetchLocation() {
        if (navigator.geolocation) {
            navigator.geolocation.getCurrentPosition(
                (position) => {
                    const lat = position.coords.latitude;
                    const lon = position.coords.longitude;
                    const urlParams = new URLSearchParams(window.parent.location.search);
                    if (urlParams.get('lat') != lat || urlParams.get('lon') != lon) {
                        urlParams.set('lat', lat);
                        urlParams.set('lon', lon);
                        window.parent.location.search = urlParams.toString();
                    }
                },
                (error) => {
                    console.warn("Geolocation access denied or failed: ", error.message);
                },
                { timeout: 10000, maximumAge: 60000, enableHighAccuracy: true }
            );
        }
    }
    fetchLocation();
</script>
""", height=0, width=0)

query_params = st.query_params
user_lat = query_params.get("lat")
user_lon = query_params.get("lon")

# If geolocation coordinates are not yet available in query parameters, prompt the user
if not user_lat or not user_lon:
    st.markdown("""
    <div class="command-card welcome-card" style="text-align: center; padding: 40px 20px;">
        <h3>📍 Location Access Required</h3>
        <p style="color: #a1a1aa; margin-top: 10px;">
            Please allow location access in your browser prompt to anchor your live position on the weather radar and load local NWS telemetry.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    with st.expander("📍 Or Enter Coordinates Manually"):
        with st.form("manual_coord_form"):
            man_lat = st.number_input("Latitude", value=42.82, format="%.4f")
            man_lon = st.number_input("Longitude", value=-95.805, format="%.4f")
            if st.form_submit_button("Load Location"):
                st.query_params["lat"] = str(man_lat)
                st.query_params["lon"] = str(man_lon)
                st.rerun()
    st.stop()

try:
    lat = float(user_lat)
    lon = float(user_lon)
except ValueError:
    st.error("Invalid coordinates provided in URL parameters.")
    st.stop()

@st.fragment(run_every=60)
def load_live_weather(lat, lon):
    headers = {
        "User-Agent": "WeatherCommandApp (wsnk836@gmail.com)",
        "Accept": "application/geo+json"
    }

    if "selected_forecast_day" not in st.session_state:
        st.session_state.selected_forecast_day = None

    st.subheader("⚠️ Active NWS Weather Alerts")
    try:
        alerts_url = f"https://api.weather.gov/alerts/active?point={lat},{lon}"
        alerts_response = requests.get(alerts_url, headers=headers, timeout=10).json()
        alerts = alerts_response.get("features", [])
        
        if len(alerts) > 0:
            for alert in alerts:
                props = alert.get("properties", {})
                event = props.get("event", "Weather Alert")
                headline = props.get("headline", "Severe weather alert issued.")
                description = props.get("description", "No description provided.")
                severity = props.get("severity", "Unknown")
                status_color = "#ef4444" if severity in ["Extreme", "Severe"] else "#f87171"
                
                st.markdown(f"""
                <div class="alert-card-severe" style="border-left-color: {status_color};">
                    <strong style="color: {status_color};">🚨 {event}</strong><br/>
                    <span style="color: #f4f4f5; font-size: 0.9rem; margin-top: 4px; display: block;">{headline}</span>
                </div>
                """, unsafe_allow_html=True)
                
                with st.expander("📄 View Full Warning Statement"):
                    st.write(description)
        else:
            st.markdown("""
            <div class="alert-card-clear">
                🟢 <strong>All Clear:</strong> No active warnings or advisories for your current location.
            </div>
            """, unsafe_allow_html=True)
            
    except Exception as e:
        st.error(f"Could not reach NWS alert servers: {e}")

    st.markdown("<div style='margin: 15px 0;'></div>", unsafe_allow_html=True)

    col_left, col_right = st.columns([1.1, 1], gap="large")

    with col_left:
        st.subheader("🌦️ Current Conditions")
        try:
            points_url = f"https://api.weather.gov/points/{lat},{lon}"
            points_response = requests.get(points_url, headers=headers, timeout=10).json()
            forecast_url = points_response["properties"]["forecast"]
            radar_station = points_response["properties"].get("radarStation", "KFSD")
            
            forecast_response = requests.get(forecast_url, headers=headers, timeout=10).json()
            periods = forecast_response["properties"]["periods"]
            
            current = periods[0]
            
            m1, m2, m3 = st.columns(3)
            with m1:
                st.metric("🌡️ Temp", f"{current['temperature']}°{current['temperatureUnit']}")
            with m2:
                st.metric("💨 Wind", f"{current['windSpeed']}")
            with m3:
                st.metric("☁️ Sky", current['shortForecast'])
            
            st.markdown(f"""
            <div style="background: #121316; border: 1px solid #27272a; border-radius: 10px; padding: 10px 14px; margin: 10px 0 15px 0; color: #d4d4d8; font-size: 0.88rem;">
                <strong>📋 Summary:</strong> {current['detailedForecast']}
            </div>
            """, unsafe_allow_html=True)
            
            daily_forecasts = []
            i = 0
            while i < len(periods):
                p = periods[i]
                if p['isDaytime']:
                    day_name = p['name']
                    day_detailed = p['detailedForecast']
                    high_temp = f"{p['temperature']}°{p['temperatureUnit']}"
                    wind_speed = p['windSpeed']
                    wind_dir = p.get('windDirection', '')
                    low_temp = "N/A"
                    night_detailed = ""
                    if i + 1 < len(periods) and not periods[i+1]['isDaytime']:
                        night_p = periods[i+1]
                        low_temp = f"{night_p['temperature']}°{night_p['temperatureUnit']}"
                        night_detailed = night_p['detailedForecast']
                        i += 1
                    daily_forecasts.append({"day": day_name, "high": high_temp, "low": low_temp, "detailed": day_detailed, "low_detailed": night_detailed, "wind_speed": wind_speed, "wind_dir": wind_dir})
                else:
                    night_name = p['name']
                    day_label = "Today" if night_name.lower() == "tonight" else night_name.replace(" Night", "").strip()
                    low_temp = f"{p['temperature']}°{p['temperatureUnit']}"
                    night_detailed = p['detailedForecast']
                    wind_speed = p['windSpeed']
                    wind_dir = p.get('windDirection', '')
                    high_temp = "N/A"
                    day_detailed = ""
                    if i + 1 < len(periods) and periods[i+1]['isDaytime']:
                        day_p = periods[i+1]
                        high_temp = f"{day_p['temperature']}°{day_p['temperatureUnit']}"
                        day_detailed = day_p['detailedForecast']
                        i += 1
                    daily_forecasts.append({"day": day_label, "high": high_temp, "low": low_temp, "detailed": day_detailed, "low_detailed": night_detailed, "wind_speed": wind_speed, "wind_dir": wind_dir})
                i += 1

            if not st.session_state.selected_forecast_day or st.session_state.selected_forecast_day not in [d['day'] for d in daily_forecasts]:
                st.session_state.selected_forecast_day = daily_forecasts[0]['day']

            st.subheader("📅 Outlook")
            tab3, tab7 = st.tabs(["3-Day", "7-Day"])
            
            with tab3:
                st.markdown("<div style='height: 4px;'></div>", unsafe_allow_html=True)
                days_to_show_3 = daily_forecasts[:3]
                cols3 = st.columns(len(days_to_show_3))
                for idx, d_item in enumerate(days_to_show_3):
                    with cols3[idx]:
                        is_selected = (d_item['day'] == st.session_state.selected_forecast_day)
                        btn_label = f"📍 {d_item['day']}" if is_selected else d_item['day']
                        if st.button(btn_label, key=f"btn_3d_{idx}_{d_item['day']}", use_container_width=True):
                            st.session_state.selected_forecast_day = d_item['day']
                            st.rerun()

            with tab7:
                st.markdown("<div style='height: 4px;'></div>", unsafe_allow_html=True)
                days_to_show_7 = daily_forecasts[:7]
                cols7 = st.columns(len(days_to_show_7))
                for idx, d_item in enumerate(days_to_show_7):
                    with cols7[idx]:
                        is_selected = (d_item['day'] == st.session_state.selected_forecast_day)
                        btn_label = f"📍 {d_item['day']}" if is_selected else d_item['day']
                        if st.button(btn_label, key=f"btn_7d_{idx}_{d_item['day']}", use_container_width=True):
                            st.session_state.selected_forecast_day = d_item['day']
                            st.rerun()

            selected_record = next((d for d in daily_forecasts if d['day'] == st.session_state.selected_forecast_day), daily_forecasts[0])
            display_high = selected_record['high'] if selected_record['high'] != "N/A" else f"{current['temperature']}°{current['temperatureUnit']}"
            display_low = selected_record['low'] if selected_record['low'] != "N/A" else f"{current['temperature']}°{current['temperatureUnit']}"

            st.markdown(f"""
            <div style="background: #18191f; border: 1px solid #27272a; border-left: 3px solid #ef4444; border-radius: 10px; padding: 18px 20px; margin-top: 15px;">
                <div style="font-weight: 700; color: #f87171; font-size: 1.05rem; margin-bottom: 10px;">
                    🏛️ Forecast Report • {selected_record['day']}
                </div>
                {f'<div style="font-size: 0.92rem; color: #f4f4f5; margin-bottom: 8px;"><strong>Daytime:</strong> {selected_record["detailed"]}</div>' if selected_record['detailed'] else ''}
                {f'<div style="font-size: 0.92rem; color: #d4d4d8; margin-bottom: 12px;"><strong>Nighttime:</strong> {selected_record["low_detailed"]}</div>' if selected_record['low_detailed'] else ''}
                <div style="display: flex; flex-wrap: wrap; gap: 18px; margin-top: 12px; font-size: 0.85rem; color: #a1a1aa; border-top: 1px solid #27272a; padding-top: 10px;">
                    <div>🌡️ High: <strong style="color: #fafafa;">{display_high}</strong></div>
                    <div>🌡️ Low: <strong style="color: #fafafa;">{display_low}</strong></div>
                    <div>💨 Wind: <strong style="color: #fafafa;">{selected_record['wind_speed']} ({selected_record['wind_dir']})</strong></div>
                    <div>📡 Station: <strong style="color: #fafafa;">{radar_station}</strong></div>
                </div>
            </div>
            """, unsafe_allow_html=True)

        except Exception as e:
            st.error(f"Could not load NWS forecast telemetry: {e}")

        st.markdown("<div style='margin: 15px 0;'></div>", unsafe_allow_html=True)

        st.subheader(f"📡 Live Doppler Radar ({radar_station})")
        cst_time = datetime.now(ZoneInfo("America/Chicago")).strftime('%I:%M:%S %p %Z')
        st.caption(f"🔄 Sync active • {cst_time} • 📍 Device location anchored to ({lat:.4f}, {lon:.4f})")
        
        radar_url = f"https://radar.weather.gov/ridge/standard/{radar_station}_loop.gif?t={int(time.time())}"
        
        st.markdown(f"""
        <div class="radar-wrapper">
            <img src="{radar_url}" class="radar-img" alt="Radar Loop">
            <div class="user-pin-container">
                <div class="user-dot"></div>
                <div class="user-label">Your Device Location</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    with col_right:
        st.markdown("""
        <div class="command-card welcome-card">
            👋 <strong>Device Location Locked.</strong> This dashboard uses your device's live browser GPS telemetry to pull regional NWS radar loops and active weather alerts.
        </div>
        """, unsafe_allow_html=True)

        st.subheader("📍 Location Override")
        with st.form("coord_form"):
            st.write("Manually adjust coordinates if needed:")
            manual_lat = st.number_input("Latitude", value=lat, format="%.4f")
            manual_lon = st.number_input("Longitude", value=lon, format="%.4f")
            submitted = st.form_submit_button("Update Location")
            if submitted:
                st.query_params["lat"] = str(manual_lat)
                st.query_params["lon"] = str(manual_lon)
                st.rerun()

load_live_weather(lat, lon)
