
import re
import numpy as np
import pandas as pd

PATTERN = re.compile(
    r"(?P<name>[A-Za-z][A-Za-z0-9 /_-]{0,50}?)\s*:\s*"
    r"(?P<value>[-+]?\d+(?:\.\d+)?)\s*"
    r"(?P<unit>[^\n(]*)"
    r"\(\s*(?:reference\s*range|normal\s*range)\s*:"
    r"\s*(?P<low>[-+]?\d+(?:\.\d+)?)\s*"
    r"(?:-|–|to)\s*(?P<high>[-+]?\d+(?:\.\d+)?)\s*\)",
    re.IGNORECASE
)

def analyze_report(text):
    columns = ["Test", "Value", "Unit", "Reference Range", "Status"]

    if not isinstance(text, str) or not text.strip():
        return pd.DataFrame(columns=columns)

    results = []

    for match in PATTERN.finditer(text):
        name = match.group("name").strip()
        value = float(match.group("value"))
        low = float(match.group("low"))
        high = float(match.group("high"))

        if low > high:
            continue

        if value < low:
            status = "Below reference range"
        elif value > high:
            status = "Above reference range"
        else:
            status = "Within reference range"

        results.append({
            "Test": name,
            "Value": value,
            "Unit": match.group("unit").strip(),
            "Reference Range": f"{low:g} - {high:g}",
            "Status": status
        })

    return pd.DataFrame(results, columns=columns)


def generate_summary(df):
    if df.empty:
        return "No supported test results were found."

    statuses = df["Status"].to_numpy()

    below = int(np.sum(statuses == "Below reference range"))
    within = int(np.sum(statuses == "Within reference range"))
    above = int(np.sum(statuses == "Above reference range"))

    lines = [
        f"**Tests analyzed:** {len(df)}",
        f"**Below supplied range:** {below}",
        f"**Within supplied range:** {within}",
        f"**Above supplied range:** {above}",
        "",
        "**Findings:**"
    ]

    for _, row in df.iterrows():
        lines.append(
            f"- **{row['Test']}**: {row['Value']:g} "
            f"{row['Unit']} — {row['Status']}."
        )

    lines.append(
        "\n*Informational comparison only, not a diagnosis. "
        "Verify findings with the original report and a healthcare professional.*"
    )

    return "\n".join(lines)
