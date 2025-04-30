def remove_none(d):
    """
    Recursively remove keys with None values, empty dicts, or empty lists from dictionaries.
    """
    if isinstance(d, dict):
        cleaned = {k: remove_none(v) for k, v in d.items() if v is not None}
        # Remove keys where the value is an empty dict or empty list
        return {k: v for k, v in cleaned.items() if not (v == {} or v == [])}
    elif isinstance(d, list):
        cleaned_list = [remove_none(v) for v in d]
        # Remove empty dicts/lists from the list
        return [v for v in cleaned_list if not (v == {} or v == [])]
    else:
        return d