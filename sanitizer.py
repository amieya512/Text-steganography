import re

def sanitize_cover_text(text):
    """
    Cleans the cover text to avoid invisible character conflicts.
    Returns: (clean_text, removed_characters_list)
    """

    removed = []

    # 1. Remove zero-width characters that may break decoding
    zero_width = [
        "\u200b",  # zero-width space
        "\u200c",  # zero-width non-joiner
        "\u200d",  # zero-width joiner
        "\ufeff"   # BOM
    ]

    for zw in zero_width:
        if zw in text:
            removed.append(zw)
            text = text.replace(zw, "")

    # 2. Normalize whitespace (multiple spaces → one space)
    new_text = re.sub(r"\s+", " ", text)
    if new_text != text:
        removed.append("extra_whitespace")
        text = new_text

    return text, removed
