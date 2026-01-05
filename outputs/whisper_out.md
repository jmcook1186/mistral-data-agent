### **PROMPT FOR SPEC**

**Objective:**
Design a **technical specification** for analyzing asynchronous email-based "assemblies" (structured conversations with fixed participants and rounds). The goal is to quantify thematic convergence, sentiment evolution, and participant dynamics.

**Data Schema:**
The input CSV files contain decomposed "positions" with the following columns:
- `round_id` (int): Unique identifier for each round.
- `participant_id` (str): Unique identifier for each participant.
- `position_text` (str): Raw text of the participant’s position.
- `sentiment_score` (float): Precomputed sentiment score (-1 to 1).
- `theme` (str): Extracted theme (e.g., "ethics," "monitoring").
- `timestamp` (datetime): When the position was submitted.

**Requirements:**

1. **Data Validation & Preprocessing**
   - Validate for missing values, duplicates, and outliers.
   - Log data quality issues and propose handling (e.g., impute missing sentiment scores with median).
   - Standardize timestamps to UTC.

2. **Core Analyses**
   - **Thematic Convergence:**
     - Compute Jaccard similarity between themes across rounds.
     - Cluster themes using TF-IDF + K-means (elbow method for *k*).
   - **Sentiment Evolution:**
     - Plot sentiment trends per participant/round (line plots with confidence intervals).
     - Test for significant changes (Kruskal-Wallis for non-parametric data).
   - **Participant Dynamics:**
     - Network graph of participant interactions (weighted by theme overlap).
     - Identify outliers (participants with consistently low thematic alignment).

3. **Visualizations**
   - **Heatmap:** Jaccard similarity between rounds.
   - **Line Plot:** Sentiment trends (grouped by participant/theme).
   - **Network Graph:** Participant interactions (use `networkx` + `matplotlib`).

4. **Edge Cases**
   - Handle sparse data (e.g., rounds with <3 participants).
   - Flag participants with >20% missing data.

5. **Outputs**
   - CSV: Processed data with added metrics (e.g., `theme_cluster`, `sentiment_change`).
   - PNG: All visualizations (300 DPI, labeled axes).
   - TXT: Log of data issues and handling decisions.

**Code Hints (Pseudocode):**
```python
# Thematic convergence
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
vectorizer = TfidfVectorizer()
X = vectorizer.fit_transform(df["theme"])
kmeans = KMeans(n_clusters=3, random_state=42).fit(X)

# Sentiment trends
import seaborn as sns
sns.lineplot(data=df, x="round_id", y="sentiment_score", hue="participant_id")
```

**Prioritization:**
- Must-have: Thematic convergence, sentiment trends.
- Nice-to-have: Network graph, outlier detection.

**Constraints:**
- Use only Python (Pandas, Scikit-learn, Matplotlib/Seaborn).
- No external APIs or proprietary tools.

---

### **PROMPT FOR QUANT**

**Objective:**
Write a **300–1000 word report** extracting actionable insights from the email assembly data. Assume a non-technical audience (e.g., program managers).

**Structure:**

1. **Executive Summary (3–5 bullets)**
   - Example: *"Themes converged by 40% by Round 3, but ‘ethics’ remained divisive (Jaccard similarity = 0.2)."*

2. **Deep Dive**
   - **Thematic Analysis:** Which themes gained/lost traction? Highlight clusters.
   - **Temporal Trends:** How did sentiment evolve? Note inflection points.
   - **Participant Dynamics:** Who drove consensus? Who resisted?

3. **Visualization Interpretation**
   - Describe the heatmap: *"Dark red cells show high theme overlap between Rounds 1 and 2."*
   - Explain the sentiment plot: *"Participant B’s sentiment dropped sharply in Round 3 (p < 0.05)."*

4. **Recommendations**
   - Prioritize 2–3 actions (e.g., *"Revisit ‘ethics’ in Round 4 with structured prompts"*).
   - Justify with data (e.g., *"Low Jaccard similarity suggests unresolved tension"*).

**Guidelines:**
- **Avoid Jargon:** Replace "Kruskal-Wallis" with *"statistical test for trends."*
- **Cite Values:** *"Sentiment improved by 0.3 points (from -0.1 to 0.2)."*
- **Limitations:** Note if small sample size (e.g., *"Only 5 participants in Round 2"*).

**Example:**
> *"Participant A consistently bridged gaps between themes (centrality score = 0.8). Recommend assigning them a facilitator role in future rounds."*

**Constraints:**
- No fabricated data.
- Use only provided visualizations (no new plots).

---
**Key Notes for Both Agents:**
- **Spec:** Focus on reproducibility (set `random_state=42`).
- **Quant:** Link every insight to a visualization or statistic.