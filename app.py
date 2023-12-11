from processing import *
import numpy as np
import os
from flask import Flask, render_template, request
from werkzeug.utils import secure_filename

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/', methods=['GET','POST'])
def home():
    if request.method == 'GET':
        return render_template('index.html')
    else:
        if 'file' not in request.files:
            return render_template('index2.html', msg="Please Select File!")
        file = request.files['file']
        if file.filename == '':
            return render_template('index2.html', msg="Please Select File!")
        if file:
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            df = prepare_df(f'./uploads/{filename}')
            total_messages = df.shape[0]
            total_media_messages = df[df["Message"]=='<Media omitted>'].shape[0]
            total_emojis = sum(df['emoji'].str.len())
            total_links = np.sum(df.urlcount)
            media_messages_df, messages_df = get_data(df)
            users = df['Author'].unique().tolist()
            users_data = []
            for i in range(len(users)):
                req_df= messages_df[messages_df["Author"] == users[i]]
                messages_sent = req_df.shape[0]
                words_per_message = (np.sum(req_df['Word_Count']))/req_df.shape[0]
                media = media_messages_df[media_messages_df['Author'] == users[i]].shape[0]
                emojis = sum(req_df['emoji'].str.len())
                links = sum(req_df["urlcount"])
                dummy_df = messages_df[messages_df['Author'] == users[i]]
                personal_wordcloud = create_wordcloud(dummy_df, users[i])
                users_data.append([messages_sent, round(words_per_message, 2), media, emojis, links, personal_wordcloud])
            emoji_graph = create_emoji_graph(messages_df)
            emoji_graph = emoji_graph.to_html(full_html=False)
            wordcloud = create_wordcloud(messages_df, "General")
            return render_template('index2.html', total_messages=total_messages, total_media_messages=total_media_messages, total_emojis=total_emojis, total_links=total_links, users_data=users_data, emoji_graph=emoji_graph, wordcloud=wordcloud)

if __name__ == '__main__':
    app.run(debug=True)
    # <img src="data:image/png;base64,{{ i[5] }}">

# General Stats
# print(f'Total Messages: {df.shape[0]}')
# total_media_messages = df[df["Message"]=='<Media omitted>'].shape[0]
# print(f'Number of Media Shared: {total_media_messages}')
# total_emojis = sum(df['emoji'].str.len())
# print(f'Number of Emojis Shared: {total_emojis}')
# total_links = np.sum(df.urlcount)
# print(f"Number of Link Shared: {total_links}")

# Individual Stats
# media_messages_df, messages_df = get_data(df)
# users = df['Author'].unique().tolist()
# for i in range(len(users)):
#     print("--------------------------------------------------------------------------------")
#     req_df= messages_df[messages_df["Author"] == users[i]]
#     print(f'Stats of {users[i]} -')
#     print('Messages Sent:', req_df.shape[0])
#     words_per_message = (np.sum(req_df['Word_Count']))/req_df.shape[0]
#     print('Average Words per message:', round(words_per_message, 2))
#     media = media_messages_df[media_messages_df['Author'] == users[i]].shape[0]
#     print('Media Sent:', media)
#     emojis = sum(req_df['emoji'].str.len())
#     print('Emojis Sent:', emojis)
#     links = sum(req_df["urlcount"])   
#     print('Links Sent:', links)

# # Emoji Graph
# fig = create_emoji_graph(messages_df)

# # General WordCloud
# create_wordcloud(messages_df, "General").show()

# # Individual WordCloud
# for i in range(len(users)):
#     dummy_df = messages_df[messages_df['Author'] == users[i]]
#     create_wordcloud(dummy_df, users[i]).show()