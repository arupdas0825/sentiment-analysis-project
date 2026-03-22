from textblob import TextBlob

def analyze_sentiment(text):
    if not text.strip():
        return {
            "label": "Empty",
            "polarity": 0,
            "subjectivity": 0,
            "emoji": "❓"
        }

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
        "emoji": emoji
    }


def analyze_multiple(texts):
    results = []
    for text in texts:
        result = analyze_sentiment(text)
        result["text"] = text
        results.append(result)
    return results