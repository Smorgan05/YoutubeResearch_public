from googleapiclient.discovery import build
import csv

def get_comments(api_key, video_id, max_results=5000):
    youtube = build('youtube', 'v3', developerKey=api_key)
    comments = []
    next_page_token = None

    while len(comments) < max_results:
        request = youtube.commentThreads().list(
            part='snippet',
            videoId=video_id,
            maxResults=min(max_results - len(comments), 100),
            pageToken=next_page_token
        )
        response = request.execute()

        for item in response['items']:
            comment = item['snippet']['topLevelComment']['snippet']
            comments.append({
                'author': comment['authorDisplayName'],
                'text': comment['textDisplay'],
                'like_count': comment['likeCount'],
                'published_at': comment['publishedAt']
            })

        next_page_token = response.get('nextPageToken')
        if not next_page_token:
            break

    return comments

def write_comments_to_csv(comments, filename='youtube_comments.csv'):
    with open(filename, mode='w', encoding="utf-8", newline='') as file:
        writer = csv.writer(file)
        # Write the header row
        writer.writerow(['Author', 'Comment', 'Like Count', 'Published At'])
        
        # Write each comment
        for comment in comments:
            writer.writerow([
                comment['author'],
                comment['text'],
                comment['like_count'],
                comment['published_at']
            ])

if __name__ == "__main__":
    # Replace with your API key and video ID
    api_key = ''
    video_id = ''
    
    # Get the comments
    comments = get_comments(api_key, video_id)
    
    # Write the comments to a CSV file
    write_comments_to_csv(comments)
    
    print(f"Data has been written to youtube_comments.csv")
