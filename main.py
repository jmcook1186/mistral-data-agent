import os
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from dotenv import load_dotenv
from mistralai import Mistral
from agents.agents import initialize_agents

load_dotenv()

# ============================================================================
# CONFIGURATION
# ============================================================================
# Data handling thresholds (in bytes)
FULL_DATA_THRESHOLD = 50000      # < 50KB: pass full dataset
SAMPLE_DATA_THRESHOLD = 500000   # 50KB - 500KB: use random sample
# > 500KB: use summary statistics only

# Sample size for medium datasets
SAMPLE_SIZE = 500  # rows

# Random seed for reproducible sampling
RANDOM_SEED = 42

# Validate environment variables
api_key = os.getenv("MISTRAL_API_KEY")
file_path = os.getenv("FILE_PATH")

if not api_key:
    raise ValueError("MISTRAL_API_KEY not found in environment variables")
if not file_path:
    raise ValueError("FILE_PATH not found in environment variables")

# Initialize client
client = Mistral(api_key=api_key)

# Load script
try:
    with open("consensus_metrics.py", "r") as f:
        script = f.read()
    print("✓ Loaded consensus_metrics.py")
except FileNotFoundError:
    raise FileNotFoundError("consensus_metrics.py not found")
except Exception as e:
    raise Exception(f"Error reading consensus_metrics.py: {e}")

# Load input data - pass full data, sample, or summary depending on size
try:
    # Load the CSV to analyze it
    df = pd.read_csv(file_path)

    print(f"✓ Loaded data from {file_path}")
    print(f"  - {df.shape[0]} rows × {df.shape[1]} columns")

    # Decide whether to pass full data, sample, or summary based on size
    full_csv = df.to_csv(index=False)
    csv_size_kb = len(full_csv) / 1024

    if len(full_csv) > SAMPLE_DATA_THRESHOLD:  # More than 500KB by default
        # For very large files, pass summary statistics instead of raw data
        print(f"  - Dataset is very large ({csv_size_kb:.1f}KB), using summary statistics")

        # Generate comprehensive summary statistics
        summary_parts = []
        summary_parts.append(f"Dataset Shape: {df.shape[0]} rows × {df.shape[1]} columns")
        summary_parts.append(f"\nColumn Information:")
        summary_parts.append(f"Columns: {list(df.columns)}")
        summary_parts.append(f"Data Types:\n{df.dtypes.to_string()}")

        # Numeric columns statistics
        if len(df.select_dtypes(include=[np.number]).columns) > 0:
            summary_parts.append(f"\nNumeric Column Statistics:")
            summary_parts.append(df.describe().to_string())

        # Text column info (if position_text exists)
        if 'position_text' in df.columns:
            summary_parts.append(f"\nText Column ('position_text') Statistics:")
            summary_parts.append(f"  - Non-null count: {df['position_text'].notna().sum()}")
            summary_parts.append(f"  - Null count: {df['position_text'].isna().sum()}")
            summary_parts.append(f"  - Avg length: {df['position_text'].str.len().mean():.1f} chars")
            summary_parts.append(f"  - Min length: {df['position_text'].str.len().min()}")
            summary_parts.append(f"  - Max length: {df['position_text'].str.len().max()}")

            # Include a small sample of actual text
            sample_texts = df['position_text'].dropna().head(20)
            summary_parts.append(f"\nSample Text Entries (first 20):")
            for idx, text in enumerate(sample_texts, 1):
                # Truncate long texts
                display_text = text[:200] + "..." if len(text) > 200 else text
                summary_parts.append(f"{idx}. {display_text}")

        # Categorical columns value counts
        categorical_cols = df.select_dtypes(include=['object', 'category']).columns
        for col in categorical_cols:
            if col != 'position_text':  # Already handled above
                summary_parts.append(f"\nColumn '{col}' value counts:")
                summary_parts.append(df[col].value_counts().head(20).to_string())

        data_summary = "\n".join(summary_parts)

        data_info = {
            'mode': 'summary',
            'total_rows': df.shape[0],
            'total_cols': df.shape[1],
            'data_summary': data_summary,
            'note': f"NOTE: Dataset is very large ({csv_size_kb:.1f}KB). Providing summary statistics instead of raw data. Full dataset has {df.shape[0]} rows."
        }

    elif len(full_csv) > FULL_DATA_THRESHOLD:  # Between 50KB and 500KB by default
        # Use a larger random sample
        sample_size = min(SAMPLE_SIZE, df.shape[0])  # Take up to configured sample size

        # Use random sampling instead of just head() for better representation
        if df.shape[0] > sample_size:
            df_sample = df.sample(n=sample_size, random_state=RANDOM_SEED)
        else:
            df_sample = df

        data_csv = df_sample.to_csv(index=False)

        data_info = {
            'mode': 'sample',
            'sample_size': sample_size,
            'total_rows': df.shape[0],
            'csv_data': data_csv,
            'note': f"NOTE: This is a random sample of {sample_size} rows from {df.shape[0]} total rows. The sample is representative of the full dataset."
        }
        print(f"  - Dataset is large ({csv_size_kb:.1f}KB), using random sample of {sample_size} rows")
    else:
        # Pass full dataset
        data_info = {
            'mode': 'full',
            'total_rows': df.shape[0],
            'csv_data': full_csv,
            'note': "This is the complete dataset."
        }
        print(f"  - Passing full dataset to Dev agent ({csv_size_kb:.1f}KB)")

