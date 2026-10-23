
import io
import re
import streamlit as st

st.set_page_config(
    page_title="Medical Report Summarizer",
    page_icon="🩺",
    layout="wide"
)


def read_file(uploaded_file):
    try:
        from pypdf import PdfReader

        pdf_bytes = uploaded_file.getvalue()
        reader = PdfReader(io.BytesIO(pdf_bytes))

        pages = [page.extract_text() or "" for page in reader.pages]
        text = "\n".join(pages).strip()

        # OCR for scanned PDFs
        if len(text) < 100:
            from pdf2image import convert_from_bytes
            import pytesseract

            images = convert_from_bytes(pdf_bytes, dpi=200)

            ocr_pages = [
                pytesseract.image_to_string(image)
                for image in images
            ]
            text = "\n".join(ocr_pages).strip()

        # Clean extracted text
        text = text.replace("/n", "\n")
        text = text.replace("\\n", "\n")
        text = re.sub(r"\n{3,}", "\n\n", text)
        text = text.strip()

        if not text:
            raise ValueError(
                "No readable text found. Try a clearer PDF."
            )

        return text

    except Exception as e:
        raise RuntimeError(f"Could not read this PDF: {e}") from e


# Always render the interface first
st.title("🩺 Medical Report Summarizer")

st.write(
    "Upload a medical report PDF to extract text and "
    "identify findings supported by the analyzer."
)

st.info(
    "This tool provides educational summaries only. "
    "It does not diagnose medical conditions."
)

uploaded_file = st.file_uploader(
    "Choose a medical report (PDF)",
    type=["pdf"],
    key="medical_report"
)

if uploaded_file is not None:
    st.success(f"Selected file: {uploaded_file.name}")

    if st.button("Analyze Report", type="primary"):
        try:
            with st.spinner("Extracting report text..."):
                text = read_file(uploaded_file)

            st.subheader("Extracted Report Text")
            st.text_area(
                "Review the extracted text",
                value=text,
                height=250,
                key="extracted_text"
            )

            # Import the analyzer only when analysis is requested
            from analyzer import analyze_report

            with st.spinner("Analyzing report..."):
                results = analyze_report(text)

            st.subheader("Analysis Results")

            if results is None:
                st.warning("The analyzer returned no results.")

            elif hasattr(results, "empty") and results.empty:
                st.info(
                    "No supported findings were detected. "
                    "Please review the original report."
                )

            elif isinstance(results, str):
                st.write(results)

            elif isinstance(results, dict):
                st.json(results)

            else:
                st.dataframe(
                    results,
                    use_container_width=True,
                    hide_index=True
                )

        except Exception as e:
            st.error("The report could not be processed.")
            st.exception(e)

st.divider()

st.caption(
    "Always verify extracted text against the original report "
    "and consult a qualified healthcare professional."
)
