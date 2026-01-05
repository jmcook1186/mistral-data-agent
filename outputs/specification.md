### **Technical Specification: Asynchronous Email Assembly Analysis**

**Author:** Spec
**Version:** 1.0
**Date:** 2026-01-05
**Target Audience:** Dev (Mistral AI Agent)

---

## **1. Overview**
This spec defines the implementation for analyzing asynchronous email-based "assemblies" (structured conversations with fixed participants and rounds). The goal is to quantify **thematic convergence**, **sentiment evolution**, and **participant dynamics** using Python, Pandas, Scikit-learn, Matplotlib, and Seaborn.

---

## **2. Data Schema & Validation**

### **Input Data**
- CSV files with columns:
  - `round_id` (int)
  - `participant_id` (str)
  - `position_text` (str)
  - `sentiment_score` (float, range: -1 to 1)
  - `theme` (str)
  - `timestamp` (datetime)

### **Validation & Preprocessing**
- **Missing Values:**
  - Log missing values by column.
  - Impute missing `sentiment_score` with the median of the participant’s other scores.
  - Drop rows missing `position_text` or `theme`.
- **Outliers:**
  - Flag `sentiment_score` outside [-1, 1].
  - Log participants with >20% missing data.
- **Standardization:**
  - Convert `timestamp` to UTC.
  - Ensure `round_id` is sequential and starts at 1.

**Output:**
- Log file (`data_issues.txt`) with summary of issues and handling.
- Cleaned DataFrame for analysis.

---

## **3. Core Analyses**

### **A. Thematic Convergence**
- **Jaccard Similarity:**
  - For each pair of rounds, compute Jaccard similarity of themes.
  - Output: Heatmap (Seaborn) of similarity between rounds.
- **Theme Clustering:**
  - Vectorize themes using `TfidfVectorizer`.
  - Cluster using K-means, with *k* determined by the elbow method.
  - Add `theme_cluster` column to DataFrame.

**Code Hint:**
```python
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
vectorizer = TfidfVectorizer()
X = vectorizer.fit_transform(df["theme"])
kmeans = KMeans(n_clusters=3, random_state=42).fit(X)
```

### **B. Sentiment Evolution**
- **Trend Analysis:**
  - Line plot (Seaborn) of `sentiment_score` by `round_id`, grouped by `participant_id` and `theme`.
  - Add 95% confidence intervals.
- **Statistical Testing:**
  - Kruskal-Wallis test for significant changes in sentiment across rounds.

**Code Hint:**
```python
import seaborn as sns
sns.lineplot(data=df, x="round_id", y="sentiment_score", hue="participant_id", ci=95)
```

### **C. Participant Dynamics**
- **Network Graph:**
  - Construct a weighted graph (NetworkX) where nodes are participants and edges are weighted by theme overlap (Jaccard similarity).
  - Visualize with `matplotlib`.
- **Outlier Detection:**
  - Flag participants with consistently low thematic alignment (e.g., Jaccard < 0.2 for all rounds).

**Code Hint:**
```python
import networkx as nx
G = nx.Graph()
# Add nodes and edges based on theme overlap
nx.draw(G, with_labels=True)
```

---

## **4. Visualizations**

- **Heatmap:** Jaccard similarity between rounds (Seaborn).
- **Line Plot:** Sentiment trends (Seaborn, with confidence intervals).
- **Network Graph:** Participant interactions (NetworkX + Matplotlib).
- **Save all visualizations as PNG (300 DPI, labeled axes).**

---

## **5. Edge Cases & Constraints**

- **Sparse Data:**
  - Skip rounds with <3 participants.
  - Log skipped rounds.
- **Missing Data:**
  - Exclude participants with >20% missing data from network analysis.
- **Constraints:**
  - Use only Python (Pandas, Scikit-learn, Matplotlib/Seaborn, NetworkX).
  - No external APIs or proprietary tools.

---

## **6. Outputs**

- **CSV:** Processed data with added metrics (`theme_cluster`, `sentiment_change`).
- **PNG:** All visualizations.
- **TXT:** Log of data issues and handling decisions.

---

## **7. Implementation Notes for Dev**

- **Modularity:**
  - Implement each analysis (thematic, sentiment, network) as a separate function.
  - Use `pandas` for data manipulation, `scikit-learn` for clustering/testing, and `seaborn/matplotlib` for visualization.
- **Error Handling:**
  - Log errors and continue with available data.
- **Performance:**
  - Vectorize operations where possible.
  - Use `n_jobs=-1` for parallelizable Scikit-learn functions.

---

## **8. Example Workflow**

```python
import pandas as pd
from sklearn.metrics import jaccard_score
import seaborn as sns
import networkx as nx

def analyze_assembly(df):
    # Preprocess
    df = preprocess_data(df)

    # Thematic convergence
    jaccard_matrix = compute_jaccard(df)
    plot_jaccard_heatmap(jaccard_matrix)

    # Sentiment evolution
    plot_sentiment_trends(df)

    # Participant dynamics
    G = build_network(df)
    plot_network(G)

    return df, jaccard_matrix, G
```

---

**Next Steps for Dev:**
- Implement data validation and preprocessing.
- Build modular functions for each analysis.
- Generate visualizations and outputs as specified.
- Log all data issues and handling decisions.