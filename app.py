import streamlit as st
import streamlit.components.v1 as components
import requests
import time
from datetime import datetime
from zoneinfo import ZoneInfo

# Page Configuration
st.set_page_config(
    page_title="Marcus Weather Command", 
    page_icon="📡",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- AUTOMATIC MOBILE & BROWSER NAMING ---
components.html("""
<script>
    window.parent.document.title = "Marcus Weather Command";
    
    let metaApple = window.parent.document.createElement('meta');
    metaApple.name = "apple-mobile-web-app-title";
    metaApple.content = "Marcus Weather";
    window.parent.document.head.appendChild(metaApple);

    let metaApp = window.parent.document.createElement('meta');
    metaApp.name = "application-name";
    metaApp.content = "Marcus Weather";
    window.parent.document.head.appendChild(metaApp);
</script>
""", height=0, width=0)

# --- REDESIGNED TACTICAL CRIMSON & CARBON CSS ---
st.markdown("""
<style>
    /* Global App Styling - Tactical Carbon & Crimson Alert Palette */
    .stApp {
        background-color: #0c0d10;
        color: #f4f4f5;
        font-family: system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
    }

    /* Hero Header Banner */
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

    /* Quick Access Nav Bar */
    .quick-nav-container {
        display: flex;
        gap: 8px;
        background: #121316;
        border: 1px solid #27272a;
        border-radius: 12px;
        padding: 10px;
        margin-bottom: 20px;
        overflow-x: auto;
    }
    .quick-nav-btn {
        background: #18191f;
        border: 1px solid #27272a;
        color: #d4d4d8;
        padding: 8px 16px;
        border-radius: 8px;
        font-size: 0.85rem;
        font-weight: 600;
        cursor: pointer;
        white-space: nowrap;
        transition: all 0.2s ease;
    }
    .quick-nav-btn:hover {
        background: #ef4444;
        color: #0c0d10;
        border-color: #ef4444;
    }

    /* Command Grid Cards */
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

    .welcome-card {
        border-left: 4px solid #ef4444;
    }

    .repeater-card {
        background: rgba(239, 68, 68, 0.05);
        border: 1px solid rgba(239, 68, 68, 0.2);
        border-left: 4px solid #f87171;
        color: #fee2e2;
    }

    .install-card {
        border-left: 4px solid #38bdf8;
        color: #d4d4d8;
        font-size: 0.9rem;
    }

    /* Alert Banners */
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

    /* Metrics Styling */
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

    /* Container Cards for Forecasts */
    [data-testid="stVerticalBlockBorderWrapper"] {
        background: #121316 !important;
        border: 1px solid #27272a !important;
        border-radius: 12px !important;
        transition: all 0.2s ease-in-out;
    }

    [data-testid="stVerticalBlockBorderWrapper"]:hover {
        border-color: #ef4444 !important;
        transform: translateY(-2px);
    }

    /* Forecast Icons Styling - Expanded & Fully Expanded to Column Width */
    .digital-icon-container {
        display: flex;
        justify-content: center;
        align-items: center;
        margin: 10px 0;
        width: 100%;
    }
    
    .digital-icon {
        width: 100%;
        max-width: 140px;
        height: auto;
        aspect-ratio: 1 / 1;
        border-radius: 12px;
        background: radial-gradient(circle, #22242c 0%, #121316 100%);
        border: 1px solid #3f3f46;
        padding: 10px;
        object-fit: contain;
        display: block;
        box-shadow: 0 8px 20px rgba(0, 0, 0, 0.6);
        transition: transform 0.2s ease, border-color 0.2s ease;
    }

    .digital-icon:hover {
        transform: scale(1.05);
        border-color: #ef4444;
    }

    /* Tabs UI Polish */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background-color: transparent;
    }

    .stTabs [data-baseweb="tab"] {
        border-radius: 8px;
        padding: 6px 16px;
        background-color: #121316;
        border: 1px solid #27272a;
        color: #a1a1aa;
        font-weight: 600;
    }

    .stTabs [aria-selected="true"] {
        background: #ef4444 !important;
        color: #0c0d10 !important;
        border-color: #ef4444 !important;
        font-weight: 700 !important;
    }

    @media (max-width: 768px) {
        .block-container {
            padding: 1rem 0.75rem !important;
        }
        .hero-title {
            font-size: 1.4rem;
        }
        .digital-icon {
            max-width: 100px;
        }
    }
</style>
""", unsafe_allow_html=True)

# --- MOBILE KEEP-ALIVE & AUTO-RECONNECT WATCHDOG ---
components.html("""
<script>
    document.addEventListener("visibilitychange", function() {
        if (document.visibilityState === "visible") {
            window.parent.location.reload();
        }
    });
    setTimeout(function() {
        window.parent.location.reload();
    }, 600000);
</script>
""", height=0, width=0)

# --- HERO HEADER ---
st.markdown("""
<div class="hero-banner">
    <div class="hero-title">📡 Marcus Weather Command</div>
    <div class="hero-subtitle">Real-time NWS Telemetry & Regional GMRS Radio Operations • Cherokee County, IA</div>
</div>
""", unsafe_allow_html=True)

# --- QUICK ACCESS AUTO-SCROLL NAV BAR ---
components.html("""
<div class="quick-nav-container">
    <button class="quick-nav-btn" onclick="scrollToSec('alerts-sec')">⚠️ Alerts</button>
    <button class="quick-nav-btn" onclick="scrollToSec('conditions-sec')">🌦️ Conditions</button>
    <button class="quick-nav-btn" onclick="scrollToSec('radar-sec')">📡 Radar</button>
    <button class="quick-nav-btn" onclick="scrollToSec('news-sec')">📻 Community News</button>
    <button class="quick-nav-btn" onclick="scrollToSec('install-sec')">📲 Install</button>
    <button class="quick-nav-btn" onclick="scrollToSec('feedback-sec')">💬 Feedback</button>
</div>
<script>
    function scrollToSec(id) {
        const el = window.parent.document.getElementById(id);
        if (el) {
            el.scrollIntoView({ behavior: 'smooth', block: 'start' });
        }
    }
</script>
""", height=60, scrolling=False)


def get_enhanced_icon_url(raw_url: str) -> str:
    """Upgrades NWS icon URL resolution to large format for maximum clarity."""
    if not raw_url:
        return ""
    if "?size=" in raw_url:
        return raw_url.split("?")[0] + "?size=large"
    elif "?" in raw_url:
        return raw_url + "&size=large"
    return raw_url + "?size=large"


# ==========================================
# --- CONTINUOUSLY REFRESHING FRAGMENT ---
# ==========================================
@st.fragment(run_every=60)
def load_live_weather():
    headers = {
        "User-Agent": "MarcusWeatherApp (wsnk836@gmail.com)",
        "Accept": "application/geo+json"
    }

    # --- ACTIVE SEVERE WEATHER ALERTS ---
    st.markdown('<div id="alerts-sec"></div>', unsafe_allow_html=True)
    st.subheader("⚠️ Active NWS Weather Alerts")
    try:
        alerts_url = "https://api.weather.gov/alerts/active?point=42.8242,-95.7994"
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
                    <span style="color: #f4f4f5
