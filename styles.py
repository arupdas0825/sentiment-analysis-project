
# Premium Design System for SentiAI
# Colors:
# Cyan Blue → #00C2FF
# Electric Blue → #0099FF
# Main Background → #0B0F19
# Secondary Surface → #111827
# Card Background → rgba(255,255,255,0.04)
# Text Primary → #F9FAFB
# Text Secondary → #9CA3AF

MAIN_CSS = """
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Poppins:wght@400;600;700&family=Space+Grotesk:wght@400;500;700&display=swap');

    :root {
        --primary: #00C2FF;
        --primary-glow: rgba(0, 194, 255, 0.25);
        --bg-main: #0B0F19;
        --bg-surface: #111827;
        --card-bg: rgba(255, 255, 255, 0.04);
        --text-primary: #F9FAFB;
        --text-secondary: #9CA3AF;
        --border: rgba(255, 255, 255, 0.08);
        --success: #22C55E;
        --danger: #EF4444;
    }

    /* Global Overrides */
    .stApp {
        background-color: var(--bg-main) !important;
        color: var(--text-primary) !important;
        font-family: 'Inter', sans-serif !important;
    }

    [data-testid="stHeader"] {
        background: transparent !important;
    }

    [data-testid="stSidebar"] {
        background-color: var(--bg-surface) !important;
        border-right: 1px solid var(--border) !important;
        backdrop-filter: blur(10px);
    }

    /* Hide Streamlit elements */
    #MainMenu, footer, header { visibility: hidden; }

    /* Custom Scrollbar */
    ::-webkit-scrollbar {
        width: 8px;
    }
    ::-webkit-scrollbar-track {
        background: var(--bg-main);
    }
    ::-webkit-scrollbar-thumb {
        background: var(--border);
        border-radius: 10px;
    }
    ::-webkit-scrollbar-thumb:hover {
        background: var(--text-secondary);
    }

    /* Typography */
    h1, h2, h3 {
        font-family: 'Space Grotesk', sans-serif !important;
        font-weight: 700 !important;
        letter-spacing: -0.02em !important;
    }

    /* Hero Section */
    .hero-container {
        padding: 4rem 1rem 2rem 1rem;
        text-align: center;
    }
    
    .hero-title {
        font-family: 'Space Grotesk', sans-serif;
        font-size: 4rem;
        font-weight: 800;
        background: linear-gradient(135deg, #FFF 0%, var(--primary) 50%, #0099FF 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.5rem;
        animation: titleGradient 5s ease infinite alternate;
    }
    
    @keyframes titleGradient {
        0% { background-position: 0% 50%; }
        100% { background-position: 100% 50%; }
    }

    .typing-effect {
        font-size: 1.25rem;
        color: var(--text-secondary);
        font-family: 'Poppins', sans-serif;
        min-height: 1.5rem;
    }

    /* Premium Cards */
    .premium-card {
        background: var(--card-bg);
        border: 1px solid var(--border);
        border-radius: 20px;
        padding: 1.5rem;
        transition: all 0.3s ease;
        backdrop-filter: blur(10px);
        margin-bottom: 1rem;
    }

    .premium-card:hover {
        border-color: var(--primary);
        box-shadow: 0 0 20px var(--primary-glow);
        transform: translateY(-2px);
    }

    /* Stat Cards */
    .stat-card {
        text-align: center;
        padding: 1.5rem;
        background: var(--bg-surface);
        border: 1px solid var(--border);
        border-radius: 16px;
    }
    
    .stat-value {
        font-size: 1.75rem;
        font-weight: 700;
        color: var(--primary);
        font-family: 'Space Grotesk', sans-serif;
    }
    
    .stat-label {
        font-size: 0.75rem;
        color: var(--text-secondary);
        text-transform: uppercase;
        letter-spacing: 0.1em;
        margin-top: 0.25rem;
    }

    /* Custom Inputs */
    .stTextArea textarea {
        background: var(--bg-surface) !important;
        border: 1px solid var(--border) !important;
        border-radius: 16px !important;
        color: var(--text-primary) !important;
        padding: 1rem !important;
        transition: all 0.3s ease !important;
    }

    .stTextArea textarea:focus {
        border-color: var(--primary) !important;
        box-shadow: 0 0 15px var(--primary-glow) !important;
    }

    /* Buttons */
    .stButton > button {
        background: linear-gradient(135deg, var(--primary) 0%, #0099FF 100%) !important;
        color: #000 !important;
        font-weight: 700 !important;
        padding: 0.75rem 2rem !important;
        border-radius: 12px !important;
        border: none !important;
        transition: all 0.3s ease !important;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }

    .stButton > button:hover {
        transform: scale(1.02);
        box-shadow: 0 0 20px var(--primary-glow);
    }

    /* Result Indicators */
    .result-pill {
        display: inline-flex;
        align-items: center;
        gap: 0.5rem;
        padding: 0.5rem 1.25rem;
        border-radius: 100px;
        font-weight: 600;
        font-size: 0.875rem;
    }

    .pill-positive { background: rgba(34, 197, 94, 0.1); color: #22C55E; border: 1px solid rgba(34, 197, 94, 0.2); }
    .pill-negative { background: rgba(239, 68, 68, 0.1); color: #EF4444; border: 1px solid rgba(239, 68, 68, 0.2); }
    .pill-neutral { background: rgba(0, 194, 255, 0.1); color: #00C2FF; border: 1px solid rgba(0, 194, 255, 0.2); }

    /* Sidebar Styling */
    .sidebar-item {
        padding: 0.75rem 1rem;
        border-radius: 12px;
        margin-bottom: 0.5rem;
        cursor: pointer;
        transition: all 0.2s ease;
        display: flex;
        align-items: center;
        gap: 0.75rem;
        color: var(--text-secondary);
    }

    .sidebar-item:hover {
        background: var(--card-bg);
        color: var(--text-primary);
    }

    .sidebar-item.active {
        background: var(--primary-glow);
        color: var(--primary);
        border-left: 3px solid var(--primary);
    }

    /* Lottie Container */
    .lottie-container {
        display: flex;
        justify-content: center;
        align-items: center;
    }
</style>
"""

