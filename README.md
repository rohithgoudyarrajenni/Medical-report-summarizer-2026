# Medical Report Summarizer

A Python and Streamlit prototype that extracts supported laboratory results from text, compares values against supplied reference ranges, and generates a readable summary.

## Features
- Paste report text or upload TXT/PDF files
- Extract supported test names, values, units, and ranges
- Display structured results and summary counts
- Export extracted results to CSV
- Run automated unit tests

## Stack
Python, Streamlit, Pandas, NumPy, regular expressions, pypdf, unittest.

## Run locally
1. Install Python 3.10 or newer.
2. Run `pip install -r requirements.txt`.
3. Run `streamlit run app.py`.
4. Run tests using `python -m unittest discover -s tests -v`.

## Limitations
Supports a defined text format and numeric reference ranges. Scanned PDFs need OCR. This prototype is not a diagnostic tool. Verify extracted values against the original report.
