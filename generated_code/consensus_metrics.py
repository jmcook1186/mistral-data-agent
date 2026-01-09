import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.manifold import TSNE
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
from sklearn.decomposition import LatentDirichletAllocation
from sklearn.feature_extraction.text import CountVectorizer
from textblob import TextBlob
from dotenv import load_dotenv
from mistralai import Mistral

# Load environment variables
load_dotenv()

# Start Mistral client
client = Mistral(api_key=os.getenv("MISTRAL_API_KEY"))

def extract_position_data(file_path):
    """Load text data and extract the relevant column."""
    df = pd.read_csv(file_path)
    positions = df['position_text'].tolist()
    return positions

def embeddings_model(text_data):
    """Generate embeddings using Mistral's embeddings model."""
    results = client.embeddings.create(inputs=text_data, model="mistral-embed")
    embeddings = [data.embedding for data in results.data]
    return embeddings

def reduce_dimensions(embeddings, n_components=3):
    """Reduce dimensionality of embeddings using t-SNE."""
    tsne = TSNE(n_components=n_components, random_state=42)
    reduced_embeddings = tsne.fit_transform(np.array(embeddings))
    return reduced_embeddings

def get_optimum_n_clusters(embeddings, max_clusters=10):
    """Determine the optimal number of clusters using silhouette score."""
    scs = []
    n_clusters_range = np.arange(2, max_clusters + 1)
    for n_clusters in n_clusters_range:
        kmeans = KMeans(n_clusters=n_clusters, random_state=42)
        clusters = kmeans.fit_predict(np.array(embeddings))
        sc = silhouette_score(embeddings, clusters)
        scs.append(sc)
    optimum_n_clusters = n_clusters_range[np.argmax(scs)]
    return optimum_n_clusters

def perform_kmeans(n_clusters, embeddings):
    """Perform K-means clustering."""
    kmeans = KMeans(n_clusters=n_clusters, random_state=42)
    clusters = kmeans.fit_predict(np.array(embeddings))
    return clusters

def plot_3d_cluster_map(clusters, embeddings):
    """Plot 3D cluster map with improved visualization."""
    fig = plt.figure(figsize=(10, 8))
    ax = fig.add_subplot(projection='3d')
    scatter = ax.scatter(
        embeddings[:, 0],
        embeddings[:, 1],
        embeddings[:, 2],
        c=clusters,
        cmap='viridis',
        alpha=0.6
    )
    plt.colorbar(scatter, ax=ax, label='Cluster')
    ax.set_xlabel('Component 1')
    ax.set_ylabel('Component 2')
    ax.set_zlabel('Component 3')
    plt.title('3D Cluster Map of Email Conversations')
    plt.show()

def perform_topic_modeling(text_data, n_topics=5):
    """Perform topic modeling using LDA."""
    vectorizer = CountVectorizer(max_df=0.95, min_df=2, stop_words='english')
    doc_term_matrix = vectorizer.fit_transform(text_data)
    lda = LatentDirichletAllocation(n_components=n_topics, random_state=42)
    lda.fit(doc_term_matrix)
    return lda, vectorizer

def analyze_sentiment(text_data):
    """Analyze sentiment of text data."""
    sentiments = [TextBlob(text).sentiment.polarity for text in text_data]
    return sentiments

def run_pipeline(file_path):
    """Run the full analysis pipeline."""
    positions = extract_position_data(file_path)
    embeddings = embeddings_model(positions)
    reduced_embeddings = reduce_dimensions(embeddings)

    # Clustering
    optimum_n_clusters = get_optimum_n_clusters(reduced_embeddings)
    clusters = perform_kmeans(optimum_n_clusters, reduced_embeddings)
    plot_3d_cluster_map(clusters, reduced_embeddings)

    # Topic modeling
    lda, vectorizer = perform_topic_modeling(positions)
    print("Topics identified:")
    topic_string = ""
    for idx, topic in enumerate(lda.components_):
        topic_string = topic_string + (f"Topic {idx}: {', '.join([vectorizer.get_feature_names_out()[i] for i in topic.argsort()[-5:]])}")

    # Sentiment analysis
    sentiments = analyze_sentiment(positions)
    plt.figure(figsize=(10, 6))
    plt.hist(sentiments, bins=20, color='skyblue', edgecolor='black')
    plt.title('Distribution of Sentiments in SCI for Web R1')
    plt.xlabel('Sentiment Polarity')
    plt.ylabel('Frequency')
    plt.show()

    return clusters, reduced_embeddings, lda, sentiments, topic_string

# Run the pipeline
if __name__ == "__main__":
    run_pipeline(file_path=os.getenv("FILE_PATH"))
