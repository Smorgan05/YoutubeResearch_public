import os
import csv

def check_for_disabled_subtitles_in_directory(directory_path, output_csv_path):
    search_string = "Subtitles are disabled for this video"
    
    if not os.path.isdir(directory_path):
        print(f"The directory '{directory_path}' does not exist.")
        return
    
    results = []

    for filename in os.listdir(directory_path):
        if filename.startswith("transcript_") and filename.endswith(".txt"):
            file_path = os.path.join(directory_path, filename)
            
            if os.path.isfile(file_path):
                try:
                    with open(file_path, 'r', encoding='utf-8') as file:
                        content = file.read()
                        
                        channel_name, video_id = extract_channel_and_video_id(filename)
                        if search_string in content:
                            results.append((channel_name, video_id, "No_Transcript"))
                        else:
                            results.append((channel_name, video_id, "Transcript_Available"))
                
                except Exception as e:
                    print(f"An error occurred while reading the file '{filename}': {e}")
    
    write_results_to_csv(results, output_csv_path)

def extract_channel_and_video_id(filename):
    parts = filename.split('_')
    channel_name = parts[1]
    video_id = parts[3].split('.')[0]
    return channel_name, video_id

def write_results_to_csv(results, output_csv_path):
    with open(output_csv_path, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(["Channel Name", "Video ID", "Transcript Status"])
        writer.writerows(results)
    
    print(f"Results have been written to '{output_csv_path}'")

# Replace with your directory path and output CSV file path
directory_path = 'output_dir'
output_csv_path = 'output_results.csv'
check_for_disabled_subtitles_in_directory(directory_path, output_csv_path)
