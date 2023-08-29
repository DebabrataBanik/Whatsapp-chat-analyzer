from urlextract import URLExtract
from wordcloud import WordCloud
import pandas as pd
from collections import Counter
import emoji
extract = URLExtract()


def fetch_stats(selected_user, df):

    if selected_user != 'Overall':

        df = df[df['users'] == selected_user]

    # total number of messages
    num_message = df.shape[0]

    # total number of words
    words = []
    for message in df['message']:
        words.extend(message.split())

    # total media
    num_media_msg = df[df['message'] == '<Media omitted>\n'].shape[0]

    # total links
    links = []
    for message in df['message']:
        links.extend(extract.find_urls(message))

    return num_message, len(words), num_media_msg, len(links)


def most_busy_users(df):
    x = df['users'].value_counts().head(10)

    per_df = round((df['users'].value_counts()/df.shape[0])*100,
                   2).reset_index()
    per_df.rename(columns={'index': 'user', 'users': 'percentage'},
                  inplace=True)
    return x, per_df


def create_wordcloud(selected_user, df):

    f = open('hinglish_stopwords.txt', 'r')
    stopwords = f.read()

    if selected_user != 'Overall':
        df = df[df['users'] == selected_user]

    temp = df[df['users'] != 'Group Notifications']
    temp = temp[temp['message'] != '<Media omitted>\n']

    def remove_stopwords(message):
        y = []
        for word in message.lower().split():
            if word not in stopwords:
                y.append(word)
        return " ".join(y)

    wc = WordCloud(width=500, height=500, min_font_size=10,
                   background_color='white')
    temp['message'] = temp['message'].apply(remove_stopwords)
    df_wc = wc.generate(temp['message'].str.cat(sep=' '))
    return df_wc


def most_common_words(selected_user, df):

    f = open('hinglish_stopwords.txt', 'r')
    stopwords = f.read()

    if selected_user != 'Overall':
        df = df[df['users'] == selected_user]

    temp = df[df['users'] != 'Group Notifications']
    temp = temp[temp['message'] != '<Media omitted>\n']

    words = []
    for message in temp['message']:
        for word in message.lower().split():
            if word not in stopwords:
                words.append(word)

    most_common_df = pd.DataFrame(Counter(words).most_common(20))

    return most_common_df


def count_emoji(selected_user, df):

    if selected_user != 'Overall':
        df = df[df['users'] == selected_user]

    emojis = []
    for message in df['message']:
        emojis.extend(c for c in message if c in emoji.UNICODE_EMOJI['en'])

    emoji_df = pd.DataFrame(Counter(emojis).most_common(len(Counter(emojis))))

    return emoji_df


def monthly_timeline(selected_user, df):

    if selected_user != 'Overall':
        df = df[df['users'] == selected_user]

    df['month_no'] = df['dates'].dt.month
    timeline = df.groupby(['year', 'month_no', 'month'])[
        'message'].count().reset_index()
    time = []
    for i in range(timeline.shape[0]):
        time.append(timeline['month'][i]+"-"+str(timeline['year'][i]))
    timeline['time'] = time

    return timeline


def daily_timeline(selected_user, df):

    if selected_user != 'Overall':
        df = df[df['users'] == selected_user]

    df['date'] = df['dates'].dt.date
    daily_timeline_df = df.groupby('date')['message'].count().reset_index()

    return daily_timeline_df
