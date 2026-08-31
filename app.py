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

# --- REDESIGNED TACTICAL CRIMSON & CARBON CSS (WITH HORIZONTAL SCROLL) ---
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
