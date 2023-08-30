import streamlit as st
import preprocessor
import helper
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

st.sidebar.title('Whatsapp Chat Analyzer')

uploaded_file = st.sidebar.file_uploader("Choose a file")
if uploaded_file is not None:

    bytes_data = uploaded_file.getvalue()
    data = bytes_data.decode('utf-8')
    df = preprocessor.preprocess(data)

    # fetch unique users
    user_list = df['users'].unique().tolist()
    user_list.remove('Group Notifications')
    user_list.sort()
    user_list.insert(0, 'Overall')

    selected_user = st.sidebar.selectbox('Show analysis wrt', user_list)

    if st.sidebar.button('Show Analysis'):

        # stats
        num_msg, words, num_media_msg, links = helper.fetch_stats(
            selected_user, df)

        st.title('Statistics')

        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.header('Total messages')
            st.title(num_msg)

        with col2:
            st.header("Total Words")
            st.title(words)

        with col3:
            st.header('Media shared')
            st.title(num_media_msg)

        with col4:
            st.header('Links shared')
            st.title(links)

        # timeline
        timeline_df = helper.monthly_timeline(selected_user, df)
        st.title('Monthly Timeline')

        fig, ax = plt.subplots()
        ax.plot(timeline_df['time'], timeline_df['message'], color='green')
        plt.xticks(rotation='vertical')
        st.pyplot(fig)

        daily_timeline_df = helper.daily_timeline(selected_user, df)
        st.title("Daily Timeline")

        fig, ax = plt.subplots()
        # plt.figure(figsize=(18, 10))
        ax.plot(daily_timeline_df['date'],
                daily_timeline_df['message'], color='blue')
        plt.xticks(rotation='vertical')
        st.pyplot(fig)

        # group level analysis
        # most busy users
        if selected_user == 'Overall':
            st.title('Most Busy Users')
            x, new_df = helper.most_busy_users(df)

            constrained_df = new_df[new_df['count'] > 2]
            constrained_df.rename(
                columns={'percentage': 'user', 'count': 'percentage'}, inplace=True)

            col1, col2 = st.columns(2)

            with col1:
                fig, ax = plt.subplots()
                ax.bar(x.index, x.values)
                plt.xticks(rotation='vertical')
                st.pyplot(fig)

            with col2:
                fig1, ax1 = plt.subplots()
                highest_percentage_index = constrained_df['percentage'].idxmax(
                )
                explode = [0.1 if i == highest_percentage_index else 0 for i in range(
                    len(constrained_df))]
                ax1.pie(constrained_df['percentage'], explode=explode, shadow=True, labels=constrained_df['user'],
                        autopct='%1.1f%%', startangle=90)
                # Equal aspect ratio ensures the pie chart is circular.
                ax1.axis('equal')
                st.pyplot(fig1)

        # WordCloud
        st.title('Wordcloud')
        df_wc = helper.create_wordcloud(selected_user, df)
        fig, ax = plt.subplots()
        plt.imshow(df_wc)
        st.pyplot(fig)

        # most common words

        most_common_df = helper.most_common_words(selected_user, df)

        fig, ax = plt.subplots()
        ax.barh(most_common_df[0], most_common_df[1])
        st.pyplot(fig)

        # emoji analyst
        emoji_df = helper.count_emoji(selected_user, df)

        col1, col2 = st.columns(2)

        with col1:
            st.dataframe(emoji_df)

        with col2:
            fig, ax = plt.subplots()
            ax.pie(emoji_df[1].head(),
                   labels=emoji_df[0].head(), autopct='%0.2f')
            st.pyplot(fig)

        #activity timeline

        week_activity,month_activity = helper.activity_map(selected_user,df)

        st.title('Activity timeline')
        col1,col2=st.columns(2)

        with col1:
            st.header('Weekdays Activity')
            fig,ax=plt.subplots()
            ax.bar(week_activity.index,week_activity.values)
            plt.xticks(rotation='vertical')
            st.pyplot(fig)

        with col2:
            st.header('Months Activity')
            fig,ax=plt.subplots()
            ax.bar(month_activity.index,month_activity.values,color='green')
            plt.xticks(rotation='vertical')
            st.pyplot(fig)

        #Heatmap
        st.title("Activity Heatmap")
        user_heatmap=helper.heatmap(selected_user,df)
        fig,ax=plt.subplots()
        sns.heatmap(user_heatmap)
        st.pyplot(fig)
