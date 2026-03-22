import pandas as pd

def load_csv(file):
    try:
        df = pd.read_csv(file)
        if "text" not in df.columns:
            return None, "CSV file-এ 'text' নামের column থাকতে হবে!"
        texts = df["text"].dropna().tolist()
        return texts, None
    except Exception as e:
        return None, str(e)


def results_to_dataframe(results):
    df = pd.DataFrame(results)
    df = df[["text", "label", "polarity", "subjectivity", "emoji"]]
    return df


def get_summary(results):
    total = len(results)
    positive = sum(1 for r in results if r["label"] == "Positive")
    negative = sum(1 for r in results if r["label"] == "Negative")
    neutral = sum(1 for r in results if r["label"] == "Neutral")
    return {
        "Total": total,
        "Positive 😊": positive,
        "Negative 😞": negative,
        "Neutral 😐": neutral
    }

