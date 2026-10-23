
import re
import pandas as pd


def analyze_report(text):
    columns = ["Section", "Finding", "Details"]

    if not isinstance(text, str) or not text.strip():
        return pd.DataFrame(columns=columns)

    # Normalize OCR text for matching
    normalized = text.lower()
    normalized = normalized.replace("×", "x")
    normalized = re.sub(r"\s+", " ", normalized)

    results = []

    def add(section, finding, details):
        results.append({
            "Section": section,
            "Finding": finding,
            "Details": details
        })

    # UTERUS
    if re.search(r"mild(?:ly)?\s+bulky.{0,30}uterus|bulky\s+uterus", normalized):
        add(
            "Ultrasound",
            "Mildly bulky uterus",
            "The report describes the uterus as mildly bulky."
        )

    # FIBROIDS AND MEASUREMENTS
    if re.search(r"fibroid", normalized):
        add(
            "Ultrasound",
            "Uterine fibroids",
            "The report mentions uterine fibroids. "
            "A clinician can interpret their significance alongside symptoms."
        )

    # Intramural lesions
    if "intramural" in normalized and (
        "lesion" in normalized or "fibroid" in normalized
    ):
        measurements = re.findall(
            r"(\d{1,3})\s*x\s*(\d{1,3})\s*mm",
            normalized
        )

        detail = "The report describes intramural lesion(s) in the uterine muscle."

        if measurements:
            detail += (
                " Measurements found in the text: "
                + ", ".join(f"{a} x {b} mm" for a, b in measurements[:8])
                + ". Verify the measurements against the original report."
            )

        add(
            "Ultrasound",
            "Intramural uterine lesions",
            detail
        )

    # OVARIES
    if re.search(r"both ovaries are normal|normal in size.{0,50}ovaries", normalized):
        add(
            "Ultrasound",
            "Ovaries",
            "Both ovaries are described as normal in the report."
        )

    # FREE FLUID
    if re.search(r"no free fluid", normalized):
        add(
            "Ultrasound",
            "Free fluid",
            "No free fluid is reported."
        )

    # ASCITES
    if re.search(r"no ascites", normalized):
        add(
            "Ultrasound",
            "Ascites",
            "No ascites is reported."
        )

    # BOWEL GAS
    if re.search(r"gaseous distension|bowel loops", normalized):
        add(
            "Ultrasound",
            "Bowel gas",
            "Gaseous distension of bowel loops is mentioned in the report."
        )

    # KIDNEYS
    if re.search(r"both kidneys are normal|kidneys are normal in size", normalized):
        add(
            "Ultrasound",
            "Kidneys",
            "The kidneys are described as normal in the report."
        )

    # LIVER
    if re.search(r"liver.{0,100}(normal in size|homogenous echotexture|homogeneous echotexture)", normalized):
        add(
            "Ultrasound",
            "Liver",
            "The report describes the liver as normal in size and/or echotexture."
        )

    # LAB REPORT KEYWORDS
    lab_terms = [
        ("Hemoglobin", r"\b(hemoglobin|haemoglobin|hgb|hb)\b"),
        ("White blood cells", r"\b(wbc|white blood cell count|total leucocyte count)\b"),
        ("Platelets", r"\b(platelet count|platelets)\b"),
        ("Glucose", r"\b(glucose|blood sugar)\b"),
        ("Creatinine", r"\bcreatinine\b"),
        ("Cholesterol", r"\bcholesterol\b"),
    ]

    for name, pattern in lab_terms:
        if re.search(pattern, normalized):
            add(
                "Laboratory",
                name,
                f"The report mentions {name}. Check its value, units, "
                "and laboratory reference range."
            )

    if not results:
        add(
            "General",
            "No matching rules",
            "The extracted text did not match the current rules. "
            "Check the Extracted Report Text section for OCR quality."
        )

    return pd.DataFrame(results, columns=columns)
