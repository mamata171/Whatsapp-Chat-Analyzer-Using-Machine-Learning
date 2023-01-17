import numpy as np
import pandas as pd
import re
from datetime import datetime


def preprocess(data):
    pattern = "\d{1,2}/\d{2}/\d{2}, \d{1,2}:\d{2} [ap]m"
    messages = re.split(pattern,data)[1:]
    df1 = pd.DataFrame()
    df1["messages"] = messages
    df1['dates1'] = re.findall(pattern,data)
    df1[["Date","Time"]] = df1["dates1"].str.split(',',expand = True)
    df1.drop('dates1',axis = 1,inplace = True)
    message = []
    for msg in df1['messages']:
        msg = msg.strip(" -")
        msg= msg.strip("\n")
        msg = msg.replace("\n","")
        message.append(msg)
    df1['messages'] = message

    # separate users and messages 
    users = []
    messages = []
    for message in df1['messages']:
        entry = re.split('([\w\W]+?):\s', message)
        if entry[1:]:# user name
            users.append(entry[1])
            messages.append(entry[2])
        else:
            users.append('group_notification')
            messages.append(entry[0])

    df1['user'] =  users    
    df1['message'] = messages
    
    df1.drop('messages',axis=1,inplace = True)
    df1['Date'] = pd.to_datetime(df1['Date'])

    # data cleaning 
    # 1. remove all the <Media omitted> messages
    images = df1[df1['message'] == '<Media omitted>']
    # print("Total number of Images + Videos Shared: ", len(images))
    # df1.drop(images.index, inplace=True)
    # df1.reset_index(inplace = True,drop = True)

    notifications = df1[df1['user'] == 'group_notification']
    df1.drop(notifications.index,inplace = True)
    df1.reset_index(inplace = True,drop = True)

    def convert24(time):
        t = str(datetime.strptime(time, ' %I:%M %p')).split(' ')[1]
        return t
    
    df1['Time'] = df1['Time'].apply(convert24)

    def hours(time):
        return time[:2]
    df1['hour'] = df1['Time'].apply(hours)

    # splitting month year and day
    df1['year'] = df1['Date'].dt.year
    df1['month_num'] = df1['Date'].dt.month
    df1['month'] = df1['Date'].dt.month_name()
    df1['day'] = df1['Date'].dt.day
    df1['Day_name'] = df1['Date'].dt.day_name()

    df1['hour'] = df1['hour'].astype('int')
    period = []
    for hour in df1[['Day_name','hour']]['hour']:
        if hour == 23:
            period.append(str(hour) + "-" + str('00'))
        elif hour == 0:
            period.append(str('00') + "-" + str(hour+1))
        else:
            period.append(str(hour) + "-" + str(hour+1))
    df1['period'] = period
    deleted_msgs = df1[df1['message'] == 'This message was deleted']
    df1 = df1.drop(deleted_msgs.index)

    empty_msg = df1[df1['message'] == '']
    df1 = df1.drop(empty_msg.index)

    df1.reset_index(drop = True,inplace = True)

    return df1

