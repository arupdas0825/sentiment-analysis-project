from textblob import TextBlob
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from transformers import pipeline

# ─── VADER Analyzer ────────────────────────────────────
vader = SentimentIntensityAnalyzer()

# ─── BERT Analyzer (lazy load) ─────────────────────────
bert_analyzer = None

def load_bert():
    global bert_analyzer
    if bert_analyzer is None:
        bert_analyzer = pipeline(
            "sentiment-analysis",
            model="distilbert-base-uncased-finetuned-sst-2-english"
        )
    return bert_analyzer


# ══════════════════════════════════════════════════════
# TextBlob Analysis
# ══════════════════════════════════════════════════════
def analyze_textblob(text):
    blob = TextBlob(text)
    polarity = blob.sentiment.polarity
    subjectivity = blob.sentiment.subjectivity

    if polarity > 0.1:
        label = "Positive"
        emoji = "😊"
    elif polarity < -0.1:
        label = "Negative"
        emoji = "😞"
    else:
        label = "Neutral"
        emoji = "😐"

    return {
        "label": label,
        "polarity": round(polarity, 3),
        "subjectivity": round(subjectivity, 3),
        "confidence": round(abs(polarity) * 100, 1),
        "emoji": emoji,
        "engine": "TextBlob"
    }


# ══════════════════════════════════════════════════════
# VADER Analysis
# ══════════════════════════════════════════════════════
def analyze_vader(text):
    scores = vader.polarity_scores(text)
    compound = scores["compound"]

    if compound >= 0.05:
        label = "Positive"
        emoji = "😊"
    elif compound <= -0.05:
        label = "Negative"
        emoji = "😞"
    else:
        label = "Neutral"
        emoji = "😐"

    return {
        "label": label,
        "polarity": round(compound, 3),
        "subjectivity": round(scores["neu"], 3),
        "confidence": round(abs(compound) * 100, 1),
        "emoji": emoji,
        "engine": "VADER",
        "pos": round(scores["pos"], 3),
        "neg": round(scores["neg"], 3),
        "neu": round(scores["neu"], 3)
    }


# ══════════════════════════════════════════════════════
# BERT Analysis
# ══════════════════════════════════════════════════════
def analyze_bert(text):
    model = load_bert()

    # BERT max token limit 512
    truncated = text[:512]
    result = model(truncated)[0]

    raw_label = result["label"]
    score = result["score"]

    label = "Positive" if raw_label == "POSITIVE" else "Negative"
    emoji = "😊" if label == "Positive" else "😞"
    polarity = round(score if label == "Positive" else -score, 3)

    return {
        "label": label,
        "polarity": polarity,
        "subjectivity": 0.0,
        "confidence": round(score * 100, 1),
        "emoji": emoji,
        "engine": "BERT"
    }


# ══════════════════════════════════════════════════════
# Main Function — Engine Select করে Call হবে
# ══════════════════════════════════════════════════════
def analyze_sentiment(text, engine="VADER"):
    if not text.strip():
        return {
            "label": "Empty",
            "polarity": 0,
            "subjectivity": 0,
            "confidence": 0,
            "emoji": "❓",
            "engine": engine
        }

    if engine == "TextBlob":
        return analyze_textblob(text)
    elif engine == "BERT":
        return analyze_bert(text)
    else:
        return analyze_vader(text)


def analyze_multiple(texts, engine="VADER"):
    results = []
    for text in texts:
        result = analyze_sentiment(text, engine)
        result["text"] = text
        results.append(result)
    return results