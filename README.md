# Mistral Multi-Agent Data Analysis System

A multi-agent data analysis pipeline that combines machine learning techniques with Mistral AI's collaborative agent capabilities to perform clustering, topic modeling, and sentiment analysis on text data. The system uses three specialized agents—Whisper (product manager), Quant (data analyst), and Dev (software engineer)—working together to generate comprehensive insights and actionable recommendations.

## Overview

This project is part of a wider initiative around observing, tracking and mapping the underlying structure of deliberative conversations that happen asynchronously via email. The first use case for this has been running series of assemblies deisgned to bring groups of stakeholders to consensus over the content of technical specifications. As the conversations are happening by email, a separate email client captures the response bodies, anonymizes them and decomposes them into discrete "positions" or "ideas". These positions are collected in a csv file for each round of deliberation.

This project processes text data from those 'position' CSV files and generates comprehensive analysis reports using a multi-agent system. It uses Mistral's embedding model to create vector representations of text, applies dimensionality reduction and clustering to identify patterns, performs topic modeling to extract themes, and analyzes sentiment. The results are then processed by three specialized AI agents working collaboratively:

- **Whisper**: Acts as a product manager and prompt engineer, designing optimized prompts for the other agents to ensure high-quality outputs
- **Quant**: A data analyst agent that interprets the analysis results, identifies key trends and insights, and generates detailed reports with actionable recommendations
- **Dev**: A software engineer agent that writes Python code for visualizations, implements additional analyses recommended by Quant, and ensures code quality with testing and error handling

Eventually this will integrate with the email client and other agents such that the assembly can be orchestrated and monitored agentically.

## Features

### Core Analysis Pipeline
- **Text Embedding Generation**: Leverages Mistral's `mistral-embed` model to generate high-quality embeddings
- **Dimensionality Reduction**: Uses t-SNE to reduce embeddings to 3D for visualization
- **Intelligent Clustering**: Automatically determines optimal cluster count using silhouette scores and performs K-means clustering
- **Topic Modeling**: Extracts key topics using Latent Dirichlet Allocation (LDA)
- **Sentiment Analysis**: Analyzes sentiment polarity of text using TextBlob
- **3D Visualization**: Generates interactive 3D cluster maps and sentiment distribution histograms

### Multi-Agent System
- **Collaborative Agent Architecture**: Three specialized agents work together to provide comprehensive analysis
- **Whisper Agent**: An "agent-whisperer" whose task is something like a product manager - Whisper designs good prompts that ensure Dev and Quant do their job well.
- **Quant Agent**: Generates detailed reports (300-1000 words) with key insights, trends, statistical analysis, and recommendations for further investigation
- **Dev Agent**: Implements code for advanced visualizations, statistical tests, and additional analyses based on Quant's recommendations
- **Agent Tools**: Quant and Dev agents have access to web search and code interpreter tools for enhanced capabilities

## Prerequisites

