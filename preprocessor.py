import re
import pandas as pd


def preprocess(data):
    pattern = '\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{2}\s-\s'

    messages = re.split(pattern, data)[1:]
    dates = re.findall(pattern, data)

    df = pd.DataFrame({'user_messages': messages, 'message_dates': dates})

    df['message_dates'] = pd.to_datetime(
        df['message_dates'], format='%d/%m/%y, %H:%M - ')

    df.rename(columns={'message_dates': 'dates'}, inplace=True)

    users = []
    messages = []
    for message in df['user_messages']:
        entry = re.split('([\w\W]+?):\s', message)
        if entry[1:]:
            users.append(entry[1])
            messages.append(entry[2])
        else:
            users.append('Group Notifications')
            messages.append(entry[0])

    df['users'] = users
    df['message'] = messages
    df.drop(columns='user_messages', inplace=True)

    df['year'] = df['dates'].dt.year
    df['month'] = df['dates'].dt.month_name()
    df['day'] = df['dates'].dt.day
    df['hour'] = df['dates'].dt.hour
    df['minute'] = df['dates'].dt.minute
    df['day_name']=df['dates'].dt.day_name()
    df['date']=df['dates'].dt.date
    df['month_no']=df['dates'].dt.month

    period = []
    for hour in df['hour']:
        if hour == 23:
            period.append(str(hour) + "-" + str('00'))
        elif hour == 0:
            period.append(str('00') + "-" + str(hour + 1))
        else:
            period.append(str(hour) + "-" + str(hour + 1))

    df['period'] = period

    return df
