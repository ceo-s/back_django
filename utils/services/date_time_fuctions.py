from datetime import datetime, timedelta

def weekstart_date(date: str):
    """
    Берёт дату и возвращает дату понедельника её недели.
    """
    # date = datetime.strptime(date, "%Y-%m-%d")
    weekday = date.weekday()
    delta = timedelta(weekday)
    result : datetime = date - delta
    return str(result)


def weekend_date(date: str):
    """
    Берёт дату и возвращает дату воскресенья её недели.
    """
    # date = datetime.strptime(date, "%Y-%m-%d")
    weekday = date.weekday()
    delta = timedelta(weekday)
    result : datetime = date - delta + timedelta(6)
    return str(result)

def get_weeks_count(date1:str, date2:str):
    """
    Берёт временной интервал и возвращает количество недель.
    """
    date1 = datetime.strptime(date1, "%Y-%m-%d").date()
    date2 = datetime.strptime(date2, "%Y-%m-%d").date()
    for i in range(abs((date2 - date1).days // 7)):
        week_start = date1 + timedelta(weeks=i)
        week_end = week_start + timedelta(days=6)
        yield (str(week_start), str(week_end))


def get_interval_dates(date1: str, date2: str):
    """
    Берёт временной интервал и возвращает все даты в нём.
    """
    date1 = datetime.strptime(date1, "%Y-%m-%d").date()
    date2 = datetime.strptime(date2, "%Y-%m-%d").date()
    day = timedelta(1)
    interval_dates = [date1]
    while date1 != date2:
        date1 += day
        interval_dates.append(date1)
    return interval_dates

# print(get_interval_dates("2023-04-28", "2023-05-20"))
