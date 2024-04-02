# Ownership: The NFT buyer will have full and exclusive ownership rights to the code, including the right to access, use, modify, execute, and distribute the code for any purpose, including commercial use. 
# Updates and Improvements: The buyer is entitled to all future updates and improvements made to the code, without any additional costs or restrictions.
# License: The code is provided with an open-source license (e.g., MIT License) to ensure maximum flexibility for the buyer.

# Note: The code is provided "as is" without warranties or guarantees of any kind.

import pandas as pd
import streamlit as st 
from googleapiclient.discovery import build
import csv
import sqlite3
import numpy as np
from datetime import timedelta
import json
from pymongo import MongoClient
# Set up the YouTube API service
try:
        def apiconnect():
            api_key = 'Your_api_key'
            api_service_name = "youtube"
            api_version = "v3"
            Youtube = build(api_service_name, api_version, developerKey=api_key)
            return Youtube

        # Call the apiconnect() function to initialize the Youtube object
        youtube = apiconnect()


        #Channel_name = input("Enter channel name: ")
        Channel_name = st.text_input("Enter channel name: ")


        # Use the Youtube object to search for the channel
        request = youtube.search().list(
            part="id,snippet",
            type="channel",
            maxResults=1,
            q=Channel_name,
        )
        response = request.execute()

        Channel_Id = response['items'][0]['id']['channelId']

        request = youtube.channels().list(
            part="snippet,contentDetails,statistics",
            id=Channel_Id
        )
        Response = request.execute()

        channel_id = response["items"][0]["id"]["channelId"]
        channel_name=response["items"][0]["snippet"]["title"]
        channel_description =response["items"][0]["snippet"]["description"]
        channel_subscribers =Response["items"][0]["statistics"]["subscriberCount"]
        channel_view_count=Response["items"][0]["statistics"]["viewCount"]
        channel_video_count=Response["items"][0]["statistics"]["videoCount"]
        channel_published_date=Response["items"][0]["snippet"]["publishedAt"]
        playlist_id =Response["items"][0]["contentDetails"]["relatedPlaylists"]["uploads"]

        channel_video_count = int(channel_video_count)
        channel_view_count = int(channel_view_count)
        channel_subscribers = int(channel_subscribers)

        data ={
                "channel_id": [channel_id],
                "channel_name": [channel_name],
                "channel_description": [channel_description],
                "channel_subscribers": [channel_subscribers],
                "channel_view_count": [channel_view_count],
                "channel_video_count": [channel_video_count],
                "channel_published_date": [channel_published_date],
                "playlist_id": [playlist_id],
            }
        with open ('channelinfo.json', 'w') as json_file:
            json.dump(data, json_file, indent=4)


        input_file_path = 'channelinfo.json'
        output_file_path = 'channelinfo.csv'

        df = pd.read_json(input_file_path)
        df.to_csv(output_file_path, index=False)      

        nextPageToken = None
        max_pages = 100
        for _ in range(max_pages):
            # Request the playlist items with the current nextPageToken
            request = youtube.playlistItems().list(
                part="snippet",
                playlistId=playlist_id,
                maxResults=10,
                pageToken=nextPageToken  # Use the nextPageToken from the previous page
            )

            # Execute the request
            response = request.execute()

            video_data_list = []

            for item in response['items']:
                video_id = item['snippet']['resourceId']['videoId']
                request = youtube.videos().list(
                    part="snippet,statistics,contentDetails,id",
                    id=video_id
                )
                response = request.execute()
                
                
                # Extract video information
                video_info = {
                    "video_id": video_id,
                    "channel_title": response['items'][0]['snippet']['channelTitle'],
                    "title": response['items'][0]['snippet']['title'],
                    "description": response['items'][0]['snippet']['description'],
                    "publish_at": response['items'][0]['snippet']['publishedAt'],
                    "view_count": response['items'][0]['statistics']['viewCount'],
                    "like_count": response['items'][0]['statistics']['likeCount'],
         
                    "duration": response['items'][0]['contentDetails']['duration']
                    }
                
                # Append the video information to the list
                video_data_list.append(video_info)

            # Write the list of video data to a JSON file
            with open('video_data.json', 'w', encoding='utf-8') as json_file:
                json.dump(video_data_list, json_file, ensure_ascii=False, indent=4)
            
            input_json_file = 'video_data.json'
            output_csv_file = 'video_data.csv'

            # Load the JSON data into a pandas DataFrame
            df = pd.read_json(input_json_file)

            # Convert the DataFrame to a CSV file
            df.to_csv(output_csv_file, index=False)      
            #print("JSON file 'video_data.json' created successfully.")

            # Update nextPageToken with the token for the next page (if available)
            nextPageToken = response.get('nextPageToken')

            # Exit the loop if there are no more pages to retrieve
            if not nextPageToken:
                break
        import json

        # Step 1: Read the JSON file
        input_file_path = 'video_data.json'
        output_file_path = 'output.json'

        with open(input_file_path, 'r') as json_file:
            data = json.load(json_file)

        # Step 2: Modify the data types
        for item in data:
            if 'duration' in item:
                duration = timedelta()
                iso_duration = item['duration']
                hours_pos = iso_duration.find("H")
                if "H" in iso_duration and hours_pos != -1:
                    hours = int(iso_duration[2:hours_pos])
                    duration += timedelta(hours=hours)

                minutes_pos = iso_duration.find("M")
                if "M" in iso_duration and minutes_pos != -1:
                    if hours_pos != -1:
                        minutes = int(iso_duration[hours_pos + 1:minutes_pos])
                    else:
                        minutes = int(iso_duration[2:minutes_pos])
                    duration += timedelta(minutes=minutes)

                seconds_pos = iso_duration.find("S")
                if "S" in iso_duration and seconds_pos != -1:
                    if minutes_pos != -1:
                        seconds = int(iso_duration[minutes_pos + 1:seconds_pos])
                    elif hours_pos != -1:
                        seconds = int(iso_duration[hours_pos + 1:seconds_pos])
                    else:
                        seconds = int(iso_duration[2:seconds_pos])
                    duration += timedelta(seconds=seconds)

                # Convert the duration to SQL time format
                seconds_in_day = duration.total_seconds()
                hours, remainder = divmod(seconds_in_day, 3600)
                minutes, seconds = divmod(remainder, 60)
                sql_time_format = "{:02}:{:02}:{:02}".format(int(hours), int(minutes), int(seconds))
                item['duration'] = sql_time_format
            if 'publish_at' in item:
                item['publish_at'] = item['publish_at'].split('T')[0]
            if 'view_count' in item:
                item['view_count'] = int(item['view_count'])
            if 'like_count' in item:
                item['like_count'] = int(item['like_count'])
            if 'comment_count' in item:
                item['comment_count'] = int(item['comment_count'])
        

        # Step 3: Write back to JSON
        with open(output_file_path, 'w') as json_file:
            json.dump(data, json_file, indent=4)
            
        print(f"Data types modified and saved to {output_file_path}")

        input_file_path = 'output.json'
        output_file_path = 'output.csv'

        df = pd.read_json(input_file_path)
        df.to_csv(output_file_path, index=False)      

            



        

        #/////////////////////////////////////////////////////////////////////////////////////////////////////////
        def datatable():
            df= pd.read_csv("output.csv")
            st.dataframe(df)

        def main():
            try:
                st.write('channel Name:',channel_name)
                st.write('Total Subscribers:',channel_subscribers)
                st.write('Total Views:',channel_view_count)
                st.write('Total Videos:',channel_video_count)
            except IndexError:
                st.write("IndexError: list index out of range. Please provide a valid index.")
        def outputtab():
            tab1, tab2, tab3 = st.tabs(["Channelfulldata", "ChannelData", "VideoDetails",])

            with tab1:
                datatable()
                st.balloons()
            with tab2:
                main()
                st.balloons()
            with tab3:
                Video_id=st.text_input("Enter video id : ")
                try:
                    def vd(Video_id):
                        request = youtube.videos().list(
                        part="snippet,contentDetails,statistics",
                        id=Video_id,
                        )
                        response = request.execute()
                        vid_id =response["items"][0]["snippet"]["thumbnails"]["medium"]["url"]
                        video_info=response['items'][0]
                        
                        st.title("video details")
                        st.image(vid_id)
                        video_link=f'https://www.youtube.com/watch?v={video_info["id"]}'
                        st.video(video_link)
                        st.balloons()  
                        return video_info
                    vd(Video_id)
                except:
                    st.error("Enter a valid video id")
                st.balloons()     
        st.write (outputtab())
                
        st.subheader('Save data in to SQL ,Channel Data in SQL Database',divider='rainbow')
                
        def save():
            if st.button("Load Data"):
                df = pd.read_csv("channelinfo.csv")

                conn = sqlite3.connect("channelinfo.db")
                df.to_sql("channelinfo", conn, if_exists="append",index=False)

                conn.commit()
                conn.close()
                
                df = pd.read_csv("output.csv")
                conn = sqlite3.connect("Youtube.db")
                df.to_sql("Youtube", conn, if_exists="append",index=False)
                conn.commit()
                conn.close()
                
                
            if st.button("Clear"):
                conn = sqlite3.connect("channelinfo.db")
                conn.execute("DELETE FROM channelinfo")
                conn.commit()
                conn.close()
                
                conn = sqlite3.connect("Youtube.db")
                conn.execute("DELETE FROM Youtube")
                conn.commit()
                conn.close()
        st.write(save())

    




        st.subheader('Data Analysis',divider='rainbow')

        def one():
            conn= sqlite3.connect("Youtube.db")
            query ="SELECT channel_title,title FROM Youtube;"
            df=pd.read_sql_query(query, conn)
            return df
        df1=one()
        def two():
            conn= sqlite3.connect("channelinfo.db")
            query ="SELECT channel_name,channel_video_count FROM channelinfo GROUP BY channel_name ORDER BY channel_video_count DESC;"
            df=pd.read_sql_query(query, conn)
            return df
        df2=two()
        def three():
            conn= sqlite3.connect("Youtube.db")
            query ="SELECT channel_title,title,SUM(view_count) as total_view FROM Youtube GROUP BY channel_title,title ORDER BY view_count DESC LIMIT 10;"
            df=pd.read_sql_query(query, conn)
            return df
        df3=three()
        def four():
            conn= sqlite3.connect("Youtube.db")
            query ="SELECT title,comment_count FROM Youtube ORDER BY comment_count DESC;"
            df=pd.read_sql_query(query, conn)
            return df
        df4=four()
        def five():
            conn= sqlite3.connect("Youtube.db")
            query ="""
                SELECT channel_title,title,SUM(like_count) as total_like    
                FROM Youtube 
                GROUP BY channel_title,title
                ORDER BY total_like DESC;
            """
            df=pd.read_sql_query(query, conn)
            return df
        df5=five()
        def six():
            conn= sqlite3.connect("Youtube.db")
            query = "SELECT title,like_count  FROM Youtube GROUP BY title "
            df=pd.read_sql_query(query, conn)
            return df
        df6=six()
        def seven():
            conn= sqlite3.connect("Youtube.db")
            query = "SELECT channel_title, SUM(view_count) AS total_view FROM Youtube GROUP BY channel_title ORDER BY total_view DESC;"
            df=pd.read_sql_query(query, conn)
            return df
        df7=seven()
        def eight():
            conn= sqlite3.connect("Youtube.db")
            query = "SELECT DISTINCT channel_title, publish_at FROM Youtube WHERE publish_at BETWEEN '2022-01-01' AND '2023-01-01';"
            df=pd.read_sql_query(query, conn)
            return df
        df8=eight()
        def nine():
            conn= sqlite3.connect("Youtube.db")
            query = """
                SELECT channel_title,AVG(duration) as total_duration FROM Youtube GROUP BY channel_title ORDER BY total_duration DESC
                """
            df=pd.read_sql_query(query, conn)
            return df
        df9=nine()
        def ten():
            conn= sqlite3.connect("Youtube.db")
            query = """
                SELECT channel_title,comment_count FROM Youtube  ORDER BY comment_count DESC
                """
            df=pd.read_sql_query(query, conn)
            return df
        df10=ten()
        option=st.selectbox('questions',('#1What are the names of all the videos and their corresponding channels?',
                                        '#2Which channels have the most number of videos, and how many videos do they have?',
                                        '#3What are the top 10 most viewed videos and their respective channels?',
                                        '#4How many comments were made on each video, and what are their corresponding video names?',
                                        '#5Which videos have the highest number of likes, and what are their corresponding channel names?',
                                        '#6What is the total number of likes and dislikes for each video, and what are their corresponding video names?',
                                        '#7What is the total number of views for each channel, and what are their corresponding channel names?',
                                        '#8What are the names of all the channels that have published videos in the year2022?',
                                        '#9What is the average duration of all videos in each channel, and what are their corresponding channel names?',
                                        '#10Which videos have the highest number of comments, and what are their corresponding channel names?'
                                        ))


        if option=='#1What are the names of all the videos and their corresponding channels?':
            st.write(df1)
        if option=='#2Which channels have the most number of videos, and how many videos do they have?':
            st.write(df2)
            st.bar_chart(df2.set_index('channel_name')['channel_video_count'])
        if option=='#3What are the top 10 most viewed videos and their respective channels?':
            st.write(df3)
            st.bar_chart(df3.set_index('title')['total_view'])
        if option=='#4How many comments were made on each video, and what are their corresponding video names?':
            st.write(df4)
            st.bar_chart(df4.set_index('title')['comment_count'])
        if option=='#5Which videos have the highest number of likes, and what are their corresponding channel names?':
            st.write(df5)
            st.bar_chart(df5.set_index('title')['total_like'])
        if option=='#6What is the total number of likes and dislikes for each video, and what are their corresponding video names?':
            st.write(df6)
            st.bar_chart(df6.set_index('title')['like_count'])
        if option=='#7What is the total number of views for each channel, and what are their corresponding channel names?':
            st.write(df7)
            st.bar_chart(df7.set_index('channel_title')['total_view'])
        if option=='#8What are the names of all the channels that have published videos in the year2022?':
            st.write(df8)
        if option=='#9What is the average duration of all videos in each channel, and what are their corresponding channel names?':
            st.write(df9)
        if option=='#10Which videos have the highest number of comments, and what are their corresponding channel names?':
            st.write(df10)
            st.bar_chart(df10.set_index('channel_title')['comment_count'])
except IndexError:
    st.write("not found")
