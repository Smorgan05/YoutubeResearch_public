from googleapiclient.discovery import build
import re
import csv

# Set up the YouTube API client
api_key = ''
youtube = build('youtube', 'v3', developerKey=api_key)

def get_video_details(video_id):
    try:
        # Fetch video details
        response = youtube.videos().list(
            part='snippet',
            id=video_id
        ).execute()

        if 'items' in response and len(response['items']) > 0:
            snippet = response['items'][0]['snippet']
            description = snippet.get('description', '')
            channel_id = snippet['channelId']
            tags = snippet.get('tags', [])
            return channel_id, description, tags
        return None, None, None
    except Exception as e:
        print(f"An error occurred while fetching video details: {e}")
        return None, None, None

def get_channel_name(channel_id):
    try:
        # Fetch channel details
        response = youtube.channels().list(
            part='snippet',
            id=channel_id
        ).execute()

        if 'items' in response and len(response['items']) > 0:
            return response['items'][0]['snippet']['title']
        return None
    except Exception as e:
        print(f"An error occurred while fetching channel details: {e}")
        return None

def extract_collaborations(description):
    # Regex to find YouTube channel mentions in the description
    pattern = r'@[^\s@]+'
    collaborations = re.findall(pattern, description)
    return list(set(collaborations))

def read_video_ids_from_csv(input_csv_path):
    video_data = []
    with open(input_csv_path, mode='r', encoding='utf-8') as file:
        reader = csv.reader(file)
        next(reader)  # Skip the header row
        for row in reader:
            if len(row) >= 3:  # Ensure there are at least three columns
                video_id = row[2]
                video_data.append(row)
    return video_data

def add_collaborations_to_csv(input_csv_path, output_csv_path):
    video_data = read_video_ids_from_csv(input_csv_path)
    
    with open(output_csv_path, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        header = ["ChannelName", "Video Title", "Video ID", "Published At", "Collaborating Channels"]
        writer.writerow(header)

        for row in video_data:
            video_id = row[2]
            channel_id, description, _ = get_video_details(video_id)
            if channel_id and description:
                collaborations = extract_collaborations(description)
                row.append(", ".join(collaborations))
            else:
                row.append("No collaborations found")
            writer.writerow(row)
            print(f"Collaborations for video ID {video_id}: {collaborations}")

# Replace with your input CSV file path and output CSV file path
input_csv_path = 'chunk_3.csv'
output_csv_path = 'chunk_3_collaborations.csv'
add_collaborations_to_csv(input_csv_path, output_csv_path)
