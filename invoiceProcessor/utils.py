import re
from datetime import datetime


def guess_date(text):

    patterns = [
        r"\b(\d{1,2}[./-]\d{1,2}[./-]\d{2,4})\b",
        r"\b(\d{4}-\d{1,2}-\d{1,2})\b",
    ]

    for pattern in patterns:
        match = re.search(pattern, text)
        if match:
            date_str = match.group(1)
            # Attempt to parse with multiple formats
            for fmt in ["%d/%m/%Y", "%d.%m.%Y", "%Y-%m-%d", "%d-%m-%Y", "%d/%m/%y"]:
                try:
                    dt = datetime.strptime(date_str, fmt)
                    return dt.strftime("%Y-%m-%d")
                except ValueError:
                    pass
    return None


def guess_amount(text):

    match = re.search(r"(\d{1,3}(?:,\d{3})*\.\d{2})", text)  # e.g. 1,234.56 or 123.45
    if match:
        return match.group(1)

    match = re.search(r"(\d{1,3}(?:\.\d{3})*,\d{2})", text)  # e.g. 1.234,56
    if match:
        return match.group(1)

    return None
