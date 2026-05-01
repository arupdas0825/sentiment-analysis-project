
import streamlit as st
from fpdf import FPDF
import base64

def generate_pdf_report(res, text):
    pdf = FPDF()
    pdf.add_page()
    
    # Title
    pdf.set_font("Arial", 'B', 24)
    pdf.set_text_color(0, 194, 255)
    pdf.cell(200, 20, "SentiAI Pro - Sentiment Report", ln=True, align='C')
    
    pdf.ln(10)
    
    # Section: Input
    pdf.set_font("Arial", 'B', 14)
    pdf.set_text_color(50, 50, 50)
    pdf.cell(200, 10, "Analyzed Content:", ln=True)
    pdf.set_font("Arial", '', 12)
    pdf.multi_cell(0, 10, text)
    
    pdf.ln(10)
    
    # Section: Results
    pdf.set_font("Arial", 'B', 14)
    pdf.cell(200, 10, "Analysis Metrics:", ln=True)
    pdf.set_font("Arial", '', 12)
    pdf.cell(200, 10, f"Sentiment: {res['label']}", ln=True)
    pdf.cell(200, 10, f"Polarity: {res['polarity']}", ln=True)
    pdf.cell(200, 10, f"Confidence: {res['confidence']}%", ln=True)
    pdf.cell(200, 10, f"Emotion: {res.get('emotion', 'N/A')}", ln=True)
    pdf.cell(200, 10, f"Toxicity: {res.get('toxicity', 0)}%", ln=True)
    
    pdf.ln(10)
    
    # AI Summary
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(200, 10, "AI Generated Explanation:", ln=True)
    pdf.set_font("Arial", 'I', 11)
    pdf.multi_cell(0, 10, res.get('ai_explanation', 'No explanation provided.'))
    
    return pdf.output(dest='S').encode('latin-1')

def get_pdf_download_link(pdf_bytes, filename="report.pdf"):
    b64 = base64.b64encode(pdf_bytes).decode()
    return f'<a href="data:application/octet-stream;base64,{b64}" download="{filename}" style="text-decoration: none;"><div style="background: var(--primary); color: #000; padding: 0.75rem; border-radius: 12px; text-align: center; font-weight: bold; margin-top: 1rem;">⬇️ DOWNLOAD PDF REPORT</div></a>'

# Mock functions for advanced features
def analyze_voice(audio_file):
    return {"sentiment": "Positive", "confidence": 88.5, "emotion": "Calm", "pitch": "Medium"}

def analyze_youtube(url):
    return {"title": "Sample Video", "sentiment": "Mixed", "total_comments": 1500, "pos_perc": 45, "neg_perc": 30, "neu_perc": 25}

def analyze_pdf(pdf_file):
    return {"pages": 12, "sentiment": "Formal / Professional", "confidence": 92.0}
