# Mistral Multi-Agent Data Analysis System

A multi-agent data analysis pipeline that combines machine learning techniques with Mistral AI's collaborative agent capabilities to perform clustering, topic modeling, and sentiment analysis on text data. The system uses four specialized agents—Whisper (prompt engineer), Spec (software architect), Dev (software engineer), and Quant (data analyst)—working together to generate comprehensive insights and actionable recommendations.

## Overview

This project is part of a wider initiative around observing, tracking and mapping the underlying structure of deliberative conversations that happen asynchronously via email. The first use case for this has been running series of assemblies deisgned to bring groups of stakeholders to consensus over the content of technical specifications. As the conversations are happening by email, a separate email client captures the response bodies, anonymizes them and decomposes them into discrete "positions" or "ideas". These positions are collected in a csv file for each round of deliberation.

This project processes text data from those 'position' CSV files and generates comprehensive analysis reports using a multi-agent system. It uses Mistral's embedding model to create vector representations of text, applies dimensionality reduction and clustering to identify patterns, performs topic modeling to extract themes, and analyzes sentiment. The results are then processed by five specialized AI agents working collaboratively:

- **Whisper**: Acts as a prompt engineer, designing optimized prompts for the other agents to ensure high-quality outputs and coordinating the team
- **Spec**: A software architect agent that examines the existing analysis script, identifies opportunities for enhancement, and writes technical specifications for additional analyses
- **Dev**: A software engineer agent that implements Spec's technical specifications, writing Python code for visualizations and additional analyses with proper testing and error handling
- **Quant**: A data analyst agent that interprets the results from Dev's code execution, identifies key trends and insights, and generates detailed reports with actionable recommendations
- **Critique**: A quality assurance agent that audits all agent outputs, provides learning materials for future runs, and updates prompts—creating a quasi-reinforcement learning loop for continuous improvement

Eventually this will integrate with the email client and other agents such that the assembly can be orchestrated and monitored agentically.

## System Architecture

![Multi-Agent Data Analysis System Flow](system_flow_diagram.png)

The diagram above illustrates the complete 5-agent architecture and information flow through the system.


## Features

### Core Analysis Pipeline
- **Text Embedding Generation**: Leverages Mistral's `mistral-embed` model to generate high-quality embeddings
- **Dimensionality Reduction**: Uses t-SNE to reduce embeddings to 3D for visualization
- **Intelligent Clustering**: Automatically determines optimal cluster count using silhouette scores and performs K-means clustering
- **Topic Modeling**: Extracts key topics using Latent Dirichlet Allocation (LDA)
- **Sentiment Analysis**: Analyzes sentiment polarity of text using TextBlob
- **3D Visualization**: Generates interactive 3D cluster maps and sentiment distribution histograms

### Multi-Agent System
- **Collaborative Agent Architecture**: Four specialized agents work together in a coordinated pipeline to provide comprehensive analysis
- **Whisper Agent**: Prompt engineer that designs optimized prompts for Spec and Quant, ensuring clear requirements and high-quality outputs
- **Spec Agent**: Software architect that examines the existing analysis script, identifies enhancement opportunities, and creates technical specifications for Dev to implement
- **Dev Agent**: Software engineer that implements Spec's technical specifications, writing production-ready Python code with visualizations, tests, and error handling
- **Quant Agent**: Data analyst that interprets results from Dev's code execution, generating detailed reports (300-1000 words) with key insights, trends, and statistical analysis
- **Agent Tools**: Spec and Quant have access to web search tools; Dev has code interpreter for executing and validating implementations

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

### Handling Large CSV Files

The system automatically handles different file sizes using a three-tier approach:

- **< 50KB**: Full dataset passed to Dev agent
- **50KB - 500KB**: Random sample (500 rows by default) passed to Dev agent
- **> 500KB**: Summary statistics and sample texts passed instead of raw data

For large files, you can adjust thresholds in `main.py`:
```python
FULL_DATA_THRESHOLD = 50000      # Increase to pass more full data
SAMPLE_DATA_THRESHOLD = 500000   # Increase to allow larger samples
SAMPLE_SIZE = 500                # Increase sample size (e.g., 1000 rows)
```

**See [LARGE_FILES.md](LARGE_FILES.md) for detailed guidance on analyzing large datasets.**

## Usage

### Run the Full Multi-Agent System (Recommended)

To run the complete multi-agent pipeline:

