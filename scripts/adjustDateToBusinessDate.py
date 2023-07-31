import datetime


def adjust_date_to_business_date(date, holidays_list):
    date_datetime = datetime.datetime.strptime(date, "%d/%m/%Y")
    while date_datetime.weekday() >= 5 or date_datetime.weekday() == 6 or date in holidays_list:
        date_datetime += datetime.timedelta(days=1)
    return date_datetime.strftime("%d/%m/%Y")
