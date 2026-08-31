from datetime import datetime, timedelta
import time
from zoneinfo import ZoneInfo
import requests
import streamlit as st
import streamlit.components.v1 as components

# Page Configuration
st.set_page_config(
    page_title="Marcus Weather Command",
    page_icon="📡",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# --- BROWSER LOCALSTORAGE BRIDGE (PUSH NOTIFICATIONS REMOVED) ---
localStorage_sync_code = """
<script>
    const urlParams = new URLSearchParams(window.location.search);
    const hasParams = urlParams.has('lat');

    if (hasParams) {
        if (urlParams.has('lat')) localStorage.setItem('nws_lat', urlParams.get('lat'));
        if (urlParams.has('lon')) localStorage.setItem('nws_lon', urlParams.get('lon'));
        if (urlParams.has('loc_name')) localStorage.setItem('nws_loc_name', urlParams.get('loc_name'));
        sessionStorage.setItem('nws_synced', 'true');
    } else {
        const alreadySynced = sessionStorage.getItem('nws_synced');
        
        if (!alreadySynced) {
            const savedLat = localStorage.getItem('nws_lat');
            const savedLon = localStorage.getItem('nws_lon');
            const savedLoc = localStorage.getItem('nws_loc_name');

            if (savedLat) {
                const lat = savedLat || '42.8242';
                const lon = savedLon || '-95.7994';
                const loc = savedLoc || 'Marcus, IA';
                
                sessionStorage.setItem('nws_synced', 'true');
                
                const newUrl = window.location.pathname + `?lat=${lat}&lon=${lon}&loc_name=${encodeURIComponent(loc)}`;
                
                if (window.top && window.top.history && window.top.history.replaceState) {
                    window.top.history.replaceState(null, '', newUrl);
                    window.top.location.href = newUrl;
                }
            } else {
                sessionStorage.setItem('nws_synced', 'true');
            }
        }
    }
</script>
"""
components.html(localStorage_sync_code, height=0)

# --- TACTICAL CRIMSON & CARBON CSS ---
st.markdown(
    """
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
    .repeater-card {
        background: rgba(239, 68, 68, 0.05);
        border: 1px solid rgba(239, 68, 68, 0.2);
        border-left: 4px solid #f87171;
        color: #fee2e2;
    }
    .install-card { border-left: 4px solid #38bdf8; color: #d4d4d8; font-size: 0.9rem; }
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
    @media (max-width: 768px) {
        .block-container { padding: 1rem 0.75rem !important; }
        .hero-title { font-size: 1.4rem; }
    }
</style>
""",
    unsafe_allow_html=True,
)

# --- RESOLVE & PERSIST QUERY PARAMS ---
query_params = st.query_params
default_lat = "42.8242"
default_lon = "-95.7994"

lat_str = query_params.get("lat", default_lat)
lon_str = query_params.get("lon", default_lon)
location_name = query_params.get("loc_name", "Marcus, IA")

try:
  ACTIVE_LAT = round(float(lat_str), 4)
  ACTIVE_LON = round(float(lon_str), 4)
except ValueError:
  ACTIVE_LAT = float(default_lat)
  ACTIVE_LON = float(default_lon)
  location_name = "Marcus, IA"

# --- HERO HEADER ---
st.markdown(
    """
<div class="hero-banner">
    <div class="hero-title">📡 Marcus Weather Command</div>
    <div class="hero-subtitle">Real-time NWS Telemetry & Regional Operations</div>
</div>
""",
    unsafe_allow_html=True,
)

# ==========================================
# --- ZIP CODE & LOCATION SELECTOR PANEL ---
# ==========================================
with st.expander("📍 Change Location (Enter ZIP Code or City Name)", expanded=False):
  with st.form("zip_search_form"):
    loc_input = st.text_input(
        "ZIP Code or City",
        placeholder="e.g. 51035 or Cherokee, IA",
        value="" if location_name == "Marcus, IA" else location_name,
    )
    submitted = st.form_submit_button("Update Location Grid")

    if submitted and loc_input.strip():
      try:
        geo_url = f"https://nominatim.openstreetmap.org/search?q={requests.utils.quote(loc_input)}&format=json&countrycodes=us&limit=1"
        geo_resp = requests.get(
            geo_url, headers={"User-Agent": "MarcusWeatherApp"}, timeout=5
        ).json()

        if geo_resp:
          new_lat = geo_resp[0]["lat"]
          new_lon = geo_resp[0]["lon"]
          new_name = geo_resp[0].get("display_name", loc_input).split(",")[0]

          st.query_params["lat"] = new_lat
          st.query_params["lon"] = new_lon
          st.query_params["loc_name"] = new_name

          update_js = f"""
                    <script>
                        localStorage.setItem('nws_lat', '{new_lat}');
                        localStorage.setItem('nws_lon', '{new_lon}');
                        localStorage.setItem('nws_loc_name', '{new_name}');
                        sessionStorage.setItem('nws_synced', 'true');
                    </script>
                    """
          components.html(update_js, height=0)

          st.success(f"Location locked to: {geo_resp[0].get('display_name')}")
          time.sleep(0.5)
          st.rerun()
        else:
          st.error(
              "Location not found. Please try a valid US ZIP code or city name."
          )
      except Exception as e:
        st.error(f"Geocoding connection error: {e}")


# ==========================================
# --- CONTINUOUSLY REFRESHING FRAGMENT ---
