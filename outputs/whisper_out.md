### **PROMPT FOR SPEC**

**Objective:**
Critically examine the provided `script.py` and design a **technical specification** for deeper analysis of asynchronous email conversations ("assemblies"). The goal is to quantify thematic convergence, assess sentiment evolution, and identify participant dynamics across rounds.

**Data Schema:**
The input CSV files contain the following columns (confirm and adjust if discrepancies exist):
- `round_id` (int): Unique identifier for each round.
- `participant_id` (str): Unique identifier for each participant.
- `position_text` (str): Raw text of the participant’s position.
- `sentiment_score` (float): Precomputed sentiment score (-1 to 1).
- `theme` (str): Extracted thematic label (e.g., "ethics", "monitoring").
- `timestamp` (datetime): When the position was submitted.

**Tasks:**

1. **Data Requirements:**
   - Validate the input data for:
     - Missing values (handle via imputation or exclusion, with justification).
     - Duplicates (remove or flag).
     - Outliers in `sentiment_score` (use IQR or Z-score; document thresholds).
   - Confirm the schema matches the above. If not, document discrepancies and propose adjustments.
   - Preprocessing steps:
     - Normalize text (lowercase, remove stopwords, lemmatize) for thematic analysis.
     - Bin `sentiment_score` into categories (e.g., "negative", "neutral", "positive") if needed.

2. **Methodology:**
   - **Thematic Analysis:**
     - Use **TF-IDF + K-Means** (or LDA) to cluster positions by theme. Specify:
       - Number of clusters (justified via elbow method/silhouette score).
       - Preprocessing steps (e.g., n-grams, custom stopwords).
     - Calculate **Jaccard similarity** between rounds to quantify thematic convergence.
   - **Sentiment Analysis:**
     - Test for **statistically significant changes** in sentiment across rounds using:
       - Kruskal-Wallis (non-parametric ANOVA) for >2 groups.
       - Mann-Whitney U for pairwise comparisons.
     - Report p-values, effect sizes (e.g., Cliff’s Delta), and confidence intervals.
   - **Participant Dynamics:**
     - Compute **participant consistency** (e.g., cosine similarity of their positions across rounds).
     - Identify outliers (participants with low consistency or extreme sentiment shifts).
   - **Visualizations:**
     - **Thematic convergence**: Heatmap of Jaccard similarity between rounds.
       - Axes: `round_id` (x and y).
       - Color scale: Viridis (0–1 similarity).
       - Title: "Thematic Convergence Across Rounds (Jaccard Similarity)".
     - **Sentiment trends**: Boxplot of `sentiment_score` by `round_id`.
       - Axes: `round_id` (x), `sentiment_score` (y).
       - Color: Coolwarm diverging palette.
       - Annotate p-values for significant differences.
     - **Participant trajectories**: Line plot of sentiment per participant across rounds.
       - Facet by `participant_id` if >10 participants; else, use distinct colors.
       - Highlight outliers (e.g., dashed lines for participants with >2σ sentiment shifts).

3. **Outputs:**
   - Tables:
     - `thematic_clusters.csv`: Cluster assignments per position, with centroid terms.
     - `sentiment_stats.csv`: Mean/median sentiment per round, with statistical test results.
     - `participant_consistency.csv`: Consistency scores and outlier flags per participant.
   - Plots: Save as PNG/PDF with high DPI (300+). Include raw data (e.g., `.pickle`) for reproducibility.
   - Metrics:
     - Thematic convergence score (mean Jaccard similarity across rounds).
     - Sentiment trend slope (linear regression of median sentiment over rounds).

4. **Edge Cases:**
   - **Sparse data**: If <3 participants/round, flag as unreliable; exclude or note limitations.
   - **Single-round data**: Skip longitudinal analyses (e.g., sentiment trends).
   - **Ties in clustering**: Use deterministic seeding (e.g., `random_state=42`).

