### **Technical Specification for Enhanced Analysis of Asynchronous Conversation Assemblies**

---

## **1. Code Review Findings**

### **Strengths**
- **Embedding Generation**: Uses Mistral’s embeddings for semantic representation of positions.
- **Dimensionality Reduction**: Applies t-SNE for visualization-friendly 3D embeddings.
- **Clustering**: Dynamically determines optimal cluster count using silhouette scores.
- **Topic Modeling**: Uses LDA for topic extraction.
- **Sentiment Analysis**: Basic sentiment polarity analysis via TextBlob.

### **Gaps & Opportunities**
1. **Temporal Analysis**:
   - No analysis of how positions, topics, or sentiment evolve across rounds.
   - No tracking of participant influence or response patterns over time.

2. **Participant Dynamics**:
   - No identification of key participants (e.g., bridges, outliers, or influencers).
   - No network analysis (e.g., reply graphs, interaction frequency).

3. **Topic & Cluster Stability**:
   - No comparison of topic/cluster consistency between rounds.
   - No statistical testing for consensus convergence.

4. **Visualization**:
   - Static 3D plots; no interactive or round-over-round visualizations.
   - No heatmaps or network graphs for participant dynamics.

5. **Robustness**:
   - Assumes all rounds have equal participation; no handling for missing data or uneven participation.
   - No validation of cluster/topic quality (e.g., coherence scores).

---

## **2. Technical Specification**

### **Objective**
Enhance the analysis pipeline to:
- Quantify temporal evolution of topics, sentiment, and clusters.
- Identify key participants and interaction patterns.
- Visualize round-over-round dynamics and consensus metrics.

---

### **Inputs**
- **Data**:
  - CSV files with columns: `round_id`, `participant_id`, `position_text`, `timestamp`, `sentiment_score` (if precomputed).
  - Preprocessed embeddings (from `script.py`).
- **Parameters**:
  - `min_participants_per_round`: Minimum number of participants required for round-level analysis (default: 3).
  - `min_cluster_size`: Minimum size for a cluster to be considered stable (default: 5).
  - `topic_coherence_threshold`: Minimum coherence score for a topic to be retained (default: 0.4).

---

### **Methods**

#### **A. Temporal Analysis**
1. **Round-Over-Round Topic Evolution**:
   - For each round, extract topics using LDA (as in `script.py`).
   - Compare topic distributions between rounds using **Jensen-Shannon divergence**.
   - Track topic prevalence and sentiment per round.

2. **Cluster Stability**:
   - For each round, cluster positions using K-means (as in `script.py`).
   - Compute **Adjusted Rand Index (ARI)** to measure cluster consistency between rounds.

3. **Sentiment Trends**:
   - Plot mean sentiment per round.
   - Identify rounds with significant sentiment shifts (using t-tests).

#### **B. Participant Dynamics**
1. **Influence Network**:
   - Construct a directed graph where edges represent replies or semantic similarity between positions.
   - Use `networkx` to identify central participants (e.g., high betweenness centrality).

2. **Response Patterns**:
   - Compute response latency (time between rounds for each participant).
   - Flag participants with consistently high/low latency.

#### **C. Consensus Metrics**
1. **Cluster Adoption**:
   - Track how many participants contribute to each cluster per round.
   - Identify clusters that grow/shrink significantly.

2. **Semantic Similarity**:
   - Use cosine similarity on embeddings to measure intra-cluster cohesion and inter-cluster separation.

---

### **Outputs**
- **Files**:
  - `topic_evolution.json`: Topic distributions and divergence scores per round.
  - `participant_influence.csv`: Centrality metrics and response patterns.
  - `consensus_metrics.csv`: Cluster stability, ARI, and adoption rates.
- **Visualizations**:
  - **Heatmap**: Round-over-round topic prevalence.
  - **Network Graph**: Participant influence network (using `networkx` and `matplotlib`).
  - **Line Plot**: Mean sentiment per round with significance markers.
  - **Bar Chart**: Cluster adoption rates per round.

---

### **Validation**
- **Topic Quality**: Retain only topics with coherence score > `topic_coherence_threshold`.
- **Participation Check**: Skip rounds with < `min_participants_per_round`.
- **Cluster Stability**: Flag rounds with ARI < 0.3 as unstable.

---

## **3. Visualization Requirements**
- Use `matplotlib` and `seaborn` for all static plots.
- For network graphs, use `networkx` with spring layout.
- Ensure colorblind-friendly palettes and clear axis labels.

---

## **4. Pseudocode Snippets**

### **Round-Over-Round Topic Comparison**
```python
from scipy.spatial.distance import jensenshannon
from sklearn.metrics import adjusted_rand_score

# Assume `topics_per_round` is a dict: {round_id: [topic_distribution]}
round_ids = sorted(topics_per_round.keys())
for i in range(len(round_ids)-1):
    r1, r2 = round_ids[i], round_ids[i+1]
    js_div = jensenshannon(topics_per_round[r1], topics_per_round[r2])
    print(f"JS Divergence between {r1} and {r2}: {js_div:.3f}")
```

### **Influence Network**
```python
import networkx as nx

G = nx.DiGraph()
# Add edges based on replies or semantic similarity
centrality = nx.betweenness_centrality(G)
```

---

## **5. Dependencies**
- Add to `requirements.txt`:
  ```
  networkx>=3.0
  scipy>=1.10.0
  ```

---
**Next Steps for Dev**:
- Implement the temporal and participant analysis modules.
- Generate the specified visualizations and output files.
- Validate results against the specified thresholds.