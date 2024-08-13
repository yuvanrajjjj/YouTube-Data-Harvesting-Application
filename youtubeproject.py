import googleapiclient.discovery
import pandas as pd
import mysql.connector
import time
import streamlit as slt
import datetime
from streamlit_option_menu import option_menu
import plotly.express as px

#API key connection to interact with youtube API
def connect_api_key():
    api_key="AIzaSyAqw4jPNNArMCiz8tQ5OaLqrmHv-cO6Fxg"
    api_service_name = "youtube"
    api_version = "v3"
    youtube=googleapiclient.discovery.build(api_service_name,
    api_version,developerKey=api_key)
    return youtube
youtube=connect_api_key()

# Function to retrieve channel details from YouTube
def get_channal_info(channel_id):
        LIST_DATA=[]
        request = youtube.channels().list(
            part="contentDetails,snippet,statistics",
            id=channel_id
        )
        response=request.execute()
        for i in response['items']:
                data=dict(channel_name=i['snippet']['title'],
                channel_id=i['id'],
                subscriptioncount=i['statistics']['subscriberCount'],
                viewscount=i['statistics']['viewCount'],
                description=i['snippet']['description'],
                playlist_id=i['contentDetails']['relatedPlaylists']['uploads'])
                LIST_DATA.append(data)

        return LIST_DATA

# Function to retrieve Video_ids from YouTube with help of channel_id
def get_video_id(channel_id):
    Video_ids=[]
    try:
        request=youtube.channels().list(part="contentDetails",
                                        id=channel_id)
        response=request.execute()
        playlist_id=response['items'][0]['contentDetails']['relatedPlaylists']['uploads']
        next_page_token=None
        while True:
            request_video=youtube.playlistItems().list(part="contentDetails,snippet",
                                                    playlistId= playlist_id,
                                                    maxResults=50,
                                                pageToken=next_page_token)
            response_video=request_video.execute()
            for i in range(len(response_video['items'])):
                data_1=response_video['items'][i]['snippet']['resourceId']['videoId']
                Video_ids.append(data_1)
            next_page_token=response_video.get('nextPageToken')
            if next_page_token is None:
                break
    except:
        pass
    return Video_ids

# Function to retrieve video details from YouTube
def time_duration(t):
            a = pd.Timedelta(t)
            b = str(a).split()[-1]
            return b
def get_video_info(Video_ids):
    video_data=[]
    try:
        for video_id in Video_ids:
            resquest_videoid=youtube.videos().list(
                part='contentDetails,snippet,statistics',
                id=video_id
            )            
            response_videoid=resquest_videoid.execute()
            for i in response_videoid['items']:
                data2=dict(Video_id=i['id'],
                            video_name=i['snippet']['title'],
                            channel_name=i['snippet']['channelTitle'],
                            video_description=i['snippet']['description'],
                            PublishedAt=i['snippet']['publishedAt'].replace("T"," ").replace("Z"," "),
                            view_count=i['statistics']['viewCount'],
                            like_count=i['statistics']['likeCount'],
                            Favorite_count=i['statistics']['favoriteCount'],
                            comment_count=i['statistics']['commentCount'],
                            duration=time_duration(i['contentDetails']['duration']),
                            Thumbnail=i['snippet']['thumbnails']['default']['url'],
                            caption_status=i['contentDetails']['caption'] )
            video_data.append(data2)
    except:
        pass
    return video_data

# Function to retrieve comments details from YouTube
def get_commend_info(Video_ids):
    video_comments=[]
    try:
        for video_id in Video_ids:
            request_comment = youtube.commentThreads().list(
                part="snippet",
                videoId=video_id
            )
            response_comment=request_comment.execute()
            #response_comment
            for i in response_comment['items']:
                data_3=dict(comment_id=i['snippet']['topLevelComment']['id'],
                            comment_text=i['snippet']['topLevelComment']['snippet']['textDisplay'],
                            comment_authour=i['snippet']['topLevelComment']['snippet']['authorDisplayName'],
                            comment_publishedat=i['snippet']['topLevelComment']['snippet']['publishedAt'].replace("T"," ").replace("Z"," "))
                video_comments.append(data_3)
    except:
        pass
    return video_comments