5. **Code Hints:**
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
   ```
   - Use `scipy.stats` for Kruskal-Wallis/Mann-Whitney.
   - Log warnings for edge cases (e.g., `logging.warning("Round 3 has <3 participants")`).

6. **Evaluation Metrics:**
   - **Success Criteria**:
     - Thematic convergence score ≥0.6 (indicates moderate agreement).
     - Sentiment trend slope ≠0 with p<0.05 (significant change).
   - **Cost-Benefit**:
     - Justify computational trade-offs (e.g., LDA vs. K-Means for clustering).

7. **Deliverables:**
   - A Markdown file (`spec.md`) with sections:
     1. **Objective** (1–2 sentences).
     2. **Data Validation** (steps and handling rules).
     3. **Methodology** (algorithms, tests, visualizations).
     4. **Outputs** (tables, plots, metrics).
     5. **Edge Cases** (handling rules).
     6. **Evaluation** (success criteria).
   - Pseudocode snippets (as above) in a `code_hints/` directory.

---
---

### **PROMPT FOR QUANT**

**Objective:**
Generate a **300–1000 word report** extracting actionable insights from the email assembly data. Assume the audience is non-technical (e.g., program managers). Focus on **thematic convergence**, **sentiment evolution**, and **participant dynamics**.

**Tasks:**

1. **Executive Summary:**
   - 3–5 bullet points of **key findings**. Example:
     - *"Thematic convergence increased by 40% from Round 1 to Round 3 (Jaccard similarity: 0.45→0.63), suggesting growing consensus."*
     - *"Participant X showed the highest sentiment volatility (σ=1.2), acting as a potential outlier."*

2. **Deep Dive:**
   - **Thematic Analysis**:
     - Which themes dominated each round? Did any emerge/disappear?
     - Quantify convergence using the Jaccard score. Example:
       *"Rounds 1 and 2 shared only 30% of themes (Jaccard=0.3), but Rounds 2–3 shared 63%, indicating convergence on ‘ethics’ and ‘monitoring’."*
   - **Sentiment Trends**:
     - Describe changes in sentiment across rounds. Link to statistical tests:
       *"Median sentiment improved significantly from Round 1 (0.1) to Round 3 (0.5; p=0.02, Kruskal-Wallis)."*
     - Highlight outliers (e.g., participants with counter-trend shifts).
   - **Participant Dynamics**:
     - Who drove consensus? Who resisted? Example:
       *"Participants A/C consistently aligned with the majority (consistency score=0.9), while Participant B diverged (score=0.4)."*

3. **Dataset Explanations:**
   - For **each dataset** created by Dev (e.g., `thematic_clusters.csv`, `sentiment_stats.csv`):
     - **What it contains**: Columns and their meaning.
     - **How it was derived**: Steps taken (e.g., "TF-IDF + K-Means with k=5").
     - **Insights**: Example:
       *"`thematic_clusters.csv` shows 5 themes. ‘Ethics’ (Cluster 2) grew from 20% to 45% of positions across rounds, suggesting prioritization."*

4. **Visualization Explanations:**
   - For **each plot** (e.g., heatmap, boxplot, line plot):
     - **What it shows**: Axes, colors, and data represented.
     - **Key patterns**: Example:
       *"The **sentiment boxplot** reveals Round 2 had the widest sentiment spread (IQR=0.8), driven by debate over ‘monitoring’."*
     - **Implications**: Link to recommendations. Example:
       *"The **participant trajectories plot** shows Participant D’s sentiment dropped sharply in Round 3, warranting follow-up."*

5. **Data Limitations:**
   - Explicitly state:
     - Missing data (e.g., "Round 1 lacks 2 participants’ positions").
     - Small sample size (e.g., "Only 3 rounds limit trend reliability").
     - Potential biases (e.g., "Sentiment scores may not capture sarcasm").

6. **Recommendations:**
   - **Prioritized actions** with data backing. Example:
     1. *"Revisit ‘ethics’ (Cluster 2) in Round 4: It’s the top theme but had the lowest sentiment (median=0.2)."*
     2. *"Engage Participant B 1:1: Their low consistency (0.4) suggests misalignment."*
   - **Avoid**: Vague suggestions like "improve communication." Instead, specify *how* (e.g., "facilitate a Round 4 sub-group on ‘ethics’").

7. **Checklist:**
   - [ ] All datasets explained (list names).
   - [ ] All visualizations described (list names).
   - [ ] Limitations documented.
   - [ ] Recommendations are SMART (Specific, Measurable, Achievable, Relevant, Time-bound).

**Formatting:**
- **Headings**: Use `## Executive Summary`, `## Thematic Analysis`, etc.
- **Visuals**: Embed plots (if available) with captions. Example:
  *"![Sentiment Trends](plots/sentiment_boxplot.png)*
  *Figure 1: Sentiment distribution across rounds. Round 3 shows significantly higher median sentiment (p=0.02)."*
- **Tables**: Present key metrics in Markdown tables. Example:

  | Round | Median Sentiment | Thematic Convergence (Jaccard) |
  |-------|------------------|--------------------------------|
  | 1     | 0.1              | 0.45                           |
  | 2     | 0.3              | 0.55                           |

**Tone:**
- **Avoid jargon**: Replace "TF-IDF" with "text similarity analysis."
- **Use analogies**: E.g., "Thematic convergence is like groups gradually agreeing on a restaurant choice."
- **Highlight urgency**: Flag critical findings (e.g., *"Low convergence in Round 1 risks delayed decisions"*).

**Deliverables:**
- A Markdown file (`report.md`) with the above structure.
- A `checklist.txt` confirming all datasets/visualizations were addressed.

---
---