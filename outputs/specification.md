### **Technical Specification: Asynchronous Email Conversation Analysis**

**Objective:**
This specification details the requirements and methodology for analyzing asynchronous email conversations ("assemblies") to quantify thematic convergence, assess sentiment evolution, and identify participant dynamics across rounds. The output will enable stakeholders to understand how discussions evolve over time and identify key participants or themes.

---

## **1. Data Validation & Preprocessing**

### **Data Requirements**
- **Input:** CSV files with the following columns:
  - `round_id` (int)
  - `participant_id` (str)
  - `position_text` (str)
  - `sentiment_score` (float, range: -1 to 1)
  - `theme` (str)
  - `timestamp` (datetime)

- **Validation Steps:**
  1. **Missing Values:**
     - Drop rows missing `round_id`, `participant_id`, or `position_text`.
     - Impute missing `sentiment_score` with the median of the participant's other scores, if available; else, drop.
     - Flag missing `theme` as "unknown" and exclude from thematic analysis.
  2. **Duplicates:**
     - Remove exact duplicates (same `participant_id`, `round_id`, and `position_text`).
  3. **Outliers:**
     - For `sentiment_score`, use IQR: exclude scores outside [Q1 - 1.5*IQR, Q3 + 1.5*IQR].
  4. **Schema Confirmation:**
     - Log any discrepancies and propose adjustments (e.g., casting `round_id` to int).

- **Preprocessing:**
  - **Text Normalization:**
    - Lowercase, remove stopwords, lemmatize using `nltk` or `spaCy`.
    - Use `CountVectorizer` with `max_df=0.95`, `min_df=2`, and custom stopwords.
  - **Sentiment Binning:**
    - Bin `sentiment_score` into "negative" (<-0.1), "neutral" (-0.1 to 0.1), "positive" (>0.1).

---

## **2. Methodology**

### **A. Thematic Analysis**
- **Clustering:**
  - Use **TF-IDF + K-Means** (preferred) or **LDA** for thematic clustering.
  - **Number of Clusters:** Use the elbow method and silhouette score to determine optimal `k`.
  - **Similarity Metric:** Calculate **Jaccard similarity** between rounds to quantify thematic convergence.
- **Output:**
  - `thematic_clusters.csv`: Cluster assignments, centroid terms, and Jaccard similarities.

### **B. Sentiment Analysis**
- **Statistical Tests:**
  - Kruskal-Wallis for overall differences across rounds.
  - Mann-Whitney U for pairwise comparisons.
  - Report p-values, effect sizes (Cliff’s Delta), and 95% confidence intervals.
- **Output:**
  - `sentiment_stats.csv`: Mean/median sentiment per round, statistical test results.

### **C. Participant Dynamics**
- **Consistency Metric:**
  - Compute cosine similarity of participants' positions across rounds.
  - Flag outliers (participants with consistency <0.3 or sentiment shifts >2σ).
- **Output:**
  - `participant_consistency.csv`: Consistency scores and outlier flags.

---

## **3. Visualizations**

### **A. Thematic Convergence**
- **Heatmap:**
  - Axes: `round_id` (x and y).
  - Color scale: Viridis (0–1 similarity).
  - Title: "Thematic Convergence Across Rounds (Jaccard Similarity)".

### **B. Sentiment Trends**
- **Boxplot:**
  - Axes: `round_id` (x), `sentiment_score` (y).
  - Color: Coolwarm diverging palette.
  - Annotate p-values for significant differences.

### **C. Participant Trajectories**
- **Line Plot:**
  - Facet by `participant_id` if >10 participants; else, use distinct colors.
  - Highlight outliers with dashed lines.

---

## **4. Outputs**

- **Tables:**
  - `thematic_clusters.csv`
  - `sentiment_stats.csv`
  - `participant_consistency.csv`
- **Plots:**
  - Save as PNG/PDF (DPI=300).
  - Include raw data (`.pickle`) for reproducibility.
- **Metrics:**
  - Thematic convergence score (mean Jaccard similarity).
  - Sentiment trend slope (linear regression of median sentiment over rounds).

---

## **5. Edge Cases**

- **Sparse Data:** Flag rounds with <3 participants as unreliable; exclude from longitudinal analysis.
- **Single-Round Data:** Skip sentiment trend analysis.
- **Ties in Clustering:** Use deterministic seeding (`random_state=42`).

---

## **6. Evaluation Metrics**

- **Success Criteria:**
  - Thematic convergence score ≥0.6.
  - Sentiment trend slope ≠0 with p<0.05.
- **Cost-Benefit:**
  - Prefer K-Means for speed; use LDA for interpretability.

---

## **7. Deliverables**

- **Markdown File (`spec.md`):**
  - Sections: Objective, Data Validation, Methodology, Outputs, Edge Cases, Evaluation.
- **Pseudocode Snippets:**
  - Provide in a `code_hints/` directory.

---

## **8. Code Hints**

```python
# Example: Jaccard similarity between rounds
from sklearn.metrics import jaccard_score
from itertools import combinations

rounds = df.groupby('round_id')['position_text'].apply(set)
round_pairs = list(combinations(rounds.index, 2))
similarities = {
    f"round_{i}_vs_{j}": jaccard_score(rounds[i], rounds[j])
    for i, j in round_pairs
}

# Example: Kruskal-Wallis test
from scipy.stats import kruskal

round_groups = [group['sentiment_score'].values for name, group in df.groupby('round_id')]
stat, p = kruskal(*round_groups)
```

---

**Next Steps for Dev:**
- Implement data validation and preprocessing as specified.
- Use the provided pseudocode for clustering, statistical tests, and visualization.
- Output tables and plots in the required formats.
- Handle edge cases with logging and warnings.