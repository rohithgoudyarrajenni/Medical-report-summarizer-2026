
import io
import re
import pytesseract
import streamlit as st
from pdf2image import convert_from_bytes
from pypdf import PdfReader


def read_file(uploaded_file):
    pdf_bytes = uploaded_file.getvalue()

    # Step 1: Try extracting normal PDF text
    reader = PdfReader(io.BytesIO(pdf_bytes))
    pages = [page.extract_text() or "" for page in reader.pages]
    text = "\n".join(pages).strip()

    # Step 2: Use OCR if the PDF is scanned or has little text
    if len(text) < 100:
        images = convert_from_bytes(pdf_bytes, dpi=200)
        ocr_pages = [
            pytesseract.image_to_string(image)
            for image in images
        ]
        text = "\n".join(ocr_pages).strip()

    # Step 3: Fix incorrectly represented newline sequences
    text = text.replace("/n", "\n")
    text = text.replace("\\n", "\n")
    text = re.sub(r"\n{3,}", "\n\n", text)
    text = text.strip()

    if not text:
        raise ValueError(
            "No readable text found. Try a clearer scanned PDF."
        )

    return text
