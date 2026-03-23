import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
from wordcloud import WordCloud
from analyzer import analyze_multiple
from collections import Counter
import re

matplotlib.use("Agg")


def load_and_analyze(filepath, engine="VADER", limit=100):
    df = pd.read_csv(filepath)
    if "text" not in df.columns:
        return None, "CSV-তে 'text' column নেই!"
    texts = df["text"].dropna().tolist()[:limit]
    results = analyze_multiple(texts, engine)
    result_df = pd.DataFrame(results)
    result_df["text"] = texts
    return result_df, None


def plot_polarity_distribution(df):
    fig, ax = plt.subplots(figsize=(8, 4))
    fig.patch.set_facecolor("#1e1e2e")
    ax.set_facecolor("#1e1e2e")
    colors = []
    for p in df["polarity"]:
        if p > 0.1:
            colors.append("#00d4ff")
        elif p < -0.1:
            colors.append("#ff4b4b")
        else:
            colors.append("#ffa500")
    ax.bar(range(len(df)), df["polarity"], color=colors, alpha=0.8)
    ax.axhline(y=0, color="white", linestyle="--", alpha=0.5)
    ax.set_xlabel("Text Index", color="white")
    ax.set_ylabel("Polarity Score", color="white")
    ax.set_title("Polarity Distribution", color="white", fontsize=14)
    ax.tick_params(colors="white")
    for spine in ax.spines.values():
        spine.set_edgecolor("#444")
    return fig


def generate_wordcloud(df, sentiment_filter="All"):
    if sentiment_filter != "All":
        filtered = df[df["label"] == sentiment_filter]
    else:
        filtered = df
    if filtered.empty:
        return None
    all_text = " ".join(filtered["text"].tolist())
    all_text = re.sub(r"[^a-zA-Z\s]", "", all_text.lower())
    stopwords = {
        "the", "a", "an", "is", "it", "this",
        "was", "and", "or", "but", "in", "on",
        "at", "to", "for", "of", "with", "i"
    }
    wc = WordCloud(
        width=800,
        height=400,
        background_color="#1e1e2e",
        colormap="cool",
        stopwords=stopwords,
        max_words=100
    ).generate(all_text)
    fig, ax = plt.subplots(figsize=(10, 5))
    fig.patch.set_facecolor("#1e1e2e")
    ax.imshow(wc, interpolation="bilinear")
    ax.axis("off")
    ax.set_title(
        f"Word Cloud — {sentiment_filter}",
        color="white",
        fontsize=14
    )
    return fig


def get_top_sentences(df, sentiment="Positive", n=5):
    filtered = df[df["label"] == sentiment]
    if filtered.empty:
        return []
    sorted_df = filtered.sort_values(
        "polarity",
        ascending=(sentiment == "Negative")
    )
    return sorted_df[["text", "polarity", "confidence"]].head(n).to_dict("records")


def plot_word_frequency(df, top_n=15):
    all_text = " ".join(df["text"].tolist()).lower()
    all_text = re.sub(r"[^a-zA-Z\s]", "", all_text)
    stopwords = {
        "the", "a", "an", "is", "it", "this", "was",
        "and", "or", "but", "in", "on", "at", "to",
        "for", "of", "with", "i", "my", "me"
    }
    words = [w for w in all_text.split() if w not in stopwords and len(w) > 2]
    freq = Counter(words).most_common(top_n)
    words_list = [f[0] for f in freq]
    counts = [f[1] for f in freq]
    fig, ax = plt.subplots(figsize=(8, 5))
    fig.patch.set_facecolor("#1e1e2e")
    ax.set_facecolor("#1e1e2e")
    ax.barh(words_list[::-1], counts[::-1], color="#00d4ff", alpha=0.8)
    ax.set_xlabel("Frequency", color="white")
    ax.set_title(f"Top {top_n} Most Frequent Words", color="white", fontsize=14)
    ax.tick_params(colors="white")
    for spine in ax.spines.values():
        spine.set_edgecolor("#444")
    return fig