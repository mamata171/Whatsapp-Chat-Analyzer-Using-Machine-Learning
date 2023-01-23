import pandas as pd
import numpy as np
from urlextract import URLExtract
from wordcloud import WordCloud
import emoji
import nltk
from collections import Counter
from nltk.corpus import stopwords
nltk.download('stopwords')
sw = stopwords.words('english')


def fetch_stats(selected_user,df):

    if selected_user != "Overall":
        df = df[df['user'] == selected_user]
        
    # Number of messages
    num_msges = df.shape[0]

    # number of words
    words = []
    for message in df['message']:
        words.extend(message.split())
    

    # Fetch number of media messages
    num_media_msg =  df[df['message'] == '<Media omitted>'].shape[0]
    
    # Fetch number of links shared
    links = []
    extractor = URLExtract()
    for message in df['message']:
        links.extend(extractor.find_urls(message))

    return num_msges,len(words),num_media_msg,len(links)

def monthly_timeline(selected_user,df):
    if selected_user != "Overall":
        df = df[df['user'] == selected_user]

    timeline = df.groupby(['year','month_num','month']).count()['message'].reset_index()
    time = []
    for i in range(len(timeline)):
        time.append(timeline['month'][i] + "-" + str(timeline['year'][i]))
    
    timeline['time'] = time
    return timeline

def daily_timeline(selected_user,df):
    if selected_user != "Overall":
        df = df[df['user'] == selected_user]
    daily_timeline = df.groupby('Date').count()['message'].reset_index()
    return daily_timeline


def week_activity_map(selected_user,df):
    if selected_user != "Overall":
        df = df[df['user'] == selected_user]
    return df['Day_name'].value_counts()


def month_activity_map(selected_user,df):
    if selected_user != "Overall":
        df = df[df['user'] == selected_user]
    return df['month'].value_counts()

def activity_heatmap(selected_user,df):
    if selected_user != "Overall":
        df = df[df['user'] == selected_user]
    user_heatmap = df.pivot_table(index = 'Day_name',columns = 'period',values = 'message',aggfunc = 'count').fillna(0)
    return user_heatmap

def most_busy_user(df):
    x = df['user'].value_counts().head()
    
    df = round((df['user'].value_counts()/len(df))*100,2).reset_index().rename(columns = {'index' : 'Name','user':'Percent'})
    return x,df

def create_wordcloud(selected_user,df):
    if selected_user != "Overall":
        df = df[df['user'] == selected_user]

    temp = df[df['message'] != '<Media omitted>']
    def remove_sw(message):
        y = []
        for word in message.lower().split():
            if word not in sw and word!='k' and word!='ok':
                y.append(word)
            return " ".join(y)

    wc = WordCloud(width=400,height=300,min_font_size = 10,background_color='black')
    temp['message'] = temp['message'].apply(remove_sw)
    df_wc = wc.generate(temp['message'].str.cat(sep = " "))
    return df_wc

def most_common_words(selected_user,df):
    if selected_user != "Overall":
        df = df[df['user'] == selected_user]

    temp = df[df['message'] != "<Media omitted>"]

    words = []
    sw = stopwords.words('english')
    for message in temp['message']:
        for word in message.lower().split():
            if word not in sw and word!='k' and word!='ok' and word[:5] !='https':
                words.append(word)
    
    ret_df = pd.DataFrame(Counter(words).most_common(20))        
    return ret_df

def emoji_helper(selected_user,df):
    if selected_user != "Overall":
        df = df[df['user'] == selected_user]

    emojis = []
    for message in df['message']:
        emojis.extend([c for c in message if c in emoji.UNICODE_EMOJI['en']])

    emoji_df = pd.DataFrame(Counter(emojis).most_common(len(Counter(emojis)))).rename(columns = {0:'emoji',1:'count'})
    return emoji_df
