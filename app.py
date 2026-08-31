import streamlit as st
import streamlit.components.v1 as components
import requests
import time

# Page Configuration
st.set_page_config(
    page_title="Marcus Weather", 
    page_icon="📡",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- AUTOMATIC MOBILE & BROWSER NAMING ---
components.html("""
<script>
    window.parent.document.title = "Marcus Weather";
    
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

# --- MODERN WEATHER CONSOLE CUSTOM CSS ---
st.markdown("""
<style>
    /* Dark console background theme & global font adjustments */
    .stApp {
        background-color: #0e1117;
        color: #e0e6ed;
    }

    /* Custom Header Banner */
    .hero-banner {
        background: linear-gradient(135deg, #1e2640 0%, #0f172a 100%);
        border: 1px solid #2e3a59;
        border-radius: 16px;
        padding: 20px 24px;
        margin-bottom: 20px;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.4);
    }
    
    .hero-title {
        font-size: 2rem;
        font-weight: 800;
        color: #38bdf8;
        margin: 0;
        display: flex;
        align-items: center;
        gap: 10px;
    }

    .hero-subtitle {
        color: #94a3b8;
        font-size: 0.95rem;
        margin-top: 4px;
    }

    /* Welcome Message Styling */
    .welcome-card {
        background-color: #1e293b;
        border: 1px solid #334155;
        border-left: 5px solid #38bdf8;
        border-radius: 10px;
        padding: 16px 20px;
        margin-bottom: 20px;
        color: #f1f5f9;
        font-size: 1.05rem;
        line-height: 1.5;
    }

    /* Radio Repeater Box */
    .repeater-card {
        background: rgba(14, 165, 233, 0.1);
        border: 1px solid rgba(56, 189, 248, 0.3);
        border-left: 5px solid #0284c7;
        border-radius: 10px;
        padding: 12px 18px;
        margin-bottom: 24px;
        color: #e0f2fe;
    }

    /* Weather Alert Styling */
    .alert-card-severe {
        background: rgba(239, 68, 68, 0.12);
        border: 1px solid rgba(239, 68, 68, 0.4);
        border-left: 5px solid #ef4444;
        border-radius: 10px;
        padding: 14px 18px;
        margin-bottom: 15px;
    }

    .alert-card-clear {
        background: rgba(34, 197, 94, 0.1);
        border: 1px solid rgba(34, 197, 94, 0.3);
        border-left: 5px solid #22c55e;
        border-radius: 10px;
        padding: 12px 18px;
        margin-bottom: 20px;
        color: #dcfce7;
    }

    /* Metric Display Cards */
    [data-testid="stMetric"] {
        background-color: #1e293b;
        border: 1px solid #334155;
        border-radius: 12px;
        padding: 12px 16px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.2);
    }

    /* Forecast Container Cards */
    [data-testid="stVerticalBlockBorderWrapper"] {
        background-color: #1a2234 !important;
        border: 1px solid #2e3a59 !important;
        border-radius: 14px !important;
        transition: all 0.25s ease-in-out;
    }

    [data-testid="stVerticalBlockBorderWrapper"]:hover {
        border-color: #38bdf8 !important;
        transform: translateY(-2px);
        box-shadow: 0 6px 16px rgba(56, 189, 248, 0.15);
    }

    /* Radar Frame Styling */
    .radar-container {
        border: 1px solid #334155;
        border-radius: 16px;
        overflow: hidden;
        background-color: #111827;
        padding: 10px;
    }

    /* Tab bar styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
    }

    .stTabs [data-baseweb="tab"] {
        border-radius: 8px;
        padding: 8px 16px;
        background-color: #1e293b;
        color: #94a3b8;
    }

    .stTabs [aria-selected="true"] {
        background-color: #0284c7 !important;
        color: #ffffff !important;
    }

    /* Mobile view tweaks */
    @media (max-width: 768px) {
        .block-container {
            padding: 0.75rem 0.5rem !important;
        }
        [data-testid="column"] {
            min-width: 140px !important;
            margin-bottom: 0.5rem;
        }
        .hero-title {
            font-size: 1.4rem;
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

# NWS API Headers
headers = {
    "User-Agent": "MarcusWeatherDashboard/1.0 (contact@example.com)",
    "Cache-Control": "no-cache, no-store, must-revalidate",
    "Pragma": "no-cache"
}

# --- HERO HEADER ---
st.markdown("""
<div class="hero-banner">
    <div class="hero-title">📡 Marcus Weather Command</div>
    <div class="hero-subtitle">Live NWS Data & Regional Radio Operations • Cherokee County, IA</div>
</div>
""", unsafe_allow_html=True)

# --- WELCOME MESSAGE ---
st.markdown("""
<div class="welcome-card">
    👋 <strong>Welcome to the Marcus Weather Command!</strong><br> 
    This is your centralized dashboard for real-time local weather updates, and live doplar radar. Keep this app open for continuous severe weather monitoring. Stay safe and informed!
</div>
""", unsafe_allow_html=True)

# --- REPEATER ANNOUNCEMENT BANNER ---
st.markdown("""
<div class="repeater-card">
    <strong>📻 GMRS REPEATER GOING ACTIVE 12/01/2026:</strong> Tune into <strong>Channel 22</strong> (462.725 MHz) • <strong>PL Tone 123.0 Hz</strong> — Open for local use!
</div>
""", unsafe_allow_html=True)


# ==========================================
# --- CONTINUOUSLY REFRESHING FRAGMENT ---
# ==========================================
@st.fragment(run_every=60)
def load_live_weather():

    # --- ACTIVE SEVERE WEATHER ALERTS ---
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
                
                status_color = "#ef4444" if severity in ["Extreme", "Severe"] else "#f59e0b"
                
                st.markdown(f"""
                <div class="alert-card-severe" style="border-left-color: {status_color};">
                    <strong style="color: {status_color}; font-size: 1.1rem;">🚨 {event}</strong><br/>
                    <span style="color: #f1f5f9;">{headline}</span>
                </div>
                """, unsafe_allow_html=True)
                
                with st.expander("📄 Read Official NWS Warning Statement"):
                    st.write(description)
        else:
            st.markdown("""
            <div class="alert-card-clear">
                🟢 <strong>All Clear:</strong> No active severe weather warnings or watches for Marcus, IA.
            </div>
            """, unsafe_allow_html=True)
            
    except Exception as e:
        st.error("Could not fetch active NWS alerts data.")

    st.markdown("---")

    # --- CURRENT CONDITIONS & FORECAST ---
    st.subheader("🌦️ Current Conditions & Local Forecast")
    try:
        points_url = "https://api.weather.gov/points/42.8242,-95.7994"
        points_response = requests.get(points_url, headers=headers, timeout=10).json()
        forecast_url = points_response["properties"]["forecast"]
        
        forecast_response = requests.get(forecast_url, headers=headers, timeout=10).json()
        periods = forecast_response["properties"]["periods"]
        
        current = periods[0]
        
        # Current Metric Row
        col1, col2, col3 = st.columns(3)
        col1.metric("🌡️ Temperature", f"{current['temperature']} °{current['temperatureUnit']}")
        col2.metric("💨 Wind", f"{current['windSpeed']} {current['windDirection']}")
        col3.metric("☁️ Conditions", current['shortForecast'])
        
        st.info(f"**Detailed Summary:** {current['detailedForecast']}")
        
        # --- PROCESS PERIODS INTO DAILY CARDS ---
        daily_forecasts = []
        i = 0
        while i < len(periods):
            p = periods[i]
            if p['isDaytime']:
                day_name = p['name']
                high = f"{p['temperature']}°{p['temperatureUnit']}"
                forecast = p['shortForecast']
                icon = p.get('icon', '')
                
                low = "N/A"
                if i + 1 < len(periods) and not periods[i+1]['isDaytime']:
                    low = f"{periods[i+1]['temperature']}°{periods[i+1]['temperatureUnit']}"
                    i += 1  
                
                daily_forecasts.append({
                    "day": day_name, "high": high, "low": low,
                    "forecast": forecast, "icon": icon
                })
            else:
                day_name = p['name']
                low = f"{p['temperature']}°{p['temperatureUnit']}"
                forecast = p['shortForecast']
                icon = p.get('icon', '')
                daily_forecasts.append({
                    "day": day_name, "high": "N/A", "low": low,
                    "forecast": forecast, "icon": icon
                })
            i += 1

        # --- EXTENDED FORECAST TABS ---
        st.write("")
        tab5, tab7 = st.tabs(["📅 5-Day Outlook", "📅 7-Day Outlook"])
        
        with tab5:
            days_to_show = daily_forecasts[:5]
            cols5 = st.columns(len(days_to_show))
            for idx, day_data in enumerate(days_to_show):
                with cols5[idx]:
                    with st.container(border=True):
                        st.markdown(f"#### {day_data['day']}")
                        if day_data['icon']:
                            st.image(day_data['icon'], width=52)
                        st.markdown(f"🔥 **High:** {day_data['high']}")
                        st.markdown(f"❄️ **Low:** {day_data['low']}")
                        st.caption(day_data['forecast'])

        with tab7:
            days_to_show = daily_forecasts[:7]
            cols7 = st.columns(len(days_to_show))
            for idx, day_data in enumerate(days_to_show):
                with cols7[idx]:
                    with st.container(border=True):
                        st.markdown(f"#### {day_data['day']}")
                        if day_data['icon']:
                            st.image(day_data['icon'], width=52)
                        st.markdown(f"🔥 **High:** {day_data['high']}")
                        st.markdown(f"❄️ **Low:** {day_data['low']}")
                        st.caption(day_data['forecast'])

    except Exception as e:
        st.error(f"Could not load NWS forecast data: {e}")

    st.markdown("---")

    # --- LIVE RADAR LOOP ---
    st.subheader("📡 Live Doppler Radar (KFSD - Sioux Falls)")
    current_time = time.strftime('%I:%M:%S %p')
    st.caption(f"🔄 Live auto-updating feed • Last synced at {current_time}")

    # Unique timestamp parameter forces browser to download latest animated radar frame
    radar_url = f"https://radar.weather.gov/ridge/standard/KFSD_loop.gif?t={int(time.time())}"
    
    # Styled Radar Card Container
    with st.container(border=True):
        st.image(radar_url, use_container_width=True)


# Execute auto-refresh fragment
load_live_weather()

# ==========================================
# --- GITHUB REPOSITORY LINK FOOTER ---
# ==========================================
st.markdown("""
<div style="text-align: center; color: #94a3b8; font-size: 0.95rem; padding-top: 30px; padding-bottom: 20px;">
    <hr style="border: none; border-top: 1px solid #334155; margin-bottom: 20px;">
    💻 View the source code or contribute on 
    <a href="https://github.com/wsnk836/marcus-weather-app" target="_blank" style="color: #38bdf8; text-decoration: none;