# Function to retrieve playlists details from YouTube
def get_playlist_info(channel_id):
    playlist=[]
    try:
        next_page_token=None
        while True:
            request_playlist=youtube.playlists().list(
                part="contentDetails,snippet",
                channelId=channel_id,
                maxResults=50,
                pageToken=next_page_token
            )
            response_playlist=request_playlist.execute()

            for i in response_playlist['items']:
                data_4=dict(playlist_id=i['id'],
                            channel_id=i['snippet']['channelId'],
                            playlist_name=i['snippet']['title'])
                playlist.append(data_4)
                
            next_page_token=response_playlist.get('nextPageToken')
            if next_page_token is None:
                break
    except:
        pass
    return playlist

                                           
# streamlit-Application Details
with slt.sidebar:
    web=option_menu(
        menu_title="Youtube Data Harvesting",
        options=["HOME","DATA COLLECTION","MIGRATE TO SQL","DATA ANALYSIS AND VISUALIZATION"],
        icons=["house","upload","database","bar-chart"]
 )

# Home_page settings
if web == "HOME":
    # Display the YouTube logo
    slt.image("youtubelogo.jpg", width=500)

    # Welcome Title
    slt.markdown("<h1 style='text-align: center; color: blue;'>🎉 Welcome to YouTube Data Harvesting 🎉</h1>",
                 unsafe_allow_html=True)

    # Project Overview Section
    slt.markdown("<h2 style='color: red;'>📋 Project Overview:</h2>", unsafe_allow_html=True)
    slt.markdown('''
    <div style="font-size:18px; line-height:1.6">
        Explore comprehensive analytics and insights from YouTube data. 
        This dashboard allows you to gather, analyze, and visualize YouTube channel 
        and video data using the latest API technologies and SQL-based data warehousing.
        Leverage Streamlit for an interactive and user-friendly experience.
    </div>
    ''', unsafe_allow_html=True)

    # Core Technologies Section
    slt.markdown("<h2 style='color: red;'>💻 Core Technologies:</h2>", unsafe_allow_html=True)
    slt.markdown('''
    <div style="font-size:18px; line-height:1.6">
        <ul>
            <li>Python</li>
            <li>YouTube Data API</li>
            <li>SQL Database Management</li>
            <li>Data Visualization with Streamlit</li>
        </ul>
    </div>
    ''', unsafe_allow_html=True)

    # Features Section
    slt.markdown("<h2 style='color: red;'>🚀 Features:</h2>", unsafe_allow_html=True)
    slt.markdown('''
    <div style="font-size:18px; line-height:1.6">
        <ul>
            <li>🔍 <b>Data Collection:</b> Fetch and aggregate YouTube channel and video information.</li>
            <li>🗄️ <b>Data Warehousing:</b> Store and manage data efficiently using SQL.</li>
            <li>📊 <b>Data Analysis:</b> Query and analyze data for meaningful insights.</li>
            <li>📈 <b>Visualization:</b> Create interactive charts and reports with Streamlit.</li>
        </ul>
    </div>
    ''', unsafe_allow_html=True)

# Data-page setting
if web == "DATA COLLECTION":
    # Title for the Data Collection section
    slt.markdown("<h1 style='text-align: center; color: blue;'>🔍 YouTube Data Collection</h1>", unsafe_allow_html=True)

    # Text input for Channel ID
    C = slt.text_input("📺 Enter the Channel ID")

    if C:
        channel_s = get_channal_info(channel_id=C)
        video_s = get_video_info(Video_ids=get_video_id(channel_id=C))
        playlist_s = get_playlist_info(channel_id=C)
        comments_s = get_commend_info(Video_ids=get_video_id(channel_id=C))

    # Submit button
    if slt.button("🚀 Submit"):
        slt.success("✅ Channel ID submitted successfully!")

        with slt.spinner('⏳ Fetching data, please wait...'):
            time.sleep(5)

            # Displaying the dataframes with headers
            slt.markdown("<h2 style='color: red;'>📊 Channel Information</h2>", unsafe_allow_html=True)
            slt.dataframe(channel_s)

            slt.markdown("<h2 style='color: red;'>🎥 Video Information</h2>", unsafe_allow_html=True)
            slt.dataframe(video_s)

            slt.markdown("<h2 style='color: red;'>💬 Comments Information</h2>", unsafe_allow_html=True)
            slt.dataframe(comments_s)

            slt.markdown("<h2 style='color: red;'>📜 Playlist Information</h2>", unsafe_allow_html=True)
            slt.dataframe(playlist_s)

