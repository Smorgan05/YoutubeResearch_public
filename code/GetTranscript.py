import csv
import os
import time
from youtube_transcript_api import YouTubeTranscriptApi

def get_transcript(video_id):
    try:
        # Check if subtitles are available
        if not YouTubeTranscriptApi.has_transcript(video_id):
            return "Subtitles are disabled for this video."
        
        # Fetch transcript
        transcript = YouTubeTranscriptApi.get_transcript(video_id)

        # Combine transcript segments
        full_transcript = " ".join([segment['text'] for segment in transcript])

        return full_transcript
    except Exception as e:
        return str(e)

def save_transcript_to_file(transcript, filename):
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    with open(filename, 'w', encoding='utf-8') as file:
        file.write(transcript)

def read_video_ids_and_channels_from_csv(file_path):
    data = []
    with open(file_path, mode='r', encoding='utf-8') as file):
        reader = csv.reader(file)
        next(reader)  # Skip the header row
        for row in reader:
            if len(row) >= 4:  # Ensure there are at least four columns
                channel_name = row[0]
                video_id = row[2]
                date = row[3]
                data.append((channel_name, video_id, date))
    return data

if __name__ == "__main__":
    # Replace with your CSV file path
    csv_file_path = 'Channel_videos_merged.csv'
    
    # Set the output directory
    output_dir = 'output_dir2'
    
    data = read_video_ids_and_channels_from_csv(csv_file_path)
    batch_size = 5
    
    for i in range(0, len(data), batch_size):
        batch = data[i:i+batch_size]
        for channel_name, video_id, date in batch:
            transcript = get_transcript(video_id)
            if transcript != "Subtitles are disabled for this video." and not transcript.startswith("An error occurred"):
                filename = os.path.join(output_dir, f'transcript_{channel_name}_{video_id}.txt')
                save_transcript_to_file(transcript, filename)
                print(f"Transcript for video ID {video_id} from channel {channel_name} (Date: {date}) has been saved to {filename}")
            else:
                print(f"Transcript not found or an error occurred for video ID {video_id}: {transcript}")
        # Pause briefly between batches
        time.sleep(2)  # Adjust the sleep time as needed
