# Mistral Data Agent

A data analysis pipeline that combines machine learning techniques with Mistral AI's agent capabilities to perform clustering, topic modeling, and sentiment analysis on text data.

## Overview

This project is part of a wider initiative around observing, tracking and mapping the underlying structure of deliberative conversations that happen asynchronously via email. The first use case for this has been running series of assemblies deisgned to bring groups of stakeholders to consensus over the content of technical specifications. As the conversations are happening by email, a separate email client captures the response bodies, anonymizes them and decomposes them into discrete "positions" or "ideas". These positions are collected in a csv file for each round of deliberation.

This project processes text data from those 'position' CSV files and generates comprehensive analysis reports. It uses Mistral's embedding model to create vector representations of text, applies dimensionality reduction and clustering to identify patterns, performs topic modeling to extract themes, and analyzes sentiment. The results are then interpreted by a Mistral AI agent that generates detailed markdown reports with insights and recommendations.

Eventually this will integrate with the email client and other agents such that the assembly can be orchestrated and monitored agentically.

## Features

- **Text Embedding Generation**: Leverages Mistral's `mistral-embed` model to generate high-quality embeddings
- **Dimensionality Reduction**: Uses t-SNE to reduce embeddings to 3D for visualization
- **Intelligent Clustering**: Automatically determines optimal cluster count using silhouette scores and performs K-means clustering
- **Topic Modeling**: Extracts key topics using Latent Dirichlet Allocation (LDA)
- **Sentiment Analysis**: Analyzes sentiment polarity of text using TextBlob
- **3D Visualization**: Generates interactive 3D cluster maps and sentiment distribution histograms
- **AI-Powered Analysis**: Uses Mistral's agent API to generate intelligent summary reports with actionable insights

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

### Run only the Analysis Pipeline

To run only the analysis pipeline (clustering, topic modeling, sentiment analysis):

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

### Generate an AI Analysis Report

To run the full pipeline and generate an AI-powered summary report:

```bash
python main.py
```

This will:
- Run the complete analysis pipeline
- Pass the results to a Mistral AI agent
- Generate a detailed markdown report with insights and recommendations
- Save the report as `summary_report.md`


## Project Structure

```
mistral-data-agent/
├── consensus_metrics.py    # Core analysis pipeline
├── main.py                 # Main script with AI agent integration
├── requirements.txt        # Python dependencies
├── .env                    # Environment configuration (not in git)
├── .gitignore              # Git ignore rules
├── summary_report_example.md  # Example output report
└── README.md              # This file
```

## Output

### Analysis Pipeline Output

The pipeline generates:
1. **3D Cluster Visualization**: Interactive plot showing clustered data points
2. **Console Output**: Identified topics with top keywords
3. **Sentiment Histogram**: Distribution of sentiment polarity scores

### AI-Generated Report

The agent generates a comprehensive markdown report including:
- Cluster distribution and interpretation
- Key topics identified with keywords and themes
- Sentiment analysis with statistics (mean, median, standard deviation)
- Interpretation of findings
- Recommendations for additional analyses
- Suggestions for advancing the conversation

See `summary_report_example.md` for a sample output.

## How It Works

1. **Data Loading**: Extracts text from the `position_text` column in your CSV file
2. **Embedding Generation**: Converts text to high-dimensional vectors using Mistral's embedding model
3. **Dimensionality Reduction**: Reduces embeddings to 3D using t-SNE for visualization
4. **Optimal Clustering**: Tests different cluster counts (2-10) and selects the optimal number using silhouette scores
5. **K-means Clustering**: Groups similar text entries together
6. **Topic Modeling**: Applies LDA to identify underlying themes and extracts top keywords per topic
7. **Sentiment Analysis**: Calculates sentiment polarity (-1 to +1) for each text entry
8. **AI Analysis**: Mistral agent reviews all results and generates actionable insights