except FileNotFoundError:
    raise FileNotFoundError(f"Data file not found: {file_path}")
except Exception as e:
    raise Exception(f"Error reading data file: {e}")

# Load prompt
try:
    with open("prompts/whisper_message.txt", "r") as f:
        whisper_message = f.read()
    print("✓ Loaded whisper prompt")
except FileNotFoundError:
    raise FileNotFoundError("prompts/whisper_message.txt not found")
except Exception as e:
    raise Exception(f"Error reading whisper prompt: {e}")

# Ensure outputs directory exists
os.makedirs("outputs", exist_ok=True)

# Initialize agents
try:
    whisper, quant, dev, spec = initialize_agents()
    print("✓ Initialized all agents\n")
except Exception as e:
    raise Exception(f"Error initializing agents: {e}")

# ============================================================================
# WHISPER AGENT - Prompt Engineering
# ============================================================================
print("=" * 80)
print("CALLING WHISPER AGENT")
print("=" * 80)

try:
    whisper_response = client.beta.conversations.start(
        agent_id=whisper.id,
        inputs=whisper_message,
    )
    print(f"✓ Whisper responded with {len(whisper_response.outputs)} output(s)")
except Exception as e:
    raise Exception(f"Error calling Whisper agent: {e}")

# Parse Whisper response
try:
    if not whisper_response.outputs:
        raise ValueError("Whisper returned no outputs")

    whisper_content = whisper_response.outputs[0].content
    if not whisper_content:
        raise ValueError("Whisper returned empty content")

    # Split the response to extract spec and quant messages
    if "PROMPT FOR QUANT" not in whisper_content:
        raise ValueError("Whisper response missing 'PROMPT FOR QUANT' delimiter")

    spec_message, quant_message = whisper_content.split("PROMPT FOR QUANT", 1)

    print(f"✓ Parsed Spec message ({len(spec_message)} chars)")
    print(f"✓ Parsed Quant message ({len(quant_message)} chars)")

except Exception as e:
    raise Exception(f"Error parsing Whisper response: {e}")

# Save Whisper response to disk
try:
    with open("outputs/whisper_out.md", "w") as f:
        f.write(whisper_content)
    print("✓ Saved whisper_out.md\n")
except Exception as e:
    print(f"⚠ Warning: Could not save whisper_out.md: {e}\n")

# ============================================================================
# SPEC AGENT - Software Architecture
# ============================================================================
print("=" * 80)
print("CALLING SPEC AGENT")
print("=" * 80)

try:
    spec_response = client.beta.conversations.start(
        agent_id=spec.id,
        inputs=f"{spec_message}. The existing Python script to use as a starting point is: {script}",
    )
    print(f"✓ Spec responded with {len(spec_response.outputs)} output(s)")
except Exception as e:
    raise Exception(f"Error calling Spec agent: {e}")

# Parse Spec response - extract all text content from MessageOutputEntry
specification = []

for i, output in enumerate(spec_response.outputs):
    try:
        # Check if this is a MessageOutputEntry with text content
        if hasattr(output, 'content') and output.content:
            specification.append(output.content)
            print(f"✓ Output {i}: Found text content ({len(output.content)} chars)")
        # Skip tool outputs (web search results)
        elif hasattr(output, 'tool_name'):
            print(f"  Output {i}: Tool output ({output.tool_name}) - skipping")
        else:
            print(f"  Output {i}: Unknown output type - skipping")
    except Exception as e:
        print(f"⚠ Warning: Error processing output {i}: {e}")

