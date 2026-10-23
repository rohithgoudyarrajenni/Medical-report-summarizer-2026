
    # Intramural uterine lesions
    if "intramural" in normalized and (
        "lesion" in normalized or "fibroid" in normalized
    ):
        # Extract measurements only from the uterine lesion descriptions.
        lesion_measurements = []

        lesion_patterns = [
            r"posterior myometrium.{0,180}?"
            r"(?:measuring|measures)\s*(\d{1,3})\s*x\s*(\d{1,3})\s*mm",

            r"anterior myometrium.{0,180}?"
            r"(?:measuring|measures)\s*(\d{1,3})\s*x\s*(\d{1,3})\s*mm",
        ]

        for pattern in lesion_patterns:
            match = re.search(pattern, normalized)
            if match:
                lesion_measurements.append(
                    f"{match.group(1)} x {match.group(2)} mm"
                )

        detail = (
            "The report describes lesions within the uterine muscle wall."
        )

        if lesion_measurements:
            detail += (
                " Reported lesion measurements: "
                + ", ".join(lesion_measurements)
                + "."
            )

        detail += (
            " Confirm the measurements against the original report."
        )

        add(
            "Ultrasound",
            "Intramural uterine lesions",
            detail
        )
