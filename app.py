from processing import *
import numpy as np
import plotly.express as px
import collections

chat_file_path = 'WhatsApp Chat with Siddharth.txt'
combined_chat = combine_lines(chat_file_path)
df = parse_messages(combined_chat)
df['emoji'] = df["Message"].apply(get_emojis)
df['url'] = df["Message"].apply(get_urls)
df['urlcount'] = df['url'].apply(get_url_count)

# General Stats
print(f'Total Messages: {df.shape[0]}')
total_media_messages = df[df["Message"]=='<Media omitted>'].shape[0]
print(f'Number of Media Shared: {total_media_messages}')
total_emojis = sum(df['emoji'].str.len())
print(f'Number of Emojis Shared: {total_emojis}')
total_links = np.sum(df.urlcount)
print(f"Number of Link Shared: {total_links}")

# Individual Stats
media_messages_df = df[df['Message'] == '<Media omitted>']
messages_df = df.drop(media_messages_df.index)
messages_df['Letter_Count'] = messages_df['Message'].apply(lambda s : len(s))
messages_df['Word_Count'] = messages_df['Message'].apply(lambda s : len(s.split(' ')))
messages_df["MessageCount"] = 1

users = df['Author'].unique().tolist()
for i in range(len(users)):
    print("--------------------------------------------------------------------------------")
    req_df= messages_df[messages_df["Author"] == users[i]]
    print(f'Stats of {users[i]} -')
    print('Messages Sent:', req_df.shape[0])
    words_per_message = (np.sum(req_df['Word_Count']))/req_df.shape[0]
    print('Average Words per message:', round(words_per_message, 2))
    media = media_messages_df[media_messages_df['Author'] == users[i]].shape[0]
    print('Media Sent:', media)
    emojis = sum(req_df['emoji'].str.len())
    print('Emojis Sent:', emojis)
    links = sum(req_df["urlcount"])   
    print('Links Sent:', links)

# Emoji Graph
total_emojis_list = list(set([a for b in messages_df.emoji for a in b]))
total_emojis = len(total_emojis_list)

total_emojis_list = list([a for b in messages_df.emoji for a in b])
emoji_dict = dict(collections.Counter(total_emojis_list))
emoji_dict = sorted(emoji_dict.items(), key=lambda x: x[1], reverse=True)
emoji_df = pd.DataFrame(emoji_dict, columns=['emoji', 'count'])
fig = px.pie(emoji_df, values='count', names='emoji')
fig.update_traces(textposition='inside', textinfo='percent+label')
fig.show()