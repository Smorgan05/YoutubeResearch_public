import csv
import os
from googleapiclient.discovery import build
from datetime import datetime, timedelta

def get_channel_uploads_playlist_id(api_key, channel_name):
    youtube = build('youtube', 'v3', developerKey=api_key)
    request = youtube.search().list(
        part='snippet',
        q=channel_name,
        type='channel'
    )
    response = request.execute()

    if response['items']:
        channel_id = response['items'][0]['id']['channelId']
        request = youtube.channels().list(
            part='contentDetails',
            id=channel_id
        )
        response = request.execute()
        if response['items']:
            uploads_playlist_id = response['items'][0]['contentDetails']['relatedPlaylists']['uploads']
            return uploads_playlist_id
    return None

def get_videos_from_playlist(api_key, playlist_id, start_date, end_date):
    youtube = build('youtube', 'v3', developerKey=api_key)
    videos = []
    next_page_token = None

    while True:
        request = youtube.playlistItems().list(
            part='snippet',
            playlistId=playlist_id,
            maxResults=50,
            pageToken=next_page_token
        )
        response = request.execute()

        for item in response['items']:
            video_published_at = item['snippet']['publishedAt']
            video_published_at_date = datetime.strptime(video_published_at, "%Y-%m-%dT%H:%M:%SZ")
            if start_date <= video_published_at_date <= end_date:
                videos.append({
                    'title': item['snippet']['title'],
                    'videoId': item['snippet']['resourceId']['videoId'],
                    'publishedAt': video_published_at
                })

        next_page_token = response.get('nextPageToken')
        if not next_page_token:
            break
    
    return videos

def write_videos_to_csv(videos, channel_name):
    filename = f"{channel_name}_videos.csv"
    try:
        with open(filename, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(['Title', 'Video ID', 'Published At'])
            for video in videos:
                writer.writerow([video['title'], video['videoId'], video['publishedAt']])
        print(f"Data for {channel_name} has been written to {filename}")
    except FileNotFoundError:
        print(f"Error: The file {filename} could not be created. Please check the directory path and try again.")

if __name__ == "__main__":
    # Replace with your API key and an array of channel names
    api_key = ''
    channel_names = ['MooLer','Moon','Nerd Word','Nerdrotic']  # Add your channel names here

    # Define the date range
    start_date = datetime(2023, 1, 1)
    end_date = datetime(2024, 1, 1)

    for channel_name in channel_names:
        uploads_playlist_id = get_channel_uploads_playlist_id(api_key, channel_name)
        if uploads_playlist_id:
            videos = get_videos_from_playlist(api_key, uploads_playlist_id, start_date, end_date)
            if videos:
                write_videos_to_csv(videos, channel_name)
            else:
                print(f"No videos found for {channel_name} in the specified date range.")
        else:
            print(f"Channel not found or invalid channel name: {channel_name}")
