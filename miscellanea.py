import datetime


def get_past_month():
    now = datetime.datetime.now()
    month = now.month
    year = now.year
    month -= 1
    if month <= 0:
        month = 12
        year -= 1
    return month, year
