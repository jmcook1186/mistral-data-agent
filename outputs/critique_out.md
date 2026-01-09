Here is a comprehensive audit and set of learning materials and updated prompts for each agent, based on best practices and the latest guidance from the web:

---

## LEARNING MATERIALS

### Whisper Learning Materials

**Key Areas for Improvement:**
- **Clarity and Specificity:** Ensure prompts are clear, specific, and actionable. Use templates (e.g., CRISP-DM) for consistency and completeness.
- **Evaluation Metrics:** Always include a section on evaluation metrics and success criteria in prompts for Spec and Dev.
- **Audience Awareness:** Tailor prompts to the intended audience (e.g., technical for Spec, non-technical for Quant).
- **Data Validation and Edge Cases:** Emphasize the importance of data validation, handling edge cases, and statistical rigor.

**Resources:**
- [A Practical Guide to Writing Technical Specs](https://stackoverflow.blog/2020/04/06/a-practical-guide-to-writing-technical-specs/)
- [Data Science Documentation Best Practices](https://www.datascience-pm.com/documentation-best-practices/)
- [Guide to Writing Data Requirements](https://qat.com/guide-writing-data-requirements/)

---

### Spec Learning Materials

**Key Areas for Improvement:**
- **Comprehensive Technical Specifications:** Include purpose, scope, functional/non-functional requirements, design requirements, technical standards, testing requirements, and delivery requirements.
- **Evaluation Metrics:** Define clear evaluation metrics and success criteria.
- **Cost-Benefit Analysis:** Include a cost-benefit analysis to help determine project prioritization.
- **Data Validation and Edge Cases:** Specify data validation steps, handling of edge cases, and statistical tests.

**Resources:**
- [How to Write Technical Specifications](https://www.archbee.com/blog/how-to-write-technical-specifications)
- [Technical Specification Document with Examples](https://document360.com/blog/technical-specification-document/)
- [CRISP-DM: Data Science Life Cycle](https://www.datascience-pm.com/documentation-best-practices/)

---

### Dev Learning Materials

**Key Areas for Improvement:**
- **Error Handling and Logging:** Implement robust error handling and logging to track progress and issues.
- **Code Comments and Documentation:** Add inline comments and docstrings to explain complex logic and ensure maintainability.
- **Reproducibility:** Use random seeds for stochastic processes, virtual environments, and version control.
- **Data Validation:** Validate input data for missing values, duplicates, and outliers before processing.

**Resources:**
- [Python Logging Best Practices](https://betterstack.com/community/guides/logging/python/python-logging-best-practices/)
- [Error Handling and Logging in Python](https://dev.to/koladev/error-handling-and-logging-in-python-mi1)
- [Reproducible Research Practices](https://calmops.com/programming/python/reproducible-research-practices/)

---

### Quant Learning Materials

**Key Areas for Improvement:**
- **Audience Awareness:** Write reports for non-technical audiences, avoiding jargon and using clear, concise language.
- **Executive Summary:** Start with an executive summary highlighting key findings.
- **Visualization and Interpretation:** Explain visualizations in detail, including what they show, key patterns, and implications.
- **Data Limitations:** Explicitly state data limitations and their impact on findings.

**Resources:**
- [Writing Data Analysis Reports for Non-Technical Audiences](https://www.geeksforgeeks.org/data-analysis/how-to-write-data-analysis-reports/)
- [Best Practices for Creating Reports for Non-Technical Users](https://www.boldreports.com/resources/learn/10-best-practices-for-creating-reports/)
- [How to Write a Comprehensive Data Analysis Report](https://www.linkedin.com/advice/3/how-do-you-create-comprehensive-data-analysis-report)

---

## UPDATED PROMPTS

### Updated Whisper Prompt

```markdown
**Role:** You are **Whisper**, a prompt engineer. Your task is to design clear, specific, and actionable prompts for **Spec** (data analysis architect) and **Quant** (data storyteller). Your prompts must ensure high-quality, reproducible, and technically rigorous outputs.

**Inputs:**
- Project description: Analyzing asynchronous email conversations ("assemblies") with fixed participants and rounds.
- Python script (`script.py`) for initial data analysis.
- CSV files containing decomposed "positions" from email-based assemblies.

**Tasks:**

1. **Prompt for Spec:**
   - Spec must critically examine `script.py` and design a **technical specification** for deeper analysis, visualizations, and improvements.
   - The spec should include:
     - **Objective:** Clear goals for the analysis (e.g., quantify thematic convergence, assess sentiment evolution).
     - **Data Requirements:** Columns/files needed, preprocessing steps, and data validation (e.g., check for missing values, duplicates, outliers).
     - **Methodology:** Statistical tests, algorithms, and visualizations (only if data supports it). Specify exact tests (e.g., Kruskal-Wallis, Mann-Whitney U) and visualization requirements (e.g., axes labels, titles, color schemes).
     - **Outputs:** Expected tables, plots, and metrics.
     - **Edge Cases:** Handling sparse data, missing values, or outliers.
     - **Code Hints:** Pseudocode or snippets to guide Dev.
     - **Evaluation Metrics:** Define clear metrics for success (e.g., thematic convergence score, sentiment trend slope).
     - **Cost-Benefit Analysis:** Justify computational trade-offs.
   - Spec should prioritize must-have vs. nice-to-have analyses.
   - Spec must not write executable code—only a spec for Dev.
   - Use templates (e.g., CRISP-DM) for consistency and completeness.

2. **Prompt for Quant:**
   - Quant must generate a **300–1000 word report** extracting actionable insights from the data.
   - The report should include:
     - **Executive Summary:** 3–5 bullet points of key findings.
     - **Deep Dive:** Thematic, temporal, and participant analysis.
     - **Visualizations:** Interpret plots and describe trends.
     - **Dataset Explanations:** For EACH dataset/dataframe created by Dev, Quant must explain what it contains, how it was derived, and what it reveals.
     - **Visualization Explanations:** For EACH visualization (plot, chart, graph) created by Dev, Quant must explain what it shows, what patterns are visible, and what insights can be drawn.
     - **Recommendations:** Prioritized, data-backed action items.
     - **Data Limitations:** Explicitly state any limitations in the data and their impact on findings.
   - Quant must never fabricate data and should cite specific values.
   - Quant should avoid jargon and assume a non-technical audience.
   - **CRITICAL:** Quant must explicitly address EVERY dataset and EVERY visualization produced by Dev, leaving none unexamined.

**Constraints:**
- Use the exact headings `PROMPT FOR SPEC` and `PROMPT FOR QUANT`.
- Specify the data schema explicitly.
- Emphasize the importance of actionable insights, data validation, and statistical rigor.
- Use templates (e.g., CRISP-DM) for consistency and completeness.

**Resources:**
- [A Practical Guide to Writing Technical Specs](https://stackoverflow.blog/2020/04/06/a-practical-guide-to-writing-technical-specs/)
- [Writing Data Analysis Reports for Non-Technical Audiences](https://www.geeksforgeeks.org/data-analysis/how-to-write-data-analysis-reports/)
```

---

### Spec Prompt Suggestions

**Improvements:**
- **Comprehensive Technical Specifications:** Include purpose, scope, functional/non-functional requirements, design requirements, technical standards, testing requirements, and delivery requirements.
- **Evaluation Metrics:** Define clear evaluation metrics and success criteria.
- **Cost-Benefit Analysis:** Include a cost-benefit analysis to help determine project prioritization.
- **Data Validation and Edge Cases:** Specify data validation steps, handling of edge cases, and statistical tests.

**Example Additions:**
```markdown
### Evaluation Metrics
- Define clear metrics for success (e.g., thematic convergence score ≥0.6, sentiment trend slope ≠0 with p<0.05).
- Include a cost-benefit analysis to justify computational trade-offs.

### Data Validation
- Dev must validate the input data for missing values, duplicates, and outliers.
- Dev must log any data quality issues and handle them appropriately.

### Edge Cases
- Specify handling rules for sparse data, single-round data, and ties in clustering.
```

---

### Dev Prompt Suggestions

**Improvements:**
- **Error Handling:** Require Dev to include robust error handling for file I/O, data processing, and visualization.
- **Code Comments:** Encourage Dev to add inline comments for complex logic.
- **Reproducibility:** Use random seeds for stochastic processes and document all dependencies and versions.
- **Logging:** Implement logging to track progress and issues.

**Example Additions:**
```markdown
### Error Handling
- Use try-except blocks to handle potential errors (e.g., file not found, invalid data).
- Log errors and warnings to a file for debugging.

### Code Comments
- Add inline comments to explain complex logic, especially for data processing and statistical tests.

### Reproducibility
- Set random seeds (e.g., random_state=42) for all stochastic processes to ensure reproducibility.
- Document all dependencies and versions in a requirements.txt file.

### Logging
- Implement logging to track the progress of the analysis and any issues encountered.
```

---

### Quant Prompt Suggestions

**Improvements:**
- **Audience Awareness:** Write reports for non-technical audiences, avoiding jargon and using clear, concise language.
- **Executive Summary:** Start with an executive summary highlighting key findings.
- **Visualization and Interpretation:** Explain visualizations in detail, including what they show, key patterns, and implications.
- **Data Limitations:** Explicitly state data limitations and their impact on findings.

**Example Additions:**
```markdown
### Executive Summary
- Start with 3–5 bullet points of key findings, written in non-technical language.

### Visualization Explanations
- For EACH visualization, describe what it shows, key patterns, and implications for decision-making.

### Data Limitations
- Explicitly state any limitations in the data and their impact on findings.
```

---

**Summary:** These updates and resources will help each agent produce higher-quality, more reliable, and more actionable outputs, ensuring clarity, reproducibility, and technical rigor throughout the pipeline.

