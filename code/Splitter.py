import csv
import os

def split_csv(input_csv_path, output_dir, lines_per_chunk=10000):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    with open(input_csv_path, mode='r', encoding='utf-8') as infile:
        reader = csv.reader(infile)
        header = next(reader)

        file_count = 0
        lines_count = 0
        output_file = None
        writer = None

        for row in reader:
            if lines_count % lines_per_chunk == 0:
                if output_file:
                    output_file.close()
                output_file = open(os.path.join(output_dir, f'chunk_{file_count}.csv'), 'w', newline='', encoding='utf-8')
                writer = csv.writer(output_file)
                writer.writerow(header)
                file_count += 1

            writer.writerow(row)
            lines_count += 1

        if output_file:
            output_file.close()

# Replace with your input CSV file path and output directory path
input_csv_path = 'Channel_videos_merged.csv'
output_dir = 'output_chunks'
split_csv(input_csv_path, output_dir)
