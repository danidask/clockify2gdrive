import datetime


def get_past_month_start_end():
    now = datetime.datetime.now()
    month = now.month
    year = now.year
    end_date = datetime.datetime.strptime('{}/1/{}'.format(month, year), "%m/%d/%Y")
    end_date -= datetime.timedelta(milliseconds=1)
    month -= 1
    if month <= 0:
        month = 12
        year -= 1
    start_date = datetime.datetime.strptime('{}/1/{}'.format(month, year), "%m/%d/%Y")
    return (start_date, end_date)


def get_past_month_str():
    now = datetime.datetime.now()
    past_month = now - datetime.timedelta(days=28)
    return past_month.strftime("%Y-%m")