if web == "MIGRATE TO SQL":
    # Title for the SQL Migration section
    slt.markdown("<h1 style='text-align: center; color: blue;'>🔄 Migrate YouTube Data to SQL</h1>",
                 unsafe_allow_html=True)

    # Input for Channel ID
    C = slt.text_input("🎯 Enter the Channel ID")

    # Migration button
    if slt.button("💾 Migrate to SQL"):
        slt.info("🔌 Connecting to MySQL database...")

        conn = mysql.connector.connect(host="localhost", user="root", password="123456789", database="youtube")

        if conn.is_connected():
            slt.success("✅ Connected to MySQL database successfully!")
        else:
            slt.error("❌ Failed to connect to the database.")

        # Create or connect to the database
        my_cursor = conn.cursor()
        my_cursor.execute("CREATE DATABASE IF NOT EXISTS youtube")
        my_cursor.close()

        # Creating tables with feedback messages
        slt.info("🛠️ Setting up database tables...")

        my_cursor = conn.cursor()

        # Create table - CHANNEL
        my_cursor.execute('''CREATE TABLE IF NOT EXISTS channel (
                                channel_name VARCHAR(225),
                                channel_id VARCHAR(225) PRIMARY KEY,
                                subscriptioncount BIGINT,
                                viewscount INT,
                                description TEXT,
                                playlist_id VARCHAR(225)
                            )''')

        # Create table - VIDEO
        my_cursor.execute('''CREATE TABLE IF NOT EXISTS videos (
                                Video_id VARCHAR(225) PRIMARY KEY,
                                video_name VARCHAR(225),
                                channel_name VARCHAR (225),
                                video_description TEXT,
                                PublishedAt TIMESTAMP,
                                view_count BIGINT,
                                like_count BIGINT,
                                Favorite_count INT,
                                comment_count  INT,
                                duration TIME,
                                Thumbnail TEXT,
                                caption_status TEXT
                            )''')

        # Create table - PLAYLIST
        my_cursor.execute('''CREATE TABLE IF NOT EXISTS playlist (
                                playlist_id VARCHAR(225),
                                channel_id VARCHAR(225),
                                playlist_name VARCHAR(225)
                            )''')

        # Create table - COMMENT
        my_cursor.execute('''CREATE TABLE IF NOT EXISTS comments (
                                comment_id VARCHAR(225),
                                comment_text TEXT,
                                comment_authour VARCHAR(225),
                                comment_publishedat TIMESTAMP
                            )''')

        my_cursor.close()
        slt.success("📂 Tables created successfully!")

        # Transform corresponding data into pandas dataframes
        slt.info("🔄 Transforming data into dataframes...")
        df_channel = pd.DataFrame(get_channal_info(channel_id=C))
        df_video = pd.DataFrame(get_video_info(Video_ids=get_video_id(channel_id=C)))
        df_playlist = pd.DataFrame(get_playlist_info(channel_id=C))
        df_comments = pd.DataFrame(get_commend_info(Video_ids=get_video_id(channel_id=C)))

        # Insert DataFrame into channel table
        my_cursor = conn.cursor()
        slt.info("📤 Migrating channel data...")
        for index, row in df_channel.iterrows():
            table_insert_query = '''INSERT INTO channel (channel_name, channel_id, subscriptioncount, viewscount, description, playlist_id)
                                    VALUES (%s, %s, %s, %s, %s, %s)'''
            values = (
            row["channel_name"], row["channel_id"], row["subscriptioncount"], row["viewscount"], row["description"],
            row["playlist_id"])
            my_cursor.execute(table_insert_query, values)

        conn.commit()
        my_cursor.close()

        # Insert DataFrame into playlist table
        my_cursor = conn.cursor()
        slt.info("📤 Migrating playlist data...")
        for index, row in df_playlist.iterrows():
            table_insert_query1 = '''INSERT INTO playlist (playlist_id, channel_id, playlist_name)
                                    VALUES (%s, %s, %s)'''
            values = (row["playlist_id"], row["channel_id"], row["playlist_name"])
            my_cursor.execute(table_insert_query1, values)

        conn.commit()
        my_cursor.close()

        # Insert DataFrame into comments table
        my_cursor = conn.cursor()
        slt.info("📤 Migrating comments data...")
        for index, row in df_comments.iterrows():
            table_insert_query2 = '''INSERT INTO comments (comment_id, comment_text, comment_authour, comment_publishedat)
                                    VALUES (%s, %s, %s,%s)'''
            values = (row["comment_id"], row["comment_text"], row["comment_authour"], row["comment_publishedat"])
            my_cursor.execute(table_insert_query2, values)

        conn.commit()
        my_cursor.close()

        # Insert DataFrame into videos table
        my_cursor = conn.cursor()
        slt.info("📤 Migrating videos data...")
        for index, row in df_video.iterrows():
            table_insert_queryy = '''INSERT INTO videos (Video_id, video_name, channel_name ,video_description, PublishedAt, view_count, like_count,
                                                        Favorite_count, comment_count, duration, Thumbnail, caption_status)
                                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'''
            values = (
            row["Video_id"], row["video_name"], row["channel_name"], row["video_description"], row["PublishedAt"],
            row["view_count"], row["like_count"],
            row["Favorite_count"], row["comment_count"], row["duration"], row["Thumbnail"], row["caption_status"])
            my_cursor.execute(table_insert_queryy, values)

        conn.commit()
        my_cursor.close()

        slt.success("🎉 Data migration to SQL completed successfully!")

