import locale
import datetime
locale.setlocale(locale.LC_ALL, "ru")

def edit_text(text):
    if len(text) < 2000:
        return text
    else:
        return f'{text[:1997]}...'

def edit_date(date):
    if date == "Сегодня":
        return datetime.date.today().strftime("%d %B %Yг.")
    elif date == "Вчера":
        today = datetime.datetime.today()
        delta = datetime.timedelta(days = 1)
        return (today - delta).strftime("%d %B %Yг.")
    else:
        return date
