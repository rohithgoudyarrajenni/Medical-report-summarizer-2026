
import io
import re
import streamlit as st
import pytesseract
from pdf2image import convert_from_bytes
from pypdf import PdfReader

from analyzer import analyze_report


st.set_page_config(
    page_title="Medical Report Summarizer",
    page_icon="🩺",
    layout="wide"
)


def read_file(uploaded_file):
    pdf_bytes = uploaded_file.getvalue()

    # Extract text from a normal PDF
    reader = PdfReader(io.BytesIO(pdf_bytes))
    pages = [page.extract_text() or "" for page in reader.pages]
    text = "\n".join(pages).strip()

    # Use OCR for scanned PDFs
    if len(text) < 100:
        images = convert_from_bytes(pdf_bytes, dpi=200)
        ocr_pages = [
            pytesseract.image_to_string(image)
            for image in images
        ]
        text = "\n".join(ocr_pages).strip()

    # Clean up extracted text
    text = text.replace("/n", "\n")
    text = text.replace("\\n", "\n")
    text = re.sub(r"\n{3,}", "\n\n", text)
    text = text.strip()

    if not text:
        raise ValueError(
            "No readable text found. Try a clearer PDF."
        )

    return text


# Page interface
st.title("🩺 Medical Report Summarizer")
st.write(
    "Upload a medical report PDF to extract its text "
    "and review supported medical findings."
)

uploaded_file = st.file_uploader(
    "Upload your medical report",
    type=["pdf"]
)

if uploaded_file is not None:
    st.success(f"Uploaded: {uploaded_file.name}")

    if st.button("Analyze Report", type="primary"):
        with st.spinner("Reading your report..."):
            try:
                text = read_file(uploaded_file)

                st.subheader("Extracted Report Text")
                st.text_area(
                    "Review the extracted text",
                    value=text,
                    height=250
                )

                st.subheader("Analysis Results")

                # Run your existing analyzer
                results = analyze_report(text)

                if results:
                    st.write(results)
                else:
                    st.info(
                        "Text was extracted, but no supported "
                        "findings were identified. This analyzer "
                        "may not recognize narrative radiology "
                        "reports yet."
                    )

            except Exception as e:
                st.error(
                    "Could not process this PDF. "
                    "Check the app logs for details."
                )
                st.exception(e)

st.divider()
st.caption(
    "Educational support only. This tool does not provide "
    "a medical diagnosis. Consult a qualified healthcare professional."
)