#query and visualization-page setting
if web=="DATA ANALYSIS AND VISUALIZATION":
    slt.header("SELECT THE QUESTIONS TO GET INSIGHTS")
    options=slt.selectbox("Select options",("1.What are the names of all the videos and their corresponding channels?",
                          "2.Which channels have the most number of videos, and how many videos do they have?",
                          "3.What are the top 10 most viewed videos and their respective channels?",
                          "4.How many comments were made on each video, and what are their corresponding video names?",
                          "5.Which videos have the highest number of likes, and what are their corresponding channel names?",
                          "6.What is the total number of likes and dislikes for each video, and what are  their corresponding video names?",
                          "7.What is the total number of views for each channel, and what are their corresponding channel names?",
                          "8.What are the names of all the channels that have published videos in the year 2022?",
                          "9.What is the average duration of all videos in each channel, and what are their corresponding channel names?",
                          "10.Which videos have the highest number of comments, and what are their corresponding channel names?"))
    
    # Query to excute 1st Question
    if options=="1.What are the names of all the videos and their corresponding channels?":
            if slt.button("SUBMIT"):
                conn = mysql.connector.connect(host="localhost", user="root", password="123456789",database="youtube")
                my_cursor = conn.cursor()
                my_cursor.execute(''' select video_name,channel_name from videos
                                order by channel_name''')
                out=my_cursor.fetchall()
                que_1=pd.DataFrame(out,columns=["vidoe_name","channel_name"])
                slt.success("ANSWER")
                slt.write(que_1)

    # Query to excute 2nd Question
    if options=="2.Which channels have the most number of videos, and how many videos do they have?":
            if slt.button("SUBMIT"):
                conn = mysql.connector.connect(host="localhost", user="root", password="123456789",database="youtube")
                my_cursor = conn.cursor()
                my_cursor.execute(''' select distinct channel_name, count(Video_id) from videos
                                    group by channel_name
                                    order by count(Video_id)  desc''')
                out=my_cursor.fetchall()
                que_2=pd.DataFrame(out,columns=["channel_name","video_count"])
                slt.success("ANSWER")
                slt.write(que_2)

                # Setting up the option "Data Visualization" in streamlit page
                fix=px.bar(que_2, x="channel_name",y="video_count",title="VIDEOS COUNT")
                slt.plotly_chart(fix)

    # Query to excute 3rd Question
    if options=="3.What are the top 10 most viewed videos and their respective channels?":
            if slt.button("SUBMIT"):
                conn = mysql.connector.connect(host="localhost", user="root", password="123456789",database="youtube")
                my_cursor = conn.cursor()
                my_cursor.execute(''' select channel_name,video_name,view_count  from videos
                                order by view_count desc ''')
                out=my_cursor.fetchall()
                que_3=pd.DataFrame(out,columns=["channel_name","video_name","view_count"])
                slt.success("ANSWER")
                slt.write(que_3)

                # Setting up the option "Data Visualization" in streamlit page
                fix=px.bar(que_3, x="channel_name",y="view_count",title="VIDEOS COUNT",color="channel_name")
                slt.plotly_chart(fix)

    # Query to excute 4th Question
    if options=="4.How many comments were made on each video, and what are their corresponding video names?":
            if slt.button("SUBMIT"):
                conn = mysql.connector.connect(host="localhost", user="root", password="123456789",database="youtube")
                my_cursor = conn.cursor()
                my_cursor.execute(''' select video_name, comment_count from videos
                                    order by comment_count desc limit 100''')
                out=my_cursor.fetchall()
                que_4=pd.DataFrame(out,columns=["video_name","total_comments_count"])
                slt.success("ANSWER")
                slt.write(que_4)

    # Query to excute 5th Question
    if options=="5.Which videos have the highest number of likes, and what are their corresponding channel names?":
            if slt.button("SUBMIT"):
                conn = mysql.connector.connect(host="localhost", user="root", password="123456789",database="youtube")
                my_cursor = conn.cursor()
                my_cursor.execute(''' select videos.video_name,videos.like_count,videos.channel_name  from videos
                                    order by videos.like_count desc limit 100''')
                out=my_cursor.fetchall()
                que_5=pd.DataFrame(out,columns=["video_name","like_count","channel_name"])
                slt.success("ANSWER")
                slt.write(que_5)

                # Setting up the option "Data Visualization" in streamlit page
                fix=px.bar(que_5, x="channel_name",y="like_count",title="LIKE COUNT",color="channel_name")
                slt.plotly_chart(fix)

    # Query to excute 6th Question
    if options=="6.What is the total number of likes and dislikes for each video, and what are  their corresponding video names?":
            if slt.button("SUBMIT"):
                conn = mysql.connector.connect(host="localhost", user="root", password="123456789",database="youtube")
                my_cursor = conn.cursor()
                my_cursor.execute(''' select video_name,like_count  from videos
                                    order by like_count desc limit 100''')
                out=my_cursor.fetchall()
                que_6=pd.DataFrame(out,columns=["video_name","like_count"])
                slt.success("ANSWER")
                slt.write(que_6)

    # Query to excute 7th Question
    if options=="7.What is the total number of views for each channel, and what are their corresponding channel names?":
            if slt.button("SUBMIT"):
                conn = mysql.connector.connect(host="localhost", user="root", password="123456789",database="youtube")
                my_cursor = conn.cursor()
                my_cursor.execute(''' select channel_name,viewscount as total_views from channel
                                    order by viewscount desc ''')
                out=my_cursor.fetchall()
                que_7=pd.DataFrame(out,columns=["channel_name","total_views"])
                slt.success("ANSWER")
                slt.write(que_7)

                # Setting up the option "Data Visualization" in streamlit page
                fix=px.bar(que_7, x="channel_name",y="total_views",title="TOTAL_VIEWS",color="channel_name")
                slt.plotly_chart(fix)

    # Query to excute 8th Question
    if options=="8.What are the names of all the channels that have published videos in the year 2022?":
            if slt.button("SUBMIT"):
                conn = mysql.connector.connect(host="localhost", user="root", password="123456789",database="youtube")
                my_cursor = conn.cursor()
                my_cursor.execute(''' select channel_name,video_name, PublishedAt from videos
                                    where year(videos.PublishedAt)=2022
                                ''')
                out=my_cursor.fetchall()
                que_8=pd.DataFrame(out,columns=["channel_name","video_name","PublishedAt"])
                slt.success("ANSWER")
                slt.write(que_8)

    # Query to excute 9th Question      
    if options=="9.What is the average duration of all videos in each channel, and what are their corresponding channel names?":
            if slt.button("SUBMIT"):
                conn = mysql.connector.connect(host="localhost", user="root", password="123456789",database="youtube")
                my_cursor = conn.cursor()
                my_cursor.execute(''' select channel_name,avg(duration)/60 as durations from videos
                                    group by channel_name
                                    order by durations
                                ''')
                out=my_cursor.fetchall()
                que_9=pd.DataFrame(out,columns=["channel_name","durations"])
                slt.success("ANSWER")
                slt.write(que_9)

                # Setting up the option "Data Visualization" in streamlit page
                fix=px.bar(que_9, x="channel_name",y="durations",title="VIDEO TIME DURATION",color="channel_name")
                slt.plotly_chart(fix)

    # Query to excute 10th Question
    if options=="10.Which videos have the highest number of comments, and what are their corresponding channel names?":
            if slt.button("SUBMIT"):
                conn = mysql.connector.connect(host="localhost", user="root", password="123456789",database="youtube")
                my_cursor = conn.cursor()
                my_cursor.execute(''' select video_name,comment_count,channel_name from videos
                                    order by comment_count desc limit 100''')
                out=my_cursor.fetchall()
                que_10=pd.DataFrame(out,columns=["video_name","comment_count","channel_name"])
                slt.success("ANSWER")
                slt.write(que_10)

                # Setting up the option "Data Visualization" in streamlit page
                fix=px.bar(que_10, x="channel_name",y="comment_count",title="HIGHEST COMMENTS COUNT",color="channel_name")
                slt.plotly_chart(fix)
