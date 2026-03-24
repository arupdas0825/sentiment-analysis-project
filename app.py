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
    </style>
""", unsafe_allow_html=True)

# ─── Title ─────────────────────────────────────────────
st.markdown(
    '<div class="title">🧠 Sentiment Analysis Tool</div>',
    unsafe_allow_html=True
)
st.markdown(
    '<div class="subtitle">Analyze emotions behind any text using AI</div>',
    unsafe_allow_html=True
)
st.divider()

# ─── Sidebar ───────────────────────────────────────────
st.sidebar.image(
    "https://upload.wikimedia.org/wikipedia/commons/c/c3/Python-logo-notext.svg",
    width=80
)
st.sidebar.title("⚙️ Options")
mode = st.sidebar.radio(
    "Mode select করো:",
    ["Single Text", "Multiple Texts", "Upload CSV", "📊 Dashboard"]
)

st.sidebar.divider()

# NLP Engine
st.sidebar.subheader("🧠 NLP Engine")
engine = st.sidebar.radio(
    "Engine choose করো:",
    ["VADER", "TextBlob", "BERT"],
    help="VADER = Social media\nTextBlob = Simple\nBERT = Most accurate"
)

if engine == "VADER":
    st.sidebar.success("⚡ Fast | Great for social media")
elif engine == "TextBlob":
    st.sidebar.info("🔵 Basic | Good for simple sentences")
elif engine == "BERT":
    st.sidebar.warning("🤖 Slow first load | Highest accuracy")

st.sidebar.divider()

# Multilingual Toggle
st.sidebar.subheader("🌍 Language")
multilingual = st.sidebar.toggle(
    "Auto-detect & Translate",
    value=False,
    help="Bengali, Hindi সহ যেকোনো ভাষা detect করে translate করবে"
)

st.sidebar.divider()
st.sidebar.info("Made by **Arup** 🚀\nBrainware University")


# ══════════════════════════════════════════════════════
# HELPER — Translation
# ══════════════════════════════════════════════════════
def apply_translation(text):
    from translator import translate_to_english
    trans = translate_to_english(text)
    lang = trans["lang_info"]
    st.info(
        f"{lang['flag']} **{lang['name']}** detected"
        + (" → Translated to English ✅"
           if trans["was_translated"] else " (No translation needed)")
    )
    if trans["was_translated"]:
        st.caption(f"📝 Translated: *{trans['translated']}*")
    return trans["translated"]


# ══════════════════════════════════════════════════════
# MODE 1 — Single Text
# ══════════════════════════════════════════════════════
if mode == "Single Text":
    st.subheader("📝 Single Text Analysis")

    user_input = st.text_area(
        "তোমার text এখানে লেখো:",
        placeholder="e.g. আমি তোমাকে ভালোবাসি / I love Python!",
        height=150
    )

    if st.button("🔍 Analyze", use_container_width=True):
        if user_input.strip():
            with st.spinner("Analyzing..."):
                if multilingual:
                    analysis_text = apply_translation(user_input)
                else:
                    analysis_text = user_input

                result = analyze_sentiment(analysis_text, engine)

            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric(
                    "Sentiment",
                    f"{result['emoji']} {result['label']}"
                )
            with col2:
                st.metric(
                    "Polarity",
                    result['polarity'],
                    help="-1 = Negative, +1 = Positive"
                )
            with col3:
                st.metric(
                    "Subjectivity",
                    result['subjectivity'],
                    help="0 = Objective, 1 = Subjective"
                )
            with col4:
                st.metric(
                    "Confidence",
                    f"{result['confidence']}%"
                )

            # VADER extra scores
            if engine == "VADER" and "pos" in result:
                st.divider()
                v1, v2, v3 = st.columns(3)
                v1.metric("Positive Score", result["pos"])
                v2.metric("Negative Score", result["neg"])
                v3.metric("Neutral Score",  result["neu"])

            st.divider()
            st.write("**Polarity Meter:**")
            polarity_pct = (result['polarity'] + 1) / 2
            st.progress(polarity_pct)

            if result['label'] == "Positive":
                st.success("✅ এই text-টা **Positive** sentiment বহন করছে!")
            elif result['label'] == "Negative":
                st.error("❌ এই text-টা **Negative** sentiment বহন করছে!")
            else:
                st.warning("⚠️ এই text-টা **Neutral** sentiment বহন করছে!")
        else:
            st.warning("কিছু একটা লেখো আগে!")


# ══════════════════════════════════════════════════════
# MODE 2 — Multiple Texts
# ══════════════════════════════════════════════════════
elif mode == "Multiple Texts":
    st.subheader("📋 Multiple Text Analysis")

    raw = st.text_area(
        "প্রতিটা line-এ একটা করে text লেখো:",
        placeholder="I love this!\nThis is terrible.\nআমি খুশি।",
        height=200
    )

    if st.button("🔍 Analyze All", use_container_width=True):
        texts = [t.strip() for t in raw.strip().split("\n") if t.strip()]

        if texts:
            with st.spinner("Analyzing all texts..."):
                if multilingual:
                    from translator import translate_multiple
                    trans_results = translate_multiple(texts)

                    translated_count = sum(
                        1 for t in trans_results if t["was_translated"]
                    )
                    if translated_count > 0:
                        st.info(
                            f"🌍 {translated_count} টা text translate হয়েছে"
                        )

                    lang_counts = {}
                    for t in trans_results:
                        lang = t["lang_info"]["name"]
                        lang_counts[lang] = lang_counts.get(lang, 0) + 1

                    st.write("**Detected Languages:**")
                    for lang, count in lang_counts.items():
                        st.write(f"  • {lang}: {count} texts")

                    analysis_texts = [t["translated"] for t in trans_results]
                else:
                    analysis_texts = texts

                results = analyze_multiple(analysis_texts, engine)

            df = results_to_dataframe(results)
            summary = get_summary(results)

            st.divider()
            st.subheader("📊 Summary")
            cols = st.columns(4)
            for i, (key, val) in enumerate(summary.items()):
                cols[i].metric(key, val)

            st.divider()
            st.subheader("🥧 Sentiment Distribution")
            labels_list = ["Positive 😊", "Negative 😞", "Neutral 😐"]
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
                labels=labels_list,
                autopct="%1.1f%%",
                colors=colors,
                startangle=140,
                textprops={"color": "white"}
            )
            for at in autotexts:
                at.set_color("white")
            st.pyplot(fig)

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
                with st.spinner("Analyzing CSV..."):
                    if multilingual:
                        from translator import translate_multiple
                        trans_results = translate_multiple(texts)
                        analysis_texts = [
                            t["translated"] for t in trans_results
                        ]
                    else:
                        analysis_texts = texts

                    results = analyze_multiple(analysis_texts, engine)

                df = results_to_dataframe(results)
                summary = get_summary(results)

                st.divider()
                st.subheader("📊 Summary")
                cols = st.columns(4)
                for i, (key, val) in enumerate(summary.items()):
                    cols[i].metric(key, val)

                st.divider()
                st.subheader("📊 Bar Chart")
                fig, ax = plt.subplots(figsize=(6, 3))
                fig.patch.set_facecolor("#1e1e2e")
                ax.set_facecolor("#1e1e2e")
                ax.bar(
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


# ══════════════════════════════════════════════════════
# MODE 4 — Analytics Dashboard
# ══════════════════════════════════════════════════════
elif mode == "📊 Dashboard":
    from dashboard import (
        load_and_analyze,
        plot_polarity_distribution,
        generate_wordcloud,
        get_top_sentences,
        plot_word_frequency
    )

    st.subheader("📊 Analytics Dashboard")
    st.info("Real dataset load করে full analysis দেখাও!")

    col_upload, col_limit = st.columns(2)
    with col_upload:
        dash_file = st.file_uploader(
            "Dataset upload করো (CSV):",
            type=["csv"],
            key="dashboard_upload"
        )
    with col_limit:
        limit = st.slider(
            "কতটা row analyze করবো?",
            min_value=10,
            max_value=500,
            value=50,
            step=10
        )

    use_sample = st.checkbox("Sample IMDB dataset use করো", value=True)

    if st.button("🚀 Generate Dashboard", use_container_width=True):
        with st.spinner("Dashboard তৈরি হচ্ছে..."):
            if use_sample:
                df, error = load_and_analyze(
                    "data/imdb.csv", engine, limit
                )
            elif dash_file:
                import tempfile, os
                with tempfile.NamedTemporaryFile(
                    delete=False, suffix=".csv"
                ) as tmp:
                    tmp.write(dash_file.read())
                    tmp_path = tmp.name
                df, error = load_and_analyze(tmp_path, engine, limit)
                os.unlink(tmp_path)
            else:
                st.warning(
                    "File upload করো অথবা sample dataset select করো!"
                )
                st.stop()

        if error:
            st.error(error)
        else:
            total = len(df)
            pos   = len(df[df["label"] == "Positive"])
            neg   = len(df[df["label"] == "Negative"])
            neu   = len(df[df["label"] == "Neutral"])
            avg_conf = round(df["confidence"].mean(), 1)

            st.divider()
            st.subheader("📈 Overview")
            c1, c2, c3, c4, c5 = st.columns(5)
            c1.metric("Total", total)
            c2.metric("Positive 😊", pos)
            c3.metric("Negative 😞", neg)
            c4.metric("Neutral 😐",  neu)
            c5.metric("Avg Confidence", f"{avg_conf}%")

            st.divider()
            st.subheader("📉 Polarity Distribution")
            st.pyplot(plot_polarity_distribution(df))

            st.divider()
            st.subheader("🔤 Word Frequency")
            st.pyplot(plot_word_frequency(df))

            st.divider()
            st.subheader("☁️ Word Cloud")
            wc_filter = st.selectbox(
                "Filter by sentiment:",
                ["All", "Positive", "Negative", "Neutral"]
            )
            wc_fig = generate_wordcloud(df, wc_filter)
            if wc_fig:
                st.pyplot(wc_fig)

            st.divider()
            col_pos, col_neg = st.columns(2)
            with col_pos:
                st.subheader("🏆 Top 5 Positive")
                for i, row in enumerate(
                    get_top_sentences(df, "Positive", 5), 1
                ):
                    st.markdown(
                        f"**{i}.** {row['text'][:80]}...  "
                        f"`Polarity: {row['polarity']}`"
                    )
            with col_neg:
                st.subheader("💔 Top 5 Negative")
                for i, row in enumerate(
                    get_top_sentences(df, "Negative", 5), 1
                ):
                    st.markdown(
                        f"**{i}.** {row['text'][:80]}...  "
                        f"`Polarity: {row['polarity']}`"
                    )

            st.divider()
            st.subheader("📄 Full Results")
            st.dataframe(
                df[["text", "label", "polarity", "confidence"]],
                use_container_width=True
            )

            csv_out = df.to_csv(index=False).encode("utf-8")
            st.download_button(
                "⬇️ Download Full Results",
                data=csv_out,
                file_name="dashboard_results.csv",
                mime="text/csv",
                use_container_width=True
            )