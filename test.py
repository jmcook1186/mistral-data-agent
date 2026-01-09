import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from sklearn.manifold import TSNE
from sklearn.cluster import KMeans, DBSCAN
from sklearn.metrics import silhouette_score, pairwise_distances_argmin_min
from sklearn.decomposition import LatentDirichletAllocation
from sklearn.feature_extraction.text import CountVectorizer
from scipy.stats import f_oneway
from textblob import TextBlob
import seaborn as sns
from generated_code.consensus_metrics import (
    embeddings_model,
    reduce_dimensions,
    get_optimum_n_clusters,
    perform_kmeans,
    perform_topic_modeling,
    analyze_sentiment
)

# Set random seed for reproducibility
np.random.seed(42)

# Placeholder for round metadata and participant roles
def generate_round_metadata(n_samples):
    """Generate placeholder round metadata for testing."""
    return np.random.randint(1, 4, size=n_samples)

def generate_participant_roles(n_samples):
    """Generate placeholder participant roles for testing."""
    roles = ['Facilitator', 'Participant', 'Observer']
    return np.random.choice(roles, size=n_samples)

# Visualizations
def plot_3d_cluster_map(clusters, reduced_embeddings, sentiments):
    """
    Generate a 3D plot of clusters colored by sentiment.

    Parameters:
    - clusters: Array of cluster labels.
    - reduced_embeddings: 2D array of reduced embeddings.
    - sentiments: Array of sentiment scores.

    Returns:
    - Matplotlib figure.
    """
    fig = plt.figure(figsize=(12, 9))
    ax = fig.add_subplot(111, projection='3d')

    # Create scatter plot with sentiment as color
    scatter = ax.scatter(
        reduced_embeddings[:, 0],
        reduced_embeddings[:, 1],
        reduced_embeddings[:, 2],
        c=sentiments,
        cmap='viridis',
        s=50,
        alpha=0.6,
        edgecolors='w',
        linewidth=0.5
    )

    # Add colorbar for sentiment
    cbar = plt.colorbar(scatter, ax=ax, pad=0.1, shrink=0.8)
    cbar.set_label('Sentiment', rotation=270, labelpad=20)

    # Add cluster markers with different shapes
    unique_clusters = np.unique(clusters)
    markers = ['o', 's', '^', 'D', 'v', '<', '>', 'p', '*', 'h']

    # Create a legend for clusters
    for i, cluster_id in enumerate(unique_clusters):
        mask = clusters == cluster_id
        marker = markers[i % len(markers)]
        ax.scatter(
            reduced_embeddings[mask, 0][0:1],
            reduced_embeddings[mask, 1][0:1],
            reduced_embeddings[mask, 2][0:1],
            marker=marker,
            s=100,
            label=f'Cluster {cluster_id}',
            alpha=0
        )

    ax.set_xlabel('Component 1')
    ax.set_ylabel('Component 2')
    ax.set_zlabel('Component 3')
    ax.set_title('3D Cluster Map Colored by Sentiment', fontsize=14, pad=20)
    ax.legend(loc='upper right', bbox_to_anchor=(1.15, 1))

    plt.tight_layout()
    plt.savefig('3d_cluster_map.png', dpi=300, bbox_inches='tight')
    plt.show()

    return fig

def plot_topic_prevalence_heatmap(clusters, lda, vectorizer, positions):
    """
    Create a topic prevalence heatmap across clusters.

    Parameters:
    - clusters: Array of cluster labels.
    - lda: Fitted LDA model.
    - vectorizer: Fitted CountVectorizer.
    - positions: List of position texts.

    Returns:
    - Matplotlib figure.
    """
    doc_topic_dist = lda.transform(vectorizer.transform(positions))
    df = pd.DataFrame(doc_topic_dist, columns=[f"Topic_{i}" for i in range(doc_topic_dist.shape[1])])
    df['Cluster'] = clusters

    cluster_topic_mean = df.groupby('Cluster').mean()

    # Create figure and heatmap
    fig, ax = plt.subplots(figsize=(12, 8))

    sns.heatmap(
        cluster_topic_mean,
        annot=True,
        fmt='.3f',
        cmap='viridis',
        cbar_kws={'label': 'Prevalence'},
        ax=ax,
        linewidths=0.5,
        linecolor='gray'
    )

    ax.set_title('Topic Prevalence Heatmap Across Clusters', fontsize=14, pad=20)
    ax.set_xlabel('Topics', fontsize=12)
    ax.set_ylabel('Clusters', fontsize=12)

    plt.tight_layout()
    plt.savefig('topic_prevalence_heatmap.png', dpi=300, bbox_inches='tight')
    plt.show()

    return fig

def plot_sentiment_distribution(sentiments):
    """
    Plot a sentiment distribution histogram.

    Parameters:
    - sentiments: Array of sentiment scores.

    Returns:
    - Matplotlib figure.
    """
    plt.figure(figsize=(10, 6))
    plt.hist(sentiments, bins=20, color='skyblue', edgecolor='black')
    plt.title('Distribution of Sentiments')
    plt.xlabel('Sentiment Polarity')
    plt.ylabel('Frequency')
    plt.savefig('sentiment_distribution.png', dpi=300)
    plt.show()

