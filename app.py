import streamlit as st
import Preprocessor,helper
import matplotlib.pyplot as plt
import seaborn as sb

st.sidebar.title("Whatsapp Chat Analyzer")

uploaded_file = st.sidebar.file_uploader("Choose a file")
if uploaded_file is not None:
    bytes_data = uploaded_file.getvalue()
    data = bytes_data.decode("utf-8")
    # st.text(data)

    df = Preprocessor.preprocess(data)

    # To display dataframe in streamlit 
    # st.dataframe(df)

    user_list = df['user'].unique().tolist()
    user_list.sort()
    user_list.insert(0,"Overall")
    selected_user = st.sidebar.selectbox("Show analysis wrt user",user_list)

    if st.sidebar.button("Show Analysis"):
        num_msges,num_words,num_media_msg,num_link_msg =  helper.fetch_stats(selected_user,df)

        st.title("Top Statistics")
        col1,col2,col3,col4 = st.columns(4)

        with col1:
            st.header("Total Messages")
            st.title(num_msges)
        with col2:
            st.header("Total words")
            st.title(num_words)
        with col3:
            st.header("Media shared")
            st.title(num_media_msg)
        with col4:
            st.header("Links shared")
            st.title(num_link_msg)

        # Monthly Timeline
        st.title("Monthly Timeline")
        timeline = helper.monthly_timeline(selected_user,df)
        fig,ax = plt.subplots()
        ax.plot(timeline['time'],timeline['message'],color = 'green')
        plt.xticks(rotation = 'vertical')
        st.pyplot(fig)

        # Daily Timeline
        st.title("Daily Timeline")
        daily_timeline = helper.daily_timeline(selected_user,df)
        fig,ax = plt.subplots()
        ax.plot(daily_timeline['Date'],daily_timeline['message'])
        plt.xticks(rotation = 'vertical')
        st.pyplot(fig)

        # Activity map
        st.title("Activity Map")
        col1,col2 = st.columns(2)

        with col1:
            st.header("Most busy day")
            busy_day = helper.week_activity_map(selected_user,df)
            fig,ax = plt.subplots()
            ax.bar(busy_day.index,busy_day.values)
            plt.xticks(rotation = 'vertical')
            st.pyplot(fig)

        with col2:
            st.header("Most busy month")
            busy_month = helper.month_activity_map(selected_user,df)
            fig,ax = plt.subplots()
            ax.bar(busy_month.index,busy_month.values,color = 'orange')
            plt.xticks(rotation = 'vertical')
            st.pyplot(fig)

        st.title("Weekly Activity Map")
        user_heatmap = helper.activity_heatmap(selected_user,df)
        fig,ax = plt.subplots()
        ax = sb.heatmap(user_heatmap)
        st.pyplot(fig)


        # Finding the bussiest users in the group(Group level)
        if selected_user == 'Overall':
            st.title("Most Busy Users")
            x,new_df = helper.most_busy_user(df)
            fig,ax = plt.subplots()
            col1,col2 = st.columns(2)

            with col1:
                ax.bar(x.index,x.values,color = "red")
                plt.xticks(rotation = 45)
                st.pyplot(fig)

            with col2:
                st.dataframe(new_df)
            
        # Wordcloud
        st.title("WordCloud")
        df_wc = helper.create_wordcloud(selected_user,df)
        fig,ax = plt.subplots()
        plt.axis('off')
        ax.imshow(df_wc)
        st.pyplot(fig)

        st.title("Most Common Words")
        most_common_word_df = helper.most_common_words(selected_user,df)
        fig,ax = plt.subplots()
        ax.bar(most_common_word_df[0],most_common_word_df[1])
        plt.xticks(rotation = 'vertical')
        st.pyplot(fig)

        # Emoji Ananlysis
        st.title("Emoji Analysis")
        emoji_df = helper.emoji_helper(selected_user,df)

        col1,col2 = st.columns(2)
        with col1:
            st.dataframe(emoji_df)
        with col2:
            fig,ax = plt.subplots()
            ax.pie(emoji_df['count'].head(),labels = emoji_df["emoji"].head(),autopct="%0.2f")
            st.pyplot(fig)
    