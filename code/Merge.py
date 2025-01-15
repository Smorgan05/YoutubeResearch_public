import os
import csv

def merge_csv_files(input_folder, output_file):
    csv_files = [file for file in os.listdir(input_folder) if file.endswith('.csv')]
    merged_data = []

    # Define the header for the merged CSV file
    headers = ['ChannelName', 'Video Title', 'Video ID', 'Published At', 'Collaborating Channels']

    for csv_file in csv_files:
        channel_name = os.path.splitext(csv_file)[0]
        with open(os.path.join(input_folder, csv_file), mode='r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                merged_row = {
                    'ChannelName': row['ChannelName'],
                    'Video Title': row['Video Title'],
                    'Video ID': row['Video ID'],
                    'Published At': row['Published At'],
                    'Collaborating Channels': row['Collaborating Channels']
                }
                merged_data.append(merged_row)

    with open(output_file, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=headers)
        writer.writeheader()
        writer.writerows(merged_data)

if __name__ == "__main__":
    # Specify the folder containing the input CSV files
    input_folder = ''
    
    # Specify the output file name
    output_file = 'merged_videos.csv'
    
    merge_csv_files(input_folder, output_file)
    print(f"Data has been merged into {output_file}")