def get_hero_html():
    return """
    <div class="hero-container">
        <div class="hero-title">SentiAI Pro</div>
        <div class="typing-effect" id="typing-text">Next-Generation Sentiment Intelligence Dashboard</div>
    </div>
    """

def get_stat_card(value, label, icon=""):
    return f"""
    <div class="stat-card">
        <div class="stat-value">{value}</div>
        <div class="stat-label">{icon} {label}</div>
    </div>
    """

def get_result_card(sentiment, score, confidence, text, engine):
    pill_class = f"pill-{sentiment.lower()}"
    glow_style = ""
    if sentiment == "Positive": glow_style = "box-shadow: 0 0 30px rgba(34, 197, 94, 0.15);"
    elif sentiment == "Negative": glow_style = "box-shadow: 0 0 30px rgba(239, 68, 68, 0.15);"
    else: glow_style = "box-shadow: 0 0 30px rgba(0, 194, 255, 0.15);"

    return f"""
    <div class="premium-card" style="{glow_style}">
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 1rem;">
            <div class="result-pill {pill_class}">
                {sentiment}
            </div>
            <div style="color: var(--text-secondary); font-size: 0.8rem;">
                Engine: <span style="color: var(--primary);">{engine}</span>
            </div>
        </div>
        <div style="font-size: 1.1rem; color: var(--text-primary); margin-bottom: 1.5rem; line-height: 1.6;">
            "{text}"
        </div>
        <div style="display: grid; grid-template-columns: repeat(2, 1fr); gap: 1rem;">
            <div style="background: rgba(255,255,255,0.02); padding: 0.75rem; border-radius: 12px; border: 1px solid var(--border);">
                <div style="font-size: 0.7rem; color: var(--text-secondary); text-transform: uppercase;">Polarity</div>
                <div style="font-size: 1.2rem; font-weight: 700; color: var(--primary);">{score}</div>
            </div>
            <div style="background: rgba(255,255,255,0.02); padding: 0.75rem; border-radius: 12px; border: 1px solid var(--border);">
                <div style="font-size: 0.7rem; color: var(--text-secondary); text-transform: uppercase;">Confidence</div>
                <div style="font-size: 1.2rem; font-weight: 700; color: var(--primary);">{confidence}%</div>
            </div>
        </div>
    </div>
    """
