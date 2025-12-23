# Handling Large CSV Files with Dev Agent

## Overview

The Dev agent runs in a remote Mistral sandbox and cannot access local files directly. Data must be passed through the API, which has input size limits. The system now supports three modes for handling different file sizes.

## Three-Tier Data Handling System

### Mode 1: Full Data (< 50KB)
- **When:** CSV file is smaller than 50KB
- **What:** The complete dataset is embedded as a string in the Dev agent prompt
- **How:** Dev loads it using `pd.read_csv(StringIO(csv_data))`
- **Best for:** Small to medium datasets (< ~1000 rows of typical text data)

### Mode 2: Random Sample (50KB - 500KB)
- **When:** CSV file is between 50KB and 500KB
- **What:** A random sample of 500 rows (configurable) is embedded in the prompt
- **How:**
  - Uses `df.sample(n=500, random_state=42)` for reproducible sampling
  - Random sampling provides better representation than just `head()`
  - Dev receives CSV data and can perform full analysis on the sample
- **Best for:** Large datasets where sampling maintains statistical validity

### Mode 3: Summary Statistics (> 500KB)
- **When:** CSV file is larger than 500KB
- **What:** Comprehensive summary statistics replace raw data
- **Includes:**
  - Dataset shape (rows × columns)
  - Column names and data types
  - Descriptive statistics (mean, std, min, max, quartiles) for numeric columns
  - Text column statistics (length, null counts) for text data
  - Sample of 20 text entries (truncated to 200 chars each)
  - Value counts for categorical columns
- **How:** Dev receives structured summary and can:
  - Design analyses based on distributions
  - Generate synthetic data if needed for visualizations
  - Focus on statistical insights derivable from summary stats
- **Best for:** Very large datasets (10,000+ rows) where full embedding is impractical

## Configuration

You can adjust the thresholds in `main.py` (lines 14-23):

```python
# Data handling thresholds (in bytes)
FULL_DATA_THRESHOLD = 50000      # < 50KB: pass full dataset
SAMPLE_DATA_THRESHOLD = 500000   # 50KB - 500KB: use random sample
# > 500KB: use summary statistics only

# Sample size for medium datasets
SAMPLE_SIZE = 500  # rows

# Random seed for reproducible sampling
RANDOM_SEED = 42
```

## How to Analyze Larger Files

### Option 1: Increase Sample Size (Recommended for most cases)
If your dataset is 50KB - 500KB, increase the sample size:

```python
SAMPLE_SIZE = 1000  # Increase from 500 to 1000 rows
```

This works well because:
- Random sampling preserves statistical properties
- 1000 rows is usually sufficient for clustering, topic modeling, sentiment analysis
- Still stays within API limits

### Option 2: Increase Summary Threshold
If you want to pass more raw data before switching to summaries:

```python
SAMPLE_DATA_THRESHOLD = 1000000  # Increase to 1MB
SAMPLE_SIZE = 1000               # Use 1000 rows for samples
```

### Option 3: Adjust Full Data Threshold
If you're hitting the 50KB limit too quickly:

```python
FULL_DATA_THRESHOLD = 100000  # Increase to 100KB for full data
```

### Option 4: Pre-process Locally
For very large files (> 1MB), consider pre-processing before running the pipeline:

1. **Filter data locally:**
   ```python
   # In a separate script before running main.py
   df = pd.read_csv('large_file.csv')
   df_filtered = df[df['some_column'] == 'filter_value']
   df_filtered.to_csv('filtered_data.csv', index=False)
   ```

2. **Create embeddings locally:**
   Since embeddings are the bottleneck, you could generate them locally using the Mistral API:
   ```python
   from mistralai import Mistral

   client = Mistral(api_key=api_key)
   texts = df['position_text'].tolist()

   # Batch embedding generation
   embeddings = []
   batch_size = 100
   for i in range(0, len(texts), batch_size):
       batch = texts[i:i+batch_size]
       response = client.embeddings.create(
           model="mistral-embed",
           inputs=batch
       )
       embeddings.extend([item.embedding for item in response.data])

   # Save embeddings
   np.save('embeddings.npy', np.array(embeddings))
   ```

3. **Pass pre-computed embeddings:**
   Modify `consensus_metrics.py` to accept pre-computed embeddings instead of generating them

## Understanding the Tradeoffs

| Mode | Data Size | Pros | Cons |
|------|-----------|------|------|
| **Full Data** | < 50KB | • Complete accuracy<br>• All analysis possible<br>• No sampling bias | • Limited to small files<br>• API input limits |
| **Random Sample** | 50KB - 500KB | • Good representation<br>• Full analysis on sample<br>• Statistically valid | • Some information loss<br>• May miss rare patterns |
| **Summary Stats** | > 500KB | • Handles very large files<br>• Fast to process<br>• No API limits | • Cannot perform full analysis<br>• Limited to summary insights<br>• No direct text analysis |

## Example: Analyzing a 2MB CSV

Your file has 10,000 rows of text data (~2MB CSV):

1. **Current behavior:** Uses summary statistics mode
   - Dev receives column info, descriptive stats, 20 sample texts
   - Can identify broad patterns but not perform detailed clustering

2. **To get better analysis:**
   ```python
   # Option A: Increase sample size and threshold
   SAMPLE_DATA_THRESHOLD = 3000000  # 3MB
   SAMPLE_SIZE = 2000               # 2000 rows
   ```
   - Now 2000 random rows are passed to Dev
   - Full clustering, topic modeling, sentiment analysis possible
   - Results are representative of full dataset

3. **For even larger files (> 10MB):**
   - Pre-process locally: generate embeddings in batches
   - Save embeddings and run clustering/topic modeling locally
   - Pass final results to Quant agent for interpretation

## Best Practices

1. **Start with defaults:** The current thresholds (50KB/500KB/500 rows) work well for most use cases

2. **Monitor API errors:** If you get "Failed to persist entries" errors, decrease thresholds

3. **Use random sampling:** Always better than head/tail for statistical validity

4. **Trust the summary mode:** For very large files, summary statistics + 20 sample texts often provide sufficient insight

5. **Consider your analysis goals:**
   - Need exact cluster assignments? → Use sampling mode with large sample
   - Need general trends? → Summary mode works fine
   - Need to preserve all data? → Pre-process locally

## Technical Limitations

- **Mistral API input limit:** ~1-2MB per request (varies by model)
- **No file upload:** Mistral SDK doesn't support file uploads to code_interpreter
- **Remote sandbox:** Files saved by Dev agent are inaccessible to you
- **String embedding only:** Data must be passed as strings in prompts

## Future Improvements

Potential enhancements to consider:

1. **Stratified sampling:** Sample proportionally from clusters/categories
2. **Chunk-based processing:** Multiple Dev agent calls for different data chunks
3. **Local embedding generation:** Pre-compute embeddings to reduce prompt size
4. **Compression:** Compress CSV before embedding (though limited benefit)
5. **Delta encoding:** For time-series data, pass differences instead of values
