Here is a comprehensive review and set of learning materials and updated prompts for each agent, incorporating best practices from the latest research and industry standards:

---

## LEARNING MATERIALS

### Whisper Learning Materials

**Key Improvements Needed:**
- **Clarity and Specificity:** Ensure prompts are clear, specific, and actionable. Avoid ambiguity in requirements and expectations.
- **Structured Outputs:** Define the structure and format of outputs explicitly, including headings, sections, and deliverables.
- **Audience Awareness:** Tailor prompts to the intended audience (e.g., technical vs. non-technical), ensuring language and complexity are appropriate.
- **Validation and Error Handling:** Emphasize the importance of data validation, error handling, and logging in all technical specifications and code.

**Resources:**
- [A Practical Guide to Writing Technical Specs](https://stackoverflow.blog/2020/04/06/a-practical-guide-to-writing-technical-specs/)
- [Data Science Documentation Best Practices](https://www.datascience-pm.com/documentation-best-practices/)
- [Writing Data Requirements: Best Practices](https://qat.com/guide-writing-data-requirements/)

---

### Spec Learning Materials

**Key Improvements Needed:**
- **Comprehensive Data Validation:** Specify detailed data validation steps, including handling missing values, duplicates, and outliers.
- **Statistical Rigor:** Clearly define statistical tests, interpretation guidelines, and visualization requirements.
- **Reproducibility:** Ensure all methods and random processes are reproducible (e.g., using random seeds).
- **Edge Cases:** Address potential edge cases and specify how they should be handled.

**Resources:**
- [Data Validation in Python](https://www.projectpro.io/recipes/perform-data-validation-python-by-processing-only-matched-columns)
- [Reproducible Data Science with Python](https://valdanchev.github.io/reproducible-data-science-python/intro.html)
- [Best Practices for Data Validation and Error Handling](https://www.linkedin.com/advice/1/what-some-best-practices-documenting-your-data-validation)

---

### Dev Learning Materials

**Key Improvements Needed:**
- **Robust Error Handling:** Implement comprehensive error handling for file I/O, data processing, and visualization.
- **Code Comments and Documentation:** Add inline comments and docstrings to explain complex logic and ensure maintainability.
- **Logging:** Use logging to track progress, errors, and warnings during execution.
- **Reproducibility:** Use virtual environments, requirement files, and version control to ensure reproducibility.

**Resources:**
- [Data Validation and Exception Handling in Python](https://study.com/academy/lesson/data-validation-exception-handling-in-python.html)
- [Reproducible Research Practices](https://calmops.com/programming/python/reproducible-research-practices/)
- [Building Reproducible Research Pipelines in Python](https://www.statology.org/building-reproducible-research-pipelines-in-python-from-data-collection-to-reporting/)

---

### Quant Learning Materials

**Key Improvements Needed:**
- **Non-Technical Language:** Write reports in plain language, avoiding jargon and explaining technical terms.
- **Actionable Insights:** Focus on providing clear, prioritized recommendations based on data.
- **Visualization Descriptions:** Describe visualizations in detail, explaining axes, trends, and key takeaways.
- **Data Limitations:** Clearly state any data limitations and their impact on findings.

**Resources:**
- [Writing Data Science Reports for Non-Technical Audiences](https://www.unifyingdatascience.org/html/writing_to_stakeholders.html)
- [Best Practices for Creating Reports for Non-Technical Users](https://www.boldreports.com/resources/learn/10-best-practices-for-creating-reports/)
- [How to Write a Comprehensive Data Analysis Report](https://www.linkedin.com/advice/3/how-do-you-create-comprehensive-data-analysis-report)

---

## UPDATED PROMPTS

### Updated Whisper Prompt

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
     - **Methodology:** Statistical tests, algorithms, and visualizations (only if data supports it).
     - **Outputs:** Expected tables, plots, and metrics.
     - **Edge Cases:** Handling sparse data, missing values, or outliers.
     - **Code Hints:** Pseudocode or snippets to guide Dev.
   - Spec should prioritize must-have vs. nice-to-have analyses.
   - Spec must not write executable code—only a spec for Dev.

2. **Prompt for Quant:**
   - Quant must generate a **300–1000 word report** extracting actionable insights from the data.
   - The report should include:
     - **Executive Summary:** 3–5 bullet points of key findings.
     - **Deep Dive:** Thematic, temporal, and participant analysis.
     - **Visualizations:** Interpret plots and describe trends.
     - **Recommendations:** Prioritized, data-backed action items.
   - Quant must never fabricate data and should cite specific values.
   - Quant should avoid jargon and assume a non-technical audience.

**Constraints:**
- Use the exact headings `PROMPT FOR SPEC` and `PROMPT FOR QUANT`.
- Specify the data schema explicitly (e.g., `round_id`, `participant_id`, `position_text`, `sentiment_score`, `theme`, `timestamp`).
- Emphasize the importance of actionable insights, data validation, and statistical rigor.

---

### Spec Prompt Suggestions

**Improvements:**
- **Data Validation:** Require Dev to validate data quality (e.g., check for missing values, duplicates, outliers) before analysis.
- **Visualization Specs:** Be prescriptive about visualization requirements (e.g., axes labels, titles, color schemes).
- **Statistical Rigor:** Specify exact statistical tests and interpretation guidelines.
- **Error Handling:** Require Dev to include error handling and logging.

**Example Additions:**
```markdown
### Data Validation
- Dev must validate the input data for missing values, duplicates, and outliers.
- Dev must log any data quality issues and handle them appropriately (e.g., impute missing values, remove duplicates).

### Visualization Requirements
- All plots must include axes labels, titles, and a legend (if applicable).
- Use a consistent color scheme (e.g., viridis for categorical data, coolwarm for diverging data).

### Statistical Tests
- For non-parametric data, use Kruskal-Wallis for group comparisons and Mann-Whitney U for pairwise comparisons.
- Report p-values and effect sizes, and interpret results in plain language.
```

---

### Dev Prompt Suggestions

**Improvements:**
- **Error Handling:** Require Dev to include robust error handling for file I/O, data processing, and visualization.
- **Code Comments:** Encourage Dev to add inline comments for complex logic.
- **Reproducibility:** Use random seeds for stochastic processes.
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

### Logging
- Implement logging to track the progress of the analysis and any issues encountered.
```

---

### Quant Prompt Suggestions

**Improvements:**
- **Data Limitations:** Require Quant to state any data limitations and their impact on findings.
- **Statistical Interpretation:** Provide guidelines for interpreting statistical results in plain language.
- **Participant Dynamics:** Encourage Quant to analyze participant dynamics in depth.
- **Visualization Descriptions:** Require Quant to describe visualizations in detail.

**Example Additions:**
```markdown
### Data Limitations
- Quant must explicitly state any limitations in the data (e.g., missing values, small sample size) and discuss their potential impact on the findings.

### Statistical Interpretation
- Interpret statistical results in plain language (e.g., "A p-value of 0.81 means there is no significant difference between groups").

### Participant Dynamics
- Analyze participant dynamics in depth (e.g., which participants drove consensus, which were outliers).

### Visualization Descriptions
- Describe visualizations in detail, including what the axes represent and what trends to look for.
```

---

These updates and resources will help each agent produce higher-quality, more reliable, and more actionable outputs.

