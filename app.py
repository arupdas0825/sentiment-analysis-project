import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd
from analyzer import analyze_sentiment, analyze_multiple
from utils import load_csv, results_to_dataframe, get_summary

# ─── Page Config ───────────────────────────────────────
st.set_page_config(
    page_title="Sentiment Analysis Tool",
    page_icon="🧠",
    layout="wide"
)

# ─── Custom CSS ────────────────────────────────────────
st.markdown("""
    <style>
    .main { background-color: #0f0f0f; }
    .title { 
        font-size: 2.5rem; 
        font-weight: bold; 
        color: #00d4ff; 
        text-align: center;
    }
    .subtitle {
        text-align: center;
        color: #aaaaaa;
        margin-bottom: 2rem;
    }
    .result-box {
        background-color: #1e1e2e;
        border-radius: 12px;
        padding: 20px;
        margin-top: 10px;
    }
    </style>
""", unsafe_allow_html=True)

# ─── Title ─────────────────────────────────────────────
st.markdown('<div class="title">🧠 Sentiment Analysis Tool</div>', 
            unsafe_allow_html=True)
st.markdown('<div class="subtitle">Analyze emotions behind any text using AI</div>', 
            unsafe_allow_html=True)
st.divider()

# ─── Sidebar ───────────────────────────────────────────
st.sidebar.image(
    "https://upload.wikimedia.org/wikipedia/commons/c/c3/Python-logo-notext.svg",
    width=80
)
st.sidebar.title("⚙️ Options")
mode = st.sidebar.radio(
    "Mode select করো:",
    ["Single Text", "Multiple Texts", "Upload CSV"]
)
st.sidebar.divider()
st.sidebar.info("Made by **Arup** 🚀\nBrainware University")

# ══════════════════════════════════════════════════════
# MODE 1 — Single Text
# ══════════════════════════════════════════════════════
if mode == "Single Text":
    st.subheader("📝 Single Text Analysis")

    user_input = st.text_area(
        "তোমার text এখানে লেখো:",
        placeholder="e.g. I love programming in Python!",
        height=150
    )

    if st.button("🔍 Analyze", use_container_width=True):
        if user_input.strip():
            result = analyze_sentiment(user_input)

            col1, col2, col3 = st.columns(3)

            with col1:
                st.metric(
                    label="Sentiment",
                    value=f"{result['emoji']} {result['label']}"
                )
            with col2:
                st.metric(
                    label="Polarity",
                    value=result['polarity'],
                    help="-1 = Negative, +1 = Positive"
                )
            with col3:
                st.metric(
                    label="Subjectivity",
                    value=result['subjectivity'],
                    help="0 = Objective, 1 = Subjective"
                )

            # Polarity Bar
            st.divider()
            st.write("**Polarity Meter:**")
            polarity_pct = (result['polarity'] + 1) / 2
            st.progress(polarity_pct)

            if result['label'] == "Positive":
                st.success(f"✅ এই text-টা **Positive** sentiment বহন করছে!")
            elif result['label'] == "Negative":
                st.error(f"❌ এই text-টা **Negative** sentiment বহন করছে!")
            else:
                st.warning(f"⚠️ এই text-টা **Neutral** sentiment বহন করছে!")
        else:
            st.warning("কিছু একটা লেখো আগে!")

# ══════════════════════════════════════════════════════
# MODE 2 — Multiple Texts
# ══════════════════════════════════════════════════════
elif mode == "Multiple Texts":
    st.subheader("📋 Multiple Text Analysis")

    raw = st.text_area(
        "প্রতিটা line-এ একটা করে text লেখো:",
        placeholder="I love this!\nThis is terrible.\nThe day was okay.",
        height=200
    )

    if st.button("🔍 Analyze All", use_container_width=True):
        texts = [t.strip() for t in raw.strip().split("\n") if t.strip()]

        if texts:
            results = analyze_multiple(texts)
            df = results_to_dataframe(results)
            summary = get_summary(results)

            # Summary Cards
            st.divider()
            st.subheader("📊 Summary")
            cols = st.columns(4)
            for i, (key, val) in enumerate(summary.items()):
                cols[i].metric(key, val)

            # Pie Chart
            st.divider()
            st.subheader("🥧 Sentiment Distribution")
            labels = ["Positive 😊", "Negative 😞", "Neutral 😐"]
            sizes = [
                summary["Positive 😊"],
                summary["Negative 😞"],
                summary["Neutral 😐"]
            ]
            colors = ["#00d4ff", "#ff4b4b", "#ffa500"]

            fig, ax = plt.subplots(figsize=(5, 4))
            fig.patch.set_facecolor("#1e1e2e")
            ax.set_facecolor("#1e1e2e")
            wedges, texts_plt, autotexts = ax.pie(
                sizes,
                labels=labels,
                autopct="%1.1f%%",
                colors=colors,
                startangle=140,
                textprops={"color": "white"}
            )
            for at in autotexts:
                at.set_color("white")
            st.pyplot(fig)

            # Results Table
            st.divider()
            st.subheader("📄 Detailed Results")
            st.dataframe(df, use_container_width=True)

        else:
            st.warning("কিছু একটা লেখো আগে!")

# ══════════════════════════════════════════════════════
# MODE 3 — Upload CSV
# ══════════════════════════════════════════════════════
elif mode == "Upload CSV":
    st.subheader("📁 CSV File Upload")
    st.info("CSV file-এ অবশ্যই **'text'** নামের একটা column থাকতে হবে।")

    uploaded = st.file_uploader("CSV file choose করো:", type=["csv"])

    if uploaded:
        texts, error = load_csv(uploaded)

        if error:
            st.error(f"Error: {error}")
        else:
            st.success(f"✅ {len(texts)} টা text পাওয়া গেছে!")

            if st.button("🔍 Analyze CSV", use_container_width=True):
                results = analyze_multiple(texts)
                df = results_to_dataframe(results)
                summary = get_summary(results)

                # Summary
                st.divider()
                st.subheader("📊 Summary")
                cols = st.columns(4)
                for i, (key, val) in enumerate(summary.items()):
                    cols[i].metric(key, val)

                # Bar Chart
                st.divider()
                st.subheader("📊 Bar Chart")
                fig, ax = plt.subplots(figsize=(6, 3))
                fig.patch.set_facecolor("#1e1e2e")
                ax.set_facecolor("#1e1e2e")
                bars = ax.bar(
                    ["Positive", "Negative", "Neutral"],
                    [summary["Positive 😊"], 
                     summary["Negative 😞"], 
                     summary["Neutral 😐"]],
                    color=["#00d4ff", "#ff4b4b", "#ffa500"]
                )
                ax.tick_params(colors="white")
                for spine in ax.spines.values():
                    spine.set_edgecolor("#444")
                st.pyplot(fig)

                # Table + Download
                st.divider()
                st.subheader("📄 Detailed Results")
                st.dataframe(df, use_container_width=True)

                csv_out = df.to_csv(index=False).encode("utf-8")
                st.download_button(
                    "⬇️ Download Results CSV",
                    data=csv_out,
                    file_name="sentiment_results.csv",
                    mime="text/csv",
                    use_container_width=True
                )