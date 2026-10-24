
from medical_terms import explain_medical_terms
import io
import re
import pandas as pd
import streamlit as st

st.set_page_config(
    page_title="Medical Report Summarizer",
    page_icon="🩺",
    layout="wide",
    initial_sidebar_state="expanded"
)


# -----------------------------
# PDF TEXT EXTRACTION + OCR
# -----------------------------
def read_file(uploaded_file):
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
        text = "\n".join(
            pytesseract.image_to_string(image)
            for image in images
        ).strip()

    # Normalize line breaks and whitespace
    text = text.replace("/n", "\n")
    text = text.replace("\\n", "\n")
    text = re.sub(r"\n{3,}", "\n\n", text).strip()

    if not text:
        raise ValueError(
            "No readable text was found. Try a clearer PDF."
        )

    return text


# -----------------------------
# HEADER
# -----------------------------
st.title("🩺 Medical Report Summarizer")

st.write(
    "Extract report text and organize recognized findings "
    "into a readable overview."
)

st.caption(
    "Educational support only — not a diagnostic tool. "
    "Verify all findings against the original report."
)

st.divider()


# -----------------------------
# SIDEBAR
# -----------------------------
with st.sidebar:
    st.header("📄 Report Upload")
    st.write("Upload a PDF medical report to begin.")

    uploaded_file = st.file_uploader(
        "Choose PDF",
        type=["pdf"],
        key="medical_report"
    )

    st.divider()
    st.subheader("Features")
    st.write("🔎 PDF text extraction")
    st.write("🖨️ OCR for scanned PDFs")
    st.write("📊 Findings overview")
    st.write("📖 Medical terms in simple English")
    st.write("⬇️ CSV export")


# -----------------------------
# MAIN PAGE: WELCOME
# -----------------------------
if uploaded_file is None:
    st.subheader("Welcome")

    st.write(
        "Start by uploading a medical report using the sidebar."
    )

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("### 🔍")
        st.markdown("**Extract**")
        st.write(
            "Read text from digital and scanned PDFs."
        )

    with col2:
        st.markdown("### 📋")
        st.markdown("**Organize**")
        st.write(
            "Group recognized findings into a clear table."
        )

    with col3:
        st.markdown("### 📥")
        st.markdown("**Export**")
        st.write(
            "Download the analysis as a CSV file."
        )


# -----------------------------
# ANALYZE REPORT
# -----------------------------
else:
    st.success(f"Selected report: {uploaded_file.name}")

    if st.button(
        "🚀 Analyze Report",
        type="primary",
        use_container_width=True
    ):
        try:
            with st.spinner("Extracting report text..."):
                report_text = read_file(uploaded_file)

            from analyzer import analyze_report

            with st.spinner("Organizing findings..."):
                results = analyze_report(report_text)

            # Convert analyzer output into a DataFrame
            if isinstance(results, pd.DataFrame):
                findings = results.copy()

            elif isinstance(results, list):
                findings = pd.DataFrame(results)

            elif isinstance(results, dict):
                findings = pd.DataFrame([results])

            elif isinstance(results, str):
                findings = pd.DataFrame([
                    {
                        "Section": "General",
                        "Finding": "Summary",
                        "Details": results
                    }
                ])

            else:
                findings = pd.DataFrame()

            # Save results in Streamlit session state
            st.session_state["report_text"] = report_text
            st.session_state["report_findings"] = findings
            st.session_state["report_filename"] = uploaded_file.name

            st.success("Report analyzed successfully!")

        except Exception as e:
            st.error("The report could not be processed.")
            st.exception(e)


# -----------------------------
# DISPLAY ANALYSIS
# -----------------------------
if "report_text" in st.session_state:

    report_text = st.session_state["report_text"]
    findings = st.session_state["report_findings"]

    st.divider()
    st.header("📊 Report Overview")

    total = len(findings)

    # Count recognized report sections
    if total > 0 and "Section" in findings.columns:
        sections = findings["Section"].fillna("").astype(str)

        radiology_count = int(
            sections.str.contains(
                "ultrasound|radiology",
                case=False,
                regex=True
            ).sum()
        )

        laboratory_count = int(
            sections.str.contains(
                "laboratory|lab",
                case=False,
                regex=True
            ).sum()
        )

    else:
        radiology_count = 0
        laboratory_count = 0

    c1, c2, c3 = st.columns(3)

    c1.metric("Recognized Entries", total)
    c2.metric("Radiology Entries", radiology_count)
    c3.metric("Laboratory Entries", laboratory_count)

    st.caption(
        "These numbers count rule matches, not disease severity "
        "or the number of confirmed medical conditions."
    )

    # -----------------------------
    # KEY FINDINGS
    # -----------------------------
    st.divider()
    st.header("🔎 Key Findings")

    if findings.empty:
        st.info(
            "No findings were returned by the analyzer."
        )

    elif "Finding" in findings.columns:
        for _, row in findings.iterrows():

            finding_name = str(
                row.get("Finding", "Finding")
            )

            section_name = str(
                row.get("Section", "General")
            )

            details = str(
                row.get("Details", "")
            )

            with st.container(border=True):
                st.markdown(f"**{finding_name}**")
                st.caption(section_name)
                st.write(details)

    else:
        st.info(
            "The analyzer returned data, but no Finding column "
            "was available to display individual findings."
        )

    # -----------------------------
    # MEDICAL TERMS IN SIMPLE ENGLISH
    # -----------------------------
    st.divider()
    st.header("📖 Medical Terms in Simple English")

    try:
        term_explanations = explain_medical_terms(report_text)

        if term_explanations:
            st.caption(
                "Plain-language explanations of terms found in "
                "the report. Educational use only — not a diagnosis."
            )

            for item in term_explanations:
                st.markdown(f"### 🔹 {item['term']}")
                st.caption(item["type"])
                st.write(item["meaning"])
                st.divider()

        else:
            st.info(
                "No supported medical terms found in this report."
            )

    except Exception as e:
        st.warning(
            "Medical term explanations could not be generated. "
            "You can still view your report findings below."
        )
        st.exception(e)

    # -----------------------------
    # FINDINGS TABLE + CSV DOWNLOAD
    # -----------------------------
    st.divider()
    st.header("📥 Export Findings")

    if not findings.empty:
        st.dataframe(
            findings,
            use_container_width=True,
            hide_index=True
        )

        csv_data = findings.to_csv(
            index=False
        ).encode("utf-8")

        st.download_button(
            label="⬇️ Download Findings as CSV",
            data=csv_data,
            file_name="medical_report_findings.csv",
            mime="text/csv",
            use_container_width=True
        )

    else:
        st.info(
            "No findings are available to export."
        )

    # -----------------------------
    # ORIGINAL EXTRACTED TEXT
    # -----------------------------
    st.divider()
    st.header("📄 Extracted Report Text")

    with st.expander("View original extracted text"):
        st.text_area(
            "Extracted text",
            value=report_text,
            height=300,
            disabled=True
        )

    # -----------------------------
    # MEDICAL DISCLAIMER
    # -----------------------------
    st.warning(
        "This application uses text extraction and rule-based "
        "matching. It may miss findings or misinterpret OCR errors. "
        "It does not diagnose conditions. Confirm the report with "
        "a qualified clinician."
    )


# -----------------------------
# FOOTER
# -----------------------------
st.divider()
st.caption("Medical Report Summarizer")
