import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd
from analyzer import analyze_sentiment, analyze_multiple
from utils import load_csv, results_to_dataframe, get_summary

st.set_page_config(
    page_title="Sentiment Analysis Tool",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Poppins:wght@500;600;700&display=swap');

/* Base */
html, body, .stApp { background: #0B1120 !important; font-family: 'Inter', sans-serif !important; color: #F8FAFC !important; }
[data-testid="stSidebar"] { background: #0F172A !important; border-right: 1px solid rgba(255,255,255,0.08) !important; }
#MainMenu, footer { visibility: hidden; }
::-webkit-scrollbar { width: 6px; height: 6px; }
::-webkit-scrollbar-track { background: transparent; }
::-webkit-scrollbar-thumb { background: rgba(255,255,255,0.1); border-radius: 4px; }
::-webkit-scrollbar-thumb:hover { background: rgba(255,255,255,0.2); }

/* Top Right Fork */
.fork-btn { position: absolute; top: 1rem; right: 1rem; color: #94A3B8; font-size: 0.85rem; display: flex; align-items: center; gap: 0.5rem; font-family: 'Inter', sans-serif; font-weight: 500; }

/* Hero */
.hero { text-align: center; padding: 3rem 0 1rem 0; }
.hero-title { font-family: 'Poppins', sans-serif; font-size: 2.5rem; font-weight: 700; color: #F8FAFC; margin-bottom: 0.5rem; text-shadow: 0 0 20px rgba(34, 211, 238, 0.1); display: flex; align-items: center; justify-content: center; gap: 0.5rem; }
.hero-title span { color: #22D3EE; }
.hero-title img { width: 40px; }
.hero-sub { color: #94A3B8; font-size: 1rem; font-weight: 400; }
.divider { height: 1px; background: rgba(255,255,255,0.08); margin: 2rem 0; width: 100%; }

/* Sections */
.sec-title { font-family: 'Poppins', sans-serif; font-size: 1.2rem; font-weight: 500; color: #F8FAFC; margin-bottom: 1rem; display: flex; align-items: center; gap: 0.5rem; }
.sec-title span { color: #4A5568; font-size: 1rem; }

/* Sidebar */
.sb-header { color: #94A3B8; font-size: 0.75rem; font-weight: 600; letter-spacing: 0.05em; text-transform: uppercase; margin-bottom: 0.5rem; margin-top: 1.5rem; font-family: 'Inter', sans-serif; }
.sb-label { color: #F8FAFC; font-size: 0.85rem; margin-bottom: 0.5rem; font-family: 'Inter', sans-serif; }
.engine-desc-card { background: rgba(34, 197, 94, 0.1); border: 1px solid rgba(34, 197, 94, 0.2); border-radius: 8px; padding: 0.75rem; color: #4ADE80; font-size: 0.8rem; margin-top: 1rem; font-family: 'Inter', sans-serif; }

/* Sidebar Radio Buttons specific styling */
[data-testid="stSidebar"] .stRadio label { color: #94A3B8 !important; font-weight: 500 !important; font-size: 0.95rem !important; }
[data-testid="stSidebar"] .stRadio div[role="radiogroup"] > div { background: transparent; padding: 0.4rem 0.5rem; border-radius: 8px; transition: all 0.2s; margin-bottom: 0.2rem; }
[data-testid="stSidebar"] .stRadio div[role="radiogroup"] > div:hover { background: rgba(255,255,255,0.05); }
/* Make the checked radio option look a bit like a highlighted tab if possible via normal streamlit behavior, else it defaults nicely */

/* Inputs */
.stTextArea label { color: #F8FAFC !important; font-weight: 500 !important; font-size: 0.95rem !important; margin-bottom: 0.5rem !important; font-family: 'Inter', sans-serif; }
.stTextArea textarea { background: #111827 !important; border: 1px solid rgba(255,255,255,0.08) !important; border-radius: 8px !important; color: #F8FAFC !important; font-family: 'Inter', sans-serif !important; padding: 1rem !important; font-size: 0.95rem !important; box-shadow: inset 0 2px 4px rgba(0,0,0,0.2) !important; transition: border-color 0.2s ease, box-shadow 0.2s ease !important; }
.stTextArea textarea:focus { border-color: #22D3EE !important; box-shadow: 0 0 0 2px rgba(34, 211, 238, 0.2) !important; }

/* Button */
.stButton > button { background: linear-gradient(90deg, #06B6D4, #38BDF8) !important; color: #0B1120 !important; font-weight: 600 !important; font-family: 'Inter', sans-serif !important; border: none !important; border-radius: 8px !important; padding: 0.6rem 1rem !important; font-size: 1rem !important; transition: all 0.2s ease !important; box-shadow: 0 4px 12px rgba(6, 182, 212, 0.3) !important; width: 100% !important; display: block !important; }
.stButton > button:hover { opacity: 0.9 !important; transform: translateY(-1px) !important; box-shadow: 0 6px 16px rgba(6, 182, 212, 0.4) !important; }

/* Metric Cards */
[data-testid="stMetric"] { background: #111827 !important; border: 1px solid rgba(255,255,255,0.08) !important; border-radius: 8px !important; padding: 1rem 1.25rem !important; box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1) !important; }
[data-testid="stMetricLabel"] p { color: #94A3B8 !important; font-size: 0.75rem !important; font-weight: 500 !important; text-transform: uppercase; letter-spacing: 0.05em; }
[data-testid="stMetricValue"] { color: #F8FAFC !important; font-weight: 600 !important; font-size: 1.5rem !important; }

/* Custom Result Cards */
.card-pos, .card-neg, .card-neu { border-radius: 8px; padding: 1rem 1.25rem; font-weight: 500; margin-top: 1rem; font-size: 0.95rem; display: flex; align-items: center; gap: 0.5rem; box-shadow: 0 1px 3px 0 rgba(0, 0, 0, 0.1); }
.card-pos { background: rgba(34, 197, 94, 0.05); border: 1px solid rgba(34, 197, 94, 0.2); color: #4ADE80; }
.card-neg { background: rgba(239, 68, 68, 0.05); border: 1px solid rgba(239, 68, 68, 0.2); color: #F87171; }
.card-neu { background: rgba(148, 163, 184, 0.05); border: 1px solid rgba(148, 163, 184, 0.2); color: #CBD5E1; }

.engine-tag { display: inline-block; background: #111827; border: 1px solid rgba(255,255,255,0.08); color: #94A3B8; font-size: 0.7rem; font-weight: 500; padding: 0.25rem 0.5rem; border-radius: 4px; margin-top: 0.75rem; }

/* Progress */
.stProgress > div > div { background: #22D3EE !important; border-radius: 4px !important; }

/* Dataframes */
[data-testid="stDataFrame"] { border: 1px solid rgba(255,255,255,0.08) !important; border-radius: 8px !important; overflow: hidden !important; }
</style>
""", unsafe_allow_html=True)

# ── Sidebar
with st.sidebar:
    st.markdown('<div style="display: flex; align-items: flex-start; gap: 0.5rem; margin-bottom: 2rem; font-family: \'Poppins\', sans-serif;"><div style="font-size: 1.5rem;">🧠</div><div style="line-height: 1.2;"><div style="color: #F8FAFC; font-size: 1.1rem; font-weight: 700;">Sentiment</div><div style="font-size: 1.1rem; font-weight: 700; color: #22D3EE;">Analysis Tool</div></div></div>', unsafe_allow_html=True)
    
    st.markdown('<div class="sb-header">OPTIONS</div>', unsafe_allow_html=True)
    mode = st.radio("OPTIONS", ["Single Text", "Multiple Texts", "Upload CSV", "Dashboard"], label_visibility="collapsed")
    
    st.markdown('<div class="sb-header">NLP ENGINE</div>', unsafe_allow_html=True)
    st.markdown('<div class="sb-label">Engine choose : </div>', unsafe_allow_html=True)
    engine = st.radio("NLP ENGINE", ["VADER", "TextBlob", "BERT"], label_visibility="collapsed")
    
    if engine == "VADER":
        st.markdown(f'<div class="engine-desc-card">⚡ Fast | Great for social media text</div>', unsafe_allow_html=True)
    elif engine == "TextBlob":
        st.markdown(f'<div class="engine-desc-card" style="color: #38BDF8; border-color: rgba(56,189,248,0.2); background: rgba(56,189,248,0.1);">🔵 Simple | General text analysis</div>', unsafe_allow_html=True)
    elif engine == "BERT":
        st.markdown(f'<div class="engine-desc-card" style="color: #F87171; border-color: rgba(248,113,113,0.2); background: rgba(248,113,113,0.1);">🤖 Slow | Most accurate neural model</div>', unsafe_allow_html=True)
    
    st.markdown('<div class="sb-header">SETTINGS</div>', unsafe_allow_html=True)
    multilingual = st.toggle("🌍 Multilingual Mode", value=False)
    if multilingual:
        st.caption("Detects Bengali, Hindi, German & more")

st.markdown('<div class="fork-btn">Fork 🐙 :</div>', unsafe_allow_html=True)

# ── Hero
st.markdown('<div class="hero"><div class="hero-title">🧠 Sentiment <span>Analysis Tool</span></div><div class="hero-sub">Analyze emotions behind any text using AI</div></div><div class="divider"></div>', unsafe_allow_html=True)


def safe_translate(text):
    try:
        from translator import translate_to_english
        return translate_to_english(text)
    except Exception:
        return {"original": text, "translated": text, "lang_info": {"code": "en", "name": "English", "flag": "🇬🇧"}, "was_translated": False}


def safe_translate_multiple(texts):
    try:
        from translator import translate_multiple
        return translate_multiple(texts)
    except Exception:
        return [{"original": t, "translated": t, "lang_info": {"code": "en", "name": "English", "flag": "🇬🇧"}, "was_translated": False} for t in texts]


# ══════════════════════════════════════════════════════
# MODE 1 — Single Text
# ══════════════════════════════════════════════════════
if mode == "Single Text":
    st.markdown('<div class="sec-title">📝 Single Text Analysis <span>🔗</span></div>', unsafe_allow_html=True)
    user_input = st.text_area("তোমার text এখানে লেখো:", placeholder="e.g. I love programming in Python!", height=150, max_chars=2000)
    
    go = st.button("🔍 Analyze", use_container_width=True)

    if go:
        if user_input.strip():
            with st.spinner("Analyzing..."):
                if multilingual:
                    trans = safe_translate(user_input)
                    analysis_text = trans["translated"]
                    lang = trans["lang_info"]
                    if trans["was_translated"]:
                        st.info(f"{lang['flag']} **{lang['name']}** detected → Translated: *{analysis_text}*")
                else:
                    analysis_text = user_input
                result = analyze_sentiment(analysis_text, engine)

            st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
            c1, c2, c3, c4 = st.columns(4)
            c1.metric("Sentiment", f"{result['emoji']} {result['label']}")
            c2.metric("Polarity", result["polarity"])
            c3.metric("Subjectivity", result["subjectivity"])
            c4.metric("Confidence", f"{result['confidence']}%")

            if engine == "VADER" and "pos" in result:
                st.markdown("<br>", unsafe_allow_html=True)
                v1, v2, v3 = st.columns(3)
                v1.metric("Positive", result["pos"])
                v2.metric("Negative", result["neg"])
                v3.metric("Neutral Score", result["neu"])

            st.markdown("<br>**Polarity Meter**", unsafe_allow_html=True)
            st.progress((result["polarity"] + 1) / 2)

            if result["label"] == "Positive":
                st.markdown('<div class="card-pos">✅ Positive Sentiment Detected</div>', unsafe_allow_html=True)
            elif result["label"] == "Negative":
                st.markdown('<div class="card-neg">❌ Negative Sentiment Detected</div>', unsafe_allow_html=True)
            else:
                st.markdown('<div class="card-neu">⚪ Neutral Sentiment Detected</div>', unsafe_allow_html=True)

            st.markdown(f'<div class="engine-tag">Engine: {result["engine"]}</div>', unsafe_allow_html=True)
        else:
            st.warning("Please enter some text first.")

# ══════════════════════════════════════════════════════
# MODE 2 — Multiple Texts
# ══════════════════════════════════════════════════════
elif mode == "Multiple Texts":
    st.markdown('<div class="sec-title">📋 Multiple Text Analysis</div>', unsafe_allow_html=True)
    raw = st.text_area("Enter texts (one per line):", placeholder="I love this!\nThis is terrible.\nIt was okay.", height=180)
    
    go_all = st.button("🔍 Analyze All", use_container_width=True)

    if go_all:
        texts = [t.strip() for t in raw.strip().split("\n") if t.strip()]
        if texts:
            with st.spinner("Analyzing..."):
                if multilingual:
                    trans_all = safe_translate_multiple(texts)
                    n_trans = sum(1 for t in trans_all if t["was_translated"])
                    if n_trans > 0:
                        st.info(f"🌍 {n_trans} text(s) translated")
                    analysis_texts = [t["translated"] for t in trans_all]
                else:
                    analysis_texts = texts
                results = analyze_multiple(analysis_texts, engine)

            df = results_to_dataframe(results)
            summary = get_summary(results)

            st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
            st.markdown('<div class="sec-title">📊 Summary</div>', unsafe_allow_html=True)
            c1, c2, c3, c4 = st.columns(4)
            c1.metric("Total", summary["Total"])
            c2.metric("Positive 😊", summary["Positive 😊"])
            c3.metric("Negative 😞", summary["Negative 😞"])
            c4.metric("Neutral 😐", summary["Neutral 😐"])

            st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
            col_chart, _ = st.columns([1, 1])
            with col_chart:
                fig, ax = plt.subplots(figsize=(5, 4))
                fig.patch.set_facecolor("#0B1120")
                ax.set_facecolor("#0B1120")
                sizes = [summary["Positive 😊"], summary["Negative 😞"], summary["Neutral 😐"]]
                wedges, _, autotexts = ax.pie(sizes, labels=["Positive", "Negative", "Neutral"], autopct="%1.1f%%", colors=["#22D3EE", "#EF4444", "#94A3B8"], startangle=140, textprops={"color": "white", "fontsize": 10})
                for at in autotexts:
                    at.set_color("white")
                st.pyplot(fig)

            st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
            st.dataframe(df, use_container_width=True, hide_index=True)
        else:
            st.warning("Please enter at least one text.")

# ══════════════════════════════════════════════════════
# MODE 3 — Upload CSV
# ══════════════════════════════════════════════════════
elif mode == "Upload CSV":
    st.markdown('<div class="sec-title">📁 CSV Upload</div>', unsafe_allow_html=True)
    st.info("CSV must have a column named **text**")
    uploaded = st.file_uploader("Choose CSV file", type=["csv"])

    if uploaded:
        texts, error = load_csv(uploaded)
        if error:
            st.error(error)
        else:
            st.success(f"✅ {len(texts)} texts loaded")
            
            go_csv = st.button("🔍 Analyze CSV", use_container_width=True)

            if go_csv:
                with st.spinner("Analyzing..."):
                    results = analyze_multiple(texts, engine)
                df = results_to_dataframe(results)
                summary = get_summary(results)

                st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
                c1, c2, c3, c4 = st.columns(4)
                c1.metric("Total", summary["Total"])
                c2.metric("Positive 😊", summary["Positive 😊"])
                c3.metric("Negative 😞", summary["Negative 😞"])
                c4.metric("Neutral 😐", summary["Neutral 😐"])

                st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
                fig, ax = plt.subplots(figsize=(6, 3))
                fig.patch.set_facecolor("#0B1120")
                ax.set_facecolor("#0B1120")
                ax.bar(["Positive", "Negative", "Neutral"], [summary["Positive 😊"], summary["Negative 😞"], summary["Neutral 😐"]], color=["#22D3EE", "#EF4444", "#94A3B8"], width=0.45)
                ax.tick_params(colors="#94A3B8", labelsize=10)
                for sp in ax.spines.values():
                    sp.set_edgecolor("rgba(255,255,255,0.08)")
                st.pyplot(fig)

                st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
                st.dataframe(df, use_container_width=True, hide_index=True)
                st.download_button("⬇️ Download Results", data=df.to_csv(index=False).encode("utf-8"), file_name="sentiment_results.csv", mime="text/csv", use_container_width=True)

# ══════════════════════════════════════════════════════
# MODE 4 — Dashboard
# ══════════════════════════════════════════════════════
elif mode == "Dashboard":
    st.markdown('<div class="sec-title">📊 Analytics Dashboard</div>', unsafe_allow_html=True)
    try:
        from dashboard import load_and_analyze, plot_polarity_distribution, generate_wordcloud, get_top_sentences, plot_word_frequency

        col1, col2 = st.columns([2, 1])
        with col1:
            dash_file = st.file_uploader("Upload Dataset (CSV):", type=["csv"])
        with col2:
            limit = st.slider("Rows:", 10, 500, 50, 10)

        use_sample = st.checkbox("Use sample IMDB dataset", value=True)
        
        gen = st.button("📊 Generate Dashboard", use_container_width=True)

        if gen:
            with st.spinner("Building dashboard..."):
                if use_sample:
                    df, error = load_and_analyze("data/imdb.csv", engine, limit)
                elif dash_file:
                    import tempfile, os
                    with tempfile.NamedTemporaryFile(delete=False, suffix=".csv") as tmp:
                        tmp.write(dash_file.read())
                        tmp_path = tmp.name
                    df, error = load_and_analyze(tmp_path, engine, limit)
                    os.unlink(tmp_path)
                else:
                    st.warning("Upload a file or use sample dataset.")
                    st.stop()

            if error:
                st.error(error)
            else:
                st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
                total = len(df)
                pos = len(df[df["label"] == "Positive"])
                neg = len(df[df["label"] == "Negative"])
                neu = len(df[df["label"] == "Neutral"])
                avg_c = round(df["confidence"].mean(), 1)

                c1, c2, c3, c4, c5 = st.columns(5)
                c1.metric("Total", total)
                c2.metric("Positive 😊", pos)
                c3.metric("Negative 😞", neg)
                c4.metric("Neutral 😐", neu)
                c5.metric("Avg Confidence", f"{avg_c}%")

                st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
                st.markdown('<div class="sec-title">📉 Polarity Distribution</div>', unsafe_allow_html=True)
                st.pyplot(plot_polarity_distribution(df))

                st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
                st.markdown('<div class="sec-title">🔤 Word Frequency</div>', unsafe_allow_html=True)
                st.pyplot(plot_word_frequency(df))

                st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
                st.markdown('<div class="sec-title">☁️ Word Cloud</div>', unsafe_allow_html=True)
                wc_filter = st.selectbox("Filter:", ["All", "Positive", "Negative", "Neutral"])
                wc_fig = generate_wordcloud(df, wc_filter)
                if wc_fig:
                    st.pyplot(wc_fig)

                st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
                col_p, col_n = st.columns(2)
                with col_p:
                    st.markdown('<div class="sec-title">🏆 Top Positive</div>', unsafe_allow_html=True)
                    for i, r in enumerate(get_top_sentences(df, "Positive", 5), 1):
                        st.markdown(f"**{i}.** {r['text'][:70]}... `{r['polarity']}`")
                with col_n:
                    st.markdown('<div class="sec-title">💔 Top Negative</div>', unsafe_allow_html=True)
                    for i, r in enumerate(get_top_sentences(df, "Negative", 5), 1):
                        st.markdown(f"**{i}.** {r['text'][:70]}... `{r['polarity']}`")

                st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
                st.dataframe(df[["text", "label", "polarity", "confidence"]], use_container_width=True, hide_index=True)
                st.download_button("⬇️ Download Results", data=df.to_csv(index=False).encode("utf-8"), file_name="dashboard_results.csv", mime="text/csv", use_container_width=True)
    except ImportError:
        st.error("dashboard.py not found.")