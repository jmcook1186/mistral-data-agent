### Technical Specification for Assembly Analysis: Enhanced Pipeline

---

## 1. Overview
This specification outlines the requirements for extending the existing analysis pipeline (`script.py`) to provide deeper insights into the evolution of positions across multiple rounds of email assemblies. The goal is to:
- Track position convergence/divergence over time.
- Identify key topics and sentiment trends.
- Visualize cluster evolution and topic prominence across rounds.

---

## 2. Data Requirements

### Input Files
- One CSV file per round, each containing:
  - `position_text`: The text of each participant's position.
  - `participant_id`: Unique identifier for each participant.
  - `round`: Round number (if not already present, infer from filename).

### Key Columns
- `position_text`: For embedding, clustering, and topic modeling.
- `participant_id`: For tracking individual evolution.
- `round`: For temporal analysis.

---

## 3. Analysis Tasks

### 3.1 Temporal Cluster Analysis
- **Purpose**: Track how clusters of positions evolve across rounds.
- **Method**:
  - For each round, generate embeddings and perform K-means clustering (as in the existing script).
  - Align clusters across rounds using Hungarian algorithm (from `scipy.optimize.linear_sum_assignment`) to match clusters with the most similar centroids.
  - Calculate cluster stability metrics (e.g., Jaccard similarity of cluster members between rounds).
- **Output**:
  - Table of cluster centroids and stability scores per round.
  - Line plot of cluster size and stability over time.

### 3.2 Topic Evolution Analysis
- **Purpose**: Identify and track the prominence of topics across rounds.
- **Method**:
  - Perform LDA topic modeling for each round (as in the existing script).
  - For each topic, track its prevalence (proportion of positions assigned to it) across rounds.
  - Use `pyLDAvis` for interactive topic visualization (if available).
- **Output**:
  - Heatmap of topic prevalence by round.
  - Table of top words per topic, per round.

### 3.3 Sentiment Trend Analysis
- **Purpose**: Analyze how sentiment evolves over rounds and within clusters.
- **Method**:
  - Calculate mean sentiment per cluster, per round.
  - Plot sentiment trends for each cluster over time.
- **Output**:
  - Line plot of sentiment by cluster and round.

### 3.4 Position Convergence Metrics
- **Purpose**: Quantify the degree of convergence or divergence over rounds.
- **Method**:
  - For each participant, calculate the cosine similarity between their position embeddings in consecutive rounds.
  - Plot the distribution of similarity scores per round transition.
- **Output**:
  - Boxplot of similarity scores between rounds.

---

## 4. Visualizations

### 4.1 Cluster Evolution Plot
- **Type**: Line plot with markers.
- **Data**: Cluster centroids (reduced dimensions) and stability scores.
- **Specs**:
  - X-axis: Round number.
  - Y-axis: Cluster centroid coordinates (for each dimension).
  - Color: Cluster ID.
  - Annotation: Stability score next to each marker.

### 4.2 Topic Prevalence Heatmap
- **Type**: Heatmap.
- **Data**: Topic prevalence matrix (topics x rounds).
- **Specs**:
  - X-axis: Round number.
  - Y-axis: Topic ID.
  - Color intensity: Prevalence score.

### 4.3 Sentiment Trend Plot
- **Type**: Line plot.
- **Data**: Mean sentiment per cluster, per round.
- **Specs**:
  - X-axis: Round number.
  - Y-axis: Mean sentiment.
  - Color: Cluster ID.

### 4.4 Position Convergence Boxplot
- **Type**: Boxplot.
- **Data**: Cosine similarity scores between rounds.
- **Specs**:
  - X-axis: Round transition (e.g., "R1→R2", "R2→R3").
  - Y-axis: Similarity score.

---

## 5. Edge Cases
- **Missing Data**: If a participant is missing in a round, exclude them from temporal analysis.
- **Single Round**: If only one round is available, skip temporal analysis and focus on single-round insights.
- **Cluster Mismatch**: If cluster alignment fails, fall back to independent round analysis.

---

## 6. Validation
- **Dev** should:
  - Verify that cluster alignment is stable and meaningful by spot-checking cluster members.
  - Ensure topic prevalence sums to 1 per round.
  - Confirm that sentiment trends are plausible (e.g., no sudden jumps without cause).

---

## 7. Code Hints
- **Cluster Alignment**:
  ```python
  from scipy.optimize import linear_sum_assignment
  # Use linear_sum_assignment to match clusters between rounds
  ```
- **Temporal Analysis**:
  ```python
  df.groupby(['round', 'cluster'])['sentiment'].mean().unstack()
  ```
- **Visualization**:
  ```python
  sns.heatmap(topic_prevalence, annot=True, cmap="YlGnBu")
  ```

---
**Next Steps for Dev**:
Implement the above tasks in a modular fashion, reusing existing functions where possible. Output visualizations and tables to a `results/` directory, with clear filenames (e.g., `cluster_evolution.png`, `topic_heatmap.png`).