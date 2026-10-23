
import re
import pandas as pd


def analyze_report(text):
    columns = ["Section", "Finding", "Details"]

    if not isinstance(text, str) or not text.strip():
        return pd.DataFrame(columns=columns)

    normalized = text.lower().replace("×", "x")
    normalized = re.sub(r"\s+", " ", normalized)

    results = []

    def add(section, finding, details):
        results.append({
            "Section": section,
            "Finding": finding,
            "Details": details
        })

    # Bulky uterus
    if re.search(r"mild(?:ly)?\s+bulky.{0,30}uterus|bulky\s+uterus", normalized):
        add(
            "Ultrasound",
            "Mildly bulky uterus",
            "The report describes the uterus as mildly bulky."
        )

    # Fibroids
    if "fibroid" in normalized:
        add(
            "Ultrasound",
            "Uterine fibroids",
            "The report mentions uterine fibroids. "
            "Their significance depends on symptoms and clinical review."
        )

    # Extract measurements only from the two uterine lesion descriptions
    lesion_measurements = []

    for location in ["posterior", "anterior"]:
        pattern = (
            rf"{location}\s+myometrium.{{0,250}}?"
            rf"(?:measuring|measures)\s*"
            rf"(\d{{1,3}})\s*x\s*(\d{{1,3}})\s*mm"
        )

        match = re.search(pattern, normalized)

        if match:
            lesion_measurements.append(
                f"{location.title()} lesion: "
                f"{match.group(1)} x {match.group(2)} mm"
            )

    if "intramural" in normalized and (
        "lesion" in normalized or "fibroid" in normalized
    ):
        details = "The report describes lesion(s) within the uterine muscle."

        if lesion_measurements:
            details += " Reported measurements: " + "; ".join(
                lesion_measurements
            ) + "."

        details += " Verify measurements against the original report."

        add(
            "Ultrasound",
            "Intramural uterine lesions",
            details
        )

    # Ovaries
    if "both ovaries are normal" in normalized:
        add(
            "Ultrasound",
            "Ovaries",
            "Both ovaries are described as normal in the report."
        )

    # Free fluid
    if "no free fluid" in normalized:
        add(
            "Ultrasound",
            "Free fluid",
            "No free fluid is reported."
        )

    # Ascites
    if "no ascites" in normalized:
        add(
            "Ultrasound",
            "Ascites",
            "No ascites is reported."
        )

    # Bowel gas
    if "gaseous distension" in normalized or "bowel loops" in normalized:
        add(
            "Ultrasound",
            "Bowel gas",
            "Gaseous distension of bowel loops is mentioned."
        )

    # Kidneys
    if "both kidneys are normal" in normalized:
        add(
            "Ultrasound",
            "Kidneys",
            "The kidneys are described as normal in the report."
        )

    # Liver
    if (
        "liver" in normalized
        and (
            "homogenous echotexture" in normalized
            or "homogeneous echotexture" in normalized
        )
    ):
        add(
            "Ultrasound",
            "Liver",
            "The report describes homogeneous liver echotexture."
        )

    # Basic laboratory report keywords
    lab_terms = [
        ("Hemoglobin", r"\b(hemoglobin|haemoglobin|hgb|hb)\b"),
        ("White blood cells", r"\b(wbc|white blood cell count)\b"),
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
                f"The report mentions {name}. Check the reported value, "
                "units, and laboratory reference range."
            )

    if not results:
        add(
            "General",
            "No matching rules",
            "No supported findings matched the current rules. "
            "Review the extracted text and original report."
        )

    return pd.DataFrame(results, columns=columns)
