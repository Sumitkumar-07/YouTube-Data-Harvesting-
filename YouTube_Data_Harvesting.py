|---------------------------------------------------------------LIBRARIES---------------------------------------------------------------------------------|
import pandas as pd
import plotly.express as px
import streamlit as st
import mysql.connector as sql
import pymongo
from googleapiclient.discovery import build
from PIL import Image
import pymysql
from datetime import datetime

|------------------------------------------------------- SETTING PAGE CONFIGURATIONS----------------------------------------------------------------------|
icon = Image.open("youtube_logo.jpg")
st.set_page_config(
    page_title="Youtube Data Harvesting and Warehousing",
    page_icon=icon,
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={'About': """# This app is created by Sumit kumar!*"""})

|---------------------------------------------------------- CREATING OPTION MENU--------------------------------------------------------------------------|
selected = st.sidebar.radio(
    "Select an option:⬇️",
    options=["🏠Home", "⏳Extract and Transform", "😀View"],
)

|------------------------------------------------------------Connection To MongoDB------------------------------------------------------------------------|
client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client['youtube_data']

|------------------------------------------------------- CONNECTING WITH MYSQL DATABASE-------------------------------------------------------------------|
mydb = sql.connect(
    host="localhost",
    user="root",
    password="sumit",
    database="youtube_db"
)
mycursor = mydb.cursor(buffered=True)

|------------------------------------------------------ BUILDING CONNECTION WITH YOUTUBE API--------------------------------------------------------------|
api_key = "AIzaSyD-dOZ0jiC47X0vSURZkwokJM5gXYY2IVE"
youtube = build('youtube', 'v3', developerKey=api_key)


|-------------------------------------------------------- FUNCTION TO GET CHANNEL DETAILS-----------------------------------------------------------------|
def get_channel_details(channel_id):
    ch_data = []
    response = youtube.channels().list(
        part='snippet,contentDetails,statistics',
        id=channel_id).execute()
    for i in range(len(response['items'])):
        data = dict(
            Channel_id=channel_id[i],
            Channel_name=response['items'][i]['snippet']['title'],
            Playlist_id=response['items'][i]['contentDetails']['relatedPlaylists']['uploads'],
            Subscribers=response['items'][i]['statistics']['subscriberCount'],
            Views=response['items'][i]['statistics']['viewCount'],
            Total_videos=response['items'][i]['statistics']['videoCount'],
            Description=response['items'][i]['snippet']['description'],
            Country=response['items'][i]['snippet'].get('country')
        )
        ch_data.append(data)
    return pd.DataFrame(ch_data)


|-----------------------------------------------------------FUNCTION TO GET VIDEO IDS--------------------------------------------------------------------|
def get_channel_videos(channel_id):
    video_ids = []
    # get Uploads playlist id
    res = youtube.channels().list(id=channel_id, part='contentDetails').execute()
    playlist_id = res['items'][0]['contentDetails']['relatedPlaylists']['uploads']
    next_page_token = None

    while True:
        res = youtube.playlistItems().list(playlistId=playlist_id, part='snippet', maxResults=50, pageToken=next_page_token).execute()

        for i in range(len(res['items'])):
            video_ids.append(res['items'][i]['snippet']['resourceId']['videoId'])
        next_page_token = res.get('nextPageToken')

        if next_page_token is None:
            break
    return video_ids


|-------------------------------------------------------FUNCTION TO GET VIDEO DETAILS-------------------------------------------------------------------|
def get_video_details(v_ids):
    video_stats = []

    for i in range(0, len(v_ids), 50):
        response = youtube.videos().list(
            part="snippet,contentDetails,statistics",
            id=','.join(v_ids[i:i + 50])).execute()
        for video in response['items']:
            video_details = dict(
                Channel_name=video['snippet']['channelTitle'],
                Channel_id=video['snippet']['channelId'],
                Video_id=video['id'],
                Title=video['snippet']['title'],
                Tags=video['snippet'].get('tags'),
                Thumbnail=video['snippet']['thumbnails']['default']['url'],
                Description=video['snippet']['description'],
                Published_date=video['snippet']['publishedAt'],
                Duration=video['contentDetails']['duration'],
                Views=video['statistics']['viewCount'],
                Likes=video['statistics'].get('likeCount'),
                Comments=video['statistics'].get('commentCount'),
                Favorite_count=video['statistics']['favoriteCount'],
                Definition=video['contentDetails']['definition'],
                Caption_status=video['contentDetails']['caption']
            )
            video_stats.append(video_details)
    return pd.DataFrame(video_stats)


