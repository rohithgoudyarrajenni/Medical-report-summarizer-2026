
import re
import pandas as pd


def analyze_report(text):
    """
    Analyze extracted medical report text.
    Supports basic laboratory and radiology keyword detection.
    This is an educational aid, not a diagnostic system.
    """

    if not isinstance(text, str) or not text.strip():
        return pd.DataFrame(
            columns=["Section", "Finding", "Details"]
        )

    # Normalize text for matching
    normalized = re.sub(r"\s+", " ", text.lower()).strip()

    results = []

    def add(section, finding, details):
        results.append({
            "Section": section,
            "Finding": finding,
            "Details": details
        })

    # -----------------------------------
    # 1. UTERUS AND FIBROID FINDINGS
    # -----------------------------------
    if re.search(r"\b(mildly bulky|mild bulky|bulky uterus)\b", normalized):
        add(
            "Radiology",
            "Bulky uterus",
            "The report describes the uterus as mildly bulky."
        )

    if re.search(r"\bfibroid", normalized):
        measurements = re.findall(
            r"(\d+(?:\.\d+)?)\s*[x×]\s*(\d+(?:\.\d+)?)\s*mm",
            normalized
        )

        fibroid_details = (
            "The report mentions uterine fibroid(s). "
            "Clinical significance depends on symptoms and medical review."
        )

        if measurements:
            fibroid_details += (
                " Measurements detected in the report: "
                + ", ".join(
                    f"{a} × {b} mm" for a, b in measurements
                )
                + ". Check the original report to confirm which measurements "
                  "belong to the fibroids."
            )

        add(
            "Radiology",
            "Uterine fibroids",
            fibroid_details
        )

    # Detect explicitly described intramural lesions
    if "intramural" in normalized and (
        "lesion" in normalized or "fibroid" in normalized
    ):
        add(
            "Radiology",
            "Intramural uterine lesions",
            "The report describes lesion(s) within the uterine muscle wall."
        )

    # -----------------------------------
    # 2. OTHER RADIOLOGY FINDINGS
    # -----------------------------------
    if re.search(r"\b(normal ovaries|both ovaries are normal)\b", normalized):
        add(
            "Radiology",
            "Ovaries",
            "Both ovaries are described as normal in the report."
        )

    if "no free fluid" in normalized:
        add(
            "Radiology",
            "Free fluid",
            "No free fluid is reported in the examined area."
        )

    if "no ascites" in normalized:
        add(
            "Radiology",
            "Ascites",
            "No ascites is reported."
        )

    if "gaseous distension" in normalized or "bowel loops" in normalized:
        add(
            "Radiology",
            "Bowel gas",
            "Bowel gas or gaseous distension is mentioned. Interpret this finding clinically."
        )

    if (
        "kidneys are normal" in normalized
        or "both kidneys are normal" in normalized
    ):
        add(
            "Radiology",
            "Kidneys",
            "The kidneys are described as normal in the report."
        )

    if (
        "liver" in normalized
        and ("homogenous echotexture" in normalized
             or "homogeneous echotexture" in normalized)
    ):
        add(
            "Radiology",
            "Liver",
            "The liver is described as having homogeneous echotexture."
        )

    # -----------------------------------
    # 3. BASIC LABORATORY VALUE DETECTION
    # -----------------------------------
    # These are extracted values only; no diagnosis or reference
    # ranges are inferred from numbers alone.
    lab_patterns = [
        ("Hemoglobin", r"\b(?:haemoglobin|hemoglobin|hgb|hb)\b"),
        ("WBC", r"\b(?:wbc|white blood cell count|total leucocyte count)\b"),
        ("Platelets", r"\b(?:platelet count|platelets)\b"),
        ("Glucose", r"\b(?:blood glucose|fasting glucose|glucose)\b"),
        ("Creatinine", r"\bcreatinine\b"),
        ("Cholesterol", r"\bcholesterol\b"),
    ]

    for label, pattern in lab_patterns:
        if re.search(pattern, normalized):
            add(
                "Laboratory",
                label,
                f"The report contains a mention of {label}. "
                "Review the original value, units, and laboratory reference range."
            )

    # -----------------------------------
    # 4. FALLBACK WHEN NO RULE MATCHES
    # -----------------------------------
    if not results:
        add(
            "General",
            "No supported findings detected",
            "Text was extracted, but the current rules did not recognize "
            "specific findings. Review the extracted text and original report."
        )

    return pd.DataFrame(
        results,
        columns=["Section", "Finding", "Details"]
    )
