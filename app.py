import streamlit as st
import preprocessor, helper
import matplotlib.pyplot as plt
import seaborn as sns
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

st.sidebar.title("Whatsapp Chat Analyzer")

nav_option = st.sidebar.radio("Navigation", ["Home", "How To"])

if nav_option == "Home":
    uploaded_file = st.sidebar.file_uploader("Choose a file")
    if uploaded_file is not None:
        bytes_data = uploaded_file.getvalue()
        data = bytes_data.decode("utf-8")
        df = preprocessor.preprocess(data)

        # Filter out 'group_notification' entries
        df = df[df['user'] != 'group_notification']

        # fetch unique users
        user_list = df['user'].unique().tolist()
        user_list.sort()
        user_list.insert(0, "Overall")

        selected_user = st.sidebar.selectbox("Show analysis wrt", user_list)

        if st.sidebar.button("Show Analysis"):
            # Stats Area
            num_messages, words, num_media_messages, num_links = helper.fetch_stats(selected_user, df)
            st.title("Top Statistics")
            col1, col2, col3, col4 = st.columns(4)

            with col1:
                st.header("Total Messages")
                st.title(num_messages)
            with col2:
                st.header("Total Words")
                st.title(words)
            with col3:
                st.header("Media Shared")
                st.title(num_media_messages)
            with col4:
                st.header("Links Shared")
                st.title(num_links)

            # Monthly timeline
            st.title("Monthly Timeline")
            timeline = helper.monthly_timeline(selected_user, df)
            st.line_chart(timeline, x='time', y='message')

            # Daily timeline
            st.title("Daily Timeline")
            daily_timeline = helper.daily_timeline(selected_user, df)
            st.line_chart(daily_timeline, x='only_date', y='message')

            # Activity map
            st.title('Activity Map')
            col1, col2 = st.columns(2)

            with col1:
                st.header("Most busy day")
                busy_day = helper.week_activity_map(selected_user, df)
                st.bar_chart(busy_day, x='Day', y='message')

            with col2:
                st.header("Most busy month")
                busy_month = helper.month_activity_map(selected_user, df)
                st.bar_chart(busy_month, x='Month', y='message')

            st.title("Weekly Activity Map")
            user_heatmap = helper.activity_heatmap(selected_user, df)
            fig, ax = plt.subplots()
            ax = sns.heatmap(user_heatmap, cmap='Blues')
            st.pyplot(fig)

            # finding the busiest users in the group (Group level)
            if selected_user == 'Overall':
                st.title('Most Busy Users')
                x, new_df = helper.most_busy_users(df)
                fig, ax = plt.subplots()

                col1, col2 = st.columns(2)

                with col1:
                    ax.bar(x.index, x.values, color='cornflowerblue')
                    plt.xticks(rotation='vertical')
                    st.pyplot(fig)
                with col2:
                    st.dataframe(new_df)

            # WordCloud
            st.title("Wordcloud")
            df_wc = helper.create_wordcloud(selected_user, df)
            fig, ax = plt.subplots()
            ax.imshow(df_wc)
            st.pyplot(fig)

            # Most common words
            st.title('Most Common Words')
            most_common_df = helper.most_common_words(selected_user, df)
            st.bar_chart(most_common_df, x='word', y='count')

            # Emoji analysis
            st.title("Emoji Analysis")
            emoji_df = helper.emoji_helper(selected_user, df)
            st.bar_chart(emoji_df, x='emoji', y='count')

            # Sentiment Analysis
            st.title("Sentiment Analysis")
            positive_sentiment, negative_sentiment = helper.sentiment_analysis(selected_user, df)
            col1, col2 = st.columns(2)
            with col1:
                st.header("Most Positive Message")
                st.write(positive_sentiment[['user', 'message', 'sentiment']].iloc[0])

            with col2:
                st.header("Most Negative Message")
                st.write(negative_sentiment[['user', 'message', 'sentiment']].iloc[0])

            # Sentiment Distribution
            st.title("Sentiment Distribution")
            sentiment_counts_df = helper.sentiment_distribution(selected_user, df)
            st.bar_chart(sentiment_counts_df, x='count', y='Sentiment')

            # Daily Sentiment Trend
            st.title("Daily Sentiment Trend")
            daily_sentiment = helper.daily_sentiment_trend(selected_user, df)
            st.line_chart(daily_sentiment, x='only_date', y='sentiment')
else:
    st.title("How To Use The Whatsapp Chat Analyzer")
    st.markdown("""
    ### Instructions
    1. Upload your Whatsapp chat export file using the uploader in the sidebar.
    2. Select a user from the dropdown to filter the analysis specific to that user or choose 'Overall' for group analysis.
    3. Click on 'Show Analysis' to generate the analytics.
    
    ### Features
    - **Top Statistics**: Displays total messages, words, media shared, and links shared.
    - **Monthly Timeline**: Visualizes message count over months.
    - **Daily Timeline**: Visualizes message count over days.
    - **Activity Map**: Shows activity distribution across days of the week and months.
    - **Weekly Activity Map**: Heatmap showing hourly activity.
    - **Most Busy Users**: Displays the most active users in the group.
    - **Wordcloud**: Visual representation of the most common words.
    - **Most Common Words**: Bar chart of the most common words.
    - **Emoji Analysis**: Bar chart of the most used emojis.
    
    ### How to Export WhatsApp Chat
    1. **Open WhatsApp** on your phone.
    2. Go to the chat you want to export.
    3. Tap on the contact or group name at the top.
    4. Scroll down and select **"Export Chat"**.
    5. Choose whether to include media files or not.
    6. Select the method to share the chat (e.g., email, Google Drive).
    7. Save the exported chat file on your computer.
    
    ### Notes
    - Ensure your chat export file is in plain text format.
    - The analysis does not include messages that are media or notifications.
    """)
