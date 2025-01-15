import csv
from googleapiclient.discovery import build

def get_channel_id(api_key, channel_name):
    youtube = build('youtube', 'v3', developerKey=api_key)
    request = youtube.search().list(
        part='snippet',
        q=channel_name,
        type='channel'
    )
    response = request.execute()
    
    if response['items']:
        return response['items'][0]['id']['channelId']
    else:
        return None

def get_channel_details(api_key, channel_name):
    # Get the channel ID from the channel name
    channel_id = get_channel_id(api_key, channel_name)
    if not channel_id:
        return None, None, None, None, None

    # Build the YouTube service
    youtube = build('youtube', 'v3', developerKey=api_key)

    # Retrieve the channel details
    request = youtube.channels().list(
        part='statistics,topicDetails,brandingSettings',
        id=channel_id
    )
    response = request.execute()

    # Extract subscriber count, view count, topic details, and keywords
    if response['items']:
        subscriber_count = response['items'][0]['statistics']['subscriberCount']
        view_count = response['items'][0]['statistics']['viewCount']
        topic_details = response['items'][0].get('topicDetails', {}).get('topicCategories', [])
        keywords = response['items'][0].get('brandingSettings', {}).get('channel', {}).get('keywords', "")
        return int(subscriber_count), int(view_count), topic_details, keywords
    else:
        return None, None, None, None

if __name__ == "__main__":
    # Replace with your API key and an array of channel names
    api_key = ''
    channel_names = ['RenownedZ3r0','Robot Head','Ryan Kinel']  # Add your channel names here
    
    # Create a CSV file
    with open('youtube_channel_data.csv', mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        # Write the header row
        writer.writerow(['Channel Name', 'Subscriber Count', 'View Count', 'Topic Details', 'Keywords'])
        
        # Write channel details
        for channel_name in channel_names:
            subscriber_count, view_count, topic_details, keywords = get_channel_details(api_key, channel_name)
            if subscriber_count:
                writer.writerow([
                    channel_name,
                    subscriber_count,
                    view_count,
                    ', '.join(topic_details) if topic_details else 'None',
                    keywords if keywords else 'None'
                ])
            else:
                writer.writerow([channel_name, 'Channel not found or invalid channel name'])
                
    print("Data has been written to youtube_channel_data.csv")