```bash
python main.py
```

This orchestrates the following workflow:

1. **Whisper Agent**:
   - Receives instructions from `prompts/whisper_message.txt`
   - Designs optimized prompts for Spec and Quant agents
   - Outputs results to `outputs/whisper_out.md`
2. **Spec Agent**:
   - Receives the prompt designed by Whisper and the existing analysis script (`generated_code/consensus_metrics.py`)
   - Examines the script to understand its data analysis capabilities (embeddings, clustering, topics, sentiment)
   - Identifies opportunities for enhancement, bug fixes, or deeper analysis
   - Writes a technical specification for Dev to implement
   - Outputs specification to `outputs/specification.md`
3. **Dev Agent**:
   - Receives the technical specification from Spec and the analysis script from `generated_code/consensus_metrics.py`
   - Executes the existing analysis code (embeddings, clustering, topic modeling, sentiment analysis)
   - Implements Spec's enhancements and extensions with production-ready Python code
   - Uses code interpreter to run all code and generate outputs (data, visualizations, results)
   - Outputs code and execution results to `outputs/dev.md`
   - **Code is automatically extracted** from Dev's markdown output and saved to `generated_code/analysis.py` for local execution
4. **Quant Agent**:
   - Receives the execution results and data from Dev's code interpreter
   - Analyzes clusters, embeddings, topics, sentiments, and any additional analyses
   - **Explains EVERY dataset and visualization** created by Dev, detailing what each shows and what insights it reveals
   - Generates a comprehensive report with insights, trends, and actionable recommendations
   - Outputs analysis report to `outputs/quant_out.md`

### Standalone Analysis Script (Optional)

You can also run the generated code independently for testing or development:

```bash
# Run the core analysis pipeline
python generated_code/consensus_metrics.py

# Run the code extracted from Dev's latest output
python generated_code/analysis.py
```

The `consensus_metrics.py` script executes the baseline analysis (embeddings, clustering, topic modeling, sentiment) and displays visualizations. The `analysis.py` file is auto-generated from Dev agent's output and contains all the code created during the latest run, which you can execute locally to reproduce the visualizations.

## Project Structure

```
mistral-data-agent/
├── main.py                    # Multi-agent orchestration script with RL loop
├── create_flow_diagram.py     # System architecture visualization generator
├── agents/
│   └── agents.py              # Agent initialization (Whisper, Spec, Dev, Quant, Critique)
├── prompts/
│   ├── whisper_message.txt    # Whisper agent prompt (auto-updated by Critique)
│   └── critique_message.txt   # Critique agent instructions
├── generated_code/            # Executable code generated by Dev agent
│   ├── consensus_metrics.py   # Core analysis pipeline (embeddings, clustering, topics, sentiment)
│   └── analysis.py            # Extracted code from Dev agent (auto-generated, can be run locally)
├── outputs/
│   ├── whisper_out.md         # Whisper's designed prompts for Spec and Quant
│   ├── specification.md       # Spec's technical specification for Dev
│   ├── dev.md                 # Dev's code implementation and execution results
│   ├── quant_out.md           # Quant's analysis report
│   ├── critique_out.md        # Critique's audit and learning materials
│   ├── agent_learning_materials/  # Accumulated learning across runs
│   │   ├── whisper_learning.md    # Whisper's learning materials
│   │   ├── spec_learning.md       # Spec's learning materials
│   │   ├── dev_learning.md        # Dev's learning materials
│   │   └── quant_learning.md      # Quant's learning materials
│   └── summary_report_example.md  # Example output from earlier single-agent version
├── tests/                     # Unit test suite
│   ├── conftest.py            # Pytest fixtures
│   ├── test_agents.py         # Agent initialization tests
│   ├── test_data_handling.py  # Data processing tests
│   ├── test_learning_materials.py  # Learning materials tests
│   └── test_response_parsing.py    # Response parsing tests
├── requirements.txt           # Python dependencies
├── environment.yml            # Conda environment specification
├── .env                       # Environment configuration (not in git)
├── .gitignore                 # Git ignore rules
├── README.md                  # This file
├── CHANGELOG.md               # Version history and detailed changes
├── LARGE_FILES.md             # Guide for handling large CSV files
└── system_flow_diagram.png    # System architecture diagram
```

## Output

### Multi-Agent System Output

The multi-agent system (`main.py`) generates markdown files in the `outputs/` directory:

