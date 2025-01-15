import pandas as pd
import matplotlib.pyplot as plt
from collections import Counter
import re

def plot_top_words(csv_file, top_n=10):
    # Read the CSV file
    df = pd.read_csv(csv_file)
    
    # Concatenate all titles into one large string
    all_titles = ' '.join(df['Title'].astype(str).tolist())
    
    # Remove punctuation and split into words
    words = re.findall(r'\b\w+\b', all_titles.lower())
    
    # Count the frequency of each word
    word_counts = Counter(words)
    
    # Get the top N most common words
    top_words = word_counts.most_common(top_n)
    
    # Separate words and their counts for plotting
    words, counts = zip(*top_words)
    
    # Plot the top words
    plt.figure(figsize=(10, 6))
    plt.bar(words, counts, color='blue')
    plt.xlabel('Words')
    plt.ylabel('Frequency')
    plt.title(f'Top {top_n} Words in Video Titles')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    # Replace with your merged CSV file path
    csv_file = 'Channel_videos_merged.csv'
    
    # Plot the top words
    plot_top_words(csv_file)