- Python 3.10+
- Mistral API key (sign up at [Mistral AI](https://mistral.ai))
- CSV file with a `position_text` column containing text data to analyze (example file provided)

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd mistral-data-agent
```

2. Install dependencies using conda (recommended):
```bash
conda env create -f environment.yml
conda activate mistral
```

Or install using pip:
```bash
pip install -r requirements.txt
```

### Key Dependencies
- `mistralai` - Mistral AI SDK for embeddings and agent API
- `pandas` - Data manipulation
- `numpy` - Numerical computing
- `matplotlib` - Data visualization
- `scikit-learn` - Machine learning algorithms (t-SNE, K-means, LDA)
- `textblob` - Sentiment analysis
- `python-dotenv` - Environment variable management

## Configuration

1. Create a `.env` file in the project root:
```bash
cp .env.example .env
```

2. Add your Mistral API key and data file path:
```
MISTRAL_API_KEY=your_api_key_here
FILE_PATH=/path/to/your/data.csv
```

The CSV file must contain a column named `position_text` with the text data to analyze.

## Usage

### Run Only the Analysis Pipeline

To run only the analysis pipeline (clustering, topic modeling, sentiment analysis) without the multi-agent system:

```bash
python consensus_metrics.py
```

This will:
- Load your CSV data
- Generate embeddings using Mistral
- Perform clustering and determine optimal cluster count
- Display a 3D cluster visualization
- Identify topics using LDA
- Analyze sentiment and display a distribution histogram


### Run the Full Multi-Agent System

To run the complete multi-agent pipeline:

```bash
python main.py
```

This orchestrates the following workflow:

1. **Analysis Pipeline Execution**: Runs `consensus_metrics.py` to generate clusters, embeddings, topics, and sentiment data
2. **Whisper Agent**:
   - Receives instructions from `prompts/whisper_message.txt`
   - Designs optimized prompts for Quant and Dev agents
   - Outputs results to `outputs/whisper_out.md`
3. **Quant Agent**:
   - Receives the analysis data and the prompt designed by Whisper
   - Generates a comprehensive report analyzing clusters, topics, and sentiments
   - Includes specific recommendations and instructions for Dev
   - Outputs results to `outputs/quant_out.md`
4. **Dev Agent**:
   - Receives instructions from both Whisper and Quant
   - Writes Python code for visualizations and additional analyses
   - Implements recommendations from Quant's report
   - Outputs code and documentation to `outputs/dev_out.md`


## Project Structure

```
mistral-data-agent/
├── consensus_metrics.py       # Core analysis pipeline (embeddings, clustering, topics, sentiment)
├── main.py                    # Multi-agent orchestration script
├── prompts/
│   └── whisper_message.txt    # Initial instructions for Whisper agent
├── outputs/
│   ├── whisper_out.md         # Whisper's designed prompts for Quant and Dev
│   ├── quant_out.md           # Quant's analysis report with recommendations
│   ├── dev_out.md             # Dev's code and implementation documentation
│   └── summary_report_example.md  # Example output from earlier single-agent version
├── requirements.txt           # Python dependencies
├── .env                       # Environment configuration (not in git)
├── .gitignore                 # Git ignore rules
└── README.md                  # This file
```

## Output

### Analysis Pipeline Output

The pipeline (`consensus_metrics.py`) generates:
1. **3D Cluster Visualization**: Interactive plot showing clustered data points
2. **Console Output**: Identified topics with top keywords
3. **Sentiment Histogram**: Distribution of sentiment polarity scores

### Multi-Agent System Output

The multi-agent system (`main.py`) generates markdown files in the `outputs/` directory:

1. **whisper_out.md**: Contains two carefully engineered prompts
   - **PROMPT FOR QUANT**: Detailed instructions for the data analysis agent, specifying what insights to extract, how to structure the report, and what recommendations to provide
   - **PROMPT FOR DEV**: Instructions for the software engineering agent on code quality, visualization standards, and testing requirements

2. **quant_out.md**: Comprehensive analysis report (300-1000 words) including:
   - **Cluster Analysis**: Distribution, cohesion metrics, and interpretation of distinct position groups
   - **Topic Trends**: Dominant topics with keywords, outlier topics, and topic-cluster relationships
   - **Sentiment Analysis**: Summary statistics, distribution patterns, outliers, and sentiment-cluster correlations
   - **Actionable Insights**: Identification of consensus/conflict areas, assembly health assessment, and facilitator recommendations
   - **INSTRUCTIONS FOR DEV**: Specific technical tasks for visualizations, statistical analyses, and data collection recommendations

3. **dev_out.md**: Implementation documentation including:
   - **Python Code**: Executable functions for interactive visualizations (Plotly, Bokeh), statistical tests, and outlier detection
   - **Code Documentation**: Inline comments, docstrings, and usage examples
   - **Test Cases**: Validation logic and edge case handling
   - **Visualization Outputs**: Both static high-resolution images and interactive HTML files

See `outputs/summary_report_example.md` for a sample output from the earlier single-agent version.

## How It Works

### Stage 1: Data Analysis Pipeline

1. **Data Loading**: Extracts text from the `position_text` column in your CSV file
2. **Embedding Generation**: Converts text to high-dimensional vectors using Mistral's `mistral-embed` model
3. **Dimensionality Reduction**: Reduces embeddings to 3D using t-SNE for visualization
4. **Optimal Clustering**: Tests different cluster counts (2-10) and selects the optimal number using silhouette scores
5. **K-means Clustering**: Groups similar text entries together
6. **Topic Modeling**: Applies LDA to identify underlying themes and extracts top keywords per topic
7. **Sentiment Analysis**: Calculates sentiment polarity (-1 to +1) for each text entry using TextBlob

### Stage 2: Multi-Agent Collaboration

8. **Whisper (Prompt Engineering)**:
   - Reads the initial task description from `prompts/whisper_message.txt`
   - Analyzes the requirements for both Quant and Dev agents
   - Designs two optimized prompts with specific instructions, output formats, and quality standards
   - Uses delimiters ("PROMPT FOR QUANT" and "PROMPT FOR DEV") to separate prompts for programmatic extraction

9. **Quant (Data Analysis)**:
   - Receives the analysis data (clusters, embeddings, topics, sentiments) and Whisper's prompt
   - Performs deep analysis to identify trends, patterns, and insights
   - Generates a structured report with cluster interpretations, topic analysis, and sentiment patterns
   - Provides actionable recommendations and creates a dedicated section ("INSTRUCTIONS FOR DEV") with technical tasks for Dev

10. **Dev (Software Engineering)**:
    - Receives instructions from both Whisper and the "INSTRUCTIONS FOR DEV" section from Quant
    - Writes executable Python code for:
      - Interactive visualizations (3D plots, heatmaps, timelines)
      - Statistical analyses (correlation tests, cluster stability metrics)
      - Outlier detection and additional data exploration
    - Includes comprehensive documentation, error handling, and test cases
    - Ensures all code is production-ready and returns machine-readable outputs for further analysis

### Agent Coordination

The agents work sequentially but collaboratively:
- **Whisper** ensures the other agents have clear, well-structured instructions
- **Quant** focuses on extracting insights and identifying what additional work is needed
- **Dev** implements Quant's recommendations with high-quality, tested code
- All outputs use markdown format with specific delimiter patterns for programmatic processing