|--------------------------------------------------------FUNCTION TO GET COMMENT DETAILS----------------------------------------------------------------|
def get_comments_details(v_id):
    comment_data = []
    try:
        next_page_token = None
        while True:
            response = youtube.commentThreads().list(part="snippet,replies", videoId=v_id, maxResults=100, pageToken=next_page_token).execute()
            for cmt in response['items']:
                data = dict(
                    Comment_id=cmt['id'],
                    Video_id=cmt['snippet']['videoId'],
                    Comment_text=cmt['snippet']['topLevelComment']['snippet']['textDisplay'],
                    Comment_author=cmt['snippet']['topLevelComment']['snippet']['authorDisplayName'],
                    Comment_posted_date=cmt['snippet']['topLevelComment']['snippet']['publishedAt'],
                    Like_count=cmt['snippet']['topLevelComment']['snippet']['likeCount'],
                    Reply_count=cmt['snippet']['totalReplyCount']
                )
                comment_data.append(data)
            next_page_token = response.get('nextPageToken')
            if next_page_token is None:
                break
    except:
        pass
    return pd.DataFrame(comment_data)


|------------------------------------------------------FUNCTION TO GET CHANNEL NAMES FROM MONGODB------------------------------------------------------------|
def channel_names():
    ch_name = []
    for i in db.channel_details.find():
        ch_name.append(i['Channel_name'])
    return ch_name


|-------------------------------------------------------------------HOME PAGE-----------------------------------------------------------------------------|
if selected == "🏠Home":
    # Title Image

    col1, col2 = st.columns(2, gap='medium')
    col1.markdown("<p class='title'>YouTube Data Harvesting and Warehousing</p>", unsafe_allow_html=True)
    col1.markdown("#   ")
    col1.markdown("#   ")
    col1.markdown("- - - - - - - ")
    col1.markdown("## :blue[💻Technologies used] : Python, MongoDB, YouTube Data API, MySql, Streamlit", unsafe_allow_html=True)
    col1.markdown("## :blue[📑Overview] : Retrieving the YouTube channels data from the Google API, storing it in a MongoDB as data lake, migrating and transforming data into a SQL database, then querying the data and displaying it in the Streamlit app.", unsafe_allow_html=True)
    col1.markdown("- - - - - - - ")
    col2.markdown("#   ")
    col2.markdown("#   ")
    col2.markdown("#   ")
    col2.markdown("#   ")
    col2.markdown("#   ")
    col2.image("youtube_logo.jpg")
    col2.image("youtube_api.jpg")


|------------------------------------------------------------EXTRACT and TRANSFORM PAGE----------------------------------------------------------------------|
if selected == "⏳Extract and Transform":
    tab1, tab2 = st.tabs(["$\huge EXTRACT $ ", "$\huge TRANSFORM $"])

    # EXTRACT TAB
    with tab1:
        st.markdown("#    ")
        st.write("### Enter YouTube Channel_ID below:")
        ch_id = st.text_input(
            "Hint: Go to the channel's home page > Right click > View page source > Find channel_id").split(',')
        if ch_id and st.button("Extract Data"):
            ch_details = get_channel_details(ch_id)
            if not ch_details.empty:
                st.write(f'#### Extracted data from :green["{ch_details.iloc[0]["Channel_name"]}"] channel')
                st.table(ch_details)
            else:
                st.write("No data found for the given channel ID.")
        if st.button("Upload to MongoDB"):
            with st.spinner('Please Wait for it...'):
                ch_details = get_channel_details(ch_id)
                v_ids = get_channel_videos(ch_id)
                vid_details = get_video_details(v_ids)

                def comments():
                    com_d = []
                    for i in v_ids:
                        try:
                            com_d.append(get_comments_details(i))
                        except Exception as e:
                            print(f"Error processing video ID '{i}': {e}")
                    return pd.concat(com_d, ignore_index=True)

                comm_details = comments()
                collections1 = db.channel_details
                collections1.insert_many(ch_details.to_dict(orient='records'))
                collections2 = db.video_details
                collections2.insert_many(vid_details.to_dict(orient='records'))
                collections3 = db.comments_details
                collections3.insert_many(comm_details.to_dict(orient='records'))
                st.success("Upload to MongoDB successful!!")

    # TRANSFORM TAB
    with tab2:
        st.markdown("#   ")
        st.markdown("### Select a channel to begin Transformation to SQL")

        ch_names = channel_names()
        user_inp = st.selectbox("Select channel", options=ch_names)