# Additional Analyses
def cluster_stability_analysis(clusters, reduced_embeddings, round_metadata):
    """
    Perform cluster stability analysis if multi-round data is available.

    Parameters:
    - clusters: Array of cluster labels.
    - reduced_embeddings: 2D array of reduced embeddings.
    - round_metadata: Array of round identifiers.

    Returns:
    - DataFrame with stability metrics.
    """
    if round_metadata is None:
        raise ValueError("Round metadata is required for cluster stability analysis.")

    stability_results = []
    rounds = np.unique(round_metadata)

    for round_id in rounds:
        round_mask = round_metadata == round_id
        round_embeddings = reduced_embeddings[round_mask]
        round_clusters = clusters[round_mask]

        if len(np.unique(round_clusters)) > 1:
            score = silhouette_score(round_embeddings, round_clusters)
        else:
            score = np.nan

        stability_results.append({'Round': round_id, 'Silhouette Score': score})

    return pd.DataFrame(stability_results)

def perform_anova_topic_sentiment(clusters, sentiments, lda, vectorizer, positions):
    """
    Perform ANOVA to test topic-sentiment correlations.

    Parameters:
    - clusters: Array of cluster labels.
    - sentiments: Array of sentiment scores.
    - lda: Fitted LDA model.
    - vectorizer: Fitted CountVectorizer.
    - positions: List of position texts.

    Returns:
    - DataFrame with ANOVA results.
    """
    doc_topic_dist = lda.transform(vectorizer.transform(positions))
    topic_sentiment = []

    for topic_idx in range(doc_topic_dist.shape[1]):
        topic_scores = doc_topic_dist[:, topic_idx]
        group1 = sentiments[topic_scores > np.median(topic_scores)]
        group2 = sentiments[topic_scores <= np.median(topic_scores)]
        f_stat, p_value = f_oneway(group1, group2)
        topic_sentiment.append({'Topic': topic_idx, 'F-statistic': f_stat, 'p-value': p_value})

    return pd.DataFrame(topic_sentiment)

def detect_outliers_kmeans(clusters, reduced_embeddings, threshold=1.5):
    """
    Detect outliers using KMeans' transform distances.

    Parameters:
    - clusters: Array of cluster labels.
    - reduced_embeddings: 2D array of reduced embeddings.
    - threshold: Distance threshold for outliers.

    Returns:
    - Array of outlier indices.
    """
    kmeans = KMeans(n_clusters=len(np.unique(clusters)), random_state=42)
    kmeans.fit(reduced_embeddings)
    distances = np.min(kmeans.transform(reduced_embeddings), axis=1)
    outliers = np.where(distances > threshold)[0]

    return outliers

# Main pipeline
def run_analysis_pipeline(file_path):
    """
    Run the full analysis pipeline.

    Parameters:
    - file_path: Path to the CSV file containing position data.

    Returns:
    - clusters, reduced_embeddings, lda, sentiments, topic_string, round_metadata, participant_roles.
    """
    try:
        # Load data
        df = pd.read_csv(file_path)
        positions = df['position_text'].tolist()
        n_samples = len(positions)

        # Generate placeholder metadata
        round_metadata = generate_round_metadata(n_samples)
        participant_roles = generate_participant_roles(n_samples)

        # Embeddings and clustering
        embeddings = embeddings_model(positions)
        reduced_embeddings = reduce_dimensions(embeddings)
        optimum_n_clusters = get_optimum_n_clusters(reduced_embeddings)
        clusters = perform_kmeans(optimum_n_clusters, reduced_embeddings)

        # Topic modeling
        lda, vectorizer = perform_topic_modeling(positions)
        topic_string = ""
        for idx, topic in enumerate(lda.components_):
            topic_string += f"Topic {idx}: {', '.join([vectorizer.get_feature_names_out()[i] for i in topic.argsort()[-5:]])}\n"

        # Sentiment analysis
        sentiments = analyze_sentiment(positions)

        # Generate visualizations
        plot_3d_cluster_map(clusters, reduced_embeddings, sentiments)
        plot_topic_prevalence_heatmap(clusters, lda, vectorizer, positions)
        plot_sentiment_distribution(sentiments)

        # Additional analyses
        stability_results = cluster_stability_analysis(clusters, reduced_embeddings, round_metadata)
        anova_results = perform_anova_topic_sentiment(clusters, sentiments, lda, vectorizer, positions)
        outliers = detect_outliers_kmeans(clusters, reduced_embeddings)

        return clusters, reduced_embeddings, lda, sentiments, topic_string, round_metadata, participant_roles, stability_results, anova_results, outliers

    except Exception as e:
        print(f"An error occurred: {e}")
        return None

# Run the pipeline
if __name__ == "__main__":
    file_path = os.getenv("FILE_PATH")

    if file_path is None:
        print("Error: FILE_PATH environment variable is not set.")
        print("Please set FILE_PATH to the path of your CSV file.")
        print("Example: export FILE_PATH='/path/to/your/data.csv'")
        exit(1)

    result = run_analysis_pipeline(file_path=file_path)

    if result is None:
        print("Analysis pipeline failed. Please check the error messages above.")
        exit(1)

    clusters, reduced_embeddings, lda, sentiments, topic_string, round_metadata, participant_roles, stability_results, anova_results, outliers = result

    print("\nAnalysis completed successfully!")
    print(f"Number of clusters: {len(np.unique(clusters))}")
    print(f"Number of outliers detected: {len(outliers)}")
    print("\nTopics identified:")
    print(topic_string)