1. **whisper_out.md**: Contains two carefully engineered prompts
   - **PROMPT FOR SPEC**: Instructions for the software architect to examine the existing script, identify enhancement opportunities, and create technical specifications
   - **PROMPT FOR QUANT**: Detailed instructions for the data analyst to interpret execution results and generate comprehensive reports

2. **specification.md**: Technical specification document including:
   - **Analysis of Existing Script**: Review of current capabilities and limitations
   - **Enhancement Opportunities**: Identified areas for improvement, additional analyses, and visualizations
   - **Technical Specifications**: Detailed requirements for Dev to implement, including data structures, algorithms, and output formats
   - **Code Snippets**: Hints and examples for implementation, especially for complex or unusual aspects
   - **Recommendations**: Prioritized list of enhancements with rationale

3. **dev.md**: Implementation and execution documentation including:
   - **Execution of `generated_code/consensus_metrics.py`**: Results from running the core analysis pipeline (embeddings, clustering, topic modeling, sentiment)
   - **Enhanced Code**: Production-ready code implementing Spec's technical specifications and enhancements
   - **Execution Results**: Complete output from code interpreter including:
     - Cluster data and metrics (optimal cluster count, silhouette scores, groupings)
     - Reduced embeddings for visualization
     - Topic modeling results (LDA topics, keywords)
     - Sentiment analysis data (polarity scores, distributions)
     - Additional analyses and visualizations per Spec's recommendations
   - **Code Documentation**: Inline comments, docstrings, and usage examples
   - **Test Cases**: Validation logic and error handling
   - **Generated Outputs**: Saved figures, data files, and visualization outputs in `outputs/` directory

4. **quant_out.md**: Comprehensive analysis report (300-1000 words) including:
   - **Results Analysis**: Interpretation of data and visualizations generated by Dev's code
   - **Key Insights**: Trends, patterns, and significant findings
   - **Statistical Summary**: Distribution metrics, correlations, and statistical tests
   - **Actionable Recommendations**: Concrete next steps, areas for further investigation, and strategic insights

5. **critique_out.md**: Quality assurance audit and learning materials including:
   - **Learning Materials**: Detailed feedback for each agent (Whisper, Spec, Dev, Quant)
     - Strengths to reinforce in future runs
     - Areas for improvement with specific examples
     - Learning resources (documentation, best practices, research papers)
   - **Updated Prompts**: Refined prompts for all agents
     - Complete revised Whisper prompt
     - Suggestions for Spec, Dev, and Quant prompts (for Whisper to incorporate)