if not specification:
    raise ValueError("Spec agent returned no text content")

specification_text = "\n\n".join(specification)
print(f"✓ Combined specification: {len(specification_text)} chars")

# Save Spec response to disk
try:
    with open("outputs/specification.md", "w") as f:
        f.write(specification_text)
    print("✓ Saved specification.md\n")
except Exception as e:
    print(f"⚠ Warning: Could not save specification.md: {e}\n")


# ============================================================================
# DEV AGENT - Software Engineering & Execution
# ============================================================================
print("=" * 80)
print("CALLING DEV AGENT")
print("=" * 80)

try:
    # Build Dev prompt based on data mode
    if data_info['mode'] == 'summary':
        # For very large files, pass summary statistics
        dev_prompt = f"""
{specification_text}

## Existing Python Script to Extend and Run:

```python
{script}
```

## Input Data Summary:

{data_info['note']}

{data_info['data_summary']}

IMPORTANT: The full dataset contains {data_info['total_rows']} rows and {data_info['total_cols']} columns.
Since the dataset is too large to pass directly, use the summary statistics above to:
1. Understand the data structure and distributions
2. Design appropriate analyses and visualizations
3. Generate synthetic or representative data if needed for demonstration purposes
4. Focus on statistical insights that can be derived from the summary

Execute the analysis and print all key results, metrics, and findings to stdout so they can be passed to the next agent.
"""
    else:
        # For full or sample data, embed CSV
        dev_prompt = f"""
{specification_text}

## Existing Python Script to Extend and Run:

```python
{script}
```

## Input CSV Data:

{data_info['note']}

```csv
{data_info['csv_data']}
```

IMPORTANT: Load this CSV data using pandas:
```python
import pandas as pd
from io import StringIO

csv_data = '''
{data_info['csv_data']}
'''

df = pd.read_csv(StringIO(csv_data))
```

Execute the analysis code and print all key results, metrics, and findings to stdout so they can be passed to the next agent.
"""

    dev_response = client.beta.conversations.start(
        agent_id=dev.id,
        inputs=dev_prompt,
    )
    print(f"✓ Dev responded with {len(dev_response.outputs)} output(s)")
except Exception as e:
    raise Exception(f"Error calling Dev agent: {e}")

# Parse Dev response - extract text messages and code execution results
dev_text_content = []
dev_code_executions = []

for i, output in enumerate(dev_response.outputs):
    output_type = type(output).__name__
    print(f"\nOutput {i}: {output_type}")

    try:
        # Extract text content from MessageOutputEntry
        if hasattr(output, 'content') and output.content:
            dev_text_content.append(output.content)
            print(f"  ✓ Found text content ({len(output.content)} chars)")

        # Extract code execution results from ToolExecutionOutputEntry
        if hasattr(output, 'tool_name') and output.tool_name == 'code_interpreter':
            if hasattr(output, 'execution'):
                execution_result = output.execution
                exec_data = {
                    'stdout': getattr(execution_result, 'stdout', ''),
                    'stderr': getattr(execution_result, 'stderr', ''),
                    'result': getattr(execution_result, 'result', None)
                }
                dev_code_executions.append(exec_data)
                print(f"  ✓ Found code execution result")
                if exec_data['stdout']:
                    print(f"    - stdout: {len(exec_data['stdout'])} chars")
                if exec_data['stderr']:
                    print(f"    - stderr: {len(exec_data['stderr'])} chars")
                if exec_data['result']:
                    print(f"    - result: {str(exec_data['result'])[:100]}...")
            else:
                print(f"  ⚠ Tool execution has no 'execution' attribute")
    except Exception as e:
        print(f"  ⚠ Error processing output {i}: {e}")

if not dev_text_content and not dev_code_executions:
    raise ValueError("Dev agent returned no text content or code execution results")

print(f"\n✓ Collected {len(dev_text_content)} text message(s)")
print(f"✓ Collected {len(dev_code_executions)} code execution(s)")

