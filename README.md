
# 🩺 Medical Report Summarizer

A Python-based application that extracts text from medical reports, organizes recognized findings, and explains medical terminology in simple English using rule-based processing.

## ✨ Features

- 📄 Upload medical reports in PDF format.
- 🔍 Extract text from reports, including OCR support for scanned PDFs.
- 📊 Display a readable overview of recognized findings.
- 🩺 Organize supported findings into structured categories.
- 📖 Explain medical terms in simple English.
- 📏 Display recognized measurements where supported.
- 📥 Export structured findings to CSV.
- 🛡️ Include educational-use and medical verification disclaimers.

## 🛠️ Technologies Used

- Python
- Streamlit
- Pandas
- NumPy
- Regular Expressions
- pypdf
- pytesseract
- pdf2image

## ⚙️ How It Works

1. Upload a medical report as a PDF.
2. Extract report text using PDF text extraction or OCR when needed.
3. Analyze the extracted text using predefined rules.
4. Display recognized findings and supported measurements.
5. Match recognized medical terminology with predefined plain-English explanations.
6. Review the results and export structured findings when available.

## 📁 Project Structure

```text
Medical-report-summarizer-2026/
├── app.py
├── analyzer.py
├── medical_terms.py
├── requirements.txt
├── packages.txt
└── README.md
```

## 🚀 Run Locally

### 1. Clone the repository

```bash
git clone https://github.com/rohithgoudyarrajenni/Medical-report-summarizer-2026.git
```

### 2. Open the project folder

```bash
cd Medical-report-summarizer-2026
```

### 3. Install Python dependencies

```bash
pip install -r requirements.txt
```

### 4. Start the application

```bash
streamlit run app.py
```

## ⚠️ Limitations

- Analysis is based on predefined rules and supported medical terminology.
- OCR may introduce text extraction errors.
- Some findings, values, or measurements may not be recognized correctly.
- The application does not establish diagnoses or replace professional medical interpretation.

## 🔒 Privacy

Use fictional or appropriately de-identified reports for demonstrations. Avoid uploading sensitive medical information to public repositories or services without appropriate authorization and safeguards.

## 🎯 Project Purpose

This project demonstrates PDF text extraction, rule-based text analysis, data organization, and interactive application development using Python and Streamlit.

## 👨‍💻 Author

**Rohith Goud Yarrajenni**

GitHub: [rohithgoudyarrajenni](https://github.com/rohithgoudyarrajenni)

---

## 🚀 Live Application

**[Open Medical Report Summarizer](https://medical-report-summarizer-2026-wgpd5wn5mjr2txzyqynpbw.streamlit.app/)**

Try the application online to upload a report, view recognized findings, and explore medical terms explained in simple English.


*Educational project only. Always verify extracted information against the original report and consult a qualified healthcare professional for medical interpretation.*