6. **agent_learning_materials/** directory: Accumulated learning across all runs
   - **whisper_learning.md**: Cumulative learning materials for Whisper agent
   - **spec_learning.md**: Cumulative learning materials for Spec agent
   - **dev_learning.md**: Cumulative learning materials for Dev agent
   - **quant_learning.md**: Cumulative learning materials for Quant agent
   - Each file grows with each run (new materials appended with `---` separators)
   - Agents load these materials at runtime to incorporate past feedback

See `outputs/summary_report_example.md` for a sample output from the earlier single-agent version.

## How It Works

The system operates through a coordinated 5-agent pipeline with a reinforcement learning-style feedback loop:

### 1. Whisper (Prompt Engineering):
   - Reads the initial task description from `prompts/whisper_message.txt`
   - Analyzes the requirements for both Spec and Quant agents
   - Designs two optimized prompts with specific instructions, output formats, and quality standards
   - Uses delimiters ("PROMPT FOR SPEC" and "PROMPT FOR QUANT") to separate prompts for programmatic extraction

### 2. Spec (Software Architecture):
   - Receives Whisper's prompt and the `generated_code/consensus_metrics.py` analysis script
   - Examines the script to understand its data analysis capabilities:
     - Text embedding generation using Mistral's `mistral-embed` model
     - Dimensionality reduction with t-SNE
     - Optimal clustering with K-means (using silhouette scores)
     - Topic modeling with LDA
     - Sentiment analysis with TextBlob
   - Identifies opportunities for enhancement: bug fixes, additional analyses, improved visualizations, or deeper insights
   - Writes a detailed technical specification for Dev to implement
   - Includes code snippets, architectural guidance, and prioritized recommendations

### 3. Dev (Software Engineering & Execution):
   - Receives the technical specification from Spec and the `generated_code/consensus_metrics.py` script
   - **Executes the core analysis pipeline**:
     - Loads data from CSV file (extracts `position_text` column)
     - Generates embeddings using Mistral's embedding model
     - Performs dimensionality reduction, clustering, topic modeling, and sentiment analysis
   - **Implements Spec's enhancements** with production-ready Python code:
     - Enhanced visualizations (interactive plots, heatmaps, comparison charts)
     - Additional statistical analyses (correlation tests, significance testing)
     - Data transformations and feature engineering
   - Uses code interpreter to execute all code and generate outputs
   - Validates results and handles errors
   - Saves all outputs (figures, data files, analysis results) to the `outputs/` directory
   - Returns execution results including data, visualizations, and computed metrics

### 4. Quant (Data Analysis & Reporting):
   - Receives execution results and data from Dev's code interpreter
   - Analyzes the complete set of outputs:
     - Cluster distributions, cohesion metrics, and grouping patterns
     - Topic themes, keywords, and topic-cluster relationships
     - Sentiment distributions, statistics, and correlations
     - Any additional analyses performed by Dev
   - Interprets the visualizations, statistical results, and transformed data
   - Performs deep analysis to identify trends, patterns, and insights
   - Generates a comprehensive report (300-1000 words) with:
     - Results interpretation and key findings
     - Statistical summary and significance assessment
     - Actionable recommendations and strategic insights
   - Provides context-aware analysis grounded in the actual data

### 5. Critique (Quality Assurance & Continuous Learning):
   - Receives all prompts and outputs from Whisper, Spec, Dev, and Quant
   - Performs comprehensive audit examining:
     - **Accuracy**: Verifies data interpretations, statistical claims, and technical correctness
     - **Clarity**: Evaluates prompt quality, code readability, and report comprehensibility
     - **Code Quality**: Assesses Dev's code for efficiency, documentation, error handling, and best practices
     - **Actionability**: Judges whether insights and recommendations are specific and implementable
   - Generates **learning materials** for each agent:
     - Identifies strengths to reinforce
     - Highlights areas for improvement with specific examples
     - Provides learning resources (documentation, best practices, research papers)
   - Produces **updated prompts**:
     - Complete revised Whisper prompt (overwrites `prompts/whisper_message.txt`)
     - Suggestions for Spec, Dev, and Quant prompts (appended to Whisper's prompt file for her to incorporate)
   - Learning materials saved to `outputs/agent_learning_materials/` and **appended** to existing files
   - Creates a **quasi-reinforcement learning loop**: Each run's feedback improves the next run's performance

### Agent Coordination

The agents work in a sequential pipeline with clear handoffs and continuous improvement:
- **Whisper** orchestrates the workflow by designing clear, optimized prompts for Spec and Quant (incorporating learning materials from previous runs)
- **Spec** bridges requirements and implementation by examining the existing analysis script and creating detailed technical specifications for enhancements
- **Dev** executes all code (both the existing `generated_code/consensus_metrics.py` script and Spec's enhancements) using code interpreter, generating comprehensive data outputs and automatically extracting the code to `generated_code/analysis.py`
- **Quant** analyzes Dev's execution results to extract insights and provide strategic recommendations
- **Critique** audits all agent work, generates learning materials, and updates prompts for the next iteration
- All outputs use markdown format with specific delimiter patterns for programmatic processing

**Key Differences**:
1. Unlike traditional pipelines where analysis runs separately, Dev agent is the sole executor of all Python code, ensuring unified execution and result handling
2. The Critique agent creates a **reinforcement learning-style feedback loop**: each pipeline run generates "reward signals" (learning materials) that guide agents to improve on subsequent runs, without requiring manual prompt engineering

## Limitations

### API and Infrastructure Constraints
- **No File Upload Support**: Mistral SDK (v1.9.11) does not expose a native file upload API for code_interpreter. All data must be passed as strings embedded in prompts.
- **API Input Size Limits**: Prompts are limited to ~1-2MB, restricting the amount of raw data that can be passed directly to agents.
- **Remote Sandbox Execution**: Dev agent runs in a remote Mistral sandbox. Files saved during code execution are not accessible locally; results must be printed to stdout.
- **Single Execution Context**: Each agent call is stateless. Multi-pass analysis requiring intermediate file storage is not directly supported.

### Data Handling Trade-offs
- **Sampling Limitations**: For files > 500KB, the system uses random sampling or summary statistics, which may miss rare patterns or edge cases in the data.
- **Embedding Generation Overhead**: Large datasets require multiple API calls to generate embeddings, which is slow and potentially expensive (not yet implemented for local pre-processing).
- **No Incremental Processing**: Cannot process data in chunks across multiple Dev agent calls and aggregate results.

### Analysis Constraints
- **Fixed Analysis Pipeline**: The `generated_code/consensus_metrics.py` script defines a specific analysis workflow (embeddings → clustering → topics → sentiment). Adding new analysis types requires script modification.
- **Limited Agent Memory**: Agents cannot reference previous conversation rounds or outputs from past executions (no persistent memory).
- **Visualization Accessibility**: Visualizations generated by Dev agent in the sandbox cannot be retrieved directly; must be described in stdout or recreated locally.

### Architectural Limitations
- **Sequential Pipeline**: Agents run sequentially (Whisper → Spec → Dev → Quant). No parallel processing or dynamic agent collaboration.
- **No Human-in-the-Loop**: Once started, the pipeline runs to completion without opportunities for human intervention or course correction.
- **Fixed Prompt Structure**: Agent prompts are hardcoded in `agents/agents.py`. Changing agent behavior requires code changes and agent recreation.

## Future Improvements

### Near-Term Enhancements (High Priority)

1. **Local Embedding Pre-computation**
   - Generate embeddings locally in batches to avoid prompt size limits
   - Save embeddings to disk and reference them in the Dev agent prompt
   - Would enable analysis of datasets with 100,000+ rows without API constraints

2. **Chunk-Based Processing**
   - Split large datasets into chunks
   - Process each chunk with separate Dev agent calls
   - Aggregate results in a final synthesis step
   - Enables truly large-scale analysis (millions of rows)

3. **Visualization Retrieval**
   - Investigate if Mistral API supports retrieving generated figures from code_interpreter sandbox
   - Alternative: Have Dev agent generate matplotlib code that main.py can execute locally
   - Would make visualizations directly accessible without manual recreation

4. **Configurable Analysis Pipelines**
   - Move analysis configuration to a YAML or JSON file
   - Allow users to specify which analyses to run (clustering, topics, sentiment, etc.)
   - Enable custom analysis modules without modifying `generated_code/consensus_metrics.py`

### Medium-Term Enhancements

5. **Stratified Sampling**
   - Implement stratified sampling based on metadata columns (e.g., round, participant_id)
   - Ensures representative samples across categories
   - Better preserves data structure than pure random sampling

6. **Agent State Persistence**
   - Save agent conversation history to disk
   - Enable multi-session analysis where agents can reference previous work
   - Would support iterative refinement and follow-up questions

7. **Parallel Agent Execution**
   - Run independent analyses in parallel (e.g., separate Spec agents for different enhancement areas)
   - Aggregate results from multiple Dev agents
   - Significantly reduce total pipeline runtime

8. **Interactive Mode**
   - Add human-in-the-loop checkpoints (e.g., approve Spec's recommendations before Dev implements)
   - Allow users to provide feedback and request revisions
   - Implement using Claude Code's `AskUserQuestion` pattern

### Long-Term Vision

9. **Dynamic Agent Orchestration**
   - Replace fixed pipeline with a coordinator agent that decides which agents to call and in what order
   - Agents could collaborate iteratively based on intermediate results
   - Would enable more flexible and adaptive analysis workflows

10. **Multi-Round Analysis Support**
    - Automatically detect multiple CSV files (e.g., round1.csv, round2.csv)
    - Perform time-series and comparative analyses across rounds
    - Track consensus evolution and opinion shifts over time

11. **Embedding Model Fine-tuning**
    - Fine-tune Mistral embedding model on domain-specific data (deliberative conversations)
    - Could improve clustering quality and topic coherence
    - Requires substantial training data and infrastructure

12. **Real-Time Assembly Monitoring**
    - Integration with email client for live data ingestion
    - Agents monitor ongoing assemblies and provide real-time insights
    - Alert facilitators to emerging patterns, consensus points, or divergence

13. **Automated Report Generation**
    - Generate formatted PDF/HTML reports with embedded visualizations
    - Include executive summaries, detailed findings, and raw data tables
    - Customize report templates based on assembly type or stakeholder audience

14. **Multi-Modal Analysis**
    - Extend beyond text to analyze attachments, links, and multimedia
    - Sentiment analysis from tone (if audio available)
    - Network analysis of reply patterns and collaboration structure
