import re
import pandas as pd
import emoji
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import plotly.express as px
import collections
from wordcloud import WordCloud, STOPWORDS
import base64
from io import BytesIO

def combine_lines(chat_file_path):
    combined_lines = []
    with open(chat_file_path, "r", encoding="utf-8") as file:
        previous_line = ""
        for line in file:
            # Check if the line starts with a date
            if re.match(r'\d{1,2}/\d{1,2}/\d{2,4}, \d{1,2}:\d{2}\u202f(AM|PM) - ', line):
                # If it does, append the previous line to the list and start a new line
                if previous_line:
                    combined_lines.append(previous_line)
                previous_line = line.strip()
            else:
                # If it doesn't start with a date, append it to the previous line
                previous_line += " " + line.strip()

        # Don't forget to add the last line
        combined_lines.append(previous_line)
    return combined_lines

def parse_messages(input_strings):
    data = []
    pattern = r'(\d{1,2}/\d{1,2}/\d{2,4}), (\d{1,2}:\d{2}\s*[AP]M) - (.*?): (.*)'

    for input_string in input_strings:
        match = re.match(pattern, input_string)
        if match:
            date, time, author, message = match.groups()
            data.append({
                'Date': date,
                'Time': time,
                'Author': author,
                'Message': message
            })

    return pd.DataFrame(data)

# function to prepare dataframe
def prepare_df(file):
    combined_chat = combine_lines(file)
    df = parse_messages(combined_chat)
    df['emoji'] = df["Message"].apply(get_emojis)
    df['url'] = df["Message"].apply(get_urls)
    df['urlcount'] = df['url'].apply(get_url_count)
    return df

# function to get more data from dataframe
def get_data(df):
    media_messages_df = df[df['Message'] == '<Media omitted>']
    messages_df = df.drop(media_messages_df.index)
    messages_df['Letter_Count'] = messages_df['Message'].apply(lambda s : len(s))
    messages_df['Word_Count'] = messages_df['Message'].apply(lambda s : len(s.split(' ')))
    messages_df["MessageCount"] = 1
    return media_messages_df, messages_df

# function to find emojis
def get_emojis(text):
    lst = []
    emojis = emoji.emoji_list(text)
    for i in emojis:
        lst.append(i['emoji'])
    return lst

# function to find urls
def get_urls(text):
    return re.findall(r'(https?://\S+)', text)

# function to find no. of urls
def get_url_count(lst):
    return len(lst) 

# function to create a graph of Emojis
def create_emoji_graph(df):
    total_emojis_list = list(set([a for b in df.emoji for a in b]))
    total_emojis_list = list([a for b in df.emoji for a in b])
    emoji_dict = dict(collections.Counter(total_emojis_list))
    emoji_dict = sorted(emoji_dict.items(), key=lambda x: x[1], reverse=True)
    emoji_df = pd.DataFrame(emoji_dict, columns=['emoji', 'count'])
    fig = px.pie(emoji_df, values='count', names='emoji')
    fig.update_traces(textposition='inside', textinfo='percent+label')
    fig = fig.to_html(full_html=False)
    return fig

# function to create a WordCloud
def create_wordcloud(df, user):
    text = " ".join(review for review in df.Message)
    stopwords = set(STOPWORDS)
    wordcloud = WordCloud(stopwords=stopwords, background_color="white").generate(text)
    plt.figure( figsize=(10,5))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis("off")
    plt.title(f"{user}")
    img = BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    plot_url = base64.b64encode(img.getvalue()).decode('utf8')
    return plot_url