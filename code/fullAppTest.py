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
        return None, None

    # Build the YouTube service
    youtube = build('youtube', 'v3', developerKey=api_key)

    # Retrieve the channel details
    request = youtube.channels().list(
        part='brandingSettings,contentDetails,id,localizations,snippet,statistics,status,topicDetails',
        id=channel_id
    )
    response = request.execute()

    # Extract all details
    if response['items']:
        details = response['items'][0]
        return details
    else:
        return None

if __name__ == "__main__":
    # Replace with your API key and an array of channel names
    api_key = ''
    channel_names = ['Geeks and Gamers', 'The Critical Drinker', 'Nerdrotic']  # Add your channel names here
    
    printed_fields = set()  # To keep track of printed fields
    
    for channel_name in channel_names:
        details = get_channel_details(api_key, channel_name)
        if details:
            print(f"Channel Name: {channel_name}")
            
            subscriber_count = details['statistics'].get('subscriberCount')
            if subscriber_count and 'Subscriber Count' not in printed_fields:
                print(f"Subscriber Count: {subscriber_count}")
                printed_fields.add('Subscriber Count')
            
            view_count = details['statistics'].get('viewCount')
            if view_count and 'View Count' not in printed_fields:
                print(f"View Count: {view_count}")
                printed_fields.add('View Count')

            description = details['snippet'].get('description', 'N/A')
            if description and 'Description' not in printed_fields:
                print(f"Description: {description}")
                printed_fields.add('Description')

            country = details['snippet'].get('country', 'N/A')
            if country and 'Country' not in printed_fields:
                print(f"Country: {country}")
                printed_fields.add('Country')

            keywords = details['brandingSettings'].get('channel', {}).get('keywords', 'N/A')
            if keywords and 'Keywords' not in printed_fields:
                print(f"Keywords: {keywords}")
                printed_fields.add('Keywords')

            topic_details = details['topicDetails'].get('topicCategories', [])
            if topic_details and 'Topic Details' not in printed_fields:
                print(f"Topic Details: {', '.join(topic_details)}")
                printed_fields.add('Topic Details')

            uploads_playlist_id = details['contentDetails']['relatedPlaylists']['uploads']
            if uploads_playlist_id and 'Uploads Playlist ID' not in printed_fields:
                print(f"Uploads Playlist ID: {uploads_playlist_id}")
                printed_fields.add('Uploads Playlist ID')

            published_at = details['snippet'].get('publishedAt')
            if published_at and 'Published At' not in printed_fields:
                print(f"Published At: {published_at}")
                printed_fields.add('Published At')

            custom_url = details['snippet'].get('customUrl', 'N/A')
            if custom_url and 'Custom URL' not in printed_fields:
                print(f"Custom URL: {custom_url}")
                printed_fields.add('Custom URL')

            status = details['status'].get('privacyStatus')
            if status and 'Status' not in printed_fields:
                print(f"Status: {status}")
                printed_fields.add('Status')

            localizations = details.get('localizations', {})
            if localizations and 'Localizations' not in printed_fields:
                print("Localizations:")
                for locale, localization in localizations.items():
                    print(f" - {locale}: {localization}")
                printed_fields.add('Localizations')
            
            print("\n")
        else:
            print(f"Channel not found or invalid channel name: {channel_name}")
