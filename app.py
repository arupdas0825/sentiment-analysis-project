import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd
from analyzer import analyze_sentiment, analyze_multiple
from utils import load_csv, results_to_dataframe, get_summary

st.set_page_config(
    page_title="SentiAI",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap');
html, body, .stApp { background: #080B14 !important; font-family: 'Space Grotesk', sans-serif !important; }
[data-testid="stSidebar"] { background: #0D1117 !important; border-right: 1px solid #1C2333 !important; }
[data-testid="stSidebar"] * { font-family: 'Space Grotesk', sans-serif !important; }
#MainMenu, footer, header { visibility: hidden; }
.hero { text-align: center; padding: 2rem 0 1rem 0; }
.hero-badge { display: inline-block; background: #00D4FF15; border: 1px solid #00D4FF30; color: #00D4FF; font-size: 0.7rem; font-weight: 600; letter-spacing: 0.15em; text-transform: uppercase; padding: 0.35rem 1rem; border-radius: 100px; margin-bottom: 1rem; }
.hero-title { font-size: 3rem; font-weight: 700; letter-spacing: -0.03em; background: linear-gradient(135deg, #FFFFFF 0%, #00D4FF 60%, #7B61FF 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text; margin-bottom: 0.6rem; }
.hero-sub { color: #4A5568; font-size: 0.95rem; }
.divider { height: 1px; background: linear-gradient(90deg, transparent, #1C2333 40%, #1C2333 60%, transparent); margin: 1.5rem 0; }
.sec-title { font-size: 1.1rem; font-weight: 600; color: #CBD5E0; margin-bottom: 1rem; }
.card-pos { background: #00FF8808; border: 1px solid #00FF8830; border-radius: 12px; padding: 1rem 1.4rem; color: #00FF88; font-weight: 600; margin-top: 1rem; }
.card-neg { background: #FF4B4B08; border: 1px solid #FF4B4B30; border-radius: 12px; padding: 1rem 1.4rem; color: #FF4B4B; font-weight: 600; margin-top: 1rem; }
.card-neu { background: #FFA50008; border: 1px solid #FFA50030; border-radius: 12px; padding: 1rem 1.4rem; color: #FFA500; font-weight: 600; margin-top: 1rem; }
.engine-tag { display: inline-block; background: #1C2333; border: 1px solid #2D3748; color: #00D4FF; font-size: 0.68rem; font-weight: 600; letter-spacing: 0.08em; text-transform: uppercase; padding: 0.2rem 0.6rem; border-radius: 6px; font-family: 'JetBrains Mono', monospace; margin-top: 0.8rem; }
.dev-card { background: #0D1117; border: 1px solid #1C2333; border-radius: 12px; padding: 1rem; text-align: center; margin-top: 0.5rem; }
.dev-name { color: #E2E8F0; font-weight: 600; font-size: 0.88rem; }
.dev-info { color: #4A5568; font-size: 0.72rem; margin-top: 0.2rem; }
.dev-target { color: #00D4FF; font-size: 0.72rem; margin-top: 0.3rem; }
[data-testid="stMetric"] { background: #0D1117 !important; border: 1px solid #1C2333 !important; border-radius: 12px !important; padding: 1rem !important; }
[data-testid="stMetricLabel"] p { color: #4A5568 !important; font-size: 0.72rem !important; text-transform: uppercase; letter-spacing: 0.08em; }
[data-testid="stMetricValue"] { color: #FFFFFF !important; font-family: 'JetBrains Mono', monospace !important; }
.stButton > button { background: linear-gradient(135deg, #00D4FF, #7B61FF) !important; color: #000 !important; font-weight: 700 !important; border: none !important; border-radius: 10px !important; }
.stButton > button:hover { opacity: 0.88 !important; }
.stTextArea textarea { background: #0D1117 !important; border: 1px solid #1C2333 !important; border-radius: 10px !important; color: #E2E8F0 !important; font-family: 'Space Grotesk', sans-serif !important; }
.stProgress > div > div { background: linear-gradient(90deg, #00D4FF, #7B61FF) !important; border-radius: 100px !important; }
.stRadio label { color: #A0AEC0 !important; }
.sb-logo { text-align: center; padding: 0.8rem 0 1rem 0; }
.sb-logo-text { font-size: 1.25rem; font-weight: 700; background: linear-gradient(135deg, #00D4FF, #7B61FF); -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text; }
.sb-logo-sub { font-size: 0.65rem; color: #4A5568; letter-spacing: 0.12em; text-transform: uppercase; margin-top: 0.15rem; }
</style>
""", unsafe_allow_html=True)

# ── Sidebar
with st.sidebar:
    st.markdown('<div class="sb-logo"><div class="sb-logo-text">🧠 SentiAI</div><div class="sb-logo-sub">Sentiment Analysis</div></div>', unsafe_allow_html=True)
    st.markdown("---")
    st.markdown("**⚡ Mode**")
    mode = st.radio("Mode", ["Single Text", "Multiple Texts", "Upload CSV", "📊 Dashboard"])
    st.markdown("---")
    st.markdown("**🔬 NLP Engine**")
    engine = st.radio("Engine", ["VADER", "TextBlob", "BERT"])
    engine_desc = {"VADER": "⚡ Fast · Social media", "TextBlob": "🔵 Simple · General", "BERT": "🤖 Slow · Most accurate"}
    st.caption(engine_desc[engine])
    st.markdown("---")
    multilingual = st.toggle("🌍 Multilingual Mode", value=False)
    if multilingual:
        st.caption("Detects Bengali, Hindi, German & more")
    st.markdown("---")
    st.markdown('<div class="dev-card"><div class="dev-name">Arup Das</div><div class="dev-info">Brainware University · CSE AIML</div><div class="dev-target">🎯 MSc Candidate — Germany</div></div>', unsafe_allow_html=True)

# ── Hero
st.markdown('<div class="hero"><div class="hero-badge">🧠 NLP Powered</div><div class="hero-title">SentiAI</div><div class="hero-sub">Production-grade Sentiment Analysis · VADER · TextBlob · BERT</div></div><div class="divider"></div>', unsafe_allow_html=True)


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
    st.markdown('<div class="sec-title">📝 Single Text Analysis</div>', unsafe_allow_html=True)
    user_input = st.text_area("Enter text:", placeholder="Type or paste any text here...", height=130)
    col_btn, _ = st.columns([1, 4])
    with col_btn:
        go = st.button("Analyze →", use_container_width=True)

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
    col_btn, _ = st.columns([1, 4])
    with col_btn:
        go_all = st.button("Analyze All →", use_container_width=True)

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
                fig.patch.set_facecolor("#080B14")
                ax.set_facecolor("#080B14")
                sizes = [summary["Positive 😊"], summary["Negative 😞"], summary["Neutral 😐"]]
                wedges, _, autotexts = ax.pie(sizes, labels=["Positive", "Negative", "Neutral"], autopct="%1.1f%%", colors=["#00D4FF", "#FF4B4B", "#FFA500"], startangle=140, textprops={"color": "white", "fontsize": 10})
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
            col_btn, _ = st.columns([1, 4])
            with col_btn:
                go_csv = st.button("Analyze CSV →", use_container_width=True)

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
                fig.patch.set_facecolor("#080B14")
                ax.set_facecolor("#080B14")
                ax.bar(["Positive", "Negative", "Neutral"], [summary["Positive 😊"], summary["Negative 😞"], summary["Neutral 😐"]], color=["#00D4FF", "#FF4B4B", "#FFA500"], width=0.45)
                ax.tick_params(colors="#4A5568", labelsize=10)
                for sp in ax.spines.values():
                    sp.set_edgecolor("#1C2333")
                st.pyplot(fig)

                st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
                st.dataframe(df, use_container_width=True, hide_index=True)
                st.download_button("⬇️ Download Results", data=df.to_csv(index=False).encode("utf-8"), file_name="sentiment_results.csv", mime="text/csv", use_container_width=True)

# ══════════════════════════════════════════════════════
# MODE 4 — Dashboard
# ══════════════════════════════════════════════════════
elif mode == "📊 Dashboard":
    st.markdown('<div class="sec-title">📊 Analytics Dashboard</div>', unsafe_allow_html=True)
    try:
        from dashboard import load_and_analyze, plot_polarity_distribution, generate_wordcloud, get_top_sentences, plot_word_frequency

        col1, col2 = st.columns([2, 1])
        with col1:
            dash_file = st.file_uploader("Upload Dataset (CSV):", type=["csv"])
        with col2:
            limit = st.slider("Rows:", 10, 500, 50, 10)

        use_sample = st.checkbox("Use sample IMDB dataset", value=True)
        col_btn, _ = st.columns([1, 4])
        with col_btn:
            gen = st.button("Generate Dashboard →", use_container_width=True)

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