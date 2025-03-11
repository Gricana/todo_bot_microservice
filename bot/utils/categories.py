def parse_categories(category_text: str):
    """
    Parses a comma-separated string of categories into a list of individual categories.

    Args:
        category_text (str): The comma-separated string containing category names.

    Returns:
        list: A list of parsed categories, with leading/trailing spaces removed.
    """
    if not category_text:
        return []

    return [
        category.strip() for category in category_text.split(",") if category.strip()
    ]
