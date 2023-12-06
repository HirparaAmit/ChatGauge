import re
import pandas as pd
import emoji

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