import streamlit as st
import streamlit.components.v1 as requests_comp
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
requests_comp.html("""
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
""", unsafe_allow_html=True)

# --- MOBILE KEEP-ALIVE & PUSH NOTIFICATION WATCHDOG ---
requests_comp.html("""
<script>
    document.addEventListener("visibilitychange", function() {
        if (document.visibilityState === "visible") {
            window.parent.location.reload();
        }
    });
    setTimeout(function() {
        window.parent.location.reload();
    }, 600000);

    // Global Browser Notification Handler injected into top-level window
    window.parent.requestWeatherNotification = function(title, bodyText) {
        if (!("Notification" in window.parent)) {
            console.log("This browser does not support desktop notification");
            return;
        }
        if (window.parent.Notification.permission === "granted") {
            new window.parent.Notification(title, { body: bodyText, icon: "https://radar.weather.gov/ridge/standard/KFSD_loop.gif" });
        } else if (window.parent.Notification.permission !== "denied") {
            window.parent.Notification.requestPermission().then(function (permission) {
                if (permission === "granted") {
                    new window.parent.Notification(title, { body: bodyText, icon: "https://radar.weather.gov/ridge/standard/KFSD_loop.gif" });
                }
            });
        }
    }
</script>
""", height=0, width=0)

# --- HERO HEADER ---
st.markdown("""
<div class="hero-banner">
    <div class="hero-title">📡 Marcus Weather Command</div>
    <div class="hero-subtitle">Real-time NWS Telemetry & Regional GMRS Radio Operations • Cherokee County, IA</div>
</div>
""", unsafe_allow_html=True)

# --- QUICK ACCESS NAV BAR ---
requests_comp.html("""
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
        if (el) { el.scrollIntoView({ behavior: 'smooth', block: 'start' }); }
    }
</script>
""", height=60, scrolling=False)


