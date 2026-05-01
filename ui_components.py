
import streamlit as st
from streamlit_lottie import st_lottie
import requests
import json

def load_lottieurl(url: str):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

# Lottie Assets
LOTTIE_AI = "https://assets10.lottiefiles.com/packages/lf20_m9ub69zb.json"
LOTTIE_ANALYTICS = "https://assets5.lottiefiles.com/packages/lf20_qpwb7qsq.json"
LOTTIE_SUCCESS = "https://assets3.lottiefiles.com/packages/lf20_pqnfmone.json"

def render_sidebar():
    with st.sidebar:
        st.markdown(f"""
            <div style="text-align: center; padding: 1rem 0;">
                <h1 style="color: #00C2FF; margin: 0; font-size: 1.8rem;">SentiAI <span style="color: #FFF;">Pro</span></h1>
                <p style="color: #9CA3AF; font-size: 0.75rem; text-transform: uppercase; letter-spacing: 0.2em;">Enterprise Analytics</p>
            </div>
        """, unsafe_allow_html=True)
        
        st.markdown("---")
        

        menu = {
            "🏠 Dashboard": "Dashboard",
            "🔍 Single Analysis": "Single",
            "📊 Bulk Analysis": "Bulk",
            "📁 CSV Upload": "CSV",
            "🎙️ Voice Analysis": "Voice",
            "🎥 YouTube Analyzer": "YouTube",
            "📱 Social Tracker": "Social",
            "📄 PDF Analysis": "PDF",
            "🤖 AI Models": "Models",
            "📈 Analytics": "Analytics",
            "⚙️ Settings": "Settings",
            "ℹ️ About": "About"
        }

        
        selection = st.radio("Navigation", list(menu.keys()), label_visibility="collapsed")
        
        st.markdown("---")
        
        # User Profile Mini Card
        st.markdown("""
            <div style="background: rgba(255,255,255,0.03); border: 1px solid rgba(255,255,255,0.08); padding: 1rem; border-radius: 12px;">
                <div style="display: flex; align-items: center; gap: 0.75rem;">
                    <div style="width: 32px; height: 32px; background: #00C2FF; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-weight: bold; color: #000;">AD</div>
                    <div>
                        <div style="font-size: 0.85rem; font-weight: 600; color: #F9FAFB;">Arup Das</div>
                        <div style="font-size: 0.7rem; color: #9CA3AF;">Pro Member</div>
                    </div>
                </div>
            </div>
        """, unsafe_allow_html=True)
        
        return menu[selection]

def render_model_selector():
    st.markdown("### 🤖 Select AI Engine")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
            <div class="premium-card" style="text-align: center; border-color: var(--primary);">
                <div style="font-size: 1.5rem;">⚡</div>
                <div style="font-weight: 700; color: #FFF; margin: 0.5rem 0;">VADER</div>
                <div style="font-size: 0.7rem; color: #9CA3AF;">Fast & Social Media Optimized</div>
                <div style="margin-top: 0.5rem;"><span class="pill-positive" style="font-size: 0.6rem;">LATEST</span></div>
            </div>
        """, unsafe_allow_html=True)
        
    with col2:
        st.markdown("""
            <div class="premium-card" style="text-align: center;">
                <div style="font-size: 1.5rem;">🔵</div>
                <div style="font-weight: 700; color: #FFF; margin: 0.5rem 0;">TextBlob</div>
                <div style="font-size: 0.7rem; color: #9CA3AF;">General Purpose Rule-based</div>
                <div style="margin-top: 0.5rem;"><span class="pill-neutral" style="font-size: 0.6rem;">STABLE</span></div>
            </div>
        """, unsafe_allow_html=True)
        
    with col3:
        st.markdown("""
            <div class="premium-card" style="text-align: center;">
                <div style="font-size: 1.5rem;">🤖</div>
                <div style="font-weight: 700; color: #FFF; margin: 0.5rem 0;">BERT</div>
                <div style="font-size: 0.7rem; color: #9CA3AF;">Deep Learning Transformer</div>
                <div style="margin-top: 0.5rem;"><span class="pill-negative" style="font-size: 0.6rem;">RESOURCES ++</span></div>
            </div>
        """, unsafe_allow_html=True)
    
    return st.select_slider("Engine Sensitivity", options=["VADER", "TextBlob", "BERT"], label_visibility="collapsed")

def render_footer():
    st.markdown("---")
    col1, col2, col3 = st.columns([2, 1, 1])
    with col1:
        st.markdown("""
            <div style="color: #4B5563; font-size: 0.8rem;">
                © 2026 SentiAI Pro. Built with Streamlit, Transformers & Passion.
            </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown("[Documentation](https://example.com)")
    with col3:
        st.markdown("[API Reference](https://example.com)")
