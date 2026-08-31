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

# --- REDESIGNED TACTICAL AMBER & CARBON CSS ---
st.markdown("""
<style>
    /* Global App Styling - Deep Carbon & Amber Phosphor Vibe */
    .stApp {
        background-color: #0c0d10;
        color: #f4f4f5;
        font-family: system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
    }

    /* Hero Header Banner */
    .hero-banner {
        background: linear-gradient(145deg, #18191f 0%, #0e0f12 100%);
        border: 1px solid #27272a;
        border-top: 3px solid #f59e0b;
        border-radius: 14px;
        padding: 26px 30px;
        margin-bottom: 24px;
        box-shadow: 0 12px 30px -10px rgba(0, 0, 0, 0.7);
    }
    
    .hero-title {
        font-size: 2.2rem;
        font-weight: 800;
        color: #fbbf24;
        margin: 0;
        display: flex;
        align-items: center;
        gap: 12px;
        letter-spacing: -0.02em;
    }

    .hero-subtitle {
        color: #a1a1aa;
        font-size: 0.98rem;
        margin-top: 8px;
        letter-spacing: 0.04em;
        text-transform: uppercase;
        font-weight: 500;
    }

    /* Welcome & Notification Cards */
    .welcome-card {
        background: rgba(24, 25, 31, 0.85);
        border: 1px solid #27272a;
        border-left: 4px solid #f59e0b;
        border-radius: 10px;
        padding: 18px 22px;
        margin-bottom: 20px;
        color: #e4e4e7;
        font-size: 1.02rem;
        line-height: 1.6;
    }

    .repeater-card {
        background: rgba(245, 158, 11, 0.06);
        border: 1px solid rgba(245, 158, 11, 0.2);
        border-left: 4px solid #fbbf24;
        border-radius: 10px;
        padding: 16px 20px;
        margin-bottom: 16px;
        color: #fef3c7;
        font-size: 0.95rem;
    }

    .install-card {
        background: rgba(24, 25, 31, 0.6);
        border: 1px solid #27272a;
        border-left: 4px solid #38bdf8;
        border-radius: 10px;
        padding: 16px 20px;
        margin-bottom: 28px;
        color: #d4d4d8;
        font-size: 0.93rem;
        line-height: 1.5;
    }

    /* Alert Banners */
    .alert-card-severe {
        background: rgba(239, 68, 68, 0.12);
        border: 1px solid rgba(239, 68, 68, 0.3);
        border-left: 4px solid #ef4444;
        border-radius: 10px;
        padding: 16px 20px;
        margin-bottom: 16px;
    }

    .alert-card-clear {
        background: rgba(16, 185, 129, 0.08);
        border: 1px solid rgba(16, 185, 129, 0.25);
        border-left: 4px solid #10b981;
        border-radius: 10px;
        padding: 14px 20px;
        margin-bottom: 20px;
        color: #d1fae5;
    }

    /* Metrics Styling */
    [data-testid="stMetric"] {
        background: #121316;
        border: 1px solid #27272a;
        border-radius: 12px;
        padding: 18px 22px;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.3);
    }
    [data-testid="stMetricLabel"] {
        font-size: 0.88rem !important;
        color: #a1a1aa !important;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }
    [data-testid="stMetricValue"] {
        font-size: 1.8rem !important;
        font-weight: 700 !important;
        color: #fafafa !important;
    }

    /* Container Cards for Forecasts */
    [data-testid="stVerticalBlockBorderWrapper"] {
        background: #121316 !important;
        border: 1px solid #27272a !important;
        border-radius: 14px !important;
        transition: all 0.2s ease-in-out;
    }

    [data-testid="stVerticalBlockBorderWrapper"]:hover {
        border-color: #f59e0b !important;
        transform: translateY(-3px);
        box-shadow: 0 10px 25px -5px rgba(245, 158, 11, 0.15);
    }

    /* Forecast Icons Styling */
    .digital-icon-container {
        display: flex;
        justify-content: center;
        align-items: center;
        margin: 10px 0;
    }
    
    .digital-icon {
        width: 60px;
        height: 60px;
        border-radius: 12px;
        background: #18191f;
        border: 1px solid #27272a;
        padding: 8px;
        object-fit: contain;
        display: block;
    }

    /* Tabs UI Polish */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background-color: transparent;
    }

    .stTabs [data-baseweb="tab"] {
        border-radius: 8px;
        padding: 8px 20px;
        background-color: #121316;
        border: 1px solid #27272a;
        color: #a1a1aa;
        font-weight: 600;
    }

    .stTabs [aria-selected="true"] {
        background: #f59e0b !important;
        color: #0c0d10 !important;
        border-color: #f59e0b !important;
        font-weight: 700 !important;
    }

    /* Responsive adjustments */
    @media (max-width: 768px) {
        .block-container {
            padding: 1rem 0.75rem !important;
        }
        .hero-title {
            font-size: 1.5rem;
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

# --- WELCOME MESSAGE ---
st.markdown("""
<div class="welcome-card">
    👋 <strong>Welcome to Marcus Weather Command.</strong> Your centralized operational dashboard for live local meteorological telemetry, high-definition Doppler radar loops, and emergency alerts. Keep this app active for continuous monitoring.
</div>
""", unsafe_allow_html=True)

# --- REPEATER ANNOUNCEMENT BANNER ---
st.markdown("""
<div class="repeater-card">
    <strong>📻 GMRS REPEATER GOING ACTIVE — 12/01/2026:</strong> Tune your mobile/base stations to <strong>Channel 22</strong> (462.725 MHz) • <strong>PL Tone 123.0 Hz</strong>. Fully open for community use!
</div>
""", unsafe_allow_html=True)

# --- INSTALLATION INSTRUCTIONS ---
st.markdown("""
<div class="install-card">
    📲 <strong>Add & Rename to Home Screen:</strong> Install this dashboard on your mobile device for quick, app-like access:<br/>
    • <strong>iOS (Safari):</strong> Tap the <strong>Share</strong> button at the bottom of the screen, select <strong>"Add to Home Screen"</strong>, rename it to <strong>"Marcus Weather"</strong>, and tap <strong>Add</strong>.<br/>
    • <strong>Android (Chrome):</strong> Tap the <strong>Menu</strong> (three vertical dots) in the top right, select <strong>"Add to Home screen"</strong> (or "Install app"), rename the shortcut to <strong>"Marcus Weather"</strong>, and confirm.
</div>
""", unsafe_allow_html=True)


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
                    <span style="color: #f4f4f5; margin-top: 4px; display: block;">{headline}</span>
                </div>
                """, unsafe_allow_html=True)
                
                with st.expander("📄 View Full Official NWS Warning Statement"):
                    st.write(description)
        else:
            st.markdown("""
            <div class="alert-card-clear">
                🟢 <strong>All Clear:</strong> No active severe weather warnings or advisories issued for Marcus, IA.
            </div>
            """, unsafe_allow_html=True)
            
    except Exception as e:
        st.error(f"Could not reach NWS alert servers: {e}")

    st.markdown("<div style='margin: 25px 0;'></div>", unsafe_allow_html=True)

    # --- CURRENT CONDITIONS & FORECAST ---
    st.subheader("🌦️ Current Conditions & Outlook")
    try:
        points_url = "https://api.weather.gov/points/42.8242,-95.7994"
        points_response = requests.get(points_url, headers=headers, timeout=10).json()
        forecast_url = points_response["properties"]["forecast"]
        
        forecast_response = requests.get(forecast_url, headers=headers, timeout=10).json()
        periods = forecast_response["properties"]["periods"]
        
        current = periods[0]
        
        # Current Metric Row
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("🌡️ Temperature", f"{current['temperature']}°{current['temperatureUnit']}")
        with col2:
            st.metric("💨 Wind Dynamics", f"{current['windSpeed']} {current['windDirection']}")
        with col3:
            st.metric("☁️ Sky State", current['shortForecast'])
        
        st.markdown(f"""
        <div style="background: #121316; border: 1px solid #27272a; border-radius: 10px; padding: 14px 18px; margin: 16px 0 24px 0; color: #d4d4d8; font-size: 0.98rem;">
            <strong>📋 Detailed Summary:</strong> {current['detailedForecast']}
        </div>
        """, unsafe_allow_html=True)
        
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

        # --- EXTENDED FORECAST TABS (3-Day & 7-Day) ---
        tab3, tab7 = st.tabs(["📅 3-Day Outlook", "📅 7-Day Outlook"])
        
        with tab3:
            st.markdown("<div style='height: 8px;'></div>", unsafe_allow_html=True)
            days_to_show = daily_forecasts[:3]
            cols3 = st.columns(len(days_to_show))
            for idx, day_data in enumerate(days_to_show):
                with cols3[idx]:
                    with st.container(border=True):
                        st.markdown(f"#### {day_data['day']}")
                        if day_data['icon']:
                            st.markdown(f"""
                            <div class="digital-icon-container">
                                <img src="{day_data['icon']}" class="digital-icon" alt="weather icon" />
                            </div>
                            """, unsafe_allow_html=True)
                        st.markdown(f"🔥 **High:** {day_data['high']}")
                        st.markdown(f"❄️ **Low:** {day_data['low']}")
                        st.caption(day_data['forecast'])

        with tab7:
            st.markdown("<div style='height: 8px;'></div>", unsafe_allow_html=True)
            days_to_show = daily_forecasts[:7]
            cols7 = st.columns(len(days_to_show))
            for idx, day_data in enumerate(days_to_show):
                with cols7[idx]:
                    with st.container(border=True):
                        st.markdown(f"#### {day_data['day']}")
                        if day_data['icon']:
                            st.markdown(f"""
                            <div class="digital-icon-container">
                                <img src="{day_data['icon']}" class="digital-icon" alt="weather icon" />
                            </div>
                            """, unsafe_allow_html=True)
                        st.markdown(f"🔥 **High:** {day_data['high']}")
                        st.markdown(f"❄️ **Low:** {day_data['low']}")
                        st.caption(day_data['forecast'])

    except Exception as e:
        st.error(f"Could not load NWS forecast telemetry: {e}")

    st.markdown("<div style='margin: 30px 0;'></div>", unsafe_allow_html=True)

    # --- LIVE RADAR LOOP ---
    st.subheader("📡 Live Doppler Radar (KFSD - Sioux Falls)")
    
    # Convert current time to Central Time (CST/CDT)
    cst_time = datetime.now(ZoneInfo("America/Chicago")).strftime('%I:%M:%S %p %Z')
    st.caption(f"🔄 Auto-syncing live feed • Last updated at {cst_time}")

    radar_url = f"https://radar.weather.gov/ridge/standard/KFSD_loop.gif?t={int(time.time())}"
    
    with st.container(border=True):
        st.image(radar_url, use_container_width=True)


