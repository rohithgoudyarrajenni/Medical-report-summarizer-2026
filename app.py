import streamlit as st
from io import BytesIO
from pypdf import PdfReader
from analyzer import analyze_report, generate_summary

st.set_page_config(page_title="Medical Report Summarizer", page_icon="🩺", layout="wide")
st.title("🩺 Medical Report Summarizer")
st.write("Extract supported laboratory results and generate a readable summary.")
st.warning("Educational prototype only. Not intended for diagnosis or treatment decisions.")

SAMPLE = """Hemoglobin: 10.5 g/dL (Reference range: 12.0-16.0)
WBC: 7500 cells/uL (Reference range: 4000-11000)
Platelets: 250000 cells/uL (Reference range: 150000-450000)
Glucose: 105 mg/dL (Reference range: 70-100)"""

def read_file(upload):
    if upload is None:
        return ""
    data = upload.getvalue()
    if upload.name.lower().endswith(".txt"):
        return data.decode("utf-8", errors="replace")
    reader = PdfReader(BytesIO(data))
    if reader.is_encrypted:
        raise ValueError("Password-protected PDFs are not supported.")
    return "\\n".join(page.extract_text() or "" for page in reader.pages)

upload = st.file_uploader("Upload report", type=["txt", "pdf"])
try:
    initial = read_file(upload) if upload else SAMPLE
except Exception as exc:
    initial = ""
    st.error(f"Could not read file: {exc}")

text = st.text_area("Medical report text", value=initial, height=220)

if st.button("Analyze Report", type="primary"):
    df = analyze_report(text)
    if df.empty:
        st.warning("No supported results found. Use the sample format. Scanned PDFs need OCR.")
    else:
        st.subheader("Summary")
        st.markdown(generate_summary(df))
        a, b, c = st.columns(3)
        a.metric("Below range", int((df["Status"] == "Below reference range").sum()))
        b.metric("Within range", int((df["Status"] == "Within reference range").sum()))
        c.metric("Above range", int((df["Status"] == "Above reference range").sum()))
        st.subheader("Extracted Results")
        st.dataframe(df, use_container_width=True, hide_index=True)
        st.download_button(
            "Download CSV", df.to_csv(index=False).encode("utf-8"),
            "medical_report_results.csv", "text/csv"
        )
        st.caption("Automated range comparisons are informational and not a diagnosis.")
