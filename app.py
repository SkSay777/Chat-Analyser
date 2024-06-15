import streamlit as st
import preprocessor,helper
import matplotlib.pyplot as plt
import seaborn as sns
# from load_emoji_font import load_emoji_font  # Import the function

st.sidebar.title("Whatsapp Chat Analyzer")

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

    selected_user = st.sidebar.selectbox("Show analysis wrt",user_list)

    if st.sidebar.button("Show Analysis"):

        # Stats Area
        num_messages, words, num_media_messages, num_links = helper.fetch_stats(selected_user,df)
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

        # monthly timeline
        st.title("Monthly Timeline")
        timeline = helper.monthly_timeline(selected_user,df)
        st.line_chart(timeline, x='time', y='message')
        # fig, ax = plt.subplots()
        # ax.plot(timeline['time'], timeline['message'],color='green')
        # plt.xticks(rotation='vertical')
        # st.pyplot(fig)

        # daily timeline
        st.title("Daily Timeline")
        daily_timeline = helper.daily_timeline(selected_user, df)
        st.line_chart(daily_timeline, x='only_date', y='message')
        # fig, ax = plt.subplots()
        # ax.plot(daily_timeline['only_date'], daily_timeline['message'], color='blue')
        # plt.xticks(rotation='vertical')
        # st.pyplot(fig)

        # activity map
        st.title('Activity Map')
        col1,col2 = st.columns(2)

        with col1:
            st.header("Most busy day")
            busy_day = helper.week_activity_map(selected_user,df)
            st.bar_chart(busy_day, x='Day', y='message')
            # fig,ax = plt.subplots()
            # ax.bar(week_timeline['day_name'],week_timeline['message'],color='purple')
            # plt.xticks(rotation='vertical')
            # st.pyplot(fig)

        with col2:
            st.header("Most busy month")
            busy_month = helper.month_activity_map(selected_user, df)
            st.bar_chart(busy_month, x='Month', y='message')
            # fig, ax = plt.subplots()
            # ax.bar(busy_month['Month'],busy_month['message'],color='orange')
            # plt.xticks(rotation='vertical')
            # st.pyplot(fig)

        st.title("Weekly Activity Map")
        user_heatmap = helper.activity_heatmap(selected_user, df)
        fig,ax = plt.subplots()
        ax = sns.heatmap(user_heatmap, cmap='Blues')
        st.pyplot(fig)

        # finding the busiest users in the group(Group level)
        if selected_user == 'Overall':
            st.title('Most Busy Users')
            x,new_df = helper.most_busy_users(df)
            fig, ax = plt.subplots()

            col1, col2 = st.columns(2)

            with col1:
                ax.bar(x.index, x.values,color='cornflowerblue')
                plt.xticks(rotation='vertical')
                st.pyplot(fig)
            with col2:
                st.dataframe(new_df)

        # WordCloud
        st.title("Wordcloud")
        df_wc = helper.create_wordcloud(selected_user,df)
        fig,ax = plt.subplots()
        ax.imshow(df_wc)
        st.pyplot(fig)

        # most common words
        st.title('Most commmon words')
        most_common_df = helper.most_common_words(selected_user,df)
        st.bar_chart(most_common_df, x='word', y='count')
        # fig,ax = plt.subplots()
        # ax.barh(most_common_df['word'],most_common_df['count'])
        # plt.xticks(rotation='vertical')
        # st.pyplot(fig)

        # Emoji analysis
        emoji_df = helper.emoji_helper(selected_user, df)
        st.title("Emoji Analysis")
        st.bar_chart(emoji_df, x='emoji', y='count')
        # col1, col2 = st.columns(2)
        #
        # with col1:
        #     st.dataframe(emoji_df)
        # with col2:
        #     # fig, ax = plt.subplots()
        #     # ax.pie(emoji_df['count'].head(), labels=emoji_df['emoji'].head(), autopct="%0.2f")
        #     # st.pyplot(fig)