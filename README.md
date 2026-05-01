# 🧠 Sentiment Analysis Tool

[![Python CI](https://github.com/arupdas0825/sentiment-analysis-project/actions/workflows/python-ci.yml/badge.svg)](https://github.com/arupdas0825/sentiment-analysis-project/actions/workflows/python-ci.yml)
[![Live Demo](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://sentiment-analysis-project-wcny5vwfqgnqhnjbbr9lbl.streamlit.app)
![Python](https://img.shields.io/badge/Python-3.11-blue?logo=python)
![FastAPI](https://img.shields.io/badge/FastAPI-REST%20API-green?logo=fastapi)
![License](https://img.shields.io/badge/License-MIT-yellow)

> A production-grade NLP-powered Sentiment Analysis platform built with
> multi-engine support, REST API, multilingual detection, and real-time
> analytics dashboard.

---

## 🌐 Live Demo
👉 [Click here to try the app](https://sentiment-analysis-project-zvtb4q6vncknfc5qvkb63w.streamlit.app/)

## Screenshots📸
<img width="1903" height="889" alt="image" src="https://github.com/user-attachments/assets/bd7407a8-bf6e-43ad-ae56-b523df934396" />
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
<img width="1904" height="863" alt="image" src="https://github.com/user-attachments/assets/cb602ea2-8543-4c37-97a9-5639ee1c89e1" />
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
<img width="1907" height="843" alt="image" src="https://github.com/user-attachments/assets/9fb02a57-9329-4566-bec2-f8132ebe8393" />
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━





---

## ✨ Features

### 🔍 Analysis Modes
- **Single Text** — Real-time sentiment with polarity meter
- **Multiple Texts** — Bulk analysis with pie chart visualization  
- **CSV Upload** — Upload any CSV and download results
- **📊 Analytics Dashboard** — WordCloud, frequency charts, top sentences

### 🧠 NLP Engines
| Engine | Speed | Accuracy | Best For |
|--------|-------|----------|----------|
| VADER | ⚡ Fast | ~85% | Social media, slang |
| TextBlob | ⚡⚡ Very Fast | ~70% | Simple text |
| BERT | 🐢 Slow | ~92% | High accuracy tasks |

### 🌍 Multilingual Support
- Auto language detection (Bengali, Hindi, German, French & more)
- Auto-translation to English before analysis
- Language flag badge in UI 🇧🇩 🇮🇳 🇩🇪

### 🚀 REST API (FastAPI)
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/health` | API status check |
| GET | `/engines` | Available engines info |
| POST | `/analyze` | Single text analysis |
| POST | `/analyze-bulk` | Bulk text (max 100) |
| POST | `/analyze-csv` | CSV file upload |

📖 Swagger UI: `http://127.0.0.1:8000/docs`

### ⚙️ DevOps
- GitHub Actions CI/CD pipeline
- Auto-test on every push with `pytest`
- Code quality check with `flake8`
- Deployed on Streamlit Cloud

---

## 🛠️ Tech Stack

| Category | Technology |
|----------|-----------|
| Language | Python 3.11 |
| UI | Streamlit |
| NLP | TextBlob, VADER, BERT (DistilBERT) |
| API | FastAPI + Uvicorn |
| Translation | Googletrans, Langdetect |
| Data | Pandas |
| Visualization | Matplotlib, WordCloud |
| Testing | Pytest, Flake8 |
| CI/CD | GitHub Actions |
| Deployment | Streamlit Cloud |

---

## 📁 Project Structure
```
sentiment-analysis-project/
│
├── .github/
│   └── workflows/
│       └── ci.yml          # GitHub Actions CI/CD
│
├── data/
│   ├── sample.csv          # Sample dataset
│   └── imdb.csv            # IMDB movie reviews dataset
│
├── tests/
│   └── test_analyzer.py    # Unit tests (7 tests)
│
├── app.py                  # Main Streamlit UI
├── analyzer.py             # Multi-engine NLP logic
├── api.py                  # FastAPI REST API
├── dashboard.py            # Analytics dashboard
├── translator.py           # Multilingual support
├── utils.py                # Helper functions
├── requirements.txt        # Dependencies
└── README.md
```

---

## ⚙️ Installation
```bash
# Clone the repository
git clone https://github.com/arupdas0825/sentiment-analysis-project.git
cd sentiment-analysis-project

# Create virtual environment
python -m venv venv
venv\Scripts\activate        # Windows
source venv/bin/activate     # Mac/Linux

# Install dependencies
pip install -r requirements.txt
python -m textblob.download_corpora
```

---

## ▶️ Run the App

### Streamlit UI
```bash
streamlit run app.py
```

### FastAPI REST API
```bash
uvicorn api:app --reload
# Swagger UI → http://127.0.0.1:8000/docs
```

### Run Tests
```bash
pytest tests/ -v
```

---

## 📊 Results Preview

| Text | Engine | Label | Polarity | Confidence |
|------|--------|-------|----------|------------|
| I love Python! | VADER | 😊 Positive | 0.677 | 67.7% |
| This is terrible | VADER | 😞 Negative | -0.68 | 68.0% |
| আমি খুশি | VADER+Translate | 😊 Positive | 0.59 | 59.0% |

---

## 🧪 Test Coverage
```
tests/test_analyzer.py
✅ test_positive_sentiment
✅ test_negative_sentiment  
✅ test_empty_text
✅ test_textblob_engine
✅ test_multiple_texts
✅ test_confidence_score
✅ test_result_keys

7 passed in 2.3s
```

---

## 🗺️ Roadmap

- [x] Multi-engine NLP (TextBlob, VADER, BERT)
- [x] Analytics Dashboard with WordCloud
- [x] Multilingual Support (Bengali, Hindi & more)
- [x] FastAPI REST API with Swagger UI
- [x] CI/CD Pipeline + Deployment
- [ ] Twitter/Reddit live sentiment analysis
- [ ] User authentication system
- [ ] Docker containerization
- [ ] Mobile app integration

---

## 👨‍💻 Developer

**Arup Das**  
B.Tech CSE (AIML) — Brainware University  
🎯 Targeting MSc in Germany

[![GitHub](https://img.shields.io/badge/GitHub-arupdas0825-black?logo=github)](https://github.com/arupdas0825)

---

## 📄 License

This project is licensed under the MIT License.