# Execute auto-refresh telemetry fragment
load_live_weather()

# ==========================================
# --- COMMUNITY FEEDBACK AND SUGGESTIONS HTML FORM ---
# ==========================================
st.markdown("<div style='margin: 40px 0 20px 0;'></div>", unsafe_allow_html=True)
st.subheader("💬 Community Feedback and Suggestions")
st.markdown("<p style='color: #a1a1aa; font-size: 0.95rem;'>Send your feedback and suggestions directly to wsnk836@gmail.com.</p>", unsafe_allow_html=True)

components.html("""
<!DOCTYPE html>
<html>
<head>
    <style>
        body {
            background-color: transparent;
            color: #f4f4f5;
            font-family: system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
            margin: 0;
            padding: 0;
        }
        .form-group {
            margin-bottom: 12px;
        }
        .row {
            display: flex;
            gap: 12px;
        }
        .col {
            flex: 1;
        }
        label {
            display: block;
            font-size: 0.85rem;
            color: #a1a1aa;
            margin-bottom: 6px;
            text-transform: uppercase;
            letter-spacing: 0.03em;
        }
        input, textarea {
            width: 100%;
            background-color: #121316;
            border: 1px solid #27272a;
            border-radius: 8px;
            color: #f4f4f5;
            padding: 10px 12px;
            font-size: 0.95rem;
            box-sizing: border-box;
            outline: none;
            transition: border-color 0.2s;
        }
        input:focus, textarea:focus {
            border-color: #f59e0b;
        }
        textarea {
            resize: vertical;
            height: 90px;
        }
        button {
            background: #f59e0b;
            color: #0c0d10;
            border: none;
            border-radius: 8px;
            padding: 11px 20px;
            font-weight: 700;
            font-size: 0.95rem;
            cursor: pointer;
            width: 100%;
            margin-top: 5px;
            transition: opacity 0.2s;
        }
        button:hover {
            opacity: 0.9;
        }
        #result {
            margin-top: 10px;
            font-size: 0.9rem;
            text-align: center;
        }
    </style>
</head>
<body>
    <form action="https://api.web3forms.com/submit" method="POST" id="web3form">
        <input type="hidden" name="access_key" value="6f59571f-f519-4655-9b50-095eed178152">
        <input type="hidden" name="subject" value="💡 Community Feedback and Suggestions from Marcus Command">
        
        <div class="row">
            <div class="col form-group">
                <label>Name *</label>
                <input type="text" name="name" placeholder="Your Name" required>
            </div>
            <div class="col form-group">
                <label>Location / Grid (Optional)</label>
                <input type="text" name="location" placeholder="Marcus, IA">
            </div>
        </div>
        
        <div class="form-group">
            <label>Your Feedback and Suggestions *</label>
            <textarea name="message" placeholder="Enter your feedback or suggestions here..." required></textarea>
        </div>
        
        <input type="checkbox" name="botcheck" style="display: none;">

        <button type="submit" id="submit-btn">Send Community Feedback and Suggestions</button>
        <div id="result"></div>
    </form>

    <script>
        const form = document.getElementById('web3form');
        const result = document.getElementById('result');

        form.addEventListener('submit', function(e) {
            e.preventDefault();
            const formData = new FormData(form);
            const object = Object.fromEntries(formData);
            const json = JSON.stringify(object);
            result.style.color = "#a1a1aa";
            result.innerHTML = "Sending feedback...";

            fetch('https://api.web3forms.com/submit', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Accept': 'application/json'
                },
                body: json
            })
            .then(async (response) => {
                let jsonResponse = await response.json();
                if (response.status == 200) {
                    result.style.color = "#10b981";
                    result.innerHTML = "✅ Feedback and suggestions sent directly to wsnk836@gmail.com!";
                    form.reset();
                } else {
                    result.style.color = "#ef4444";
                    result.innerHTML = jsonResponse.message || "Something went wrong!";
                }
            })
            .catch(error => {
                result.style.color = "#ef4444";
                result.innerHTML = "Network connection error!";
            });
        });
    </script>
</body>
</html>
""", height=290, scrolling=False)

# ==========================================
# --- GITHUB REPOSITORY LINK FOOTER ---
# ==========================================
st.markdown("""
<div style="text-align: center; color: #71717a; font-size: 0.9rem; padding-top: 30px; padding-bottom: 20px;">
    <hr style="border: none; border-top: 1px solid #27272a; margin-bottom: 20px;">
    💻 Source code available on 
    <a href="https://github.com/wsnk836/marcus-weather-app" target="_blank" style="color: #fbbf24; text-decoration: none; font-weight: 600;">
        GitHub
    </a>
</div>
""", unsafe_allow_html=True)
