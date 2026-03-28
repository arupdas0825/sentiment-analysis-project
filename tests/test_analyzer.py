import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from analyzer import analyze_sentiment, analyze_multiple

# ── Test 1: Positive Text
def test_positive_sentiment():
    result = analyze_sentiment("I love this!", "VADER")
    assert result["label"] == "Positive"
    assert result["polarity"] > 0

# ── Test 2: Negative Text
def test_negative_sentiment():
    result = analyze_sentiment("I hate this terrible thing", "VADER")
    assert result["label"] == "Negative"
    assert result["polarity"] < 0

# ── Test 3: Empty Text
def test_empty_text():
    result = analyze_sentiment("", "VADER")
    assert result["label"] == "Empty"

# ── Test 4: TextBlob Engine
def test_textblob_engine():
    result = analyze_sentiment("This is amazing!", "TextBlob")
    assert result["engine"] == "TextBlob"
    assert result["label"] in ["Positive", "Negative", "Neutral"]

# ── Test 5: Multiple Texts
def test_multiple_texts():
    texts = ["I love it!", "I hate it!", "It is okay"]
    results = analyze_multiple(texts, "VADER")
    assert len(results) == 3

# ── Test 6: Confidence Score
def test_confidence_score():
    result = analyze_sentiment("Absolutely fantastic!", "VADER")
    assert 0 <= result["confidence"] <= 100

# ── Test 7: All Keys Present
def test_result_keys():
    result = analyze_sentiment("Hello world", "VADER")
    assert "label" in result
    assert "polarity" in result
    assert "confidence" in result
    assert "emoji" in result