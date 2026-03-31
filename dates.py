from datetime import datetime


def try_parse_date(value):
    if value in (None, ''):
        return None
    if isinstance(value, datetime):
        return value.date().isoformat()
    return str(value)
