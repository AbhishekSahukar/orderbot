import re

def extract_name_fallback(text: str) -> str | None:
    # Remove possessive forms like Bob Smith's
    text = re.sub(r"(’s|'s)", "", text)

    # Extract capitalized name-like phrases
    matches = re.findall(
        r"[A-Z][a-z]+(?:\s+[A-Z][a-z]+)*",
        text
    )

    # Use the LAST match (entity usually comes last in sentences)
    return matches[-1] if matches else None
