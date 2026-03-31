def try_parse_number(value):
    if value in (None, ''):
        return None
    try:
        return float(str(value).replace('.', '').replace(',', '.'))
    except Exception:
        return None
