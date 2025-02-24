import os
import glob
from collections import Counter
from bertopic import BERTopic
from hdbscan import HDBSCAN
from umap import UMAP

# Step 1: Load all text files from a folder
def load_text_files(folder_path):
    texts = []
    file_names = []
    
    for file_path in glob.glob(os.path.join(folder_path, "*.txt")):
        with open(file_path, "r", encoding="utf-8") as file:
            texts.append(file.read().strip())  # Read and store text
            file_names.append(os.path.basename(file_path))  # Store file name
    
    return texts, file_names

# Step 2: Apply BERTopic for trend detection
def identify_trending_topics(texts):
    umap_model = UMAP(n_neighbors=3, n_components=2, metric='cosine', random_state=42)
    hdbscan_model = HDBSCAN(min_cluster_size=2)
    topic_model = BERTopic(umap_model=umap_model, hdbscan_model=hdbscan_model, calculate_probabilities=False)  # Initialize BERTopic
    topics, probs = topic_model.fit_transform(texts)  # Generate topics

    # Get global topic representation
    topic_info = topic_model.get_topic_info()  # DataFrame with topic frequencies
    sorted_topics = topic_info.sort_values(by="Count", ascending=False)  # Sort by prominence

    return topic_model, topics, sorted_topics

# Step 3: Assign trending topics to videos
def assign_trends(file_names, topics, topic_model):
    trending_dict = {}

    for file, topic in zip(file_names, topics):
        topic_words = topic_model.get_topic(topic)  # Get words describing the topic
        trending_dict[file] = f"Trending Topic: {topic}, Keywords: {topic_words}"

    return trending_dict

# Specify the folder containing translated text files
folder_path = os.path.join('translatedFiles')

# Execute the steps
texts, file_names = load_text_files(folder_path)  # Load files
topic_model, topics, sorted_topics = identify_trending_topics(texts)  # Apply BERTopic
trending_videos = assign_trends(file_names, topics, topic_model)  # Assign topics

# Print top trending topics globally
print("\n🔝 Top Trending Topics Globally:")
print(sorted_topics.head(5))  # Show top 5 trending topics

# Print trending topics for each video
print("\n🎬 Trending Topics Assigned to Videos:")
for file, trend in trending_videos.items():
    print(f"{file}: {trend}")