Here is the technical specification for enhancing the asynchronous conversation assembly analysis pipeline, based on the provided script and best practices from recent research:

---

# Technical Specification: Enhanced Asynchronous Conversation Assembly Analysis

## 1. Objective
This spec outlines additional analyses and visualizations to uncover deeper insights from asynchronous conversation data, focusing on sentiment evolution, cluster stability, participant influence, and inter-round comparisons. The goal is to provide a more comprehensive understanding of conversational dynamics and thematic evolution.

---

## 2. Data Inputs
- **Input Format**: CSV file with at least the following columns:
  - `participant_id`: Unique identifier for each participant.
  - `round`: Round number (if multi-round).
  - `position_text`: Text of the participant's position/statement.
  - `timestamp`: Optional, for temporal analysis.
- **Expected Values**: Text data should be preprocessed (lowercase, stopwords removed, lemmatized) before analysis.

---

## 3. Methodology

### 3.1 Analysis

#### a. Sentiment Evolution
- **Method**: Use `TextBlob` for sentiment polarity per statement. Track sentiment change per participant across rounds.
- **Output**: DataFrame with columns: `participant_id`, `round`, `sentiment_polarity`, `sentiment_change`.
- **Visualization**: Line plot of sentiment evolution per participant, using `matplotlib` or `seaborn`.

#### b. Cluster Stability
- **Method**: For each round, perform K-means clustering (as in the current script). Calculate Jaccard similarity between clusters across rounds to assess stability.
- **Output**: DataFrame with columns: `round`, `cluster_id`, `jaccard_similarity`.
- **Visualization**: Heatmap of cluster stability across rounds, using `seaborn`.

#### c. Participant Influence
- **Method**: For each participant, calculate:
  - **Influence Score**: Number of times their statements are clustered with others.
  - **Centrality**: Use network analysis (`networkx`) to model conversation as a graph (nodes=participants, edges=cluster co-occurrence).
- **Output**: DataFrame with columns: `participant_id`, `influence_score`, `centrality`.
- **Visualization**: Network graph of participant influence, using `networkx` and `matplotlib`.

#### d. Advanced Topic Modeling
- **Method**: Replace LDA with BERTopic for more interpretable and dynamic topics. Use `bertopic` library.
- **Output**: DataFrame with columns: `round`, `topic_id`, `topic_keywords`, `topic_size`.
- **Visualization**: Bar plot of topic prevalence per round, using `matplotlib`.

#### e. Inter-Round Comparison
- **Method**: For each topic/cluster, track size and composition across rounds. Use `pandas` for aggregation.
- **Output**: DataFrame with columns: `round`, `topic_id`, `size`, `composition_change`.
- **Visualization**: Sankey diagram of topic/cluster flow between rounds, using `plotly`.

### 3.2 Visualizations
- **Tools**: `matplotlib`, `seaborn`, `plotly`, `networkx`.
- **Requirements**:
  - All plots must have clear labels, titles, and legends.
  - Interactive plots (e.g., Sankey, network graphs) should be saved as HTML.
  - Use consistent color schemes across visualizations.

---

## 4. Outputs
- **Files**:
  - `sentiment_evolution.csv`: Sentiment change per participant.
  - `cluster_stability.csv`: Cluster similarity across rounds.
  - `participant_influence.csv`: Influence and centrality scores.
  - `topic_modeling.csv`: Topic prevalence and keywords.
  - `inter_round_comparison.csv`: Topic/cluster flow.
  - `visualizations/`: Directory for all plots (PNG/HTML).
- **Key Metrics**:
  - Sentiment volatility per participant.
  - Cluster stability score.
  - Top 3 influential participants.
  - Top 3 evolving topics.

---

## 5. Edge Cases
- **Empty Rounds**: Skip rounds with <3 responses; log warning.
- **Duplicate Positions**: Deduplicate text before analysis.
- **Non-Text Data**: Log and exclude non-text entries.

---

## 6. Validation
- **Checks**:
  - Assert that `participant_id` is consistent across rounds.
  - Assert that all visualizations are generated and saved.
  - Assert that output DataFrames have no NaN values in key columns.

---

## For Dev

### Priorities
- **Critical**: Sentiment evolution, cluster stability, participant influence.
- **High**: Advanced topic modeling, inter-round comparison.
- **Medium**: Interactive visualizations.

### Dependencies
- Install: `bertopic`, `plotly`, `networkx`.
- Sequence: Run sentiment and clustering before influence/network analysis.

### Example Data
```python
# Synthetic data for testing
data = {
    "participant_id": ["p1", "p1", "p2", "p2"],
    "round": [1, 2, 1, 2],
    "position_text": [
        "I agree with the proposal.",
        "I still agree, but with reservations.",
        "The proposal needs more work.",
        "I now support the proposal."
    ]
}
df = pd.DataFrame(data)
```

---

**References**: 