# ==========================================
# --- CONTINUOUSLY REFRESHING FRAGMENT ---
# ==========================================
@st.fragment(run_every=60)
def load_live_weather():
    headers = {
        "User-Agent": "MarcusWeatherApp (wsnk836@gmail.com)",
        "Accept": "application/geo+json"
    }

    # --- INITIALIZE SESSION STATE WITH QUERY PARAM PERSISTENCE ---
    if "selected_forecast_day" not in st.session_state:
        st.session_state.selected_forecast_day = None
    if "enable_push_alerts" not in st.session_state:
        param_val = st.query_params.get("push_alerts", "false")
        st.session_state.enable_push_alerts = (str(param_val).lower() == "true")

    # --- ACTIVE SEVERE WEATHER ALERTS ---
    st.markdown('<div id="alerts-sec"></div>', unsafe_allow_html=True)
    
    col_alert_header, col_alert_toggle = st.columns([2.5, 1])
    with col_alert_header:
        st.subheader("⚠️ Active NWS Weather Alerts")
    with col_alert_toggle:
        push_val = st.toggle("🔔 Push Alerts", value=st.session_state.enable_push_alerts, help="Enable browser push notifications when severe weather is active.")
        if push_val != st.session_state.enable_push_alerts:
            st.session_state.enable_push_alerts = push_val
            st.query_params["push_alerts"] = str(push_val).lower()

    try:
        alerts_url = "https://api.weather.gov/alerts/active?point=42.8242,-95.7994"
        alerts_response = requests.get(alerts_url, headers=headers, timeout=10).json()
        alerts = alerts_response.get("features", [])
        
        if len(alerts) > 0:
            # Trigger Browser Notification if toggled on
            if st.session_state.enable_push_alerts:
                first_alert_title = alerts[0].get("properties", {}).get("event", "Severe Weather Warning")
                first_alert_desc = alerts[0].get("properties", {}).get("headline", "New NWS weather alert active for Marcus, IA.")
                # Sanitize strings to inject safely into JS component call
                safe_title = first_alert_title.replace('"', '\\"')
                safe_desc = first_alert_desc.replace('"', '\\"').replace('\n', ' ')
                
                requests_comp.html(f"""
                <script>
                    if (window.parent.requestWeatherNotification) {{
                        window.parent.requestWeatherNotification("🚨 {safe_title}", "{safe_desc}");
                    }}
                </script>
                """, height=0, width=0)

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
                🟢 <strong>All Clear:</strong> No active warnings or advisories for Marcus, IA.
            </div>
            """, unsafe_allow_html=True)
            
    except Exception as e:
        st.error(f"Could not reach NWS alert servers: {e}")

    st.markdown("<div style='margin: 15px 0;'></div>", unsafe_allow_html=True)

    # --- TWO-COLUMN DASHBOARD LAYOUT ---
    col_left, col_right = st.columns([1.1, 1], gap="large")

    with col_left:
        # --- CURRENT CONDITIONS & METRICS ---
        st.markdown('<div id="conditions-sec"></div>', unsafe_allow_html=True)
        st.subheader("🌦️ Current Conditions")
        try:
            points_url = "https://api.weather.gov/points/42.8242,-95.7994"
            points_response = requests.get(points_url, headers=headers, timeout=10).json()
            forecast_url = points_response["properties"]["forecast"]
            
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
            
            # --- ROBUST NWS PERIOD PAIRING INTO CLEAN DAILY RECORDS ---
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
                        
                    daily_forecasts.append({
                        "day": day_name,
                        "high": high_temp,
                        "low": low_temp,
                        "detailed": day_detailed,
                        "low_detailed": night_detailed,
                        "wind_speed": wind_speed,
                        "wind_dir": wind_dir
                    })
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

                    daily_forecasts.append({
                        "day": day_label,
                        "high": high_temp,
                        "low": low_temp,
                        "detailed": day_detailed,
                        "low_detailed": night_detailed,
                        "wind_speed": wind_speed,
                        "wind_dir": wind_dir
                    })
                i += 1

            # Set default selected day if not set or invalid
            if not st.session_state.selected_forecast_day or st.session_state.selected_forecast_day not in [d['day'] for d in daily_forecasts]:
                st.session_state.selected_forecast_day = daily_forecasts[0]['day']

            # --- EXTENDED FORECAST TABS ---
            st.subheader("📅 Outlook")
            tab3, tab7 = st.tabs(["3-Day", "7-Day"])
            
            with tab3:
                st.markdown("<div style='height: 4px;'></div>", unsafe_allow_html=True)
                days_to_show_3 = daily_forecasts[:3]
                st.markdown("<p style='color: #a1a1aa; font-size: 0.8rem; margin-bottom: 6px;'>👆 Select a day below to pull up full NWS Sioux Falls telemetry:</p>", unsafe_allow_html=True)
                
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
                st.markdown("<p style='color: #a1a1aa; font-size: 0.8rem; margin-bottom: 6px;'>👆 Select a day below to pull up full NWS Sioux Falls telemetry:</p>", unsafe_allow_html=True)
                
                cols7 = st.columns(len(days_to_show_7))
                for idx, d_item in enumerate(days_to_show_7):
                    with cols7[idx]:
                        is_selected = (d_item['day'] == st.session_state.selected_forecast_day)
                        btn_label = f"📍 {d_item['day']}" if is_selected else d_item['day']
                        if st.button(btn_label, key=f"btn_7d_{idx}_{d_item['day']}", use_container_width=True):
                            st.session_state.selected_forecast_day = d_item['day']
                            st.rerun()

            selected_record = next((d for d in daily_forecasts if d['day'] == st.session_state.selected_forecast_day), daily_forecasts[0])

            display_high = selected_record['high']
            display_low = selected_record['low']
            
            current_temp_str = f"{current['temperature']}°{current['temperatureUnit']}"
            if display_high == "N/A":
                display_high = current_temp_str
            if display_low == "N/A":
                display_low = current_temp_str

            # --- FULL FORECAST DRILL-DOWN LAYER ---
            st.markdown(f"""
            <div style="background: #18191f; border: 1px solid #27272a; border-left: 3px solid #ef4444; border-radius: 10px; padding: 18px 20px; margin-top: 15px;">
                <div style="font-weight: 700; color: #f87171; font-size: 1.05rem; margin-bottom: 10px; display: flex; align-items: center; gap: 8px;">
                    🏛️ Full NWS Forecast Report • {selected_record['day']}
                </div>
                {f'<div style="font-size: 0.92rem; color: #f4f4f5; margin-bottom: 8px; line-height: 1.6;"><strong>Daytime Forecast:</strong> {selected_record["detailed"]}</div>' if selected_record['detailed'] else ''}
                {f'<div style="font-size: 0.92rem; color: #d4d4d8; margin-bottom: 12px; line-height: 1.6;"><strong>Nighttime Forecast:</strong> {selected_record["low_detailed"]}</div>' if selected_record['low_detailed'] else ''}
                <div style="display: flex; flex-wrap: wrap; gap: 18px; margin-top: 12px; font-size: 0.85rem; color: #a1a1aa; border-top: 1px solid #27272a; padding-top: 10px;">
                    <div>🌡️ High: <strong style="color: #fafafa;">{display_high}</strong></div>
                    <div>🌡️ Low: <strong style="color: #fafafa;">{display_low}</strong></div>
                    <div>💨 Wind: <strong style="color: #fafafa;">{selected_record['wind_speed']} ({selected_record['wind_dir']})</strong></div>
                    <div>📡 Station: <strong style="color: #fafafa;">NWS Sioux Falls (KFSD)</strong></div>
                </div>
            </div>
            """, unsafe_allow_html=True)

        except Exception as e:
            st.error(f"Could not load NWS forecast telemetry: {e}")

        st.markdown("<div style='margin: 15px 0;'></div>", unsafe_allow_html=True)

        # --- LIVE RADAR LOOP ---
        st.markdown('<div id="radar-sec"></div>', unsafe_allow_html=True)
        st.subheader("📡 Live Doppler Radar (KFSD)")
        cst_time = datetime.now(ZoneInfo("America/Chicago")).strftime('%I:%M:%S %p %Z')
        st.caption(f"🔄 Sync active • {cst_time}")
        radar_url = f"https://radar.weather.gov/ridge/standard/KFSD_loop.gif?t={int(time.time())}"
        with st.container(border=True):
            st.image(radar_url, use_container_width=True)

    with col_right:
        # --- WELCOME CARD ---
        st.markdown("""
        <div class="command-card welcome-card">
            👋 <strong>Welcome to Marcus Weather Command.</strong> Your centralized operational dashboard for live local meteorological telemetry, high-definition Doppler radar loops, and emergency alerts. Keep this app active for continuous monitoring.
        </div>
        """, unsafe_allow_html=True)

        # --- COMMUNITY NEWS SECTION ---
        st.markdown('<div id="news-sec"></div>', unsafe_allow_html=True)
        st.subheader("📻 Community News")
        st.markdown("""
        <div class="command-card repeater-card">
            <strong>GMRS REPEATER GOING ACTIVE — 12/01/2026:</strong> Tune to <strong>Channel 22</strong> (462.725 MHz) • <strong>PL Tone 123.0 Hz</strong>. Fully open for community use!
        </div>
        """, unsafe_allow_html=True)

        # --- INSTALL SECTION ---
        st.markdown('<div id="install-sec"></div>', unsafe_allow_html=True)
        st.subheader("📲 Install")
        st.markdown("""
        <div class="command-card install-card">
            <strong>Add & Rename to Home Screen:</strong> Install this dashboard on your mobile device:<br/>
            • <strong>iOS (Safari):</strong> Tap <strong>Share</strong>, select <strong>"Add to Home Screen"</strong>, rename it to <strong>"Marcus Weather"</strong>, and tap <strong>Add</strong>.<br/>
            • <strong>Android (Chrome):</strong> Tap the <strong>Menu</strong> (three dots), select <strong>"Add to Home screen"</strong> (or "Install app"), rename the shortcut to <strong>"Marcus Weather"</strong>, and confirm.
        </div>
        """, unsafe_allow_html=True)


# Execute auto-refresh telemetry fragment
load_live_weather()

# ==========================================
# --- COMMUNITY FEEDBACK AND SUGGESTIONS HTML FORM ---
# ==========================================
st.markdown('<div id="feedback-sec"></div>', unsafe_allow_html=True)
st.markdown("<div style='margin: 20px 0 10px 0;'></div>", unsafe_allow_html=True)
st.subheader("💬 Community Feedback and Suggestions")
st.markdown("<p style='color: #a1a1aa; font-size: 0.92rem;'>Send your feedback and suggestions directly to wsnk836@gmail.com.</p>", unsafe_allow_html=True)

requests_comp.html("""
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
        .form-group { margin-bottom: 12px; }
        .row { display: flex; gap: 12px; }
        .col { flex: 1; }
        label {
            display: block;
            font-size: 0.82rem;
            color: #a1a1aa;
            margin-bottom: 5px;
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
            font-size: 0.92rem;
            box-sizing: border-box;
            outline: none;
            transition: border-color 0.2s;
        }
        input:focus, textarea:focus { border-color: #ef4444; }
        textarea { resize: vertical; height: 80px; }
        button {
            background: #ef4444;
            color: #0c0d10;
            border: none;
            border-radius: 8px;
            padding: 10px 20px;
            font-weight: 700;
            font-size: 0.92rem;
            cursor: pointer;
            width: 100%;
            margin-top: 4px;
            transition: opacity 0.2s;
        }
        button:hover { opacity: 0.9; }
        #result { margin-top: 8px; font-size: 0.88rem; text-align: center; }
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
""", height=270, scrolling=False)

# ==========================================
# --- GITHUB REPOSITORY LINK FOOTER ---
# ==========================================
st.markdown("""
<div style="text-align: center; color: #71717a; font-size: 0.88rem; padding-top: 20px; padding-bottom: 15px;">
    <hr style="border: none; border-top: 1px solid #27272a; margin-bottom: 15px;">
    💻 Source code available on 
    <a href="https://github.com/wsnk836/marcus-weather-app" target="_blank" style="color: #f87171; text-decoration: none; font-weight: 600;">
        GitHub
    </a>
</div>
""", unsafe_allow_html=True)