# Save Dev output to file
try:
    with open("outputs/dev.md", "w") as f:
        f.write("# Dev Agent Output\n\n")

        if dev_text_content:
            f.write("## Agent Messages\n\n")
            for idx, content in enumerate(dev_text_content, 1):
                f.write(f"### Message {idx}\n\n")
                f.write(content + "\n\n")

        if dev_code_executions:
            f.write("## Code Execution Results\n\n")
            for idx, exec_result in enumerate(dev_code_executions, 1):
                f.write(f"### Execution {idx}\n\n")
                if exec_result['stdout']:
                    f.write("**Standard Output:**\n```\n")
                    f.write(exec_result['stdout'])
                    f.write("\n```\n\n")
                if exec_result['stderr']:
                    f.write("**Standard Error:**\n```\n")
                    f.write(exec_result['stderr'])
                    f.write("\n```\n\n")
                if exec_result['result']:
                    f.write(f"**Result:** {exec_result['result']}\n\n")

        if not dev_code_executions:
            f.write("\n⚠ **Warning:** No code execution results found. The Dev agent may not have used the code_interpreter tool.\n")

    print("✓ Saved dev.md\n")
except Exception as e:
    print(f"⚠ Warning: Could not save dev.md: {e}\n")

# ============================================================================
# QUANT AGENT - Data Analysis & Reporting
# ============================================================================
print("=" * 80)
print("CALLING QUANT AGENT")
print("=" * 80)

# Prepare data for Quant agent - combine all text and execution results
quant_input_parts = []

# Add quant message
quant_input_parts.append(str(quant_message))
quant_input_parts.append("\n## Dev Agent Analysis Results\n")

if dev_text_content:
    quant_input_parts.append("\n### Dev Messages\n")
    # Ensure each item is a string
    for content in dev_text_content:
        quant_input_parts.append(str(content))

if dev_code_executions:
    quant_input_parts.append("\n## Code Execution Output\n")
    for idx, exec_result in enumerate(dev_code_executions, 1):
        quant_input_parts.append(f"\n### Execution {idx}\n")
        if exec_result['stdout']:
            quant_input_parts.append(f"\n**stdout:**\n```\n{str(exec_result['stdout'])}\n```\n")
        if exec_result['stderr']:
            quant_input_parts.append(f"\n**stderr:**\n```\n{str(exec_result['stderr'])}\n```\n")
        if exec_result['result']:
            # Convert result to string (handles lists, dicts, etc.)
            result_str = str(exec_result['result'])
            quant_input_parts.append(f"\n**result:** {result_str}\n")
else:
    quant_input_parts.append("\n⚠ Note: No code execution results available from Dev agent.\n")

# Ensure all parts are strings before joining
quant_input_parts = [str(part) for part in quant_input_parts]
quant_input_data = "\n".join(quant_input_parts)
print(f"Prepared Quant input ({len(quant_input_data)} chars)")

# Call Quant agent
try:
    quant_response = client.beta.conversations.start(
        agent_id=quant.id,
        inputs=quant_input_data
    )
    print(f"✓ Quant responded with {len(quant_response.outputs)} output(s)")
except Exception as e:
    raise Exception(f"Error calling Quant agent: {e}")

# Parse Quant response - extract all text content
quant_content = []

for i, output in enumerate(quant_response.outputs):
    try:
        # Extract text content from MessageOutputEntry
        if hasattr(output, 'content') and output.content:
            quant_content.append(output.content)
            print(f"✓ Output {i}: Found text content ({len(output.content)} chars)")
        # Skip tool outputs (web search results)
        elif hasattr(output, 'tool_name'):
            print(f"  Output {i}: Tool output ({output.tool_name}) - skipping")
        else:
            print(f"  Output {i}: Unknown output type - skipping")
    except Exception as e:
        print(f"⚠ Warning: Error processing output {i}: {e}")

if not quant_content:
    raise ValueError("Quant agent returned no text content")

quant_report = "\n\n".join(quant_content)
print(f"✓ Combined report: {len(quant_report)} chars")

# Save Quant response to disk
try:
    with open("outputs/quant_out.md", "w") as f:
        f.write(quant_report)
    print("✓ Saved quant_out.md\n")
except Exception as e:
    print(f"⚠ Warning: Could not save quant_out.md: {e}\n")

# ============================================================================
# PIPELINE COMPLETE
# ============================================================================
print("=" * 80)
print("PIPELINE COMPLETED SUCCESSFULLY")
print("=" * 80)
print("\nGenerated files:")
print("  - outputs/whisper_out.md")
print("  - outputs/specification.md")
print("  - outputs/dev.md")
print("  - outputs/quant_out.md")
print("\nAll agents executed successfully!")
