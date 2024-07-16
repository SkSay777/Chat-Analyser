import re
import pandas as pd
from nltk.sentiment.vader import SentimentIntensityAnalyzer

lexicon_file = 'vader_lexicon.txt'

def preprocess(data):
    # Load custom Vader lexicon from file
    with open(lexicon_file, 'r', encoding='utf-8') as f:
        lexicon_lines = f.readlines()

    custom_lexicon = {}
    for line in lexicon_lines:
        # Skip empty lines or lines that cannot be split into exactly two parts
        line = line.strip()
        if line and '\t' in line:
            parts = line.split('\t')
            if len(parts) == 2:
                word, score = parts
                custom_lexicon[word] = float(score)
            else:
                print(f"Warning: Skipped invalid line in {lexicon_file}: {line}")
        else:
            print(f"Warning: Skipped invalid line in {lexicon_file}: {line}")

    # Initialize NLTK's Sentiment Intensity Analyzer with custom lexicon
    sia = SentimentIntensityAnalyzer()
    sia.lexicon.update(custom_lexicon)

    # Function to convert time format to 24-hour format
    def convert_to_24_hour(match):
        time_str = match.group()
        time_obj = re.match(r'(\d{1,2}):(\d{2})\s([ap]m)', time_str)
        if time_obj:
            hour, minute, period = time_obj.groups()
            hour = int(hour)
            minute = int(minute)
            if period.lower() == 'pm' and hour != 12:
                hour += 12
            elif period.lower() == 'am' and hour == 12:
                hour = 0
            return f'{hour:02d}:{minute:02d}'
        return time_str

    # Use regex to find and replace the time format
    data_modified = re.sub(r'\d{1,2}:\d{2}\s[ap]m', convert_to_24_hour, data)

    # Define the regex pattern to extract messages and dates
    pattern = r'\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{2}\s-\s'

    # Split the modified data to extract messages and dates
    messages = re.split(pattern, data_modified)[1:]
    dates = re.findall(pattern, data_modified)

    # Create a DataFrame to store the messages and dates
    df = pd.DataFrame({'user_message': messages, 'message_date': dates})
    # Convert message_date to datetime format
    df['message_date'] = pd.to_datetime(df['message_date'], format='%d/%m/%Y, %H:%M - ')

    df.rename(columns={'message_date': 'date'}, inplace=True)

    users = []
    messages = []
    for message in df['user_message']:
        entry = re.split('([\w\W]+?):\s', message)
        if entry[1:]:  # user name
            users.append(entry[1])
            messages.append(" ".join(entry[2:]))
        else:
            users.append('group_notification')
            messages.append(entry[0])

    df['user'] = users
    df['message'] = messages
    df.drop(columns=['user_message'], inplace=True)

    df['only_date'] = df['date'].dt.date
    df['year'] = df['date'].dt.year
    df['month_num'] = df['date'].dt.month
    df['Month'] = df['date'].dt.month_name()
    df['day'] = df['date'].dt.day
    df['Day'] = df['date'].dt.day_name()
    df['hour'] = df['date'].dt.hour
    df['minute'] = df['date'].dt.minute

    period = []
    for hour in df[['Day', 'hour']]['hour']:
        if hour == 23:
            period.append(str(hour) + "-" + str('00'))
        elif hour == 0:
            period.append(str('00') + "-" + str(hour + 1))
        else:
            period.append(str(hour) + "-" + str(hour + 1))

    df['period'] = period

    # Sentiment Analysis
    df['sentiment'] = df['message'].apply(lambda x: sia.polarity_scores(x)['compound'])

    return df
