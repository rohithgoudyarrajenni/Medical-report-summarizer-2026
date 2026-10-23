
import re

MEDICAL_TERMS = {
    "mildly bulky uterus": {
        "meaning": (
            "The uterus is described as slightly larger than expected. "
            "The significance depends on the person's age, symptoms, "
            "and clinical assessment."
        ),
        "type": "Report terminology"
    },
    "uterine fibroids": {
        "meaning": (
            "Fibroids are growths made of muscle and connective tissue "
            "in or around the uterus. Many are non-cancerous, but their "
            "effect depends on their size, location, and symptoms."
        ),
        "type": "Report terminology"
    },
    "intramural": {
        "meaning": (
            "Intramural means located within the muscular wall of an "
            "organ. In this report, it refers to the muscular wall "
            "of the uterus."
        ),
        "type": "Medical term"
    },
    "ovaries": {
        "meaning": (
            "The ovaries are organs that produce eggs and hormones. "
            "The report describes both ovaries as normal."
        ),
        "type": "Anatomy"
    },
    "free fluid": {
        "meaning": (
            "Free fluid means fluid detected outside organs within "
            "the abdominal or pelvic cavity. The report states that "
            "no free fluid was seen."
        ),
        "type": "Report terminology"
    },
    "ascites": {
        "meaning": (
            "Ascites means an abnormal accumulation of fluid in the "
            "abdominal cavity. The report states that no ascites was seen."
        ),
        "type": "Medical term"
    },
    "gaseous distension": {
        "meaning": (
            "This means that gas has caused bowel loops to appear "
            "distended. Its significance depends on symptoms and "
            "the full clinical assessment."
        ),
        "type": "Report terminology"
    },
    "kidneys": {
        "meaning": (
            "The kidneys filter waste from the blood and produce urine. "
            "The report describes the kidneys as normal."
        ),
        "type": "Anatomy"
    },
    "liver": {
        "meaning": (
            "The liver is an organ that processes nutrients and helps "
            "remove waste. Homogeneous echotexture means its ultrasound "
            "appearance is described as uniform."
        ),
        "type": "Anatomy"
    },
    "hemoglobin": {
        "meaning": (
            "Hemoglobin is a protein in red blood cells that carries "
            "oxygen. Its value should be interpreted using the reported "
            "units and laboratory reference range."
        ),
        "type": "Laboratory term"
    },
    "white blood cells": {
        "meaning": (
            "White blood cells help the body fight infections and "
            "participate in immune responses. The count must be "
            "interpreted using the laboratory reference range."
        ),
        "type": "Laboratory term"
    },
    "platelets": {
        "meaning": (
            "Platelets are blood components that help blood clot. "
            "The reported count and laboratory reference range matter."
        ),
        "type": "Laboratory term"
    },
    "glucose": {
        "meaning": (
            "Glucose is a type of sugar in the blood that the body "
            "uses for energy. Interpretation depends on the value, "
            "units, and whether the test was fasting."
        ),
        "type": "Laboratory term"
    },
    "creatinine": {
        "meaning": (
            "Creatinine is a waste product measured in blood tests "
            "to help assess kidney function. It is interpreted alongside "
            "other clinical information."
        ),
        "type": "Laboratory term"
    },
    "cholesterol": {
        "meaning": (
            "Cholesterol is a fatty substance in the blood. Its "
            "significance depends on the measured level and overall "
            "cardiovascular risk."
        ),
        "type": "Laboratory term"
    }
}


def explain_medical_terms(text):
    if not isinstance(text, str) or not text.strip():
        return []

    normalized = re.sub(r"\s+", " ", text.lower())
    explanations = []

    for term, info in MEDICAL_TERMS.items():
        pattern = r"(?<!\w)" + re.escape(term) + r"(?!\w)"

        if re.search(pattern, normalized):
            explanations.append({
                "term": term.title(),
                "meaning": info["meaning"],
                "type": info["type"]
            })

    return explanations
