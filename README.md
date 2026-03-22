# 🧠 Sentiment Analysis Tool

A Python-based Sentiment Analysis web app that detects emotions in text using NLP. Built with TextBlob & Streamlit, it supports single text, bulk, and CSV analysis with real-time visualizations. Designed for scalability with upcoming BERT integration, REST API, and multilingual support.

## 🚀 Features
- Single text sentiment analysis
- Multiple texts analysis with pie chart
- CSV file upload and bulk analysis
- Download results as CSV

## 🛠️ Tech Stack
- Python 3.x
- TextBlob (NLP)
- Streamlit (UI)
- Pandas (Data)
- Matplotlib (Charts)

## ⚙️ Installation
```bash
git clone https://github.com/YOUR_USERNAME/sentiment-analysis-project.git
cd sentiment-analysis-project
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python -m textblob.download_corpora
```

## ▶️ Run the App
```bash
streamlit run app.py
```

## 📁 Project Structure
```
sentiment-analysis-project/
├── app.py            # Main Streamlit UI
├── analyzer.py       # Sentiment logic
├── utils.py          # Helper functions
├── data/
│   └── sample.csv    # Sample data
└── requirements.txt
```

## 👨‍💻 Developer
**Arup Das** — Brainware University, CSE (AIML)