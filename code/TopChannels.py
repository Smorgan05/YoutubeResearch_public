import csv
from googleapiclient.discovery import build

def get_top_channels(api_key, max_results=50):
    youtube = build('youtube', 'v3', developerKey=api_key)
    request = youtube.channels().list(
        part='statistics,snippet',
        order='subscriberCount',
        maxResults=max_results
    )
    response = request.execute()
    return response['items']

def write_to_csv(channel_data, filename='top_youtube_channels.csv'):
    with open(filename, mode='w', newline='') as file:
        writer = csv.writer(file)
        # Write the header row
        writer.writerow(['Channel Name', 'Subscriber Count', 'Video Count', 'Channel ID'])
        
        # Write channel details
        for channel in channel_data:
            writer.writerow([
                channel['snippet']['title'],
                channel['statistics']['subscriberCount'],
                channel['statistics']['videoCount'],
                channel['id']
            ])

if __name__ == "__main__":
    # Replace with your API key
    api_key = ''
    
    # Get the top YouTube channels
    top_channels = get_top_channels(api_key)
    
    # Write the data to a CSV file
    write_to_csv(top_channels)
    
    print(f"Data has been written to {'top_youtube_channels.csv'}")
