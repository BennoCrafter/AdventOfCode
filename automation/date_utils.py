from datetime import datetime, date


def get_current_year() -> int:
    return datetime.now().year

def is_december() -> bool:
    return datetime.now().month == 12

def get_current_day() -> int:
    return datetime.now().day

def is_advent_time() -> bool:
    print(is_december(), get_current_day())
    return is_december() and 1 <= get_current_day() <= 24

def days_until_december() -> int:
    today = date.today()
    target_december = date(get_current_year(), 12, 1)

    if today >= target_december:
        target_december = date(get_current_year() + 1, 12, 1)

    return (target_december - today).days