|-------------------------------------------------FUNCTION TO INSERT DATA INTO MYSQL 'channels' TABLE-----------------------------------------------------------|
        def insert_into_channels():
            collections = db.channel_details
            query = """INSERT INTO channels (Channel_id, Channel_name, Playlist_id, Subscribers, Views, Total_videos, Description, Country) 
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"""
            for i in collections.find():
                try:
                    # Check if the channel_id already exists in the table
                    mycursor.execute(
                        "SELECT 1 FROM channels WHERE Channel_id = %s",
                        (i['Channel_id'],))
                    result = mycursor.fetchone()
                    if result is None:
                        mycursor.execute(query, (
                        i['Channel_id'], i['Channel_name'], i['Playlist_id'],
                        i['Subscribers'], i['Views'], i['Total_videos'],
                        i['Description'], i['Country']))
                        mydb.commit()
                except pymysql.Error as e:
                    st.error(f"Error inserting data into 'channels' table: {e}")

|---------------------------------------------------FUNCTION TO INSERT DATA INTO MYSQL 'videos' TABLE------------------------------------------------------------------------------------------------------------------------------------|
        def insert_into_videos():
            collections = db.video_details
            query = """INSERT INTO videos (Channel_name, Channel_id, Video_id, Title, Tags, Thumbnail, Description, Published_date, Duration, Views, Likes, Comments, Favorite_count, Definition, Caption_status)
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
            for i in collections.find():
                try:
                    # Check if the video_id already exists in the table
                    mycursor.execute(
                        "SELECT 1 FROM videos WHERE Video_id = %s",
                        (i['Video_id'],))
                    result = mycursor.fetchone()
                    if result is None:
                        # Convert the Tags list to a comma-separated string
                        tags_str = ','.join(i['Tags']) if i['Tags'] else None

                        # Convert Published_date to MySQL-compatible format
                        published_date = datetime.strptime(i['Published_date'],
                                                           '%Y-%m-%dT%H:%M:%SZ').strftime(
                            '%Y-%m-%d %H:%M:%S')

                        mycursor.execute(query, (
                            i['Channel_name'], i['Channel_id'], i['Video_id'],
                            i['Title'], tags_str, i['Thumbnail'],
                            i['Description'],
                            published_date, i['Duration'], i['Views'],
                            i['Likes'], i['Comments'], i['Favorite_count'],
                            i['Definition'], i['Caption_status']))
                        mydb.commit()
                except pymysql.Error as e:
                    st.error(f"Error inserting data into 'videos' table: {e}")
    
|--------------------------------------------------------FUNCTION TO INSERT DATA INTO MYSQL 'comments' TABLE-----------------------------------------------------------------------------------------|
        def insert_into_comments():
            collections = db.comments_details
            query = """INSERT INTO comments (Comment_id, Video_id, Comment_text, Comment_author, Comment_posted_date, Like_count, Reply_count)
                        VALUES (%s, %s, %s, %s, %s, %s, %s)"""
            for i in collections.find():
                try:
                    # Check if the comment_id already exists in the table
                    mycursor.execute(
                        "SELECT 1 FROM comments WHERE Comment_id = %s",
                        (i['Comment_id'],))
                    result = mycursor.fetchone()
                    if result is None:
                        # Convert Comment_posted_date to MySQL-compatible format
                        posted_date = datetime.strptime(
                            i['Comment_posted_date'],
                            '%Y-%m-%dT%H:%M:%SZ').strftime('%Y-%m-%d %H:%M:%S')

                        mycursor.execute(query, (
                            i['Comment_id'], i['Video_id'], i['Comment_text'],
                            i['Comment_author'], posted_date,
                            i['Like_count'], i['Reply_count']))
                        mydb.commit()
                except pymysql.Error as e:
                    st.error(
                        f"Error inserting data into 'comments' table: {e}")
        # TRANSFORMATION BUTTON
        if st.button("Transform Data"):
            with st.spinner('Please Wait for it...'):
                insert_into_channels()
                insert_into_videos()
                insert_into_comments()
                st.success("Transformation to SQL Database successful!!")


|------------------------------------------------------------------------VIEW PAGE--------------------------------------------------------------------------------------------|
if selected == "😀View":

    st.write("## :orange[Select any question to get Insights]")
    questions = st.selectbox('Questions',
                             [
                                 'Click the question that you would like to query',
                                 '1. What are the names of all the videos and their corresponding channels?',
                                 '2. Which channels have the most number of videos, and how many videos do they have?',
                                 '3. What are the top 10 most viewed videos and their respective channels?',
                                 '4. How many comments were made on each video, and what are their corresponding video names?',
                                 '5. Which videos have the highest number of likes, and what are their corresponding channel names?',
                                 '6. What is the total number of likes and dislikes for each video, and what are their corresponding video names?',
                                 '7. What is the total number of views for each channel, and what are their corresponding channel names?',
                                 '8. What are the names of all the channels that have published videos in the year 2022?',
                                 '9. What is the average duration of all videos in each channel, and what are their corresponding channel names?',
                                 '10. Which videos have the highest number of comments, and what are their corresponding channel names?'])

    if questions == '1. What are the names of all the videos and their corresponding channels?':
        mycursor.execute(
            """SELECT title AS Video_Title, channel_name AS Channel_Name FROM videos ORDER BY channel_name""")
        df = pd.DataFrame(mycursor.fetchall(), columns=mycursor.column_names)
        st.write(df)

    elif questions == '2. Which channels have the most number of videos, and how many videos do they have?':
        mycursor.execute("""SELECT channel_name 
            AS Channel_Name, total_videos AS Total_Videos
                                FROM channels
                                ORDER BY total_videos DESC""")
        df = pd.DataFrame(mycursor.fetchall(), columns=mycursor.column_names)
        st.write(df)
        st.write("### :green[Number of videos in each channel :]")
        # st.bar_chart(df,x= mycursor.column_names[0],y= mycursor.column_names[1])
        fig = px.bar(df,
                     x=mycursor.column_names[0],
                     y=mycursor.column_names[1],
                     orientation='v',
                     color=mycursor.column_names[0]
                     )
        st.plotly_chart(fig, use_container_width=True)

    elif questions == '3. What are the top 10 most viewed videos and their respective channels?':
        mycursor.execute("""SELECT channel_name AS Channel_Name, title AS Video_Title, views AS Views 
                                FROM videos
                                ORDER BY views DESC
                                LIMIT 10""")
        df = pd.DataFrame(mycursor.fetchall(), columns=mycursor.column_names)
        st.write(df)
        st.write("### :green[Top 10 most viewed videos :]")
        fig = px.bar(df,
                     x=mycursor.column_names[2],
                     y=mycursor.column_names[1],
                     orientation='h',
                     color=mycursor.column_names[0]
                     )
        st.plotly_chart(fig, use_container_width=True)

    elif questions == '4. How many comments were made on each video, and what are their corresponding video names?':
        mycursor.execute("""SELECT a.video_id AS Video_id, a.title AS Video_Title, b.Total_Comments
                                FROM videos AS a
                                LEFT JOIN (SELECT video_id,COUNT(comment_id) AS Total_Comments
                                FROM comments GROUP BY video_id) AS b
                                ON a.video_id = b.video_id
                                ORDER BY b.Total_Comments DESC""")
        df = pd.DataFrame(mycursor.fetchall(), columns=mycursor.column_names)
        st.write(df)

    elif questions == '5. Which videos have the highest number of likes, and what are their corresponding channel names?':
        mycursor.execute("""SELECT channel_name AS Channel_Name,title AS Title,likes AS Likes_Count 
                                FROM videos
                                ORDER BY likes DESC
                                LIMIT 10""")
        df = pd.DataFrame(mycursor.fetchall(), columns=mycursor.column_names)
        st.write(df)
        st.write("### :green[Top 10 most liked videos :]")
        fig = px.bar(df,
                     x=mycursor.column_names[2],
                     y=mycursor.column_names[1],
                     orientation='h',
                     color=mycursor.column_names[0]
                     )
        st.plotly_chart(fig, use_container_width=True)

    elif questions == '6. What is the total number of likes and dislikes for each video, and what are their corresponding video names?':
        mycursor.execute("""SELECT title AS Title, likes AS Likes_Count
                                FROM videos
                                ORDER BY likes DESC""")
        df = pd.DataFrame(mycursor.fetchall(), columns=mycursor.column_names)
        st.write(df)

    elif questions == '7. What is the total number of views for each channel, and what are their corresponding channel names?':
        mycursor.execute("""SELECT channel_name AS Channel_Name, views AS Views
                                FROM channels
                                ORDER BY views DESC""")
        df = pd.DataFrame(mycursor.fetchall(), columns=mycursor.column_names)
        st.write(df)
        st.write("### :green[Channels vs Views :]")
        fig = px.bar(df,
                     x=mycursor.column_names[0],
                     y=mycursor.column_names[1],
                     orientation='v',
                     color=mycursor.column_names[0]
                     )
        st.plotly_chart(fig, use_container_width=True)

    elif questions == '8. What are the names of all the channels that have published videos in the year 2022?':
        mycursor.execute("""SELECT channel_name AS Channel_Name
                                FROM videos
                                WHERE published_date LIKE '2022%'
                                GROUP BY channel_name
                                ORDER BY channel_name""")
        df = pd.DataFrame(mycursor.fetchall(), columns=mycursor.column_names)
        st.write(df)

    elif questions == '9. What is the average duration of all videos in each channel, and what are their corresponding channel names?':
        mycursor.execute("""SELECT channel_name AS Channel_Name,
                                AVG(duration)/60 AS "Average_Video_Duration (mins)"
                                FROM videos
                                GROUP BY channel_name
                                ORDER BY AVG(duration)/60 DESC""")
        df = pd.DataFrame(mycursor.fetchall(), columns=mycursor.column_names)
        mycursor.execute("""SELECT channel_name, 
                            SUM(duration_sec) / COUNT(*) AS average_duration
                            FROM (
                                SELECT channel_name, 
                                CASE
                                    WHEN duration REGEXP '^PT[0-9]+H[0-9]+M[0-9]+S$' THEN 
                                    TIME_TO_SEC(CONCAT(
                                    SUBSTRING_INDEX(SUBSTRING_INDEX(duration, 'H', 1), 'T', -1), ':',
                                SUBSTRING_INDEX(SUBSTRING_INDEX(duration, 'M', 1), 'H', -1), ':',
                                SUBSTRING_INDEX(SUBSTRING_INDEX(duration, 'S', 1), 'M', -1)
                                ))
                                    WHEN duration REGEXP '^PT[0-9]+M[0-9]+S$' THEN 
                                    TIME_TO_SEC(CONCAT(
                                    '0:', SUBSTRING_INDEX(SUBSTRING_INDEX(duration, 'M', 1), 'T', -1), ':',
                                    SUBSTRING_INDEX(SUBSTRING_INDEX(duration, 'S', 1), 'M', -1)
                                ))
                                    WHEN duration REGEXP '^PT[0-9]+S$' THEN 
                                    TIME_TO_SEC(CONCAT('0:0:', SUBSTRING_INDEX(SUBSTRING_INDEX(duration, 'S', 1), 'T', -1)))
                                    END AS duration_sec
                            FROM videos
                            ) AS subquery
                            GROUP BY channel_name""")
        df = pd.DataFrame(mycursor.fetchall(), columns=mycursor.column_names
                          )
        st.write(df)
        st.write("### :green[Avg video duration for channels :]")
        fig = px.bar(df,
                     x=mycursor.column_names[0],
                     y=mycursor.column_names[1],
                     orientation='v',
                     color=mycursor.column_names[0]
                     )
        st.plotly_chart(fig, use_container_width=True)
        st.write("### :green[Average video duration for channels :]")



    elif questions == '10. Which videos have the highest number of comments, and what are their corresponding channel names?':
        mycursor.execute("""SELECT channel_name AS Channel_Name,video_id AS Video_ID,comments AS Comments
                                FROM videos
                                ORDER BY comments DESC
                                LIMIT 10""")
        df = pd.DataFrame(mycursor.fetchall(), columns=mycursor.column_names)
        st.write(df)
        st.write("### :green[Videos with most comments :]")
        fig = px.bar(df,
                     x=mycursor.column_names[1],
                     y=mycursor.column_names[2],
                     orientation='v',
                     color=mycursor.column_names[0]
                     )
        st.plotly_chart(fig, use_container_width=True)
    st.markdown("#   ")
    st.markdown("## :mag: Choose the table to view the data :point_down:")
    choice = st.selectbox("", ("channels", "videos", "comments"))

|-------------------------------------------------------------FUNCTION TO SHOW TABLE DATA------------------------------------------------------------------------|
    def show_table(table_name):
        mycursor.execute(f"SELECT * FROM {table_name}")
        rows = mycursor.fetchall()
        col_names = [i[0] for i in mycursor.description]
        st.dataframe(pd.DataFrame(rows, columns=col_names))

    show_table(choice)


|------------------------------------------------------------------ MAIN FUNCTION--------------------------------------------------------------------------------|
def main():
    st.markdown("#   ")
    st.markdown("#   ")
    st.markdown("#   ")
    st.markdown("<p class='title'>YouTube Data Harvesting and Warehousing</p>", unsafe_allow_html=True)


    # CUSTOM CSS
    st.markdown(
        """
        <style>
        .title {
            font-size: 48px;
            font-weight: bold;
            color: #444;
            text-align: center;
        }
        .css-1aumxhk {
            font-size: 18px;
        }
        .css-ghj1mj {
            font-size: 24px;
            font-weight: bold;
            color: #0084ff;
        }
        </style>
        """,
        unsafe_allow_html=True
    )


# Running the app
if __name__ == "__main__":
    main()
